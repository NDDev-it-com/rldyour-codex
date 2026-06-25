#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if ROOT=$(git -C "$SCRIPT_DIR/.." rev-parse --show-toplevel 2>/dev/null); then
  :
else
  ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
fi

TMP_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/rldyour-serena-memory-freshness.XXXXXX")

cleanup() {
  rm -rf "$TMP_ROOT"
}
trap cleanup EXIT

current_state="$TMP_ROOT/current.json"
stale_state="$TMP_ROOT/stale.json"
stale_err="$TMP_ROOT/stale.err"

printf '{"head_sha":"abc1234","is_current":true}\n' > "$current_state"
printf '{"head_sha":"def5678","is_current":false}\n' > "$stale_state"

# Memories are ordinary tracked files on main; freshness is checked against the
# checked-out HEAD with no branch-specific skip.
python3 "$ROOT/scripts/check_serena_memory_freshness.py" \
  --root "$ROOT" \
  --state-file "$current_state" >/dev/null

if python3 "$ROOT/scripts/check_serena_memory_freshness.py" \
  --root "$ROOT" \
  --state-file "$stale_state" 2>"$stale_err"; then
  printf 'stale Serena memory payload unexpectedly passed\n' >&2
  exit 1
fi

grep -q 'Serena memories are stale for HEAD' "$stale_err"

printf 'Serena memory freshness smoke passed.\n'
