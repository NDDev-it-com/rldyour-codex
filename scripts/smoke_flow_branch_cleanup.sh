#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(git -C "$SCRIPT_DIR/.." rev-parse --show-toplevel)
STATE_SCRIPT="$ROOT/plugins/rldyour-flow/scripts/flow_post_task_state.py"
AUDIT_SCRIPT="$ROOT/plugins/rldyour-flow/scripts/git_sync_audit.sh"
TMP_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/rldyour-flow-branch-cleanup.XXXXXX")

cleanup() {
  rm -rf "$TMP_ROOT"
}
trap cleanup EXIT

fail() {
  printf 'fail    %s\n' "$1" >&2
  exit 1
}

ok() {
  printf 'ok      %s\n' "$1"
}

state_json() {
  (cd "$TMP_ROOT/work" && python3 "$STATE_SCRIPT")
}

json_bool() {
  python3 -c 'import json,sys; data=json.load(sys.stdin); path=sys.argv[1].split("."); cur=data
for key in path:
    cur=cur[key]
print("true" if cur else "false")' "$1"
}

json_contains() {
  python3 -c 'import json,sys; data=json.load(sys.stdin); path=sys.argv[1].split("."); value=sys.argv[2]; cur=data
for key in path:
    cur=cur[key]
print("true" if value in cur else "false")' "$1" "$2"
}

git init --bare -q "$TMP_ROOT/origin.git"
git init -q "$TMP_ROOT/work"
git -C "$TMP_ROOT/work" config user.email "flow-branch-cleanup@example.invalid"
git -C "$TMP_ROOT/work" config user.name "Flow Branch Cleanup"
git -C "$TMP_ROOT/work" remote add origin "$TMP_ROOT/origin.git"

printf '# Fixture\n' > "$TMP_ROOT/work/README.md"
git -C "$TMP_ROOT/work" add README.md
git -C "$TMP_ROOT/work" commit -q -m "chore: initial fixture"
git -C "$TMP_ROOT/work" branch -M main
git -C "$TMP_ROOT/work" push -q -u origin main

audit_output=$(cd "$TMP_ROOT/work" && "$AUDIT_SCRIPT")
if printf '%s\n' "$audit_output" | grep -Fx "origin" >/dev/null; then
  fail "git sync audit reported remote HEAD symref as cleanup candidate"
fi
ok "git sync audit ignores remote HEAD symref"

git -C "$TMP_ROOT/work" checkout -q -b ai/ry-start-cleanup-fixture
printf 'workflow branch\n' > "$TMP_ROOT/work/feature.txt"
git -C "$TMP_ROOT/work" add feature.txt
git -C "$TMP_ROOT/work" commit -q -m "feat: workflow fixture"
git -C "$TMP_ROOT/work" push -q -u origin ai/ry-start-cleanup-fixture

git -C "$TMP_ROOT/work" checkout -q main
git -C "$TMP_ROOT/work" merge -q --no-ff ai/ry-start-cleanup-fixture -m "merge workflow fixture"
git -C "$TMP_ROOT/work" push -q origin main

payload=$(state_json)
printf '%s' "$payload" | json_contains "branch_cleanup_state.local_merged_branches" "ai/ry-start-cleanup-fixture" | grep -Fx true >/dev/null \
  || fail "state did not report merged local workflow branch"
printf '%s' "$payload" | json_contains "branch_cleanup_state.remote_merged_branches" "origin/ai/ry-start-cleanup-fixture" | grep -Fx true >/dev/null \
  || fail "state did not report merged remote workflow branch"
printf '%s' "$payload" | json_bool "branch_cleanup_state.needs_cleanup" | grep -Fx true >/dev/null \
  || fail "state did not require branch cleanup"
printf '%s' "$payload" | json_bool "needs_flow_sync" | grep -Fx true >/dev/null \
  || fail "flow sync was not required for merged branch cleanup"
ok "flow state requires cleanup for merged local and remote workflow branches"

git -C "$TMP_ROOT/work" branch -d ai/ry-start-cleanup-fixture >/dev/null
git -C "$TMP_ROOT/work" push -q origin --delete ai/ry-start-cleanup-fixture
git -C "$TMP_ROOT/work" fetch -q --prune origin

payload=$(state_json)
printf '%s' "$payload" | json_bool "branch_cleanup_state.needs_cleanup" | grep -Fx false >/dev/null \
  || fail "state still required cleanup after deleting merged workflow branches"
ok "flow state clears cleanup requirement after branch removal"

printf 'Flow branch cleanup smoke passed.\n'
