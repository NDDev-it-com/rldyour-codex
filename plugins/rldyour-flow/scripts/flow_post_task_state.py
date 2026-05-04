#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


RUNTIME_IGNORED = {
    ".serena/.sync_marker",
    ".serena/.serena_sync_state.json",
    ".serena/.auto_sync_head",
    ".serena/.active_workflow_intent.json",
    ".serena/.dirty_stop_ack",
    ".serena/.flow_sync_marker",
    ".serena/.flow_post_task_state.json",
}

DOC_FILES = ("AGENTS.md", "CLAUDE.md")


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], check=False, capture_output=True, text=True)


def _stdout(*args: str) -> str:
    return _git(*args).stdout.strip()


def _porcelain_paths() -> list[str]:
    raw = _git("status", "--porcelain").stdout.rstrip("\n")
    paths: list[str] = []
    for line in raw.splitlines():
        if not line:
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if path and path not in RUNTIME_IGNORED:
            paths.append(path)
    return sorted(paths)


def _ahead_behind() -> tuple[int, int, str]:
    upstream = _stdout("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    if not upstream:
        return 0, 0, ""
    counts = _stdout("rev-list", "--left-right", "--count", f"{upstream}...HEAD")
    try:
        behind_s, ahead_s = counts.split()
        return int(ahead_s), int(behind_s), upstream
    except ValueError:
        return 0, 0, upstream


def _worktree_count() -> int:
    raw = _stdout("worktree", "list", "--porcelain")
    return sum(1 for line in raw.splitlines() if line.startswith("worktree "))


def _serena_current() -> tuple[bool, dict[str, Any]]:
    candidates = [
        Path("plugins/rldyour-serena-mcp/scripts/serena_memory_state.py"),
        Path.home() / ".codex/plugins/cache/rldyour-codex/rldyour-serena-mcp/local/scripts/serena_memory_state.py",
    ]
    for candidate in candidates:
        if not candidate.is_file():
            continue
        proc = subprocess.run(["python3", str(candidate)], check=False, capture_output=True, text=True)
        if proc.returncode != 0 or not proc.stdout.strip():
            continue
        try:
            payload = json.loads(proc.stdout)
        except json.JSONDecodeError:
            continue
        return bool(payload.get("is_current", True)), payload
    return True, {}


def _fullrepo_state() -> dict[str, Any]:
    candidates = [
        Path("plugins/rldyour-flow/scripts/fullrepo_sync.py"),
        Path.home() / ".codex/plugins/cache/rldyour-codex/rldyour-flow/local/scripts/fullrepo_sync.py",
    ]
    for candidate in candidates:
        if not candidate.is_file():
            continue
        proc = subprocess.run(
            ["python3", str(candidate), "--status-json"],
            check=False,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0 or not proc.stdout.strip():
            continue
        try:
            payload = json.loads(proc.stdout)
        except json.JSONDecodeError:
            continue
        return payload if isinstance(payload, dict) else {}
    return {}


def state() -> dict[str, Any]:
    if _git("rev-parse", "--is-inside-work-tree").returncode != 0:
        return {"is_git_repo": False, "needs_flow_sync": False, "serena_current": True}

    head_full = _stdout("rev-parse", "HEAD")
    head_sha = head_full[:7] if head_full else ""
    branch = _stdout("branch", "--show-current") or "detached"
    dirty_files = _porcelain_paths()
    ahead, behind, upstream = _ahead_behind()
    serena_current, serena_state = _serena_current()
    doc_files_present = [path for path in DOC_FILES if Path(path).is_file()]
    doc_files_changed = [path for path in dirty_files if path in DOC_FILES]
    worktree_count = _worktree_count()
    fullrepo_state = _fullrepo_state()

    worktree_agent_paths = fullrepo_state.get("worktree_agent_paths")
    if not isinstance(worktree_agent_paths, list):
        worktree_agent_paths = []
    fullrepo_needs_attention = bool(fullrepo_state) and (
        not bool(fullrepo_state.get("exclude_installed", True))
        or (bool(worktree_agent_paths) and not bool(fullrepo_state.get("remote_fullrepo_exists", False)))
    )

    needs_flow_sync = serena_current and bool(
        dirty_files or ahead or behind or doc_files_changed or fullrepo_needs_attention
    )

    fingerprint_payload = {
        "head": head_full,
        "branch": branch,
        "dirty": dirty_files,
        "ahead": ahead,
        "behind": behind,
        "serena_current": serena_current,
    }
    fingerprint = hashlib.sha256(json.dumps(fingerprint_payload, sort_keys=True).encode()).hexdigest()[:16]

    return {
        "is_git_repo": True,
        "head_sha": head_sha,
        "head_full": head_full,
        "branch": branch,
        "upstream": upstream,
        "ahead": ahead,
        "behind": behind,
        "dirty_files": dirty_files,
        "dirty_count": len(dirty_files),
        "doc_files_present": doc_files_present,
        "doc_files_changed": doc_files_changed,
        "worktree_count": worktree_count,
        "serena_current": serena_current,
        "serena_state": serena_state,
        "fullrepo_state": fullrepo_state,
        "fullrepo_needs_attention": fullrepo_needs_attention,
        "needs_flow_sync": needs_flow_sync,
        "fingerprint": fingerprint,
    }


def main() -> int:
    print(json.dumps(state(), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
