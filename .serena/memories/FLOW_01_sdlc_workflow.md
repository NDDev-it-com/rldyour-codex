<!-- Memory Metadata
Last updated: 2026-05-06
Last commit: 33ab01c fix(flow): keep ry-init memory-safe
Scope: plugins/rldyour-flow, plugins/rldyour-rules, scripts/validate_instruction_docs.py, scripts/smoke_fullrepo_sync.sh, scripts/smoke_local_git_guard.sh, scripts/smoke_flow_branch_cleanup.sh, scripts/install_local_git_hooks.sh, scripts/validate_marketplace.sh, config/skill-routing-policy.json, README.md, AGENTS.md, .claude/CLAUDE.md, system/AGENTS.md
Area: FLOW
-->

# FLOW_01_sdlc_workflow

## Purpose

`plugins/rldyour-flow` is the SDLC orchestration layer for this marketplace. It defines command entry points (`ry-*`, `flow-post-task-sync`, `instruction-docs-sync`) and lifecycle hooks, then delegates code inspection, installation, MCP transport, and other domain behavior to dedicated plugins.

## Source Of Truth

- `plugins/rldyour-flow/hooks.json`
- `plugins/rldyour-flow/hooks/session_start_context.sh`
- `plugins/rldyour-flow/hooks/post_tool_use_commit_advice.sh`
- `plugins/rldyour-flow/hooks/stop_post_task_sync.sh`
- `plugins/rldyour-flow/scripts/flow_post_task_state.py`
- `plugins/rldyour-flow/scripts/git_sync_audit.sh`
- `plugins/rldyour-flow/scripts/instruction_docs_state.py`
- `plugins/rldyour-flow/scripts/fullrepo_sync.py`
- `plugins/rldyour-flow/scripts/local_git_ai_guard.sh`
- `scripts/install_local_git_hooks.sh`
- `scripts/sync_fullrepo_branch.sh`
- `scripts/validate_marketplace.sh`
- `scripts/smoke_hooks.sh`
- `scripts/smoke_fullrepo_sync.sh`
- `scripts/smoke_fullrepo_bootstrap_init.sh`
- `AGENTS.md`
- `.claude/CLAUDE.md`
- `system/AGENTS.md`
- `docs/release-process.md`, `docs/rollback-restore.md`, `docs/observability.md`

## Entry Points

- `ry-init`: Scoped project context pack entry.
- `ry-start`: Full implementation lifecycle with context sufficiency checks.
- `ry-newp`: New-project investigation and scoped scaffold path.
- `ry-review`: Review-only workflow.
- `ry-deploy`: Deploy orchestration workflow.
- `flow-post-task-sync`: Finalization sequence after Serena sync.
- `instruction-docs-sync`: Keep `AGENTS.md` and `.claude/CLAUDE.md` aligned with verified behavior.
- `flow-post-task-sync` and `instruction-docs-sync` are registered through `rldyour-flow` skills and are part of normal stop-workflow contracts.

## Hook Contracts

`plugins/rldyour-flow/hooks.json` registers one hook per lifecycle event:

- `SessionStart`: executes `session_start_context.sh` from repo plugin first, then from installed plugin cache.
- `PostToolUse` (Bash only): executes `post_tool_use_commit_advice.sh`.
- `Stop`: executes `stop_post_task_sync.sh`.

### SessionStart

- Reads repository state via `flow_post_task_state.py`.
- Emits `hookSpecificOutput.hookEventName = SessionStart` with advisory context including:
  - branch, HEAD, upstream, ahead/behind
- worktree count
- branch cleanup counts: merged local branches, merged remote branches, and merged workflow worktree candidates
- dirty file list (trimmed in output)
  - Serena sync status
  - fullrepo status and branch/remote/exclude information
  - instruction-doc presence and flow sync signal
- Does not block execution.

### PostToolUse commit advice

- Triggers only for Bash commands that match `git commit`.
- Runs against current `HEAD`.
- Emits `systemMessage` warnings for non-Conventional-Commit subjects, long subjects, too many files, sensitive-looking paths, runtime artifacts, and agent-only paths.
- Read-only advisory behavior.

### Stop

- Uses `flow_post_task_state.py` and exits silently when:
  - Serena is stale
  - flow sync is not needed
  - flow state is malformed
- When sync is required:
  - writes `.serena/.flow_sync_marker` keyed by fingerprint
  - writes `.serena/.flow_post_task_state.json`
  - exits with code `2` and a request to run `$flow-post-task-sync`
- Includes loop guard: if hook is re-entered for same fingerprint and `stop_hook_active=true`, it exits code `0` with a single blocker message.

## Flow-Post-Task State Model

`plugins/rldyour-flow/scripts/flow_post_task_state.py` builds a compact JSON contract:

- `is_git_repo`, `head_sha`, `head_full`, `branch`, `upstream`, `ahead`, `behind`
- `dirty_files`, `dirty_count`, `worktree_count`
- `serena_current`, `serena_state`
- `doc_files_present`, `doc_files_changed`
- `fullrepo_state`, `fullrepo_needs_attention`
- `instruction_docs_state`
- `branch_cleanup_state` with cleanup base, protected branches, merged local branches, merged remote branches, merged workflow branches, merged worktree cleanup candidates, and `needs_cleanup`
- `needs_flow_sync`
- `fingerprint`

`needs_flow_sync` is true when Serena is current and any of the following is present: dirty files, ahead/behind, changed instruction docs, fullrepo attention needed, branch cleanup needed, or instruction-docs review required.

## Branch Cleanup Contract

Flow treats branch hygiene as part of final synchronization.

- Cleanup base prefers `origin/main`, then `main`, `origin/master`, `master`, then `HEAD`.
- Protected branch names are excluded: `main`, `master`, `develop`, `development`, `staging`, `production`, `prod`, `fullrepo`.
- Merged local branches, merged remote branches, and merged worktree candidates are reported in `branch_cleanup_state`.
- Branches with workflow prefixes (`ai/`, `codex/`, `ry-`, `rldyour/`) are highlighted as workflow cleanup candidates.
- Stop hook summary includes branch cleanup state; cleanup must be completed or reported as blocked before final delivery.

## Instruction Docs Contract

`instruction_docs_state.py` identifies and validates:

- required docs: `AGENTS.md`, `.claude/CLAUDE.md`
- missing docs (for fullrepo-managed projects)
- dirty instruction docs
- durable-change candidates (non-runtime paths that likely require instruction refresh)
- review reasons
- `needs_instruction_docs_review` flag

Flow stop flow uses this state to decide whether `$instruction-docs-sync` is required.

## Fullrepo Contract

`fullrepo_sync.py` is the fullrepo implementation used by flow:

- default remote branch: `fullrepo`
- wrapper: `scripts/sync_fullrepo_branch.sh` forwards `--status`, `--status-json`, `--install-exclude`, `--restore`, `--publish`, `--migrate-main`
- `publish` builds a temporary index tree from:
  - existing `HEAD`
  - added local agent-only paths
  - excludes non-agent dirty files
- refuses publish when non-agent dirty files exist.
- excludes and metadata are managed through repo `.git/info/exclude`, plus explicit runtime ignores.
- publish uses snapshot commit + `git push --force-with-lease`.

Flow stop guidance is: Serena sync → instruction-docs sync if needed → checks → commit → push → `fullrepo` publish when repo has agent-only context.

## ry-init Memory Contract

`ry-init` is read-only for Serena knowledge by default:

- it may bootstrap or restore agent-only context from `fullrepo`;
- it must not create, edit, or delete `.serena` memories unless the user explicitly asked to update/synchronize memories or an active Stop/stale-memory hook requires it;
- durable facts found during init are reported as `Memory candidates (not written)` with exact source paths;
- runtime snapshots, server log summaries, health-check timestamps, container status, and one-off audit observations are report material, not memory material, unless they reveal a stable code/config contract.

## Fullrepo Bootstrap Init

`fullrepo_sync.py --bootstrap-init` is the initialization command used before relying on agent-only context:

- installs the rldyour `.git/info/exclude` block;
- restores existing `origin/fullrepo` agent-only files when the branch exists;
- publishes local agent-only files to a new `fullrepo` when no remote branch exists;
- runs the same index cleanup as `--migrate-main` when the current branch still tracks agent-only files;
- prints final status with `bootstrap_actions`.

## Local Git Pre-Push Guard

`local_git_ai_guard.sh` is the canonical branch-aware local Git pre-push guard for rldyour-managed product repositories.

- Install into a target repository with `scripts/install_local_git_hooks.sh --repo <project> --apply`.
- The installer writes managed `.git/hooks/pre-push` and `.git/hooks/_local_guard_ai.sh` wrappers.
- If a target repository already has `pre-push`, the installer preserves it as `.git/hooks/pre-push.rldyour-previous` and replays the same pre-push stdin after the rldyour guard passes.
- Product refs use strict mode: agent-only paths, runtime/local-only paths, definite secrets, and AI-marker additions block the push.
- `refs/heads/${RLDYOUR_FULLREPO_BRANCH:-fullrepo}` uses fullrepo mode: durable AI context and AI markers are allowed, suspicious security wording is advisory, and definite secrets/runtime/local-only files still block.
- Mixed pushes are evaluated per pushed remote ref.

## Verification

- `python3 plugins/rldyour-flow/scripts/fullrepo_sync.py --status-json`
- `python3 plugins/rldyour-flow/scripts/instruction_docs_state.py --root . --json`
- `plugins/rldyour-flow/scripts/flow_post_task_state.py | python3 -m json.tool`
- `scripts/smoke_local_git_guard.sh`
- `scripts/smoke_flow_branch_cleanup.sh`
- `scripts/smoke_fullrepo_bootstrap_init.sh`
- `scripts/validate_marketplace.sh`
- `scripts/smoke_hooks.sh`
- `scripts/smoke_fullrepo_sync.sh`
- `scripts/doctor_system_codex.sh` (post-install)
- `scripts/sync_fullrepo_branch.sh --status`
- `python3 scripts/validate_instruction_docs.py`
- `python3 scripts/release_manifest.py`
- `python3 scripts/validate_plugin_versions.py`
- `python3 scripts/validate_skill_routing.py`

## Invariants

- No runtime code or setup changes in flow plugin scripts.
- No blocking prompts from SessionStart or commit-advice hooks.
- Stop hooks are blocking only for explicit sync requirements and must preserve loop safety.
- Do not publish secrets, runtime markers, or local credentials through any flow/fullrepo path.
- Fullrepo publish and restore run through safe `--force-with-lease` and wrapper scripts.
- Keep source-of-truth files (`AGENTS.md`, `.claude/CLAUDE.md`, Serena memories, hooks, scripts, workflows) synchronized before publish.
