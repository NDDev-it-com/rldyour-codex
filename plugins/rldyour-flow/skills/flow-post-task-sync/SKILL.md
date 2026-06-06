---
name: flow-post-task-sync
description: "Финализирует task state: Serena memories, agent-only files, fullrepo, git/GitHub, branches и worktrees. EN: post-task sync, finalization."
---

# Flow Post-Task Sync

## Purpose

Leave the project in a synchronized, documented, committed state. This skill runs after Serena memory sync, not instead of it.

## Workflow

1. Confirm Serena memories are current. If stale, run `serena-memory-sync` first.
2. If `flow_post_task_state.py` reports `execution.agent_role=worker`, do not run global sync. Return the worker JSON report to the orchestrator. Workers must not publish fullrepo, delete branches, push, install system configs, mutate project policy, or run final sync unless the orchestrator explicitly delegated that exact action.
3. Resolve rldyour-flow script paths before running commands. Prefer repo-local `plugins/rldyour-flow/scripts/*` when present; otherwise use `${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/rldyour-flow/local/scripts/*`. If the Stop hook provided absolute installed paths, use those.
4. Read `.serena/.flow_post_task_state.json` if present and run the resolved `flow_post_task_state.py`. Inspect `branch_cleanup_state` and run the resolved `git_sync_audit.sh` when branch/worktree cleanup is not obviously complete.
5. Inspect uncommitted changes deeply. Separate source changes, docs, Serena knowledge, generated junk, runtime markers, and secrets.
6. Run `instruction-docs-sync` when durable project instructions may have changed and `project_flow_policy.py` reports `instruction_docs.mode` is not `disabled`. Keep `AGENTS.md` optimized for Codex and `.claude/CLAUDE.md` optimized for Claude Code in fullrepo-managed or tracked-normal-branch projects according to policy.
7. Run applicable quality checks from project scripts and the resolved `detect_project_checks.sh`.
8. Commit atomically with Conventional Commits. Use separate commits for
   implementation, tests/validators, docs/instructions, license/metadata,
   generated artifacts, and Serena/fullrepo sync when that improves history
   clarity or reviewability.
9. Push to upstream when configured. If no upstream exists, ask before creating one.
10. Follow the effective `.rldyour/project-policy.json` / local / env policy before touching fullrepo or agent files. In `fullrepo.mode=disabled`, do not restore, migrate, publish, create, or install fullrepo excludes. In `normal_branch_policy.agent_files=allowed`, tracked AI instruction files are normal project files.
11. Publish `fullrepo` only when policy requires/allows it, using the resolved `fullrepo_sync.py --publish` or repo-local helper. Missing fullrepo creation requires explicit policy (`create_if_missing=true`) or explicit current user instruction.
12. Remove merged local and remote branches/worktrees only when policy allows cleanup, the branch is not protected (`main`, `dev`, `fullrepo`, etc.), the branch was created for this workflow, and no open PR depends on it. Advisory cleanup is reported, not forced.
13. Remove `.serena/.flow_sync_marker`, `.serena/.flow_post_task_state.json`, and `.serena/.flow_blocker_ack.json` only after `flow_post_task_state.py` reports no policy-allowed blocking reasons.

## Loop Guard

Do not repeatedly delete regenerated runtime marker files. If the Stop hook repeats for the same fingerprint, the hook writes `.serena/.flow_blocker_ack.json` and allows Stop; report remaining `blocking_reasons` instead of forcing new commits.

Bootstrap-only `.serena` files created by tool startup, such as an untracked `.serena/project.yml` plus runtime markers, are not meaningful project work by themselves and should not force a post-task sync loop.

## Fullrepo Branch

`fullrepo` is the default portable AI-context branch for rldyour-managed projects. Project policy may set `fullrepo.mode=disabled|advisory|auto|required` and may allow tracked instruction/AI files in normal branches. Runtime markers, caches, local env files, browser artifacts, and secrets remain forbidden in every mode.
