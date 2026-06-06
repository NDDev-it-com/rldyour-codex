#!/usr/bin/env bash
# session_start_worktree_bootstrap.sh — restore agent-only files into a fresh
# git worktree on first SessionStart.
#
# This hook runs a local-only fullrepo restore only when canonical agent-only
# markers are missing and a local origin/fullrepo ref already exists. It never
# fetches, publishes, pushes, commits, or edits non-agent project files.

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
POLICY_SCRIPT="$PLUGIN_DIR/scripts/project_flow_policy.py"

if [ ! -f "$FULLREPO_SCRIPT" ]; then
  exit 0
fi

RLDYOUR_FULLREPO_MODE=${RLDYOUR_FULLREPO_MODE:-auto}
RLDYOUR_FULLREPO_RESTORE=${RLDYOUR_FULLREPO_RESTORE:-1}
if [ -f "$POLICY_SCRIPT" ]; then
  eval "$(python3 "$POLICY_SCRIPT" --shell 2>/dev/null || true)"
fi
if [ "$RLDYOUR_FULLREPO_MODE" = "disabled" ] || [ "$RLDYOUR_FULLREPO_RESTORE" != "1" ]; then
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

FULLREPO_REMOTE=${RLDYOUR_FULLREPO_REMOTE:-origin}
FULLREPO_BRANCH=${RLDYOUR_FULLREPO_BRANCH:-fullrepo}
if ! git show-ref --verify --quiet "refs/remotes/${FULLREPO_REMOTE}/${FULLREPO_BRANCH}"; then
  exit 0
fi

set +e
RESTORE_OUT=$(python3 "$FULLREPO_SCRIPT" --remote "$FULLREPO_REMOTE" --branch "$FULLREPO_BRANCH" --restore-local 2>&1)
RESTORE_STATUS=$?
set -e

python3 - "$ROOT" "$RESTORE_STATUS" "$RESTORE_OUT" <<'PY'
import json
import sys

root, raw_status, restore_out = sys.argv[1:4]
try:
    restore_status = int(raw_status)
except ValueError:
    restore_status = 1
lines = [line for line in restore_out.splitlines() if line.strip()]
preview = lines[:12]
trailing = max(len(lines) - len(preview), 0)

if restore_status == 0:
    advisory_lines = [
        "rldyour-flow worktree bootstrap (auto-restored from local fullrepo ref):",
        f"- Worktree root: {root}.",
        "- A canonical agent-only marker (.serena/project.yml / AGENTS.md / .claude/CLAUDE.md) was missing,",
        "  so plugins/rldyour-flow/scripts/fullrepo_sync.py --restore-local ran to install the .git/info/exclude",
        "  block for this worktree and check out agent-only paths from the existing local origin/fullrepo ref.",
        "- This restore is additive and offline: no fetch, no commits, no pushes, no fullrepo --publish.",
        "- Set RLDYOUR_SKIP_WORKTREE_BOOTSTRAP=1 before starting Codex to disable this hook.",
        "- Output:",
    ]
else:
    advisory_lines = [
        "rldyour-flow worktree bootstrap (restore failed):",
        f"- Worktree root: {root}.",
        "- A canonical agent-only marker (.serena/project.yml / AGENTS.md / .claude/CLAUDE.md) was missing,",
        "  but plugins/rldyour-flow/scripts/fullrepo_sync.py --restore-local exited non-zero.",
        "- Codex continues with the current worktree state; run scripts/sync_fullrepo_branch.sh --bootstrap-init manually if agent context is missing.",
        "- This hook did not fetch, publish, push, commit, or edit non-agent files.",
        f"- Exit status: {restore_status}.",
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
