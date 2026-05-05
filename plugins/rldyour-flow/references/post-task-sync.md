# Post-Task Synchronization

Post-task sync is the last phase of meaningful work. It prevents forgotten changes, stale project knowledge, and mismatched local/GitHub/server state.

## Order

1. Serena memory freshness first.
2. Project instruction docs second: `AGENTS.md` and `.claude/CLAUDE.md`.
3. Quality checks and manual evidence third.
4. Atomic commits fourth.
5. GitHub sync fifth.
6. Fullrepo branch sync sixth.
7. Merged branch/worktree cleanup last.

## Session And Commit Advice

The flow SessionStart hook gives Codex a compact repository state packet before work starts or resumes. Treat it as an input to planning: inspect dirty files, ahead/behind state, worktree count, docs, and Serena freshness before making assumptions.

The flow PostToolUse hook emits commit advice after Bash `git commit` commands. Advice is informational and should be reviewed before pushing or final delivery, but it must not be treated as a hard failure by itself.

## Serena Interaction

`rldyour-serena-mcp` owns `.serena/memories`, `.serena/plans`, and `.serena/research`. The flow hook must not duplicate that work. It waits until the Serena state script reports current knowledge, then asks for `flow-post-task-sync`.

In fullrepo-managed projects, Serena knowledge is not committed to normal branches. The Serena commit helper may acknowledge current knowledge and clear runtime sync markers without committing when `.serena` knowledge paths are untracked/ignored. Flow then publishes the complete snapshot to `fullrepo`.

## AGENTS.md And .claude/CLAUDE.md

Codex reads `AGENTS.md` as project instructions. Update it when the task changes durable project rules, setup commands, quality gates, deploy contracts, architecture constraints, or agent workflow guidance. Keep it Codex-native and practical: repository layout, commands, checks, constraints, tool routing, and done criteria.

Claude Code reads project memory from `.claude/CLAUDE.md` in rldyour fullrepo-managed projects. Create and update it for every such project, optimized for Claude Code rather than as a thin copy of `AGENTS.md`: commands, architecture, workflow, conventions, Claude Code diagnostics, and Claude-specific settings/hooks/skills locations.

Both files must contain verified facts, not chat history or speculative plans.

For normal projects, root `AGENTS.md`, `.claude/CLAUDE.md`, and `REVIEW.md` are agent-only files and should be restored from `fullrepo`, ignored through `.git/info/exclude`, and excluded from normal branch history. Repositories that are themselves agent tooling may intentionally track selected instruction templates as product files, such as `system/AGENTS.md` in `rldyour-codex`.

Use `plugins/rldyour-flow/scripts/instruction_docs_state.py --json` to decide whether review is needed and `python3 scripts/validate_instruction_docs.py --require-agent-docs` when agent-only context is restored.

## Fullrepo Branch

`fullrepo` is the portable complete-state branch. It lets a new machine initialize with the same agent-only project context while keeping `main` and feature branches free of AI workflow files.

Post-task flow:

1. Commit and push normal source/test/docs/config changes to the current upstream branch.
2. Ensure `.git/info/exclude` has the rldyour fullrepo block.
3. If the project is ready to clean its main branch, run `fullrepo_sync.py --migrate-main` once and commit that index cleanup.
4. Run `fullrepo_sync.py --publish` after the normal branch is at its final `HEAD`.
5. Verify `fullrepo_sync.py --status-json` and branch refs before final delivery.

`fullrepo` uses safe force updates because it is a generated snapshot branch. Use `--force-with-lease`, not a blind `--force`, so an unexpected remote update cannot be silently overwritten.

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
- `flow_post_task_state.py` exposes `branch_cleanup_state`; merged local branches, merged remote branches, and merged workflow worktree candidates keep `needs_flow_sync` true until cleaned or reported as blockers.
- Delete remote branches after merge when the branch was created for this workflow and no open PR depends on it. Protected branches such as `main` and `fullrepo` are never cleanup candidates.
- Ask the user if branch ownership, merge status, or remote state is unclear.
