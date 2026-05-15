<!-- Memory Metadata
Last updated: 2026-05-16
Last commit: 1132859 feat(serena): harden codex memory sync brain
Scope: plugins/rldyour-flow/hooks.json, plugins/rldyour-flow/hooks/*.sh, plugins/rldyour-serena-mcp/hooks.json, plugins/rldyour-serena-mcp/hooks/*.sh, scripts/smoke_hooks.sh, scripts/smoke_serena_memory_taxonomy.sh
Area: HOOKS
-->

# HOOKS-01-LIFECYCLE

## Purpose

This memory records the Codex lifecycle hook contracts used by the rldyour plugins and the repository-specific wiring that must stay aligned with official Codex hook semantics.

## Source Of Truth

- `plugins/rldyour-flow/hooks.json`: Flow hook wiring.
- `plugins/rldyour-flow/hooks/session_start_worktree_bootstrap.sh`: bounded mutating SessionStart bootstrap.
- `plugins/rldyour-flow/hooks/session_start_context.sh`: read-only SessionStart context packet.
- `plugins/rldyour-flow/hooks/post_tool_use_commit_advice.sh`: non-blocking commit advice.
- `plugins/rldyour-flow/hooks/stop_post_task_sync.sh`: post-task sync Stop continuation.
- `plugins/rldyour-serena-mcp/hooks.json`: Serena hook wiring.
- `plugins/rldyour-serena-mcp/hooks/user_prompt_submit.sh`: Serena-first prompt advice.
- `plugins/rldyour-serena-mcp/hooks/prepare_auto_sync.sh`: pre-commit HEAD marker.
- `plugins/rldyour-serena-mcp/hooks/mark_sync_required.sh`: post-commit memory sync marker.
- `plugins/rldyour-serena-mcp/hooks/stop_memory_sync.sh`: stale-memory Stop gate.
- `scripts/smoke_hooks.sh`: parsed hook wiring and command-wrapper smoke.
- `scripts/smoke_serena_memory_taxonomy.sh`: Stop/mark hook memory contract smoke.

## Entry Points

- `scripts/smoke_hooks.sh`: validates hook JSON wiring and temporary lifecycle behavior.
- `scripts/smoke_serena_memory_taxonomy.sh`: validates memory-specific hook behavior.
- `scripts/install_system_codex.sh --apply`: installs plugin cache and enables Codex hooks via `[features].hooks = true`.
- `scripts/smoke_codex_hooks_migration.sh`: proves deprecated hook feature keys are removed from managed config.

## Current Behavior

- Official Codex lifecycle events used here are `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, and `Stop`.
- `PreToolUse` and `PostToolUse` match tool names such as `Bash`; `SessionStart` uses startup/resume/clear-style matching; `UserPromptSubmit` and `Stop` ignore matcher.
- Multiple hooks can be registered for the same event/matcher. `plugins/rldyour-flow/hooks.json` uses two `SessionStart` command hooks: bootstrap first, context second.
- `scripts/smoke_hooks.sh` selects the hook entry by expected script path instead of assuming exactly one hook per event/matcher.
- Hook command wrappers resolve repo-local scripts first, then installed cache paths under `${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/<plugin>/local/...`.
- `session_start_worktree_bootstrap.sh` runs `fullrepo_sync.py --restore` only when canonical agent-only markers are missing and `origin/fullrepo` exists. It never publishes, pushes, commits, or edits non-agent files.
- `session_start_context.sh` remains read-only and reports branch, HEAD, dirty state, worktrees, Serena freshness, fullrepo, and flow sync state.
- Serena `mark_sync_required.sh` emits Codex `hookSpecificOutput.additionalContext` after commit-like HEAD changes.
- Serena `stop_memory_sync.sh` blocks with exit code `2` only when memories are stale; it delegates actual memory updates to the workflow/subagent rather than editing memories inside the hook.

## Contracts And Data

- Codex hook JSON command entries use `type = command` semantics in JSON form and shell wrappers.
- Hook scripts use strict shell mode: `set -euo pipefail`, `IFS=$'\n\t'`, and `unset CDPATH`.
- Runtime markers live under `.serena/` and are ignored: `.auto_sync_head`, `.serena_sync_state.json`, `.sync_marker`, `.flow_sync_marker`, `.flow_post_task_state.json`.
- Stop hook loop guards must allow a repeated stop after the same state already requested continuation.

## Invariants

- Hooks must stay fast, bounded, and safe; expensive semantic memory work happens in the main workflow or managed subagent, not inside shell hook bodies.
- Hook output must be Codex-compatible. Do not emit Claude Code `Agent(...)` syntax or Claude-only fields as the primary path.
- The Flow Stop hook must not duplicate Serena memory sync. It waits until Serena reports current, then handles instruction docs, git/GitHub/fullrepo, and cleanup sync.
- SessionStart bootstrap must be additive only and must not publish `fullrepo`.

## Change Rules

- When adding another hook entry under an existing matcher, update `scripts/smoke_hooks.sh` expectations so the smoke selects by script path.
- When changing hook payload/output shape, verify against official Codex hook docs and run smoke tests.
- When changing hook scripts, run `shellcheck` through `scripts/validate_marketplace.sh`.

## Verification

- `scripts/smoke_hooks.sh`: parsed wiring, wrapper commands, and direct hook lifecycle checks.
- `scripts/smoke_serena_memory_taxonomy.sh`: memory hook stale/advisory/loop behavior.
- `scripts/smoke_codex_hooks_migration.sh`: installer hook feature migration.
- `scripts/validate_marketplace.sh`: shellcheck plus hook smoke coverage.
