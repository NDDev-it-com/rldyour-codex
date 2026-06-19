#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable, cast

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from project_flow_policy import load_policy


FULLREPO_BRANCH = "fullrepo"
DEFAULT_REMOTE = "origin"
FULLREPO_STATE_PATH = ".rldyour/fullrepo-state.json"
FULLREPO_STATE_SCHEMA_VERSION = 2
PUBLISH_RETRIES = 3
EXCLUDE_BEGIN = "# >>> rldyour fullrepo agent-only files >>>"
EXCLUDE_END = "# <<< rldyour fullrepo agent-only files <<<"

AGENT_ONLY_PATTERNS = (
    "AGENTS.md",
    "CLAUDE.md",
    "REVIEW.md",
    "GEMINI.md",
    "QWEN.md",
    ".cursorrules",
    ".windsurfrules",
    ".aider*",
    ".claude/**",
    ".codex/**",
    ".cursor/rules/**",
    ".roo/**",
    ".windsurf/**",
    ".openhands/**",
    ".github/copilot-instructions.md",
    ".github/instructions/**",
    ".github/prompts/**",
    ".agents/skills/**",
    ".agents/commands/**",
    ".agents/hooks/**",
    ".serena/project.yml",
    ".serena/memories/**",
    ".serena/plans/**",
    ".serena/research/**",
    ".serena/newproj/**",
    ".serena/deploy/**",
)

FULLREPO_METADATA_PATTERNS = (
    FULLREPO_STATE_PATH,
)

RUNTIME_EXCLUDE_PATTERNS = (
    ".gemini/settings.json",
    ".gemini/antigravity-cli/settings.json",
    ".gemini/antigravity-cli/mcp_config.json",
    ".gemini/hooks/hooks.json",
    ".gemini/hooks/**.sh",
    ".gemini/commands/**",
    ".gemini/agents/**",
    ".gemini/skills/**",
    ".gemini/policies/**",
    ".serena/cache/**",
    ".serena/.gitignore",
    ".serena/project.local.yml",
    ".serena/.sync_marker",
    ".serena/.serena_sync_state.json",
    ".serena/.auto_sync_head",
    ".serena/.active_workflow_intent.json",
    ".serena/.dirty_stop_ack",
    ".serena/.flow_sync_marker",
    ".serena/.flow_post_task_state.json",
    ".serena/.flow_blocker_ack.json",
    ".serena/.stop_lifecycle_timeout_marker",
    ".serena/.bootstrap_overrides.log",
)

SECRET_RE = re.compile(
    r"ctx7sk-[A-Za-z0-9-]+|"
    r"ghp_[A-Za-z0-9_]+|"
    r"github_pat_[A-Za-z0-9_]+|"
    r"sk-[A-Za-z0-9_-]{16,}|"
    r"xox[baprs]-[A-Za-z0-9-]+|"
    r"BEGIN (?:RSA|OPENSSH|PRIVATE) KEY|"
    r"Bearer\s+[A-Za-z0-9._-]{20,}"
)


class FullrepoError(RuntimeError):
    pass


def _effective_policy(policy: dict[str, object]) -> dict[str, object]:
    effective = policy.get("effective")
    return effective if isinstance(effective, dict) else {}


def _fullrepo_policy(policy: dict[str, object]) -> dict[str, object]:
    section = _effective_policy(policy).get("fullrepo")
    return section if isinstance(section, dict) else {}


def _project_policy() -> dict[str, object]:
    return load_policy(repo_root())


def _policy_value(policy: dict[str, object], key: str, default: bool) -> bool:
    value = _fullrepo_policy(policy).get(key)
    return value if isinstance(value, bool) else default


def enforce_fullrepo_policy(policy: dict[str, object], action: str, *, ignore_project_policy: bool = False) -> None:
    if ignore_project_policy:
        print(f"warning: ignoring project fullrepo policy for {action}", file=sys.stderr)
        return
    fullrepo = _fullrepo_policy(policy)
    mode = str(fullrepo.get("mode", "auto"))
    source = str(policy.get("source", "built-in defaults"))
    if mode == "disabled":
        raise FullrepoError(f"fullrepo disabled by project policy ({source}); refused {action}")
    action_key = {
        "publish": "publish",
        "restore": "restore",
        "restore-local": "restore",
        "migrate-main": "migrate_main",
        "install-exclude": "install_exclude",
    }.get(action)
    if action_key and not _policy_value(policy, action_key, True):
        raise FullrepoError(f"fullrepo {action} disabled by project policy ({source})")


def _git(*args: str, check: bool = True, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(["git", *args], check=False, capture_output=True, text=True, env=env)
    if check and proc.returncode != 0:
        details = (proc.stderr or proc.stdout).strip()
        raise FullrepoError(f"git {' '.join(args)} failed: {details}")
    return proc


def _stdout(*args: str, check: bool = True, env: dict[str, str] | None = None) -> str:
    return _git(*args, check=check, env=env).stdout.strip()


def git_identity_env() -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("GIT_AUTHOR_NAME", "Danil Silantyev")
    env.setdefault("GIT_AUTHOR_EMAIL", "rldyourmnd@users.noreply.github.com")
    env.setdefault("GIT_COMMITTER_NAME", "Danil Silantyev")
    env.setdefault("GIT_COMMITTER_EMAIL", "rldyourmnd@users.noreply.github.com")
    return env


def repo_root() -> Path:
    proc = _git("rev-parse", "--show-toplevel", check=False)
    if proc.returncode != 0:
        raise FullrepoError("Not inside a git repository")
    return Path(proc.stdout.strip())


def git_dir() -> Path:
    return Path(_stdout("rev-parse", "--git-dir")).resolve()


def normalize_path(path: str | Path) -> str:
    return str(path).replace(os.sep, "/").strip("/")


def pattern_matches(path: str, patterns: Iterable[str]) -> bool:
    normalized = normalize_path(path)
    for pattern in patterns:
        pattern = normalize_path(pattern)
        if pattern.endswith("/**"):
            prefix = pattern[:-3].rstrip("/")
            if normalized == prefix or normalized.startswith(prefix + "/"):
                return True
        if fnmatch.fnmatchcase(normalized, pattern):
            return True
    return False


def is_agent_path(path: str) -> bool:
    return pattern_matches(path, AGENT_ONLY_PATTERNS) and not pattern_matches(path, RUNTIME_EXCLUDE_PATTERNS)


def git_exclude_path() -> Path:
    return git_dir() / "info" / "exclude"


def exclude_block() -> str:
    lines = [EXCLUDE_BEGIN]
    for pattern in AGENT_ONLY_PATTERNS:
        lines.append("/" + pattern)
    for pattern in FULLREPO_METADATA_PATTERNS:
        lines.append("/" + pattern)
    for pattern in RUNTIME_EXCLUDE_PATTERNS:
        lines.append("!/" + pattern)
    lines.append(EXCLUDE_END)
    return "\n".join(lines) + "\n"


def exclude_installed() -> bool:
    path = git_exclude_path()
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    return EXCLUDE_BEGIN in text and EXCLUDE_END in text


def install_exclude(dry_run: bool = False) -> None:
    path = git_exclude_path()
    current = path.read_text(encoding="utf-8") if path.is_file() else ""
    block = exclude_block()
    pattern = re.compile(
        re.escape(EXCLUDE_BEGIN) + r".*?" + re.escape(EXCLUDE_END) + r"\n?",
        re.S,
    )
    if pattern.search(current):
        new_text = pattern.sub(block, current)
    else:
        separator = "" if not current or current.endswith("\n") else "\n"
        new_text = current + separator + block

    if new_text == current:
        print("fullrepo exclude block already installed")
        return

    if dry_run:
        print(f"dry-run: would update {path}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(new_text, encoding="utf-8")
    print(f"installed fullrepo exclude block in {path}")


def split_porcelain_path(line: str) -> str:
    path = line[3:].strip()
    if " -> " in path:
        path = path.split(" -> ", 1)[1]
    return normalize_path(path)


def dirty_non_agent_paths() -> list[str]:
    raw = _git("status", "--porcelain", "--untracked-files=all").stdout.rstrip("\n")
    paths: list[str] = []
    for line in raw.splitlines():
        if not line:
            continue
        path = split_porcelain_path(line)
        if path and not is_agent_path(path) and not pattern_matches(path, RUNTIME_EXCLUDE_PATTERNS):
            paths.append(path)
    return sorted(set(paths))


def tracked_agent_paths(ref: str = "HEAD") -> list[str]:
    raw = _stdout("ls-tree", "-r", "--name-only", ref, check=False)
    return sorted(path for path in raw.splitlines() if is_agent_path(path))


def tracked_agent_paths_in_index() -> list[str]:
    raw = _stdout("ls-files", check=False)
    return sorted(path for path in raw.splitlines() if is_agent_path(path))


def remote_branch_sha(remote: str, branch: str) -> str:
    raw = _stdout("ls-remote", "--heads", remote, branch, check=False)
    if not raw:
        return ""
    return raw.split()[0]


def remote_configured(remote: str) -> bool:
    return _git("remote", "get-url", remote, check=False).returncode == 0


def local_ref_sha(ref: str) -> str:
    return _stdout("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}", check=False)


def ref_tree_sha(ref: str) -> str:
    return _stdout("rev-parse", "--verify", "--quiet", f"{ref}^{{tree}}", check=False)


def commit_sha(ref: str) -> str:
    return _stdout("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}", check=False)


def commit_message(ref: str) -> str:
    return _stdout("log", "-1", "--format=%B", ref, check=False)


def fullrepo_state_payload(base_head: str, agent_paths: list[str]) -> dict[str, object]:
    return {
        "schema_version": FULLREPO_STATE_SCHEMA_VERSION,
        "base_branch": "main",
        "base_head": base_head,
        "base_tree": ref_tree_sha(base_head),
        "agent_only_files": len(agent_paths),
    }


def fullrepo_state_text(base_head: str, agent_paths: list[str]) -> str:
    return json.dumps(fullrepo_state_payload(base_head, agent_paths), indent=2, sort_keys=True) + "\n"


def write_fullrepo_state_blob(base_head: str, agent_paths: list[str]) -> str:
    state_file: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            prefix="rldyour-fullrepo-state.",
            delete=False,
        ) as handle:
            state_file = Path(handle.name)
            handle.write(fullrepo_state_text(base_head, agent_paths))
        return _stdout("hash-object", "-w", str(state_file))
    finally:
        if state_file is not None:
            state_file.unlink(missing_ok=True)


def ref_fullrepo_state(ref: str) -> dict[str, object]:
    proc = _git("show", f"{ref}:{FULLREPO_STATE_PATH}", check=False)
    if proc.returncode != 0 or not proc.stdout.strip():
        return {}
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def legacy_base_head(ref: str) -> str:
    match = re.search(r"^Base-branch-head:\s*([a-f0-9]{40})\s*$", commit_message(ref), re.MULTILINE)
    return match.group(1) if match else ""


def fetch_fullrepo(remote: str, branch: str) -> bool:
    spec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
    proc = _git("fetch", "--quiet", remote, spec, check=False)
    return proc.returncode == 0


def iter_worktree_agent_files(root: Path) -> list[str]:
    paths: set[str] = set()
    for pattern in AGENT_ONLY_PATTERNS:
        for candidate in root.glob(pattern):
            if ".git" in candidate.parts:
                continue
            if candidate.is_dir():
                for file_path in candidate.rglob("*"):
                    if file_path.is_file():
                        rel = normalize_path(file_path.relative_to(root))
                        if is_agent_path(rel):
                            paths.add(rel)
            elif candidate.is_file():
                rel = normalize_path(candidate.relative_to(root))
                if is_agent_path(rel):
                    paths.add(rel)
    return sorted(paths)


def scan_for_secrets(root: Path, paths: Iterable[str]) -> list[str]:
    hits: list[str] = []
    for path in paths:
        file_path = root / path
        if not file_path.is_file():
            continue
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if SECRET_RE.search(text):
            hits.append(path)
    return hits


def write_sparse_agent_tree(agent_paths: list[str]) -> str:
    with tempfile.NamedTemporaryFile(prefix="rldyour-fullrepo-index.") as tmp_index:
        env = os.environ.copy()
        env["GIT_INDEX_FILE"] = tmp_index.name
        # Start from the well-known empty tree so non-agent main content
        # (e.g. .gemini/ files that are now tracked on main) does not leak
        # into the fullrepo commit.
        _git("read-tree", "4b825dc642cb6eb9a060e54bf8d69288fbee4904", env=env)

        if agent_paths:
            _git("add", "-f", "--", *agent_paths, env=env)

        return _stdout("write-tree", env=env)


def build_agent_content_tree(root: Path) -> tuple[str, list[str]]:
    agent_paths = iter_worktree_agent_files(root)
    secret_hits = scan_for_secrets(root, agent_paths)
    if secret_hits:
        raise FullrepoError("refusing to publish secret-looking agent-only files: " + ", ".join(secret_hits))
    return write_sparse_agent_tree(agent_paths), agent_paths


def ref_agent_content_tree(ref: str) -> str:
    raw = _git("ls-tree", "-r", "-z", ref, check=False).stdout
    entries: list[tuple[str, str, str]] = []
    for item in raw.split("\0"):
        if not item:
            continue
        meta, path = item.split("\t", 1)
        mode, _kind, sha = meta.split(" ", 2)
        if path == FULLREPO_STATE_PATH:
            continue
        if is_agent_path(path):
            entries.append((mode, sha, path))

    with tempfile.NamedTemporaryFile(prefix="rldyour-fullrepo-ref-index.") as tmp_index:
        env = os.environ.copy()
        env["GIT_INDEX_FILE"] = tmp_index.name
        _git("read-tree", "4b825dc642cb6eb9a060e54bf8d69288fbee4904", env=env)
        for mode, sha, path in entries:
            _git("update-index", "--add", "--cacheinfo", mode, sha, path, env=env)
        return _stdout("write-tree", env=env)


def build_fullrepo_tree(root: Path, base_head: str) -> tuple[str, list[str]]:
    agent_tree, agent_paths = build_agent_content_tree(root)
    with tempfile.NamedTemporaryFile(prefix="rldyour-fullrepo-index.") as tmp_index:
        env = os.environ.copy()
        env["GIT_INDEX_FILE"] = tmp_index.name
        _git("read-tree", agent_tree, env=env)
        state_blob = write_fullrepo_state_blob(base_head, agent_paths)
        _git("update-index", "--add", "--cacheinfo", "100644", state_blob, FULLREPO_STATE_PATH, env=env)

        tree = _stdout("write-tree", env=env)
        return tree, agent_paths


def fullrepo_match_mode(ref: str, source_head: str, source_tree: str, *, allow_legacy: bool = True) -> tuple[str, dict[str, object]]:
    state = ref_fullrepo_state(ref)
    schema_version = state.get("schema_version")
    if schema_version == FULLREPO_STATE_SCHEMA_VERSION:
        if state.get("base_head") == source_head:
            return "exact-head", state
        if state.get("base_tree") == source_tree:
            return "exact-tree", state
    elif schema_version == 1:
        if state.get("base_head") == source_head:
            return "schema-v1-exact-head", state
    if allow_legacy and legacy_base_head(ref) == source_head:
        return "legacy-trailer", state
    return "", state


def resolve_fullrepo_ref(
    fullrepo_ref: str,
    source_ref: str = "HEAD",
    *,
    allow_legacy: bool = True,
) -> dict[str, object]:
    source_head = commit_sha(source_ref)
    if not source_head:
        raise FullrepoError(f"source ref {source_ref} does not resolve to a commit")
    source_tree = ref_tree_sha(source_head)
    tip = commit_sha(fullrepo_ref)
    if not tip:
        raise FullrepoError(f"fullrepo ref {fullrepo_ref} does not resolve to a commit")

    history = _stdout("rev-list", fullrepo_ref, check=False).splitlines()
    for commit in history:
        mode, state = fullrepo_match_mode(commit, source_head, source_tree, allow_legacy=allow_legacy)
        if not mode:
            continue
        return {
            "commit": commit,
            "mode": mode,
            "source_head": source_head,
            "source_tree": source_tree,
            "tip": tip,
            "state": state,
            "tree": ref_tree_sha(commit),
            "agent_tree": ref_agent_content_tree(commit),
        }
    raise FullrepoError(
        f"no compatible fullrepo overlay found in {fullrepo_ref} for source {source_head} "
        f"(tree {source_tree})"
    )


def resolve_fullrepo_ref_or_none(fullrepo_ref: str, source_ref: str = "HEAD") -> dict[str, object]:
    try:
        return resolve_fullrepo_ref(fullrepo_ref, source_ref)
    except FullrepoError:
        return {}


def prepare_fullrepo_commit(remote: str, branch: str) -> dict[str, object]:
    root = repo_root()
    head = _stdout("rev-parse", "HEAD")
    full_tree, agent_paths = build_fullrepo_tree(root, head)
    agent_tree, _agent_paths = build_agent_content_tree(root)

    expected_remote = remote_branch_sha(remote, branch)
    remote_ref = f"refs/remotes/{remote}/{branch}"
    resolved: dict[str, object] = {}
    if expected_remote:
        fetch_fullrepo(remote, branch)
        resolved = resolve_fullrepo_ref_or_none(remote_ref, head)

    if resolved and resolved.get("agent_tree") == agent_tree:
        return {
            "noop": True,
            "head": head,
            "agent_paths": agent_paths,
            "expected_remote": expected_remote,
            "resolved": resolved,
        }

    parent_args = ["-p", expected_remote] if expected_remote else ["-p", head]
    message = (
        f"chore(fullrepo): sync {head[:7]}\n\n"
        f"Base-branch-head: {head}\n"
        f"Base-source-tree: {ref_tree_sha(head)}\n"
        f"Agent-only-files: {len(agent_paths)}\n"
    )
    commit = _stdout("commit-tree", full_tree, *parent_args, "-m", message, env=git_identity_env())
    return {
        "noop": False,
        "head": head,
        "agent_paths": agent_paths,
        "expected_remote": expected_remote,
        "commit": commit,
        "tree": full_tree,
        "agent_tree": agent_tree,
    }


def publish(remote: str, branch: str, dry_run: bool = False, *, ignore_project_policy: bool = False) -> None:
    policy = _project_policy()
    enforce_fullrepo_policy(policy, "publish", ignore_project_policy=ignore_project_policy)
    non_agent_dirty = dirty_non_agent_paths()
    if non_agent_dirty:
        raise FullrepoError(
            "refusing to publish fullrepo while non-agent files are dirty: "
            + ", ".join(non_agent_dirty)
        )

    if _policy_value(policy, "install_exclude", True) or ignore_project_policy:
        install_exclude(dry_run=dry_run)

    last_error = ""
    for attempt in range(1, PUBLISH_RETRIES + 1):
        prepared = prepare_fullrepo_commit(remote, branch)
        head = str(prepared["head"])
        agent_paths = list(cast(list[str], prepared["agent_paths"]))
        if prepared.get("noop"):
            resolved = prepared.get("resolved")
            mode = resolved.get("mode") if isinstance(resolved, dict) else "compatible"
            commit = resolved.get("commit", "") if isinstance(resolved, dict) else ""
            print(
                f"fullrepo already has {mode} overlay {str(commit)[:12]} "
                f"for HEAD {head[:7]} plus {len(agent_paths)} agent-only files"
            )
            return

        commit = str(prepared["commit"])
        expected_remote = str(prepared.get("expected_remote") or "")
        if dry_run:
            print(f"dry-run: would update refs/heads/{branch} to {commit[:12]}")
            print(f"dry-run: would push {branch} as a normal fast-forward")
            return

        proc = _git("push", remote, f"{commit}:refs/heads/{branch}", check=False)
        if proc.returncode == 0:
            _git("update-ref", f"refs/heads/{branch}", commit)
            fetch_fullrepo(remote, branch)
            print(f"published {branch} at {commit[:12]} from HEAD {head[:7]} with {len(agent_paths)} agent-only files")
            return
        last_error = (proc.stderr or proc.stdout).strip()
        if attempt < PUBLISH_RETRIES:
            print(f"fullrepo push lost race against remote update; retrying ({attempt}/{PUBLISH_RETRIES})", file=sys.stderr)
            fetch_fullrepo(remote, branch)
            continue
        expected = expected_remote[:12] if expected_remote else "missing"
        raise FullrepoError(f"failed to fast-forward {remote}/{branch} from expected {expected}: {last_error}")


def restore(remote: str, branch: str, dry_run: bool = False, *, ignore_project_policy: bool = False) -> None:
    policy = _project_policy()
    enforce_fullrepo_policy(policy, "restore", ignore_project_policy=ignore_project_policy)
    if _policy_value(policy, "install_exclude", True) or ignore_project_policy:
        install_exclude(dry_run=dry_run)
    if not fetch_fullrepo(remote, branch):
        print(f"fullrepo branch {remote}/{branch} does not exist; restore skipped")
        return

    ref = f"refs/remotes/{remote}/{branch}"
    resolved = resolve_fullrepo_ref(ref, "HEAD")
    resolved_ref = str(resolved["commit"])
    remote_paths = tracked_agent_paths(resolved_ref)
    if not remote_paths:
        print(f"resolved fullrepo overlay {resolved_ref[:12]} has no agent-only files")
        return

    if dry_run:
        print(
            f"dry-run: would restore {len(remote_paths)} agent-only files from "
            f"{remote}/{branch}@{resolved_ref[:12]} ({resolved['mode']})"
        )
        return

    for index in range(0, len(remote_paths), 64):
        chunk = remote_paths[index : index + 64]
        _git("restore", "--source", resolved_ref, "--worktree", "--", *chunk)

    print(f"restored {len(remote_paths)} agent-only files from {remote}/{branch}@{resolved_ref[:12]} ({resolved['mode']})")


def restore_local(remote: str, branch: str, dry_run: bool = False, *, ignore_project_policy: bool = False) -> None:
    policy = _project_policy()
    enforce_fullrepo_policy(policy, "restore-local", ignore_project_policy=ignore_project_policy)
    if _policy_value(policy, "install_exclude", True) or ignore_project_policy:
        install_exclude(dry_run=dry_run)
    ref = f"refs/remotes/{remote}/{branch}"
    if _git("show-ref", "--verify", "--quiet", ref, check=False).returncode != 0:
        print(f"local fullrepo ref {remote}/{branch} does not exist; restore skipped")
        return

    resolved = resolve_fullrepo_ref(ref, "HEAD")
    resolved_ref = str(resolved["commit"])
    remote_paths = tracked_agent_paths(resolved_ref)
    if not remote_paths:
        print(f"resolved local fullrepo overlay {resolved_ref[:12]} has no agent-only files")
        return

    if dry_run:
        print(
            f"dry-run: would restore {len(remote_paths)} agent-only files from "
            f"local {remote}/{branch}@{resolved_ref[:12]} ({resolved['mode']})"
        )
        return

    for index in range(0, len(remote_paths), 64):
        chunk = remote_paths[index : index + 64]
        _git("restore", "--source", resolved_ref, "--worktree", "--", *chunk)

    print(f"restored {len(remote_paths)} agent-only files from local {remote}/{branch}@{resolved_ref[:12]} ({resolved['mode']})")


def migrate_main(dry_run: bool = False, *, ignore_project_policy: bool = False) -> None:
    policy = _project_policy()
    enforce_fullrepo_policy(policy, "migrate-main", ignore_project_policy=ignore_project_policy)
    if _policy_value(policy, "install_exclude", True) or ignore_project_policy:
        install_exclude(dry_run=dry_run)
    paths = tracked_agent_paths_in_index()
    if not paths:
        print("no tracked agent-only files in current branch index")
        return
    if dry_run:
        print("dry-run: would remove agent-only files from current branch index:")
        for path in paths:
            print(path)
        return
    _git("rm", "--cached", "-r", "--ignore-unmatch", "--", *paths)
    print(f"removed {len(paths)} agent-only files from current branch index; files remain in the working tree")


def bootstrap_init(
    remote: str,
    branch: str,
    dry_run: bool = False,
    *,
    create_missing: bool = False,
    ignore_project_policy: bool = False,
) -> None:
    policy = _project_policy()
    enforce_fullrepo_policy(policy, "restore", ignore_project_policy=ignore_project_policy)
    root = repo_root()
    local_agent_paths = iter_worktree_agent_files(root)
    remote_exists = fetch_fullrepo(remote, branch)
    actions: list[str] = []

    if _policy_value(policy, "install_exclude", True) or ignore_project_policy:
        install_exclude(dry_run=dry_run)

    if tracked_agent_paths_in_index():
        enforce_fullrepo_policy(policy, "migrate-main", ignore_project_policy=ignore_project_policy)
        actions.append("migrate-main")
        migrate_main(dry_run=dry_run, ignore_project_policy=ignore_project_policy)
    elif remote_exists:
        actions.append("restore")
        restore(remote, branch, dry_run=dry_run, ignore_project_policy=ignore_project_policy)
    elif local_agent_paths:
        may_create = create_missing or _policy_value(policy, "create_if_missing", False) or ignore_project_policy
        if may_create:
            enforce_fullrepo_policy(policy, "publish", ignore_project_policy=ignore_project_policy)
            actions.append("publish")
            publish(remote, branch, dry_run=dry_run, ignore_project_policy=ignore_project_policy)
        else:
            print(
                f"fullrepo branch {remote}/{branch} does not exist; creation skipped by project policy"
            )
    else:
        print(f"fullrepo branch {remote}/{branch} does not exist and no local agent-only files were found")

    payload = status(remote, branch)
    payload["bootstrap_actions"] = actions
    print_status(payload, as_json=False)


def status(remote: str, branch: str, *, local_only: bool = False) -> dict[str, object]:
    root = repo_root()
    policy = _project_policy()
    fullrepo_policy = _fullrepo_policy(policy)
    if str(fullrepo_policy.get("mode", "auto")) == "disabled":
        return {
            "is_git_repo": True,
            "root": str(root),
            "branch": _stdout("branch", "--show-current", check=False) or "detached",
            "head": _stdout("rev-parse", "--short=12", "HEAD", check=False),
            "remote": remote,
            "remote_configured": remote_configured(remote),
            "fullrepo_branch": branch,
            "network_checked": False,
            "remote_fullrepo_exists": False,
            "remote_fullrepo_sha": "",
            "local_fullrepo_sha": "",
            "expected_fullrepo_tree": "",
            "remote_fullrepo_tree": "",
            "local_fullrepo_tree": "",
            "fullrepo_matches_worktree": True,
            "local_fullrepo_matches_worktree": True,
            "exclude_installed": exclude_installed(),
            "tracked_agent_paths": [],
            "worktree_agent_paths": [],
            "dirty_non_agent_paths": dirty_non_agent_paths(),
            "fullrepo_needs_attention": False,
            "mode": "disabled",
            "project_policy": {
                "source": policy.get("source"),
                "source_kind": policy.get("source_kind"),
                "valid": policy.get("valid"),
                "profile": _effective_policy(policy).get("profile"),
                "effective": _effective_policy(policy),
            },
        }
    remote_ref = f"refs/remotes/{remote}/{branch}"
    has_remote = remote_configured(remote)
    remote_sha = local_ref_sha(remote_ref) if local_only else remote_branch_sha(remote, branch)
    local_sha = local_ref_sha(f"refs/heads/{branch}")
    remote_tree = ""
    remote_state: dict[str, object] = {}
    remote_resolved: dict[str, object] = {}
    if remote_sha:
        if local_only:
            pass
        elif fetch_fullrepo(remote, branch):
            pass
        remote_resolved = resolve_fullrepo_ref_or_none(remote_ref, "HEAD")
        if remote_resolved:
            remote_tree = str(remote_resolved.get("tree", ""))
            remote_state_value = remote_resolved.get("state")
            remote_state = cast(dict[str, object], remote_state_value) if isinstance(remote_state_value, dict) else {}
    local_tree = ref_tree_sha(f"refs/heads/{branch}") if local_sha else ""
    local_state = ref_fullrepo_state(f"refs/heads/{branch}") if local_sha else {}
    local_resolved = resolve_fullrepo_ref_or_none(f"refs/heads/{branch}", "HEAD") if local_sha else {}
    if local_resolved:
        local_tree = str(local_resolved.get("tree", ""))
        local_state_value = local_resolved.get("state")
        local_state = cast(dict[str, object], local_state_value) if isinstance(local_state_value, dict) else {}
    head = _stdout("rev-parse", "HEAD", check=False)
    expected_tree, agent_paths = build_fullrepo_tree(root, head)
    expected_agent_tree, _agent_paths = build_agent_content_tree(root)
    expected_state = fullrepo_state_payload(head, agent_paths)
    remote_agent_tree = str(remote_resolved.get("agent_tree", "")) if remote_resolved else ""
    local_agent_tree = str(local_resolved.get("agent_tree", "")) if local_resolved else ""
    comparison_agent_tree = remote_agent_tree or local_agent_tree
    return {
        "is_git_repo": True,
        "root": str(root),
        "branch": _stdout("branch", "--show-current", check=False) or "detached",
        "head": _stdout("rev-parse", "--short=12", "HEAD", check=False),
        "remote": remote,
        "remote_configured": has_remote,
        "fullrepo_branch": branch,
        "network_checked": not local_only,
        "remote_fullrepo_exists": bool(remote_sha),
        "remote_fullrepo_sha": remote_sha[:12] if remote_sha else "",
        "local_fullrepo_sha": local_sha[:12] if local_sha else "",
        "remote_resolved_fullrepo_sha": str(remote_resolved.get("commit", ""))[:12] if remote_resolved else "",
        "local_resolved_fullrepo_sha": str(local_resolved.get("commit", ""))[:12] if local_resolved else "",
        "remote_resolution_mode": str(remote_resolved.get("mode", "")) if remote_resolved else "",
        "local_resolution_mode": str(local_resolved.get("mode", "")) if local_resolved else "",
        "expected_fullrepo_tree": expected_tree,
        "expected_agent_tree": expected_agent_tree,
        "remote_fullrepo_tree": remote_tree,
        "local_fullrepo_tree": local_tree,
        "remote_agent_tree": remote_agent_tree,
        "local_agent_tree": local_agent_tree,
        "expected_fullrepo_state": expected_state,
        "remote_fullrepo_state": remote_state,
        "local_fullrepo_state": local_state,
        "fullrepo_matches_worktree": bool(comparison_agent_tree and comparison_agent_tree == expected_agent_tree),
        "local_fullrepo_matches_worktree": bool(local_agent_tree and local_agent_tree == expected_agent_tree),
        "exclude_installed": exclude_installed(),
        "tracked_agent_paths": tracked_agent_paths_in_index(),
        "worktree_agent_paths": agent_paths,
        "dirty_non_agent_paths": dirty_non_agent_paths(),
        "mode": str(fullrepo_policy.get("mode", "auto")),
        "project_policy": {
            "source": policy.get("source"),
            "source_kind": policy.get("source_kind"),
            "valid": policy.get("valid"),
            "profile": _effective_policy(policy).get("profile"),
            "effective": _effective_policy(policy),
        },
    }


def print_status(payload: dict[str, object], as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, sort_keys=True))
        return
    print(json.dumps(payload, indent=2, sort_keys=True))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Synchronize rldyour agent-only files through a fullrepo branch.")
    parser.add_argument("--remote", default=DEFAULT_REMOTE)
    parser.add_argument("--branch", default=FULLREPO_BRANCH)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--ignore-project-policy",
        action="store_true",
        help="Emergency override for owner-authorized fullrepo actions that project policy would normally refuse.",
    )
    parser.add_argument(
        "--create-missing",
        action="store_true",
        help="Allow --bootstrap-init to create a missing fullrepo branch when policy does not set create_if_missing.",
    )
    parser.add_argument(
        "--local-only",
        action="store_true",
        help="For status checks, use existing local refs only and do not fetch or query the remote.",
    )
    parser.add_argument(
        "--source-ref",
        default="HEAD",
        help="Source commit/tree to resolve for --resolve-json (default: HEAD).",
    )
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--status", action="store_true")
    actions.add_argument("--status-json", action="store_true")
    actions.add_argument("--install-exclude", action="store_true")
    actions.add_argument("--restore", action="store_true")
    actions.add_argument("--restore-local", action="store_true")
    actions.add_argument("--publish", action="store_true")
    actions.add_argument("--prepare-json", action="store_true")
    actions.add_argument("--resolve-json", action="store_true")
    actions.add_argument("--migrate-main", action="store_true")
    actions.add_argument("--bootstrap-init", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        repo_root()
        if args.status or args.status_json:
            print_status(status(args.remote, args.branch, local_only=args.local_only), as_json=args.status_json)
        elif args.install_exclude:
            enforce_fullrepo_policy(
                _project_policy(),
                "install-exclude",
                ignore_project_policy=args.ignore_project_policy,
            )
            install_exclude(dry_run=args.dry_run)
        elif args.restore:
            restore(args.remote, args.branch, dry_run=args.dry_run, ignore_project_policy=args.ignore_project_policy)
        elif args.restore_local:
            restore_local(
                args.remote,
                args.branch,
                dry_run=args.dry_run,
                ignore_project_policy=args.ignore_project_policy,
            )
        elif args.publish:
            publish(args.remote, args.branch, dry_run=args.dry_run, ignore_project_policy=args.ignore_project_policy)
        elif args.prepare_json:
            prepared = prepare_fullrepo_commit(args.remote, args.branch)
            print(json.dumps(prepared, indent=2, sort_keys=True))
        elif args.resolve_json:
            if args.local_only:
                ref = f"refs/heads/{args.branch}"
                if _git("show-ref", "--verify", "--quiet", ref, check=False).returncode != 0:
                    raise FullrepoError(f"local fullrepo branch {args.branch} does not exist")
            else:
                if not fetch_fullrepo(args.remote, args.branch):
                    raise FullrepoError(f"fullrepo branch {args.remote}/{args.branch} does not exist")
                ref = f"refs/remotes/{args.remote}/{args.branch}"
            print(json.dumps(resolve_fullrepo_ref(ref, args.source_ref), indent=2, sort_keys=True))
        elif args.migrate_main:
            migrate_main(dry_run=args.dry_run, ignore_project_policy=args.ignore_project_policy)
        elif args.bootstrap_init:
            bootstrap_init(
                args.remote,
                args.branch,
                dry_run=args.dry_run,
                create_missing=args.create_missing,
                ignore_project_policy=args.ignore_project_policy,
            )
    except FullrepoError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
