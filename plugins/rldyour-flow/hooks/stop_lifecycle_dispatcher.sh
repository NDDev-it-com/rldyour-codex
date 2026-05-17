#!/usr/bin/env bash
# stop_lifecycle_dispatcher.sh — serialize Serena memory gate before Flow sync gate.

set -euo pipefail
IFS=$'\n\t'
unset CDPATH

HOOK_INPUT=$(cat 2>/dev/null || true)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLOW_PLUGIN_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

find_serena_plugin_dir() {
  local candidate
  if [ -n "${RLDYOUR_SERENA_PLUGIN_ROOT:-}" ] && [ -f "$RLDYOUR_SERENA_PLUGIN_ROOT/hooks/stop_memory_sync.sh" ]; then
    printf '%s\n' "$RLDYOUR_SERENA_PLUGIN_ROOT"
    return 0
  fi

  for candidate in \
    "$FLOW_PLUGIN_DIR/../rldyour-serena-mcp" \
    "$FLOW_PLUGIN_DIR/../../rldyour-serena-mcp/local"; do
    if [ -f "$candidate/hooks/stop_memory_sync.sh" ]; then
      (cd "$candidate" && pwd)
      return 0
    fi
  done

  if ROOT=$(git -C "$FLOW_PLUGIN_DIR" rev-parse --show-toplevel 2>/dev/null); then
    candidate="$ROOT/plugins/rldyour-serena-mcp"
    if [ -f "$candidate/hooks/stop_memory_sync.sh" ]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  fi

  return 1
}

run_stop_child() {
  local script_path=$1
  local output
  local status

  set +e
  output=$(printf '%s' "$HOOK_INPUT" | bash "$script_path" 2>&1)
  status=$?
  set -e

  if [ -n "$output" ]; then
    printf '%s\n' "$output" >&2
  fi
  return "$status"
}

if SERENA_PLUGIN_DIR=$(find_serena_plugin_dir); then
  set +e
  run_stop_child "$SERENA_PLUGIN_DIR/hooks/stop_memory_sync.sh"
  SERENA_STATUS=$?
  set -e
  if [ "$SERENA_STATUS" -ne 0 ]; then
    exit "$SERENA_STATUS"
  fi
fi

run_stop_child "$FLOW_PLUGIN_DIR/hooks/stop_post_task_sync.sh"
