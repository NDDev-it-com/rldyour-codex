# Post-Task Synchronization

Post-task sync is the last phase of meaningful work. It prevents forgotten changes, stale project knowledge, and mismatched local/GitHub/server state.

## Order

1. Serena memory freshness first.
2. Project instruction docs second: `AGENTS.md` and `CLAUDE.md`.
3. Quality checks and manual evidence third.
4. Atomic commits fourth.
5. GitHub sync fifth.
6. Merged branch/worktree cleanup last.

## Session And Commit Advice

The flow SessionStart hook gives Codex a compact repository state packet before work starts or resumes. Treat it as an input to planning: inspect dirty files, ahead/behind state, worktree count, docs, and Serena freshness before making assumptions.

The flow PostToolUse hook emits commit advice after Bash `git commit` commands. Advice is informational and should be reviewed before pushing or final delivery, but it must not be treated as a hard failure by itself.

## Serena Interaction

`rldyour-serena-mcp` owns `.serena/memories`, `.serena/plans`, and `.serena/research`. The flow hook must not duplicate that work. It waits until the Serena state script reports current knowledge, then asks for `flow-post-task-sync`.

## AGENTS.md And CLAUDE.md

Codex reads `AGENTS.md` as project instructions. Update it when the task changes durable project rules, setup commands, quality gates, deploy contracts, architecture constraints, or agent workflow guidance.

`CLAUDE.md` is maintained for compatibility with Claude Code projects. Update it only when present or when a project explicitly uses it. Do not create a large generic `CLAUDE.md` in every project without need.

Both files must contain verified facts, not chat history or speculative plans.

## Loop Prevention

The Stop hook writes `.serena/.flow_sync_marker` with a fingerprint of HEAD, dirty files, ahead/behind, branch, and Serena freshness. If the same fingerprint already requested a continuation during active Stop processing, the hook allows stop to avoid a loop.

Runtime markers are ignored by git:

- `.serena/.flow_sync_marker`
- `.serena/.flow_post_task_state.json`

## Commit Rules

- Commit source changes by logical feature/fix/refactor units.
- Commit Serena/docs sync separately when it improves history clarity.
- Never commit secrets, runtime markers, browser artifacts, local env files, or accidental generated junk.
- Use Conventional Commits.
- Push to upstream when configured. If upstream is missing, ask before setting it.

## Cleanup Rules

- Remove merged worktrees and branches only after verifying they are merged into `main` and pushed if needed.
- Delete remote branches after merge when the branch was created for this workflow and no open PR depends on it.
- Ask the user if branch ownership, merge status, or remote state is unclear.
