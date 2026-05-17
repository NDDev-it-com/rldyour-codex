#!/usr/bin/env bash
set -euo pipefail

KEEP=0
REQUIRE_CODEX=0

usage() {
  cat <<'EOF'
Usage: scripts/smoke_clean_bootstrap.sh [--keep] [--require-codex]

Proves a clean-machine style path with temporary state:
1. clone the current repository;
2. restore/publish agent-only context through fullrepo bootstrap init;
3. install into a temporary CODEX_HOME;
4. run doctor/validation against that temporary install;
5. verify MCP registration and plugin routing from the cloned repo.

By default this smoke skips the live `codex mcp list` probe when Codex CLI is
not installed. Use --require-codex for strict runtime environments.

The repository must be clean so the cloned copy matches committed source of truth.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --keep)
      KEEP=1
      ;;
    --require-codex)
      REQUIRE_CODEX=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if ROOT=$(git -C "$SCRIPT_DIR/.." rev-parse --show-toplevel 2>/dev/null); then
  :
else
  ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
fi

if [ -n "$(git -C "$ROOT" status --porcelain)" ]; then
  printf 'Working tree must be clean before clean bootstrap smoke.\n' >&2
  git -C "$ROOT" status -sb >&2
  exit 1
fi

TMP_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/rldyour-clean-bootstrap.XXXXXX")
cleanup() {
  if [ "$KEEP" -ne 1 ]; then
    rm -rf "$TMP_ROOT"
  else
    printf 'Kept clean bootstrap workspace: %s\n' "$TMP_ROOT"
  fi
}
trap cleanup EXIT

CLONE_DIR="$TMP_ROOT/repo"
CODEX_HOME_DIR="$TMP_ROOT/codex-home"
SERENA_HOME_DIR="$TMP_ROOT/serena-home"

printf 'Clean bootstrap workspace: %s\n' "$TMP_ROOT"
if ! git clone --quiet --local "$ROOT" "$CLONE_DIR"; then
  printf 'Local clone failed; retrying with --no-local for cross-device filesystems.\n' >&2
  rm -rf "$CLONE_DIR"
  git clone --quiet --no-local "$ROOT" "$CLONE_DIR"
fi

cd "$CLONE_DIR"
git config user.name "rldyour-clean-bootstrap"
git config user.email "rldyour-clean-bootstrap@example.invalid"

scripts/sync_fullrepo_branch.sh --bootstrap-init
scripts/install_system_codex.sh --dry-run --codex-home "$CODEX_HOME_DIR"
scripts/install_system_codex.sh --apply --codex-home "$CODEX_HOME_DIR"

RLDYOUR_MCP_CAPABILITY_LIST_ONLY=1 \
RLDYOUR_MCP_CAPABILITY_ALLOW_MISSING_ENV=1 \
CODEX_HOME="$CODEX_HOME_DIR" \
SERENA_HOME="$SERENA_HOME_DIR" \
  scripts/doctor_system_codex.sh --codex-home "$CODEX_HOME_DIR"

if command -v codex >/dev/null 2>&1; then
  CODEX_HOME="$CODEX_HOME_DIR" codex mcp list >/dev/null
elif [ "$REQUIRE_CODEX" -eq 1 ]; then
  printf 'codex command not found; --require-codex was requested.\n' >&2
  exit 1
else
  printf 'skip    codex mcp list: codex command not found\n'
fi
python3 plugins/rldyour-flow/scripts/fullrepo_sync.py --status-json | python3 -m json.tool >/dev/null
scripts/smoke_fullrepo_sync.sh
scripts/smoke_fullrepo_bootstrap_init.sh

printf '\nClean bootstrap smoke passed.\n'
