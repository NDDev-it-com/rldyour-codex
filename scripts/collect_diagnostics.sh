#!/usr/bin/env bash
set -euo pipefail

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$ROOT"

OUTPUT=""
INCLUDE_DOCTOR=0

usage() {
  cat <<'EOF'
Usage: scripts/collect_diagnostics.sh [--output DIR] [--include-doctor]

Collect a sanitized local diagnostics bundle for rldyour-codex.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --output)
      OUTPUT=${2:-}
      if [ -z "$OUTPUT" ]; then
        printf 'missing value for --output\n' >&2
        exit 1
      fi
      shift 2
      ;;
    --include-doctor)
      INCLUDE_DOCTOR=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [ -z "$OUTPUT" ]; then
  timestamp=$(date -u '+%Y%m%dT%H%M%SZ')
  OUTPUT="diagnostics/rldyour-codex-${timestamp}"
fi

mkdir -p "$OUTPUT"

run_capture() {
  local name=$1
  shift
  {
    printf '$'
    printf ' %q' "$@"
    printf '\n\n'
    "$@"
  } >"$OUTPUT/$name" 2>&1 || {
    status=$?
    printf '\n[command exited with status %s]\n' "$status" >>"$OUTPUT/$name"
    return 0
  }
}

{
  printf 'generated_at=%s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  printf 'root=%s\n' "$ROOT"
  printf 'codex_home=%s\n' "${CODEX_HOME:-$HOME/.codex}"
  printf 'uname=%s\n' "$(uname -a)"
} >"$OUTPUT/metadata.txt"

run_capture git-status.txt git status -sb --ignored
run_capture git-log.txt git log --oneline -20
run_capture git-branch.txt git branch -avv

if command -v codex >/dev/null 2>&1; then
  run_capture codex-version.txt codex --version
  run_capture codex-mcp-list.txt codex mcp list
else
  printf 'codex command not found\n' >"$OUTPUT/codex-version.txt"
fi

if command -v gh >/dev/null 2>&1; then
  run_capture github-runs.txt gh run list --repo rldyourmnd/rldyour-codex --limit 10
fi

python3 plugins/rldyour-serena-mcp/scripts/serena_memory_state.py >"$OUTPUT/serena-memory-state.json" 2>"$OUTPUT/serena-memory-state.stderr" || true
plugins/rldyour-flow/scripts/flow_post_task_state.py >"$OUTPUT/flow-post-task-state.json" 2>"$OUTPUT/flow-post-task-state.stderr" || true
python3 plugins/rldyour-flow/scripts/fullrepo_sync.py --status-json >"$OUTPUT/fullrepo-state.json" 2>"$OUTPUT/fullrepo-state.stderr" || true
python3 scripts/release_manifest.py >"$OUTPUT/release-manifest.json" 2>"$OUTPUT/release-manifest.stderr" || true

if [ "$INCLUDE_DOCTOR" = "1" ]; then
  run_capture doctor.txt scripts/doctor_system_codex.sh
fi

printf 'Diagnostics written to %s\n' "$OUTPUT"
