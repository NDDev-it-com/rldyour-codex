#!/usr/bin/env bash
# session_start_dispatcher.sh — serialize Flow SessionStart bootstrap and context.

set -euo pipefail
IFS=$'\n\t'
unset CDPATH

HOOK_INPUT=$(cat 2>/dev/null || true)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK_INPUT_FILE=$(mktemp "${TMPDIR:-/tmp}/rldyour-session-start-input.XXXXXX")
trap 'rm -f "$HOOK_INPUT_FILE"' EXIT
printf '%s' "$HOOK_INPUT" > "$HOOK_INPUT_FILE"

python3 - "$SCRIPT_DIR" "$HOOK_INPUT_FILE" <<'PY'
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

OUTPUT_LIMIT = 8192
FAILURE_PREVIEW_LINES = 12
CHILDREN = (
    ("bootstrap", "session_start_worktree_bootstrap.sh", 6),
    ("context", "session_start_context.sh", 8),
)


script_dir = Path(sys.argv[1])
hook_input = Path(sys.argv[2]).read_text(encoding="utf-8", errors="replace")


def cap_output(text: str, limit: int = OUTPUT_LIMIT) -> str:
    if len(text) <= limit:
        return text
    omitted = len(text) - limit
    return text[:limit].rstrip() + f"\n... truncated {omitted} bytes"


def run_child(script_name: str, timeout_seconds: int) -> tuple[int, str]:
    script_path = script_dir / script_name
    if not script_path.is_file():
        return 127, f"{script_name} missing: {script_path}"
    try:
        proc = subprocess.run(
            ["bash", str(script_path)],
            input=hook_input,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        output = ""
        if isinstance(exc.output, str):
            output += exc.output
        if isinstance(exc.stderr, str):
            output += exc.stderr
        return 124, cap_output(f"{script_name} timed out after {timeout_seconds}s.\n{output}".strip())
    return proc.returncode, cap_output(proc.stdout or "")


def preview(text: str, limit: int = FAILURE_PREVIEW_LINES) -> str:
    lines = [line for line in text.splitlines() if line.strip()]
    shown = lines[:limit]
    if len(lines) > limit:
        shown.append(f"... plus {len(lines) - limit} more lines")
    return "\n".join(shown)


def extract_context(label: str, status: int, output: str) -> str:
    trimmed = output.strip()
    if status != 0:
        details = preview(trimmed)
        suffix = f"\n{details}" if details else ""
        return f"rldyour-flow SessionStart {label} failed with exit {status}.{suffix}"
    if not trimmed:
        return ""
    try:
        payload = json.loads(trimmed)
    except json.JSONDecodeError:
        return trimmed
    hook_specific = payload.get("hookSpecificOutput")
    if isinstance(hook_specific, dict):
        context = hook_specific.get("additionalContext")
        if isinstance(context, str):
            return context.strip()
    system_message = payload.get("systemMessage")
    if isinstance(system_message, str):
        return system_message.strip()
    return trimmed


contexts = [
    context
    for context in (extract_context(label, *run_child(script_name, timeout)) for label, script_name, timeout in CHILDREN)
    if context
]

if not contexts:
    raise SystemExit(0)

print(
    json.dumps(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": "\n\n".join(contexts),
            }
        }
    )
)
PY
