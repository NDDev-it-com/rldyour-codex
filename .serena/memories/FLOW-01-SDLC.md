<!-- Memory Metadata
Last updated: 2026-05-18
Last commit: 6ec3fb9 fix(hooks): harden lifecycle execution
Scope: plugins/rldyour-flow, plugins/rldyour-flow/hooks.json, plugins/rldyour-flow/hooks/*.sh, plugins/rldyour-flow/scripts/*.py, plugins/rldyour-flow/scripts/*.sh, scripts/sync_fullrepo_branch.sh, scripts/worktree_add.sh, scripts/install_local_git_hooks.sh, scripts/smoke_flow_branch_cleanup.sh, scripts/smoke_fullrepo_bootstrap_init.sh, scripts/smoke_clean_bootstrap.sh
Area: FLOW
-->

# FLOW-01-SDLC

## Purpose

`rldyour-flow` is the Codex SDLC orchestration layer. It owns command skills (`ry-init`, `ry-start`, `ry-newp`, `ry-review`, `ry-deploy`), post-task synchronization, instruction-doc synchronization, fullrepo management, worktree bootstrap, branch cleanup state, and git/GitHub finish gates.

## Source Of Truth

- `plugins/rldyour-flow/.codex-plugin/plugin.json`: plugin version `0.3.3`, capabilities, hook/skill links.
- `plugins/rldyour-flow/skills/ry-start/SKILL.md`: full implementation lifecycle.
- `plugins/rldyour-flow/skills/ry-init/SKILL.md`: scoped read-only initialization.
- `plugins/rldyour-flow/skills/flow-post-task-sync/SKILL.md`: final sync workflow.
- `plugins/rldyour-flow/skills/instruction-docs-sync/SKILL.md`: Codex/Claude instruction-doc sync.
- `plugins/rldyour-flow/scripts/fullrepo_sync.py`: fullrepo restore, migrate, publish, bootstrap-init, and status logic.
- `plugins/rldyour-flow/scripts/flow_post_task_state.py`: post-task sync state and cleanup candidates.
- `plugins/rldyour-flow/scripts/git_sync_audit.sh`: git/GitHub branch state audit.
- `plugins/rldyour-flow/hooks/session_start_dispatcher.sh`: serialized SessionStart dispatch for bootstrap before context.
- `plugins/rldyour-flow/hooks/pre_tool_use_cwd_guard.sh`: Bash command guard for active cwd and repository-root rename/delete prevention.
- `plugins/rldyour-flow/hooks/stop_lifecycle_dispatcher.sh`: ordered Stop dispatcher that runs Serena memory state before Flow post-task state.
- `plugins/rldyour-flow/hooks/session_start_worktree_bootstrap.sh`: auto-restore missing agent-only context in fresh worktrees.
- `plugins/rldyour-flow/hooks/session_start_context.sh`: read-only context packet.
- `scripts/sync_fullrepo_branch.sh`: repository wrapper for fullrepo sync.
- `scripts/worktree_add.sh`: one-step worktree creation plus fullrepo restore.

## Entry Points

- `$rldyour-flow:ry-init`: initialize scope, bootstrap agent-only context, and report memory candidates without writing memories by default.
- `$rldyour-flow:ry-start`: research, plan, implement, verify, review, commit, sync.
- `$rldyour-flow:ry-review`: review diff/scope without edits.
- `$rldyour-flow:ry-deploy`: local/GitHub/server deploy workflow.
- `scripts/worktree_add.sh <branch> [path]`: create a worktree and run `fullrepo_sync.py --restore` in it.
- `scripts/sync_fullrepo_branch.sh --bootstrap-init|--publish|--status`: standard fullrepo operations.

## Current Behavior

- Normal branches exclude agent-only files; `fullrepo` publishes current `HEAD` plus ignored agent-only files using safe `--force-with-lease`.
- `--bootstrap-init` installs excludes, restores existing `fullrepo` context when available, publishes local agent-only files when no `fullrepo` exists, and removes tracked agent-only files from the current branch index when migration is needed.
- Flow `SessionStart` wiring uses `session_start_dispatcher.sh` as a single hook entry so worktree bootstrap runs before session context under Codex hook concurrency semantics. The dispatcher runs children with bounded timeouts, uses temp-file input, starts children in their own process group, kills descendants on timeout, caps child output, and emits degraded context instead of relying only on the outer Codex timeout.
- `session_start_worktree_bootstrap.sh` restores agent-only context only from an already present local `origin/fullrepo` tracking ref when `.serena/project.yml`, `AGENTS.md`, or `.claude/CLAUDE.md` is missing. It calls `fullrepo_sync.py --restore-local`, is additive, never fetches, never publishes, and reports restore failure honestly instead of success-like wording.
- `session_start_context.sh` is a fast offline startup packet. It reports only bounded local state such as branch, HEAD, local ahead/behind, tracked dirty files, worktree count, Serena sync marker presence, local fullrepo ref/exclude state, tracked agent-only count, and project instruction docs. It does not call deep Serena/fullrepo/Flow analyzers; those belong to `ry-init`, Stop, doctor, or explicit validation.
- Flow `PreToolUse` protects active Codex session paths before Bash runs: common commands that would rename or delete the active cwd or repository root are denied with a Codex permission decision. External/manual directory renames cannot be recovered by hook code because Codex starts hooks with the session cwd.
- Flow `Stop` wiring uses `stop_lifecycle_dispatcher.sh` as the only registered Stop command. The dispatcher invokes `rldyour-serena-mcp/hooks/stop_memory_sync.sh` first and invokes `stop_post_task_sync.sh` only when Serena exits cleanly, so cross-plugin Stop ordering no longer depends on Codex concurrent hook execution.
- Flow Stop state is local-only and bounded. `stop_lifecycle_dispatcher.sh` uses process-group timeouts for Serena and Flow children, and `stop_post_task_sync.sh` sets `RLDYOUR_FLOW_STATE_LOCAL_ONLY=1` plus `RLDYOUR_FULLREPO_STATUS_LOCAL_ONLY=1` so synchronous Stop checks do not call remote fullrepo operations.
- `scripts/worktree_add.sh` refuses to create a helper worktree if `origin/fullrepo` does not exist; it does not auto-publish from a helper script.
- `flow_post_task_state.py` keeps flow sync pending when instruction docs are stale/missing, fullrepo is stale, git sync is pending, or merged workflow branches/worktrees need cleanup. Installed helper lookup honors `CODEX_HOME` before the default `~/.codex` cache so temp installs and CI smoke runs inspect the intended runtime.
- `flow_post_task_state.py` ignores bootstrap-only untracked `.serena` files created by tool startup, such as `.serena/project.yml`, `.serena/.gitignore`, `.serena/project.local.yml`, and flow runtime markers; those files alone must not force a Stop-hook `flow-post-task-sync` continuation.
- `fullrepo_sync.py --publish` supplies fallback author/committer identity to `git commit-tree`, and `scripts/smoke_clean_bootstrap.sh` configures a temporary git identity in clean clones. The clean bootstrap smoke only requires `codex mcp list` when `--require-codex` is passed.
- `ry-init` remains read-only for Serena memories by default and may report memory candidates rather than writing `.serena`.
- `flow-post-task-sync` runs after Serena memory sync and should finish by normal branch commit/push, fullrepo publish, and safe cleanup when applicable. Its skill guidance resolves helper scripts from repo-local `plugins/rldyour-flow/scripts/*` when present or from the installed plugin cache in product repositories.

## Contracts And Data

- Agent-only files include root `AGENTS.md`, `.claude/CLAUDE.md`, `REVIEW.md`, `.serena` knowledge, `.claude`, `.codex`, `.cursor/rules`, `.agents/skills`, and similar AI workflow paths.
- Standard finish order is: Serena memories and durable instruction docs from verified code, matching checks, atomic normal-branch commit/push, `fullrepo` publish from final `HEAD`, then safe cleanup of merged workflow branches/worktrees.
- `branch_cleanup_state` excludes protected branches such as `main` and `fullrepo`.
- `RLDYOUR_FULLREPO_BRANCH` controls the fullrepo branch name; default is `fullrepo`.
- `RLDYOUR_SKIP_WORKTREE_BOOTSTRAP=1` disables the SessionStart bootstrap hook.
- `RLDYOUR_FLOW_STATE_LOCAL_ONLY=1` makes Flow post-task state use local fullrepo refs and avoid network checks; Stop hooks set it automatically.
- `RLDYOUR_FULLREPO_STATUS_LOCAL_ONLY=1` makes instruction-doc/fullrepo status helpers avoid remote fetch/ls-remote calls; Stop hooks set it automatically.
- `RLDYOUR_WORKTREE_BASE_REF` and `RLDYOUR_DRY_RUN=1` control `scripts/worktree_add.sh`.

## Invariants

- Flow must not own MCP transport definitions; `rldyour-mcps` owns `.mcp.json`.
- Flow Stop must not duplicate Serena memory writing; `stop_lifecycle_dispatcher.sh` waits for Serena freshness first and only then evaluates Flow post-task sync.
- Fullrepo publishing must not run before normal branch sync when the workflow is finishing a normal product change.
- Worktree bootstrap must not fetch, push, publish, commit, or edit non-agent project files.
- Do not clean branches/worktrees unless merged state is verified and protected branches are excluded.

## Change Rules

- When fullrepo behavior changes, update `scripts/smoke_fullrepo_sync.sh`, `scripts/smoke_fullrepo_bootstrap_init.sh`, `scripts/smoke_clean_bootstrap.sh`, and this memory.
- When branch cleanup logic changes, update `scripts/smoke_flow_branch_cleanup.sh`.
- When SessionStart, Stop, or hook gate logic changes, update `scripts/smoke_hooks.sh` and `HOOKS-01-LIFECYCLE.md`.
- When instruction-doc behavior changes, run `$instruction-docs-sync` and `python3 scripts/validate_instruction_docs.py --require-agent-docs`.

## Verification

- `scripts/smoke_fullrepo_sync.sh`: fullrepo restore/publish behavior.
- `scripts/smoke_fullrepo_bootstrap_init.sh`: first-run bootstrap init and current-branch AI-file index cleanup.
- `scripts/smoke_clean_bootstrap.sh`: clean temporary install with restored fullrepo context.
- `scripts/smoke_flow_branch_cleanup.sh`: branch/worktree cleanup pending-state contract.
- `scripts/smoke_hooks.sh`: flow hook lifecycle, large-stdin drain checks, PreToolUse cwd-rename blocking, fake-network SessionStart/Stop no-fetch/no-ls-remote regressions, Stop loop guard, and bootstrap-only `.serena` no-sync regression.
- `RLDYOUR_DRY_RUN=1 scripts/worktree_add.sh test/codex-memory-brain`: helper worktree command construction.
- `plugins/rldyour-flow/scripts/flow_post_task_state.py | python3 -m json.tool`: current flow sync state.
