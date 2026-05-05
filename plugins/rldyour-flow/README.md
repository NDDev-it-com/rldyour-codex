# rldyour-flow

`rldyour-flow` is the autonomous SDLC orchestration layer for Codex.

It provides Russian-first command skills:

- `ry-init`: initialize project, module, or feature scope with Serena-first context.
- `ry-start`: implement a task through context sufficiency, research, plan, worktree, commits, quality gates, reviews, and sync.
- `ry-newp`: design and optionally scaffold a new project after deep questioning.
- `ry-review`: review a diff/scope plus affected integration graph.
- `ry-deploy`: synchronize local, GitHub, and server state, then deploy and verify.
- `instruction-docs-sync`: synchronize Codex `AGENTS.md` and Claude Code `.claude/CLAUDE.md` from verified project facts.
- `flow-post-task-sync`: finish task state by synchronizing Serena memories, agent-only files, git commits, GitHub, `fullrepo`, and branch/worktree cleanup.

## Fullrepo Branch

Normal branches keep product history clean. Agent-only files such as root `AGENTS.md`, `.claude/CLAUDE.md`, `REVIEW.md`, `.serena` knowledge, `.claude`, `.codex`, `.cursor/rules`, `.agents/skills`, and similar AI workflow files are restored locally from `fullrepo` and ignored through `.git/info/exclude`.

`plugins/rldyour-flow/scripts/fullrepo_sync.py` owns the deterministic behavior:

- `--restore`: restore agent-only context from `origin/fullrepo`.
- `--migrate-main`: remove tracked agent-only files from the current branch index while keeping them locally.
- `--publish`: publish current `HEAD` plus agent-only files to `fullrepo` with safe `--force-with-lease`.
- `--status-json`: expose state to hooks, diagnostics, and validation.

`plugins/rldyour-flow/scripts/local_git_ai_guard.sh` is the canonical local Git pre-push guard for rldyour-managed product repositories. Install it with `scripts/install_local_git_hooks.sh --apply`. It applies strict product-branch protection while treating `refs/heads/${RLDYOUR_FULLREPO_BRANCH:-fullrepo}` as the generated agent-context branch: agent-only paths and AI markers are allowed there, but definite secrets, runtime markers, browser artifacts, and local env files still block the push.

## Hook Strategy

The plugin includes advisory SessionStart and PostToolUse hooks plus a Stop hook.

The SessionStart hook is read-only. It adds a compact repository context packet to the session: branch, HEAD, upstream drift, dirty files, worktree count, Serena memory freshness, fullrepo state, and whether flow sync is pending. It tells Codex to run scoped `ry-init` when context is insufficient, but it does not mutate files or block execution.

`flow_post_task_state.py` includes branch-cleanup state. Merged local branches, merged remote branches, and merged workflow worktrees keep `needs_flow_sync` true until they are removed or reported as blockers. Protected branches such as `main` and `fullrepo` are excluded from cleanup candidates.

The PostToolUse hook watches Bash `git commit` commands and emits non-blocking commit advice for conventional commit format, oversized subjects, suspicious sensitive paths, runtime markers, browser evidence, or very broad commits. It never rejects the command.

The Stop hook does not duplicate Serena memory sync. Serena owns `.serena/memories`, `.serena/plans`, and `.serena/research` freshness. The flow Stop hook waits until Serena is current, then asks Codex to run `instruction-docs-sync` when needed and `flow-post-task-sync` for docs, git, GitHub, and fullrepo synchronization.

Loop prevention uses `.serena/.flow_sync_marker`, which is ignored by git. If the same state already requested a continuation, the hook allows stop to avoid an infinite loop.

## Reviewer Skills

- `flow-architecture-review`
- `flow-quality-review`
- `flow-consistency-review`
- `flow-integration-review`
- `flow-verification-review`
- `flow-security-review`

`ry-start` and `ry-review` orchestrate these as parallel subagent review tracks when the command workflow calls for review agents. They are not broad implicit-entry skills; this keeps normal Russian prompts routed through command and domain skills first.

## Sources

The workflow is based on Codex Skills, Hooks, AGENTS.md, and Subagents documentation; Claude Code memory, hooks, and best-practices documentation; plus GitHub Flow, Conventional Commits, Google code review practices, SRE release engineering, C4, arc42, ADR, and OWASP guidance.
