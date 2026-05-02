---
name: flow-post-task-sync
description: "Finalize task state: Serena memories, AGENTS.md/CLAUDE.md, git/GitHub, branches, worktrees. Use after ry-start/review/deploy/newp; триггеры: заверши задачу, синхронизируй."
---

# Flow Post-Task Sync

## Purpose

Leave the project in a synchronized, documented, committed state. This skill runs after Serena memory sync, not instead of it.

## Workflow

1. Confirm Serena memories are current. If stale, run `serena-memory-sync` first.
2. Read `.serena/.flow_post_task_state.json` if present and run `plugins/rldyour-flow/scripts/flow_post_task_state.py`.
3. Inspect uncommitted changes deeply. Separate source changes, docs, Serena knowledge, generated junk, runtime markers, and secrets.
4. Update `AGENTS.md` when durable Codex project instructions changed. Update `CLAUDE.md` only when present or project uses Claude Code compatibility.
5. Run applicable quality checks from project scripts and `plugins/rldyour-flow/scripts/detect_project_checks.sh`.
6. Commit atomically with Conventional Commits. Use separate commits for implementation, tests, docs/instructions, and Serena knowledge when that improves history.
7. Push to upstream when configured. If no upstream exists, ask before creating one.
8. Remove merged local and remote branches/worktrees only after verifying they are merged into `main` and no open PR depends on them.
9. Remove `.serena/.flow_sync_marker` and `.serena/.flow_post_task_state.json` after successful sync.

## Loop Guard

Do not edit runtime marker files except to remove them after sync. If the Stop hook repeats for the same fingerprint, report the blocker instead of forcing new commits.
