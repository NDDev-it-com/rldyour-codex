#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
unset CDPATH

HOOK_INPUT=$(cat 2>/dev/null || true)

if [ "${RLDYOUR_SKIP_STOP_GATES:-0}" = "1" ] || [ "${RLDYOUR_SKIP_FLOW_SYNC:-0}" = "1" ]; then
  exit 0
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  exit 0
fi

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$ROOT"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
STATE_SCRIPT="$PLUGIN_DIR/scripts/flow_post_task_state.py"
SYNC_MARKER=".serena/.flow_sync_marker"
ACK_MARKER=".serena/.flow_blocker_ack.json"

if [ ! -f "$STATE_SCRIPT" ]; then
  exit 0
fi

STATE_JSON=$(RLDYOUR_FLOW_STATE_LOCAL_ONLY=1 RLDYOUR_FULLREPO_STATUS_LOCAL_ONLY=1 python3 "$STATE_SCRIPT" 2>/dev/null || true)
if [ -z "$STATE_JSON" ]; then
  exit 0
fi

SERENA_CURRENT=$(printf "%s" "$STATE_JSON" | python3 -c 'import json,sys; print("true" if json.load(sys.stdin).get("serena_current") else "false")' 2>/dev/null || echo "true")
NEEDS_SYNC=$(printf "%s" "$STATE_JSON" | python3 -c 'import json,sys; print("true" if json.load(sys.stdin).get("needs_flow_sync") else "false")' 2>/dev/null || echo "false")
FINGERPRINT=$(printf "%s" "$STATE_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("fingerprint", ""))' 2>/dev/null || true)
HEAD_SHA=$(printf "%s" "$STATE_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("head_sha", ""))' 2>/dev/null || true)

# Serena owns memory freshness. Flow waits for Serena Stop hook to finish first.
if [ "$SERENA_CURRENT" != "true" ]; then
  exit 0
fi

if [ "$NEEDS_SYNC" != "true" ] || [ -z "$FINGERPRINT" ]; then
  rm -f "$SYNC_MARKER" "$ACK_MARKER" .serena/.flow_post_task_state.json
  exit 0
fi

STOP_HOOK_ACTIVE=$(printf "%s" "$HOOK_INPUT" | python3 -c '
import json
import sys

try:
    payload = json.load(sys.stdin)
except Exception:
    payload = {}

print("true" if payload.get("stop_hook_active") is True else "false")
' 2>/dev/null || echo "false")

if [ "$STOP_HOOK_ACTIVE" = "true" ] && [ -f "$SYNC_MARKER" ] && [ "$(cat "$SYNC_MARKER" 2>/dev/null || true)" = "$FINGERPRINT" ]; then
  mkdir -p .serena
  printf "%s" "$STATE_JSON" > .serena/.flow_post_task_state.json
  STATE_PATH=".serena/.flow_post_task_state.json" FINGERPRINT="$FINGERPRINT" HEAD_SHA="$HEAD_SHA" ACK_MARKER="$ACK_MARKER" python3 <<'PY'
import json
import os
from datetime import datetime, timezone
from pathlib import Path

state_path = Path(os.environ["STATE_PATH"])
try:
    state = json.loads(state_path.read_text(encoding="utf-8"))
except Exception:
    state = {}
policy = state.get("project_policy", {})
ack = {
    "schema_version": 1,
    "fingerprint": os.environ.get("FINGERPRINT", ""),
    "head": state.get("head_full") or os.environ.get("HEAD_SHA", ""),
    "reported_at": datetime.now(timezone.utc).isoformat(),
    "blocked_reasons": state.get("blocking_reasons", []),
    "advisory_reasons": state.get("advisory_reasons", []),
    "policy_source": policy.get("source", "built-in defaults") if isinstance(policy, dict) else "built-in defaults",
}
Path(os.environ["ACK_MARKER"]).write_text(json.dumps(ack, sort_keys=True) + "\n", encoding="utf-8")

print(json.dumps({
    "systemMessage": (
        "rldyour-flow post-task sync was already requested for this state. "
        "Allowing stop now to avoid a Stop-hook loop."
    )
}))
PY
  exit 0
fi

mkdir -p .serena
printf "%s\n" "$FINGERPRINT" > "$SYNC_MARKER"
printf "%s" "$STATE_JSON" > .serena/.flow_post_task_state.json

SUMMARY=$(printf "%s" "$STATE_JSON" | python3 -c '
import json
import sys

payload = json.load(sys.stdin)
fullrepo_state = payload.get("fullrepo_state", {})
if not isinstance(fullrepo_state, dict):
    fullrepo_state = {}
instruction_docs_state = payload.get("instruction_docs_state", {})
if not isinstance(instruction_docs_state, dict):
    instruction_docs_state = {}
tracked_agent_paths = fullrepo_state.get("tracked_agent_paths", [])
if not isinstance(tracked_agent_paths, list):
    tracked_agent_paths = []
branch_cleanup_state = payload.get("branch_cleanup_state", {})
if not isinstance(branch_cleanup_state, dict):
    branch_cleanup_state = {}
print(json.dumps({
    "branch": payload.get("branch"),
    "head": payload.get("head_sha"),
    "dirty_files": payload.get("dirty_files", []),
    "doc_files_present": payload.get("doc_files_present", []),
    "doc_files_changed": payload.get("doc_files_changed", []),
    "ahead": payload.get("ahead", 0),
    "behind": payload.get("behind", 0),
    "worktree_count": payload.get("worktree_count", 0),
    "project_policy": {
        "source": payload.get("project_policy", {}).get("source") if isinstance(payload.get("project_policy"), dict) else None,
        "source_kind": payload.get("project_policy", {}).get("source_kind") if isinstance(payload.get("project_policy"), dict) else None,
        "profile": payload.get("project_policy", {}).get("profile") if isinstance(payload.get("project_policy"), dict) else None,
        "valid": payload.get("project_policy", {}).get("valid") if isinstance(payload.get("project_policy"), dict) else None,
    },
    "blocking_reasons": payload.get("blocking_reasons", []),
    "advisory_reasons": payload.get("advisory_reasons", []),
    "instruction_docs": {
        "mode": instruction_docs_state.get("instruction_docs_mode", "auto"),
        "required": instruction_docs_state.get("required_docs", []),
        "present": instruction_docs_state.get("present_docs", []),
        "missing": instruction_docs_state.get("missing_docs", []),
        "review_needed": bool(instruction_docs_state.get("needs_instruction_docs_review")),
        "review_reasons": instruction_docs_state.get("review_reasons", []),
    },
    "fullrepo": {
        "mode": fullrepo_state.get("mode", "auto"),
        "branch": fullrepo_state.get("fullrepo_branch", "fullrepo"),
        "remote_exists": bool(fullrepo_state.get("remote_fullrepo_exists")),
        "exclude_installed": bool(fullrepo_state.get("exclude_installed", False)),
        "tracked_agent_paths": len(tracked_agent_paths),
    },
    "branch_cleanup": {
        "mode": branch_cleanup_state.get("mode", "advisory"),
        "base": branch_cleanup_state.get("base"),
        "local_merged_branches": branch_cleanup_state.get("local_merged_branches", []),
        "remote_merged_branches": branch_cleanup_state.get("remote_merged_branches", []),
        "blocking_candidates": branch_cleanup_state.get("blocking_candidates", []),
        "advisory_candidates": branch_cleanup_state.get("advisory_candidates", []),
        "worktree_cleanup_candidates": branch_cleanup_state.get("worktree_cleanup_candidates", []),
        "needs_cleanup": bool(branch_cleanup_state.get("needs_cleanup")),
    },
}, ensure_ascii=False, indent=2))
')

POLICY_GUIDANCE=$(printf "%s" "$STATE_JSON" | python3 -c '
import json
import sys

payload = json.load(sys.stdin)
policy = payload.get("project_policy", {})
effective = policy.get("effective", {}) if isinstance(policy, dict) else {}
fullrepo = effective.get("fullrepo", {}) if isinstance(effective.get("fullrepo"), dict) else {}
normal = effective.get("normal_branch_policy", {}) if isinstance(effective.get("normal_branch_policy"), dict) else {}
branch_cleanup = effective.get("branch_cleanup", {}) if isinstance(effective.get("branch_cleanup"), dict) else {}
instruction_docs = effective.get("instruction_docs", {}) if isinstance(effective.get("instruction_docs"), dict) else {}

policy_source = policy.get("source", "built-in defaults")
policy_source_kind = policy.get("source_kind", "default")
lines = [
    f"Project policy source: {policy_source} ({policy_source_kind}).",
]
fullrepo_mode = fullrepo.get("mode", "auto")
if fullrepo_mode == "disabled":
    lines.append("Fullrepo is disabled by project policy; do not restore, migrate, publish, create, or install fullrepo excludes.")
elif fullrepo_mode == "advisory":
    lines.append("Fullrepo is advisory; report drift but do not block Stop or publish without explicit user instruction.")
else:
    lines.append("Use fullrepo only when the effective project policy requires or allows it; do not create a missing fullrepo branch unless policy or current user instruction explicitly allows creation.")

if normal.get("agent_files") == "allowed":
    lines.append("Configured AI instruction files may be tracked in normal branches; do not migrate them to fullrepo.")

doc_mode = instruction_docs.get("mode", "auto")
if doc_mode == "tracked-normal-branch":
    lines.append("Instruction docs are tracked normal-branch files for this project.")
elif doc_mode == "disabled":
    lines.append("Instruction docs sync is disabled unless the user explicitly requests it.")

cleanup_mode = branch_cleanup.get("mode", "advisory")
if cleanup_mode == "disabled":
    lines.append("Branch cleanup is disabled by project policy.")
elif cleanup_mode == "advisory":
    lines.append("Merged branch cleanup is advisory; do not delete local or remote branches without explicit user confirmation.")
else:
    lines.append("Branch cleanup is strict only for configured workflow prefixes; never delete protected branches.")

print("\n".join(lines))
')

MESSAGE="[RLDYOUR-FLOW POST-TASK SYNC REQUIRED] Serena memories are current for HEAD ${HEAD_SHA:-unknown}; now synchronize project docs and git state.

Current state:
${SUMMARY}

Effective policy:
${POLICY_GUIDANCE}

Continue this turn and run the \$flow-post-task-sync workflow now.

Installed rldyour-flow script paths for repositories that do not vendor this plugin:
- Flow state: ${STATE_SCRIPT}
- Fullrepo sync: ${PLUGIN_DIR}/scripts/fullrepo_sync.py
- Git sync audit: ${PLUGIN_DIR}/scripts/git_sync_audit.sh
- Instruction docs state: ${PLUGIN_DIR}/scripts/instruction_docs_state.py

Use repo-local scripts only when they exist; otherwise use the installed paths above.

Required order:
1. Verify Serena memories are current. Do not duplicate Serena memory sync.
2. Run \$instruction-docs-sync when instruction docs review is needed. Keep AGENTS.md Codex-native and .claude/CLAUDE.md Claude Code-native, using only verified project rules, commands, deploy contracts, quality gates, or workflow facts.
3. Review all uncommitted changes. Do not commit secrets, runtime markers, browser artifacts, or accidental junk.
4. Run applicable quality checks or document why a check is unavailable.
5. Commit atomically with Conventional Commits. Keep Serena knowledge/docs sync commits separate when useful.
6. Push/synchronize with GitHub using git/gh when an upstream exists.
7. Follow the effective fullrepo policy above; publish or migrate fullrepo only when policy and current user instruction allow it.
8. Treat branch cleanup according to policy; never delete protected branches or remote branches without explicit confirmation.
9. Stop again after sync or report the exact blocker."

echo "$MESSAGE" >&2
exit 2
