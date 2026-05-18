#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
unset CDPATH

INPUT_FILE=$(mktemp)
cleanup() {
  rm -f "$INPUT_FILE"
}
trap cleanup EXIT
cat >"$INPUT_FILE" 2>/dev/null || true

python3 - "$INPUT_FILE" <<'PY'
from __future__ import annotations

import json
import os
import re
import shlex
import sys
from pathlib import Path

input_file = Path(sys.argv[1])

def load_payload() -> dict:
    try:
        payload = json.loads(input_file.read_text(encoding="utf-8", errors="replace") or "{}")
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def emit_deny(reason: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )


def command_from_payload(payload: dict) -> str:
    if str(payload.get("tool_name", "")).lower() != "bash":
        return ""
    tool_input = payload.get("tool_input", {})
    if not isinstance(tool_input, dict):
        return ""
    command = tool_input.get("command", tool_input.get("cmd", ""))
    return command if isinstance(command, str) else ""


def resolve_repo_root(cwd: Path) -> Path | None:
    git_dir = cwd / ".git"
    if git_dir.exists():
        return cwd.resolve()
    for parent in cwd.parents:
        if (parent / ".git").exists():
            return parent.resolve()
    return None


def path_arg(token: str, cwd: Path) -> Path | None:
    if not token or token.startswith("-"):
        return None
    if "$" in token or "`" in token or token.startswith("("):
        return None
    try:
        path = Path(token)
        if not path.is_absolute():
            path = cwd / path
        return path.resolve(strict=False)
    except (OSError, RuntimeError):
        return None


def is_current_or_parent(candidate: Path, cwd: Path, repo_root: Path | None) -> bool:
    protected = [cwd.resolve()]
    if repo_root is not None:
        protected.append(repo_root)
    for item in protected:
        if candidate == item:
            return True
        try:
            item.relative_to(candidate)
        except ValueError:
            continue
        return True
    return False


def dangerous_paths_from_tokens(tokens: list[str], cwd: Path, repo_root: Path | None) -> list[str]:
    dangerous: list[str] = []
    for index, token in enumerate(tokens):
        base = Path(token).name
        if base == "mv":
            args = [t for t in tokens[index + 1 :] if not t.startswith("-")]
            # mv uses the last path as destination; only source paths can destroy
            # the active cwd for the current session.
            candidates = args[:-1] if len(args) >= 2 else args
        elif base in {"rm", "rmdir"}:
            candidates = [t for t in tokens[index + 1 :] if not t.startswith("-")]
        else:
            continue
        for raw in candidates:
            resolved = path_arg(raw, cwd)
            if resolved is not None and is_current_or_parent(resolved, cwd, repo_root):
                dangerous.append(raw)
    return dangerous


def has_shell_pwd_rename(command: str) -> bool:
    patterns = (
        r"\bmv\s+(?:['\"]?\$PWD['\"]?|\$\(pwd\)|`pwd`)\b",
        r"\brm\s+[^;&|]*?(?:['\"]?\$PWD['\"]?|\$\(pwd\)|`pwd`)\b",
        r"\brmdir\s+[^;&|]*?(?:['\"]?\$PWD['\"]?|\$\(pwd\)|`pwd`)\b",
    )
    return any(re.search(pattern, command) for pattern in patterns)


payload = load_payload()
command = command_from_payload(payload)
if not command:
    raise SystemExit(0)

raw_cwd = payload.get("cwd") or os.getcwd()
try:
    cwd = Path(str(raw_cwd)).resolve(strict=False)
except (OSError, RuntimeError):
    cwd = Path.cwd().resolve(strict=False)
repo_root = resolve_repo_root(cwd) if cwd.exists() else None

try:
    tokens = shlex.split(command, posix=True)
except ValueError:
    tokens = []

dangerous = dangerous_paths_from_tokens(tokens, cwd, repo_root)
if dangerous or has_shell_pwd_rename(command):
    reason = (
        "This command appears to rename or remove the active Codex session directory "
        "or its repository root. Codex hook commands run with the session cwd; after "
        "that path is renamed/deleted, later hooks can fail before their scripts start "
        "with 'No such file or directory'. Open a new Codex session from the parent/new "
        "path, or run the rename outside the active session after stopping Codex."
    )
    emit_deny(reason)
PY
