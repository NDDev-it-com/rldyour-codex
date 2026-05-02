# rldyour-flow

`rldyour-flow` is the autonomous SDLC orchestration layer for Codex.

It provides Russian-first command skills:

- `ry-init`: initialize project, module, or feature scope with Serena-first context.
- `ry-start`: implement a task through context sufficiency, research, plan, worktree, commits, quality gates, reviews, and sync.
- `ry-newp`: design and optionally scaffold a new project after deep questioning.
- `ry-review`: review a diff/scope plus affected integration graph.
- `ry-deploy`: synchronize local, GitHub, and server state, then deploy and verify.
- `flow-post-task-sync`: finish task state by synchronizing Serena memories, `AGENTS.md`, `CLAUDE.md`, git commits, GitHub, and branch/worktree cleanup.

## Hook Strategy

The plugin includes advisory SessionStart and PostToolUse hooks plus a Stop hook.

The SessionStart hook is read-only. It adds a compact repository context packet to the session: branch, HEAD, upstream drift, dirty files, worktree count, Serena memory freshness, and whether flow sync is pending. It tells Codex to run scoped `ry-init` when context is insufficient, but it does not mutate files or block execution.

The PostToolUse hook watches Bash `git commit` commands and emits non-blocking commit advice for conventional commit format, oversized subjects, suspicious sensitive paths, runtime markers, browser evidence, or very broad commits. It never rejects the command.

The Stop hook does not duplicate Serena memory sync. Serena owns `.serena/memories`, `.serena/plans`, and `.serena/research` freshness. The flow Stop hook waits until Serena is current, then asks Codex to run `flow-post-task-sync` for docs and git synchronization.

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

The workflow is based on Codex Skills, Hooks, AGENTS.md, and Subagents documentation, plus GitHub Flow, Conventional Commits, Google code review practices, SRE release engineering, C4, arc42, ADR, and OWASP guidance.
