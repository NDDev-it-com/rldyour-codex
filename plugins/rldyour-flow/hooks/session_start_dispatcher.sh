#!/usr/bin/env bash
# session_start_dispatcher.sh — serialize Flow SessionStart bootstrap and context.

set -euo pipefail
IFS=$'\n\t'
unset CDPATH

HOOK_INPUT=$(cat 2>/dev/null || true)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

run_child() {
  local script_name=$1
  local script_path="$SCRIPT_DIR/$script_name"
  local output
  local status

  if [ ! -f "$script_path" ]; then
    printf '127\t%s missing: %s\n' "$script_name" "$script_path"
    return 0
  fi

  set +e
  output=$(printf '%s' "$HOOK_INPUT" | bash "$script_path" 2>&1)
  status=$?
  set -e

  printf '%s\t%s' "$status" "$output"
}

BOOTSTRAP_RESULT=$(run_child session_start_worktree_bootstrap.sh)
CONTEXT_RESULT=$(run_child session_start_context.sh)

python3 - "$BOOTSTRAP_RESULT" "$CONTEXT_RESULT" <<'PY'
from __future__ import annotations

import json
import sys


def split_result(raw: str) -> tuple[int, str]:
    first, sep, rest = raw.partition("\t")
    if not sep:
        return 1, raw
    try:
        return int(first), rest
    except ValueError:
        return 1, raw


def preview(text: str, limit: int = 12) -> str:
    lines = [line for line in text.splitlines() if line.strip()]
    shown = lines[:limit]
    if len(lines) > limit:
        shown.append(f"... plus {len(lines) - limit} more lines")
    return "\n".join(shown)


def extract_context(label: str, raw: str) -> str:
    status, output = split_result(raw)
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
    for context in (
        extract_context("bootstrap", sys.argv[1]),
        extract_context("context", sys.argv[2]),
    )
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
