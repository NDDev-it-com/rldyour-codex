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

smoke_root() {
  local name=$1
  local base=$2
  local serena_dir
  local flow_dir

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
