#!/usr/bin/env bash
# session_start_worktree_bootstrap.sh — restore agent-only files into a fresh
# git worktree on first SessionStart.
#
# This hook runs fullrepo_sync.py --restore only when canonical agent-only
# markers are missing and origin/fullrepo exists. It never publishes, never
# pushes, and never edits non-agent project files.

set -euo pipefail
IFS=$'\n\t'
unset CDPATH

if [ "${RLDYOUR_SKIP_WORKTREE_BOOTSTRAP:-0}" = "1" ]; then
  exit 0
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  exit 0
fi

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$ROOT"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
FULLREPO_SCRIPT="$PLUGIN_DIR/scripts/fullrepo_sync.py"

if [ ! -f "$FULLREPO_SCRIPT" ]; then
  exit 0
fi

need_bootstrap=0
for marker in ".serena/project.yml" "AGENTS.md" ".claude/CLAUDE.md"; do
  if [ ! -e "$ROOT/$marker" ]; then
    need_bootstrap=1
    break
  fi
done

if [ "$need_bootstrap" = "0" ]; then
  exit 0
fi

STATUS_JSON=$(python3 "$FULLREPO_SCRIPT" --status-json 2>/dev/null || true)
if [ -z "$STATUS_JSON" ]; then
  exit 0
fi

remote_present=$(printf "%s" "$STATUS_JSON" | python3 -c '
import json
import sys

try:
    state = json.load(sys.stdin)
except Exception:
    print("false")
    raise SystemExit(0)
print("true" if state.get("remote_fullrepo_exists") else "false")
' 2>/dev/null || echo "false")

if [ "$remote_present" != "true" ]; then
  exit 0
fi

RESTORE_OUT=$(python3 "$FULLREPO_SCRIPT" --restore 2>&1 || true)

python3 - "$ROOT" "$RESTORE_OUT" <<'PY'
import json
import sys

root, restore_out = sys.argv[1:3]
lines = [line for line in restore_out.splitlines() if line.strip()]
preview = lines[:12]
trailing = max(len(lines) - len(preview), 0)

advisory_lines = [
    "rldyour-flow worktree bootstrap (auto-restored from origin/fullrepo):",
    f"- Worktree root: {root}.",
    "- A canonical agent-only marker (.serena/project.yml / AGENTS.md / .claude/CLAUDE.md) was missing,",
    "  so plugins/rldyour-flow/scripts/fullrepo_sync.py --restore ran to install the .git/info/exclude",
    "  block for this worktree and check out agent-only paths from origin/fullrepo.",
    "- This restore is additive: no commits, no pushes, no fullrepo --publish.",
    "- Set RLDYOUR_SKIP_WORKTREE_BOOTSTRAP=1 before starting Codex to disable this hook.",
    "- Output:",
]
for line in preview:
    advisory_lines.append(f"  {line}")
if trailing:
    advisory_lines.append(f"  ... plus {trailing} more lines")

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "\n".join(advisory_lines),
    }
}))
PY
