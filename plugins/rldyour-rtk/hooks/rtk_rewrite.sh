#!/usr/bin/env bash
# rldyour-rtk (Codex) opt-in PreToolUse Bash hook.
#
# DEFAULT OFF. This hook is a no-op passthrough unless RTK_CODEX_HOOK=1 is set.
# When enabled, it delegates to `rtk rewrite` and returns a Codex
# hookSpecificOutput.updatedInput so the supported command runs through rtk and
# its output is compressed before it reaches context. Codex PreToolUse supports
# updatedInput (verified against openai/codex), so this is a real rewrite, not a
# probabilistic hint. The primary, always-on rtk mechanism for Codex remains the
# AGENTS.md / RTK.md rules file.
#
# Compression scope and validator/verbatim exclusions are governed
# machine-globally by ~/.config/rtk/config.toml [hooks] exclude_commands (see the
# control plane config/token-economy-policy.json).
set -euo pipefail
IFS=$'\n\t'

# Opt-in gate: inert unless explicitly enabled by the owner.
[ "${RTK_CODEX_HOOK:-0}" = "1" ] || exit 0
# Graceful: no rtk on PATH -> passthrough, original command runs unchanged.
command -v rtk >/dev/null 2>&1 || exit 0

INPUT_FILE=$(mktemp)
trap 'rm -f "$INPUT_FILE"' EXIT
cat >"$INPUT_FILE" 2>/dev/null || true

python3 - "$INPUT_FILE" <<'PY'
import json
import subprocess
import sys
from pathlib import Path

try:
    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace") or "{}")
except Exception:
    raise SystemExit(0)
if not isinstance(payload, dict) or str(payload.get("tool_name", "")).lower() != "bash":
    raise SystemExit(0)
tool_input = payload.get("tool_input") or {}
command = tool_input.get("command", tool_input.get("cmd", "")) if isinstance(tool_input, dict) else ""
if not isinstance(command, str) or not command.strip():
    raise SystemExit(0)

try:
    result = subprocess.run(["rtk", "rewrite", command], capture_output=True, text=True, timeout=8)
except Exception:
    raise SystemExit(0)

rewritten = (result.stdout or "").strip()
# rtk rewrite prints the rewritten command, or the original / empty when there is
# no rtk equivalent. Emit updatedInput only when it is a single-line command that
# actually changed and is an rtk invocation (defensive; never emit garbage).
if (
    result.returncode != 0
    or not rewritten
    or "\n" in rewritten
    or rewritten == command.strip()
    or not rewritten.startswith("rtk ")
):
    raise SystemExit(0)

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "permissionDecisionReason": "rtk token-economy rewrite",
        "updatedInput": {"command": rewritten},
    }
}))
PY
