#!/usr/bin/env bash
set -euo pipefail

CODEX_HOME_DIR=${CODEX_HOME:-"$HOME/.codex"}
MODE="both"

usage() {
  cat <<'EOF'
Usage: scripts/smoke_hooks.sh [--codex-home PATH] [--repo-only] [--installed-only]

Runs non-mutating smoke checks for repository and installed Codex hook scripts.
The installed checks validate the hook files Codex will use after restart/plugin-cache sync.
Lifecycle checks run in a temporary git repository and validate real hook state transitions.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --codex-home)
      shift
      CODEX_HOME_DIR=${1:?--codex-home requires a path}
      ;;
    --repo-only)
      MODE="repo"
      ;;
    --installed-only)
      MODE="installed"
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

fail() {
  printf 'fail    %s\n' "$1" >&2
  exit 1
}

run_hook() {
  local label=$1
  local path=$2
  local input=$3
  local expected=$4
  local output

  [ -f "$path" ] || fail "$label missing: $path"
  output=$(cd "$ROOT" && printf '%s' "$input" | bash "$path")
  if [ -n "$expected" ] && ! printf '%s' "$output" | grep -F "$expected" >/dev/null; then
    printf 'hook output for %s:\n%s\n' "$label" "$output" >&2
    fail "$label did not include expected text: $expected"
  fi
  printf 'ok      %s\n' "$label"
}

run_quiet_hook() {
  local label=$1
  local path=$2
  local input=$3
  local output

  [ -f "$path" ] || fail "$label missing: $path"
  output=$(cd "$ROOT" && printf '%s' "$input" | bash "$path")
  if [ -n "$output" ]; then
    printf 'hook output for %s:\n%s\n' "$label" "$output" >&2
    fail "$label should not emit output for this smoke input"
  fi
  printf 'ok      %s\n' "$label"
}

run_stop_hook() {
  local label=$1
  local path=$2
  [ -f "$path" ] || fail "$label missing: $path"
  (cd "$ROOT" && printf '{}' | RLDYOUR_SKIP_STOP_GATES=1 bash "$path")
  printf 'ok      %s\n' "$label"
}

hook_json_command() {
  local hooks_json=$1
  local event=$2
  local matcher=$3
  local expected_script=$4

  python3 - "$hooks_json" "$event" "$matcher" "$expected_script" <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path

hooks_json = Path(sys.argv[1])
event, matcher, expected_script = sys.argv[2:5]
data = json.loads(hooks_json.read_text(encoding="utf-8"))
events = data.get("hooks")
if not isinstance(events, dict):
    raise SystemExit(f"{hooks_json}: missing hooks object")
groups = events.get(event)
if not isinstance(groups, list) or not groups:
    raise SystemExit(f"{hooks_json}: missing event {event}")

if matcher == "-":
    candidates = [group for group in groups if "matcher" not in group]
else:
    candidates = [group for group in groups if group.get("matcher") == matcher]
if len(candidates) != 1:
    raise SystemExit(f"{hooks_json}: expected one {event} matcher {matcher}, found {len(candidates)}")

hook_entries = candidates[0].get("hooks")
if not isinstance(hook_entries, list) or len(hook_entries) != 1:
    raise SystemExit(f"{hooks_json}: {event} matcher {matcher} must have exactly one hook")
hook = hook_entries[0]
if hook.get("type") != "command":
    raise SystemExit(f"{hooks_json}: {event} matcher {matcher} hook type must be command")
command = hook.get("command")
if not isinstance(command, str) or not command:
    raise SystemExit(f"{hooks_json}: {event} matcher {matcher} command missing")
if expected_script not in command:
    raise SystemExit(f"{hooks_json}: {event} command does not reference {expected_script}")
timeout = hook.get("timeout")
if not isinstance(timeout, int) or timeout <= 0:
    raise SystemExit(f"{hooks_json}: {event} timeout must be a positive integer")
print(command)
PY
}

run_configured_hook() {
  local label=$1
  local hooks_json=$2
  local event=$3
  local matcher=$4
  local expected_script=$5
  local cwd=$6
  local input=$7
  local expected=$8
  local command output

  command=$(hook_json_command "$hooks_json" "$event" "$matcher" "$expected_script")
  output=$(cd "$cwd" && printf '%s' "$input" | CODEX_HOME="$CODEX_HOME_DIR" bash -lc "$command")
  if [ -n "$expected" ] && ! printf '%s' "$output" | grep -F "$expected" >/dev/null; then
    printf 'hook output for %s:\n%s\n' "$label" "$output" >&2
    fail "$label did not include expected text: $expected"
  fi
  printf 'ok      %s\n' "$label"
}

run_configured_quiet_hook() {
  local label=$1
  local hooks_json=$2
  local event=$3
  local matcher=$4
  local expected_script=$5
  local cwd=$6
  local input=$7
  local command output

  command=$(hook_json_command "$hooks_json" "$event" "$matcher" "$expected_script")
  output=$(cd "$cwd" && printf '%s' "$input" | CODEX_HOME="$CODEX_HOME_DIR" bash -lc "$command")
  if [ -n "$output" ]; then
    printf 'hook output for %s:\n%s\n' "$label" "$output" >&2
    fail "$label should not emit output for this smoke input"
  fi
  printf 'ok      %s\n' "$label"
}

run_configured_stop_hook() {
  local label=$1
  local hooks_json=$2
  local event=$3
  local expected_script=$4
  local cwd=$5
  local command

  command=$(hook_json_command "$hooks_json" "$event" "-" "$expected_script")
  (cd "$cwd" && printf '{}' | CODEX_HOME="$CODEX_HOME_DIR" RLDYOUR_SKIP_STOP_GATES=1 bash -lc "$command")
  printf 'ok      %s\n' "$label"
}

run_hook_in_dir() {
  local label=$1
  local cwd=$2
  local path=$3
  local input=$4
  local expected=$5
  local output

  [ -f "$path" ] || fail "$label missing: $path"
  output=$(cd "$cwd" && printf '%s' "$input" | bash "$path")
  if [ -n "$expected" ] && ! printf '%s' "$output" | grep -F "$expected" >/dev/null; then
    printf 'hook output for %s:\n%s\n' "$label" "$output" >&2
    fail "$label did not include expected text: $expected"
  fi
  printf 'ok      %s\n' "$label"
}

run_hook_expect_exit_in_dir() {
  local label=$1
  local cwd=$2
  local path=$3
  local input=$4
  local expected_exit=$5
  local expected_text=$6
  local output
  local status

  [ -f "$path" ] || fail "$label missing: $path"
  set +e
  output=$(cd "$cwd" && printf '%s' "$input" | bash "$path" 2>&1)
  status=$?
  set -e
  if [ "$status" -ne "$expected_exit" ]; then
    printf 'hook output for %s:\n%s\n' "$label" "$output" >&2
    fail "$label exit $status, expected $expected_exit"
  fi
  if [ -n "$expected_text" ] && ! printf '%s' "$output" | grep -F "$expected_text" >/dev/null; then
    printf 'hook output for %s:\n%s\n' "$label" "$output" >&2
    fail "$label did not include expected text: $expected_text"
  fi
  printf 'ok      %s\n' "$label"
}

make_lifecycle_repo() {
  local tmp
  tmp=$(mktemp -d "${TMPDIR:-/tmp}/rldyour-hook-smoke.XXXXXX")
  git -C "$tmp" init -q
  git -C "$tmp" config user.email "hook-smoke@example.invalid"
  git -C "$tmp" config user.name "Hook Smoke"
  mkdir -p "$tmp/.serena/memories"
  printf '# Hook smoke\n' > "$tmp/README.md"
  git -C "$tmp" add README.md
  git -C "$tmp" commit -q -m "chore: initial fixture"
  printf '%s\n' "$tmp"
}

smoke_lifecycle() {
  local name=$1
  local serena_dir=$2
  local flow_dir=$3
  local tmp
  local head_short

  printf '\n== Hook lifecycle smoke: %s ==\n' "$name"
  tmp=$(make_lifecycle_repo)
  cleanup_lifecycle() {
    rm -rf "$tmp"
  }
  trap cleanup_lifecycle RETURN

  run_hook_in_dir "$name lifecycle flow SessionStart" \
    "$tmp" "$flow_dir/hooks/session_start_context.sh" \
    '{"source":"startup"}' \
    "rldyour-flow session context"

  run_hook_in_dir "$name lifecycle serena UserPromptSubmit" \
    "$tmp" "$serena_dir/hooks/user_prompt_submit.sh" \
    '{"prompt":"изучи код проекта и архитектуру"}' \
    "Serena-first code workflow"

  run_hook_in_dir "$name lifecycle serena PreToolUse git commit" \
    "$tmp" "$serena_dir/hooks/prepare_auto_sync.sh" \
    '{"tool_name":"Bash","tool_input":{"command":"git commit -m docs"}}' \
    ""

  printf '\nChanged during lifecycle smoke.\n' >> "$tmp/README.md"
  git -C "$tmp" add README.md
  git -C "$tmp" commit -q -m "docs: update fixture"

  run_hook_in_dir "$name lifecycle serena PostToolUse git commit" \
    "$tmp" "$serena_dir/hooks/mark_sync_required.sh" \
    '{"tool_name":"Bash","tool_input":{"command":"git commit -m docs"}}' \
    "[RLDYOUR-SERENA]"

  [ -f "$tmp/.serena/.serena_sync_state.json" ] || fail "$name lifecycle missing Serena sync state"

  run_hook_expect_exit_in_dir "$name lifecycle serena Stop requires sync" \
    "$tmp" "$serena_dir/hooks/stop_memory_sync.sh" \
    '{"stop_hook_active":false}' \
    2 \
    "[RLDYOUR-SERENA SYNC REQUIRED]"

  rm -f "$tmp/.serena/.serena_sync_state.json" "$tmp/.serena/.sync_marker" "$tmp/.serena/.auto_sync_head"
  head_short=$(git -C "$tmp" rev-parse --short=7 HEAD)
  cat > "$tmp/.serena/memories/CORE_01_hook_smoke.md" <<EOF_MEMORY
<!-- Memory Metadata
Last updated: 2026-05-03
Last commit: ${head_short} docs: update fixture
Scope: README.md
Area: CORE
-->

# CORE_01_hook_smoke

## Purpose

Temporary hook lifecycle smoke memory.
EOF_MEMORY

  run_hook_expect_exit_in_dir "$name lifecycle flow Stop requires sync" \
    "$tmp" "$flow_dir/hooks/stop_post_task_sync.sh" \
    '{"stop_hook_active":false}' \
    2 \
    "[RLDYOUR-FLOW POST-TASK SYNC REQUIRED]"

  run_hook_expect_exit_in_dir "$name lifecycle flow Stop loop guard" \
    "$tmp" "$flow_dir/hooks/stop_post_task_sync.sh" \
    '{"stop_hook_active":true}' \
    0 \
    "already requested"

  git -C "$tmp" add .serena/memories/CORE_01_hook_smoke.md
  git -C "$tmp" commit -q -m "bad commit"

  run_hook_in_dir "$name lifecycle flow PostToolUse commit advice" \
    "$tmp" "$flow_dir/hooks/post_tool_use_commit_advice.sh" \
    '{"tool_name":"Bash","tool_input":{"command":"git commit -m bad"}}' \
    "[RLDYOUR-FLOW COMMIT ADVICE]"

  rm -rf "$tmp"
  trap - RETURN
}

smoke_hook_wiring() {
  local name=$1
  local serena_hooks_json=$2
  local flow_hooks_json=$3
  local cwd=$4

  printf '\n== Hook wiring smoke: %s ==\n' "$name"
  run_configured_hook "$name wiring serena UserPromptSubmit" \
    "$serena_hooks_json" UserPromptSubmit - "hooks/user_prompt_submit.sh" "$cwd" \
    '{"prompt":"изучи код проекта и найди архитектуру"}' \
    "Serena-first code workflow"

  run_configured_quiet_hook "$name wiring serena PreToolUse non-commit" \
    "$serena_hooks_json" PreToolUse Bash "hooks/prepare_auto_sync.sh" "$cwd" \
    '{"tool_name":"Bash","tool_input":{"command":"git status"}}'

  run_configured_quiet_hook "$name wiring serena PostToolUse no marker" \
    "$serena_hooks_json" PostToolUse Bash "hooks/mark_sync_required.sh" "$cwd" \
    '{"tool_name":"Bash","tool_input":{"command":"git status"}}'

  run_configured_stop_hook "$name wiring serena Stop skip gate" \
    "$serena_hooks_json" Stop "hooks/stop_memory_sync.sh" "$cwd"

  run_configured_hook "$name wiring flow SessionStart" \
    "$flow_hooks_json" SessionStart - "hooks/session_start_context.sh" "$cwd" \
    '{"source":"smoke"}' \
    "rldyour-flow session context"

  run_configured_quiet_hook "$name wiring flow PostToolUse non-commit" \
    "$flow_hooks_json" PostToolUse Bash "hooks/post_tool_use_commit_advice.sh" "$cwd" \
    '{"tool_name":"Bash","tool_input":{"command":"git status"}}'

  run_configured_stop_hook "$name wiring flow Stop skip gate" \
    "$flow_hooks_json" Stop "hooks/stop_post_task_sync.sh" "$cwd"
}

smoke_root() {
  local name=$1
  local base=$2
  local serena_dir
  local flow_dir
  local wiring_cwd
  local cleanup_wiring_cwd=""

  printf '\n== Hook smoke: %s ==\n' "$name"
  [ -d "$base" ] || fail "$name hook root missing: $base"
  if [ -d "$base/rldyour-serena-mcp/local" ]; then
    serena_dir="$base/rldyour-serena-mcp/local"
  else
    serena_dir="$base/rldyour-serena-mcp"
  fi
  if [ -d "$base/rldyour-flow/local" ]; then
    flow_dir="$base/rldyour-flow/local"
  else
    flow_dir="$base/rldyour-flow"
  fi

  if [ "$name" = "installed" ]; then
    wiring_cwd=$(make_lifecycle_repo)
    cleanup_wiring_cwd="$wiring_cwd"
  else
    wiring_cwd="$ROOT"
  fi
  smoke_hook_wiring "$name" "$serena_dir/hooks.json" "$flow_dir/hooks.json" "$wiring_cwd"
  if [ -n "$cleanup_wiring_cwd" ]; then
    rm -rf "$cleanup_wiring_cwd"
  fi

  run_hook "$name serena UserPromptSubmit" \
    "$serena_dir/hooks/user_prompt_submit.sh" \
    '{"prompt":"изучи код проекта и найди архитектуру"}' \
    "Serena-first code workflow"

  run_quiet_hook "$name serena PreToolUse non-commit" \
    "$serena_dir/hooks/prepare_auto_sync.sh" \
    '{"tool_name":"Bash","tool_input":{"command":"git status"}}'

  run_quiet_hook "$name serena PostToolUse no marker" \
    "$serena_dir/hooks/mark_sync_required.sh" \
    '{"tool_name":"Bash","tool_input":{"command":"git status"}}'

  run_stop_hook "$name serena Stop skip gate" \
    "$serena_dir/hooks/stop_memory_sync.sh"

  run_hook "$name flow SessionStart" \
    "$flow_dir/hooks/session_start_context.sh" \
    '{"source":"smoke"}' \
    "rldyour-flow session context"

  run_quiet_hook "$name flow PostToolUse non-commit" \
    "$flow_dir/hooks/post_tool_use_commit_advice.sh" \
    '{"tool_name":"Bash","tool_input":{"command":"git status"}}'

  run_stop_hook "$name flow Stop skip gate" \
    "$flow_dir/hooks/stop_post_task_sync.sh"

  smoke_lifecycle "$name" "$serena_dir" "$flow_dir"
}

if [ "$MODE" = "repo" ] || [ "$MODE" = "both" ]; then
  smoke_root "repo" "$ROOT/plugins"
fi

if [ "$MODE" = "installed" ] || [ "$MODE" = "both" ]; then
  smoke_root "installed" "$CODEX_HOME_DIR/plugins/cache/rldyour-codex"
fi

printf '\nHook smoke passed.\n'
