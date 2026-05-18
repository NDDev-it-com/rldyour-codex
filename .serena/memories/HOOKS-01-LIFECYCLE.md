<!-- Memory Metadata
Last updated: 2026-05-18
Last commit: 756c23e test(hooks): cover registered lifecycle commands
Scope: plugins/rldyour-flow/hooks.json, plugins/rldyour-flow/hooks/*.sh, plugins/rldyour-flow/scripts/fullrepo_sync.py, plugins/rldyour-flow/scripts/flow_post_task_state.py, plugins/rldyour-serena-mcp/hooks.json, plugins/rldyour-serena-mcp/hooks/*.sh, scripts/smoke_hooks.sh, scripts/smoke_serena_memory_taxonomy.sh, scripts/install_system_codex.sh, scripts/doctor_system_codex.sh, system/rules/*.rules, scripts/validate_execpolicy_rules.sh
Area: HOOKS
-->

# HOOKS-01-LIFECYCLE

## Purpose

This memory records the Codex lifecycle hook contracts used by the rldyour plugins and the repository-specific wiring that must stay aligned with official Codex hook semantics.

## Source Of Truth

- `plugins/rldyour-flow/hooks.json`: Flow hook wiring.
- `plugins/rldyour-flow/hooks/session_start_dispatcher.sh`: serialized SessionStart dispatcher for bootstrap then context.
- `plugins/rldyour-flow/hooks/stop_lifecycle_dispatcher.sh`: ordered Stop dispatcher for Serena memory gate before Flow sync gate.
- `plugins/rldyour-flow/hooks/session_start_worktree_bootstrap.sh`: bounded mutating SessionStart bootstrap.
- `plugins/rldyour-flow/hooks/session_start_context.sh`: read-only SessionStart context packet.
- `plugins/rldyour-flow/hooks/pre_tool_use_cwd_guard.sh`: Bash PreToolUse guard that blocks commands which would rename or delete the active Codex cwd or repository root.
- `plugins/rldyour-flow/scripts/fullrepo_sync.py`: fullrepo restore and local-only restore implementation used by startup bootstrap.
- `plugins/rldyour-flow/hooks/post_tool_use_commit_advice.sh`: non-blocking commit advice.
- `plugins/rldyour-flow/hooks/stop_post_task_sync.sh`: Flow post-task sync Stop continuation called by the lifecycle dispatcher.
- `plugins/rldyour-flow/scripts/flow_post_task_state.py`: flow sync state and Stop gate decision data.
- `plugins/rldyour-serena-mcp/hooks.json`: Serena UserPromptSubmit/PreToolUse/PostToolUse hook wiring; Stop is intentionally not registered here to avoid cross-plugin Stop races.
- `plugins/rldyour-serena-mcp/hooks/user_prompt_submit.sh`: Serena-first prompt advice.
- `plugins/rldyour-serena-mcp/hooks/prepare_auto_sync.sh`: pre-commit HEAD marker.
- `plugins/rldyour-serena-mcp/hooks/mark_sync_required.sh`: post-commit memory sync marker.
- `plugins/rldyour-serena-mcp/hooks/stop_memory_sync.sh`: stale-memory Stop gate.
- `scripts/smoke_hooks.sh`: parsed hook wiring and cwd-independent command smoke.
- `scripts/smoke_serena_memory_taxonomy.sh`: Stop/mark hook memory contract smoke.

## Entry Points

- `scripts/smoke_hooks.sh`: validates hook JSON wiring and temporary lifecycle behavior.
- `scripts/smoke_serena_memory_taxonomy.sh`: validates memory-specific hook behavior.
- `scripts/install_system_codex.sh --apply`: installs plugin cache, enables Codex hooks via `[features].hooks = true` plus bundled plugin hooks via `[features].plugin_hooks = true`, and refreshes trusted hashes for installed rldyour plugin hooks.
- `scripts/doctor_system_codex.sh`: verifies installed hook cache parity and live rldyour plugin hook trust/enabled state through Codex app-server.
- `scripts/smoke_codex_hooks_migration.sh`: proves deprecated `codex_hooks` aliases are removed and managed hook feature flags are forced to the supported values.

## Current Behavior

- Official Codex lifecycle events used here are `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, and `Stop`.
- Installed plugin hook declarations require both an enabled plugin and system config with `[features].hooks = true` and `[features].plugin_hooks = true`.
- `PreToolUse` and `PostToolUse` match tool names such as `Bash`; `SessionStart` uses startup/resume/clear-style matching; `UserPromptSubmit` and `Stop` ignore matcher.
- Multiple hooks can be registered for the same event/matcher, but Codex may launch matching command hooks concurrently. `plugins/rldyour-flow/hooks.json` therefore uses one Flow `SessionStart` command hook and one Flow Stop command hook.
- `session_start_dispatcher.sh` serializes `session_start_worktree_bootstrap.sh` before `session_start_context.sh`, enforces child timeouts, starts child hooks in their own process group, terminates descendant processes on timeout, caps child output, combines Codex `additionalContext`, and reports child hook failures as bounded degraded context.
- `stop_lifecycle_dispatcher.sh` serializes Stop ordering by running Serena `stop_memory_sync.sh` first and Flow `stop_post_task_sync.sh` second. If Serena exits non-zero, Flow does not run in that Stop cycle.
- `stop_lifecycle_dispatcher.sh` drains hook stdin once to a temp file and runs child Stop hooks in separate process groups with explicit child timeouts. On timeout it kills descendants and returns a targeted continuation message with exit code `2` instead of relying on Codex's outer Stop timeout.
- `stop_post_task_sync.sh` runs Flow state in local-only mode. It must not call `git fetch` or `git ls-remote`; full remote reconciliation belongs to explicit validation or the final workflow, not a synchronous Stop hook.
- Serena and Flow early-exit hooks drain stdin before returning so Codex does not hit `failed to write hook stdin: Broken pipe` when writing a larger hook payload.
- `pre_tool_use_cwd_guard.sh` blocks common `mv`, `rm`, and `rmdir` commands targeting the current session cwd or repository root, including `$PWD`, `$(pwd)`, and backtick-pwd forms. It is a proactive guard; if the directory is renamed externally before Codex invokes a hook, Codex must be restarted from a valid cwd or the old path must be restored.
- `scripts/smoke_hooks.sh` validates the dispatcher path, still selects hook entries by expected script path for future multi-hook events, and runs each hook smoke through a process-group timeout runner so one stuck hook cannot hang the whole smoke.
- `scripts/smoke_hooks.sh` has an explicit registered-hook script manifest for current Serena and Flow hook commands. If a new hook script is registered in `hooks.json`, the smoke fails until the manifest and coverage are updated.
- `scripts/smoke_hooks.sh` sends a large hook payload through every registered command hook: Serena `UserPromptSubmit`, `PreToolUse`, and `PostToolUse`; Flow `SessionStart`, `PreToolUse`, `PostToolUse`, and `Stop`; plus the Stop child scripts called by the ordered dispatcher.
- The large-stdin regression writes hook output to a temporary file, waits with an explicit timeout, then reads output. This keeps the BrokenPipe regression check itself bounded and prevents a blocked stdout pipe from hanging validation.
- Hook command entries resolve scripts through `PLUGIN_ROOT`, the official plugin-bundled hook environment variable, and do not depend on the current project cwd or hardcoded `${CODEX_HOME}` cache paths.
- `scripts/smoke_hooks.sh` rejects hook commands that use repo-relative `plugins/rldyour-*`, `${CODEX_HOME}`, `.codex/plugins/cache`, or `for p in` cache-search wrappers, then runs configured commands from a temporary git repo with `PLUGIN_ROOT`/`PLUGIN_DATA` set.
- `scripts/install_system_codex.sh --apply` uses current hashes from the app-server RPC method `hooks/list` over `codex app-server --listen stdio://` and `config/batchWrite` to keep `hooks.state` trusted after plugin cache updates. `scripts/doctor_system_codex.sh` fails if installed rldyour plugin hooks are not live, enabled, and trusted.
- `session_start_worktree_bootstrap.sh` runs `fullrepo_sync.py --restore-local` only when canonical agent-only markers are missing and a local `refs/remotes/origin/fullrepo` tracking ref already exists. It never fetches, publishes, pushes, commits, or edits non-agent files, and it says "auto-restored" only when restore exits `0`.
- `session_start_context.sh` is fast, offline, and read-only. It reports local branch, HEAD, local upstream ahead/behind, tracked dirty files, worktree count, Serena sync marker presence, local fullrepo ref/exclude state, tracked agent-only count, and project docs. It deliberately does not call `flow_post_task_state.py`, `fullrepo_sync.py --status-json`, Serena analyzers, `git fetch`, or `git ls-remote`; deep checks run in `ry-init`, Stop, doctor, or explicit validation.
- `fullrepo_sync.py --restore-local` installs the exclude block and restores agent-only files only from an already present local remote-tracking ref. Network restore remains available through the explicit `--restore` path, not SessionStart.
- `flow_post_task_state.py` expands untracked directories before evaluating dirty paths and ignores bootstrap-only untracked `.serena` files created by tool startup, such as `.serena/project.yml`, `.serena/.gitignore`, `.serena/project.local.yml`, and runtime markers.
- Serena `mark_sync_required.sh` emits Codex `hookSpecificOutput.additionalContext` after commit-like HEAD changes.
- Serena `stop_memory_sync.sh` blocks with exit code `2` only when memories are stale; it delegates actual memory updates to the workflow/subagent rather than editing memories inside the hook. It is executed by Flow's ordered Stop dispatcher, not as a separate registered plugin Stop hook.

## Contracts And Data

- Codex hook JSON command entries use `type = command` semantics and invoke plugin-local scripts with `/usr/bin/env bash -lc 'exec bash "${PLUGIN_ROOT:?PLUGIN_ROOT is required}/hooks/<script>.sh"'`; Flow `SessionStart` points at `hooks/session_start_dispatcher.sh`.
- `PLUGIN_ROOT`, `PLUGIN_DATA`, `CLAUDE_PLUGIN_ROOT`, and `CLAUDE_PLUGIN_DATA` are populated in hook smoke tests to mirror the plugin-bundled runtime environment.
- Hook scripts use strict shell mode: `set -euo pipefail`, `IFS=$'\n\t'`, and `unset CDPATH`.
- Runtime markers live under `.serena/` and are ignored: `.auto_sync_head`, `.serena_sync_state.json`, `.sync_marker`, `.flow_sync_marker`, `.flow_post_task_state.json`.
- Stop hook loop guards must allow a repeated stop after the same state already requested continuation.

## Invariants

- Hooks must stay fast, bounded, and safe; expensive semantic memory work happens in the main workflow or managed subagent, not inside shell hook bodies.
- Hook scripts must either consume all stdin or explicitly drain it before early exit. This is required because Codex sends hook JSON on stdin.
- Hook scripts cannot repair a missing session cwd after an external directory rename because Codex starts command hooks with the session cwd. Guard only commands that pass through Codex before the cwd disappears.
- Hook output must be Codex-compatible. Do not emit Claude Code `Agent(...)` syntax or Claude-only fields as the primary path.
- The Flow ordered Stop lifecycle must not duplicate Serena memory writing. It runs Serena freshness gating first, then handles instruction docs, git/GitHub/fullrepo, and cleanup sync only when Serena is current.
- The Flow Stop hook must not force `flow-post-task-sync` when the only repository changes are bootstrap-only untracked `.serena` files from tool startup.
- SessionStart bootstrap must be additive, offline, and local-ref-only. It must not fetch, publish, push, commit, or edit non-agent project files.
- Do not treat `plugin_hooks` as a legacy key; it is the supported Codex opt-in for loading bundled plugin hook files.

## Change Rules

- When adding, removing, or renaming a registered hook script, update `scripts/smoke_hooks.sh` registered-hook manifest, configured-command wiring smoke, and large-stdin drain coverage in the same change.
- When changing hook payload/output shape, verify against official Codex hook docs and run smoke tests.
- When changing hook scripts, run `shellcheck` through `scripts/validate_marketplace.sh`.
- When changing hook commands or installed hook trust behavior, run `scripts/install_system_codex.sh --apply`, `scripts/smoke_hooks.sh`, a live app-server RPC `hooks/list` trust check, and `scripts/doctor_system_codex.sh` after the normal branch is clean.

## Verification

- `scripts/smoke_hooks.sh`: parsed wiring, registered-hook script coverage, `PLUGIN_ROOT` command execution from arbitrary cwd, direct hook lifecycle checks, large-stdin drain regression checks for every registered command hook and Stop child scripts, Flow PreToolUse cwd-rename blocking, fake-network SessionStart/Stop no-fetch/no-ls-remote regressions, and bootstrap-only `.serena` Stop-loop regression checks.
- `scripts/smoke_serena_memory_taxonomy.sh`: memory hook stale/advisory/loop behavior.
- `scripts/smoke_codex_hooks_migration.sh`: installer hook feature migration.
- `scripts/validate_marketplace.sh`: shellcheck plus hook smoke coverage.
- App-server RPC method `hooks/list`: confirms installed hook `trustStatus = trusted` and `enabled = true`.
