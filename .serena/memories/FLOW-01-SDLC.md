<!-- Memory Metadata
Last updated: 2026-05-16
Last commit: 1132859 feat(serena): harden codex memory sync brain
Scope: plugins/rldyour-flow, plugins/rldyour-flow/hooks.json, plugins/rldyour-flow/hooks/*.sh, plugins/rldyour-flow/scripts/*.py, plugins/rldyour-flow/scripts/*.sh, scripts/sync_fullrepo_branch.sh, scripts/worktree_add.sh, scripts/install_local_git_hooks.sh, scripts/smoke_flow_branch_cleanup.sh, scripts/smoke_fullrepo_bootstrap_init.sh, scripts/smoke_clean_bootstrap.sh
Area: FLOW
-->

# FLOW-01-SDLC

## Purpose

`rldyour-flow` is the Codex SDLC orchestration layer. It owns command skills (`ry-init`, `ry-start`, `ry-newp`, `ry-review`, `ry-deploy`), post-task synchronization, instruction-doc synchronization, fullrepo management, worktree bootstrap, branch cleanup state, and git/GitHub finish gates.

## Source Of Truth

- `plugins/rldyour-flow/.codex-plugin/plugin.json`: plugin version `0.2.5`, capabilities, hook/skill links.
- `plugins/rldyour-flow/skills/ry-start/SKILL.md`: full implementation lifecycle.
- `plugins/rldyour-flow/skills/ry-init/SKILL.md`: scoped read-only initialization.
- `plugins/rldyour-flow/skills/flow-post-task-sync/SKILL.md`: final sync workflow.
- `plugins/rldyour-flow/skills/instruction-docs-sync/SKILL.md`: Codex/Claude instruction-doc sync.
- `plugins/rldyour-flow/scripts/fullrepo_sync.py`: fullrepo restore, migrate, publish, bootstrap-init, and status logic.
- `plugins/rldyour-flow/scripts/flow_post_task_state.py`: post-task sync state and cleanup candidates.
- `plugins/rldyour-flow/scripts/git_sync_audit.sh`: git/GitHub branch state audit.
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
- `session_start_worktree_bootstrap.sh` restores agent-only context from `origin/fullrepo` when `.serena/project.yml`, `AGENTS.md`, or `.claude/CLAUDE.md` is missing. It is additive and never publishes.
- `scripts/worktree_add.sh` refuses to create a helper worktree if `origin/fullrepo` does not exist; it does not auto-publish from a helper script.
- `flow_post_task_state.py` keeps flow sync pending when instruction docs are stale/missing, fullrepo is stale, git sync is pending, or merged workflow branches/worktrees need cleanup.
- `ry-init` remains read-only for Serena memories by default and may report memory candidates rather than writing `.serena`.
- `flow-post-task-sync` runs after Serena memory sync and should finish by normal branch commit/push, fullrepo publish, and safe cleanup when applicable.

## Contracts And Data

- Agent-only files include root `AGENTS.md`, `.claude/CLAUDE.md`, `REVIEW.md`, `.serena` knowledge, `.claude`, `.codex`, `.cursor/rules`, `.agents/skills`, and similar AI workflow paths.
- Standard finish order is: Serena memories and durable instruction docs from verified code, matching checks, atomic normal-branch commit/push, `fullrepo` publish from final `HEAD`, then safe cleanup of merged workflow branches/worktrees.
- `branch_cleanup_state` excludes protected branches such as `main` and `fullrepo`.
- `RLDYOUR_FULLREPO_BRANCH` controls the fullrepo branch name; default is `fullrepo`.
- `RLDYOUR_SKIP_WORKTREE_BOOTSTRAP=1` disables the SessionStart bootstrap hook.
- `RLDYOUR_WORKTREE_BASE_REF` and `RLDYOUR_DRY_RUN=1` control `scripts/worktree_add.sh`.

## Invariants

- Flow must not own MCP transport definitions; `rldyour-mcps` owns `.mcp.json`.
- Flow Stop must not duplicate Serena memory writing; it waits for Serena freshness first.
- Fullrepo publishing must not run before normal branch sync when the workflow is finishing a normal product change.
- Worktree bootstrap must not push, publish, commit, or edit non-agent project files.
- Do not clean branches/worktrees unless merged state is verified and protected branches are excluded.

## Change Rules

- When fullrepo behavior changes, update `scripts/smoke_fullrepo_sync.sh`, `scripts/smoke_fullrepo_bootstrap_init.sh`, `scripts/smoke_clean_bootstrap.sh`, and this memory.
- When branch cleanup logic changes, update `scripts/smoke_flow_branch_cleanup.sh`.
- When SessionStart hooks change, update `scripts/smoke_hooks.sh` and `HOOKS-01-LIFECYCLE.md`.
- When instruction-doc behavior changes, run `$instruction-docs-sync` and `python3 scripts/validate_instruction_docs.py --require-agent-docs`.

## Verification

- `scripts/smoke_fullrepo_sync.sh`: fullrepo restore/publish behavior.
- `scripts/smoke_fullrepo_bootstrap_init.sh`: first-run bootstrap init and current-branch AI-file index cleanup.
- `scripts/smoke_clean_bootstrap.sh`: clean temporary install with restored fullrepo context.
- `scripts/smoke_flow_branch_cleanup.sh`: branch/worktree cleanup pending-state contract.
- `RLDYOUR_DRY_RUN=1 scripts/worktree_add.sh test/codex-memory-brain`: helper worktree command construction.
- `plugins/rldyour-flow/scripts/flow_post_task_state.py | python3 -m json.tool`: current flow sync state.
