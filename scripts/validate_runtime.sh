#!/usr/bin/env bash
set -euo pipefail

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$ROOT"

STRICT_RUNTIME=0
CODEX_HOME_DIR=""

usage() {
  cat <<'EOF'
Usage: scripts/validate_runtime.sh [--codex-home PATH] [--strict-runtime]

Runs installed-runtime validation against a temporary CODEX_HOME by default.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --codex-home)
      shift
      CODEX_HOME_DIR=${1:?--codex-home requires a path}
      ;;
    --strict|--strict-runtime)
      STRICT_RUNTIME=1
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

cleanup_tmp=""
if [ -z "$CODEX_HOME_DIR" ]; then
  CODEX_HOME_DIR=$(mktemp -d "${TMPDIR:-/tmp}/rldyour-codex-runtime.XXXXXX")
  cleanup_tmp=$CODEX_HOME_DIR
fi

cleanup() {
  if [ -n "$cleanup_tmp" ]; then
    rm -rf "$cleanup_tmp"
  fi
}
trap cleanup EXIT

strict_args=()
if [ "$STRICT_RUNTIME" -eq 1 ]; then
  strict_args+=(--strict-runtime)
fi

scripts/install_system_codex.sh --dry-run --codex-home "$CODEX_HOME_DIR" "${strict_args[@]}"
scripts/install_system_codex.sh --apply --codex-home "$CODEX_HOME_DIR" "${strict_args[@]}"
scripts/doctor_system_codex.sh --quick --codex-home "$CODEX_HOME_DIR" "${strict_args[@]}"
if command -v codex >/dev/null 2>&1; then
  CODEX_HOME="$CODEX_HOME_DIR" scripts/validate_execpolicy_rules.sh "$CODEX_HOME_DIR/rules"
elif [ "$STRICT_RUNTIME" -eq 1 ]; then
  printf 'codex command not found; strict runtime execpolicy validation cannot run.\n' >&2
  exit 1
else
  printf 'skip    execpolicy rules validation: codex command not found\n'
fi
scripts/smoke_hooks.sh --codex-home "$CODEX_HOME_DIR"
scripts/smoke_fullrepo_sync.sh
scripts/smoke_fullrepo_bootstrap_init.sh

printf 'Runtime validation passed with CODEX_HOME=%s.\n' "$CODEX_HOME_DIR"
