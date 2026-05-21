---
name: flow-post-task-sync
description: "Finalize task state: Serena memories, agent-only files, fullrepo, git/GitHub, branches, worktrees. Use after ry-start/review/deploy/newp; триггеры: заверши задачу, синхронизируй."
---

# Flow Post-Task Sync

## Purpose

Leave the project in a synchronized, documented, committed state. This skill runs after Serena memory sync, not instead of it.

## Workflow

1. Confirm Serena memories are current. If stale, run `serena-memory-sync` first.
2. Resolve rldyour-flow script paths before running commands. Prefer repo-local `plugins/rldyour-flow/scripts/*` when present; otherwise use `${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/rldyour-flow/local/scripts/*`. If the Stop hook provided absolute installed paths, use those.
3. Read `.serena/.flow_post_task_state.json` if present and run the resolved `flow_post_task_state.py`. Inspect `branch_cleanup_state` and run the resolved `git_sync_audit.sh` when branch/worktree cleanup is not obviously complete.
4. Inspect uncommitted changes deeply. Separate source changes, docs, Serena knowledge, generated junk, runtime markers, and secrets.
5. Run `instruction-docs-sync` when durable project instructions may have changed. Keep `AGENTS.md` optimized for Codex and `.claude/CLAUDE.md` optimized for Claude Code in fullrepo-managed projects.
6. Run applicable quality checks from project scripts and the resolved `detect_project_checks.sh`.
7. Commit atomically with Conventional Commits. Use separate commits for
   implementation, tests/validators, docs/instructions, license/metadata,
   generated artifacts, and Serena/fullrepo sync when that improves history
   clarity or reviewability.
8. Push to upstream when configured. If no upstream exists, ask before creating one.
9. Keep normal branch history clean from agent-only files. Ensure `.git/info/exclude` contains the rldyour fullrepo block and move tracked agent-only files out of the current branch with `fullrepo_sync.py --migrate-main` only when the project is ready for that migration.
10. Publish the complete project snapshot to `fullrepo` through the resolved `fullrepo_sync.py --publish` or repo-local `scripts/sync_fullrepo_branch.sh --publish`. This uses safe `--force-with-lease`, not a blind force push.
11. Remove merged local and remote branches/worktrees only after verifying they are merged into `main` and no open PR depends on them. Leave protected branches such as `main` and `fullrepo`; report any ambiguous branch ownership instead of deleting silently.
12. Remove `.serena/.flow_sync_marker` and `.serena/.flow_post_task_state.json` after successful sync.

## Loop Guard

Do not edit runtime marker files except to remove them after sync. If the Stop hook repeats for the same fingerprint, report the blocker instead of forcing new commits.

Bootstrap-only `.serena` files created by tool startup, such as an untracked `.serena/project.yml` plus runtime markers, are not meaningful project work by themselves and should not force a post-task sync loop.

## Fullrepo Branch

`fullrepo` is the portable AI-context branch. It contains the normal branch tree plus agent-only files such as project `AGENTS.md`, `.claude/CLAUDE.md`, `REVIEW.md`, `.serena` knowledge, `.claude`, `.codex`, `.cursor/rules`, `.agents/skills`, and similar agent workflow files. The main branch should not track those files in normal projects; they should be restored locally from `fullrepo` and ignored through `.git/info/exclude`.
