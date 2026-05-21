# rldyour-flow

`rldyour-flow` is the autonomous SDLC orchestration layer for Codex.

It provides Russian-first command skills:

- `ry-init`: initialize project, module, or feature scope with Serena-first context.
- `ry-start`: implement a task through context sufficiency, research, plan, worktree, commits, quality gates, reviews, and sync.
- `ry-newp`: design and optionally scaffold a new project after deep questioning.
- `ry-review`: review a diff/scope plus affected integration graph.
- `ry-repair`: normalize stale docs, memories, contracts, hooks, MCP/LSP config, CI, and AI-tool context while asking the owner for ADR/business decisions.
- `ry-deploy`: synchronize local, GitHub, and server state, then deploy and verify.
- `instruction-docs-sync`: synchronize Codex `AGENTS.md` and Claude Code `.claude/CLAUDE.md` from verified project facts.
- `flow-post-task-sync`: finish task state by synchronizing Serena memories, agent-only files, git commits, GitHub, `fullrepo`, and branch/worktree cleanup.

## Fullrepo Branch

Normal branches keep product history clean. Agent-only files such as root `AGENTS.md`, `.claude/CLAUDE.md`, `REVIEW.md`, `.serena` knowledge, `.claude`, `.codex`, `.cursor/rules`, `.agents/skills`, and similar AI workflow files are restored locally from `fullrepo` and ignored through `.git/info/exclude`.

`plugins/rldyour-flow/scripts/fullrepo_sync.py` owns the deterministic behavior:

- `--restore`: restore agent-only context from `origin/fullrepo`.
- `--migrate-main`: remove tracked agent-only files from the current branch index while keeping them locally.
- `--publish`: publish current `HEAD` plus agent-only files to `fullrepo` with safe `--force-with-lease`.
- `--bootstrap-init`: initialize a repository for `ry-init` by installing excludes, restoring existing `fullrepo` context, publishing local agent-only files when no `fullrepo` exists, and removing tracked agent-only files from the current branch index when migration is needed.
- `--status-json`: expose state to hooks, diagnostics, and validation.

`plugins/rldyour-flow/scripts/local_git_ai_guard.sh` is the canonical local Git pre-push guard for rldyour-managed product repositories. Install it with `scripts/install_local_git_hooks.sh --apply`. It applies strict product-branch protection while treating `refs/heads/${RLDYOUR_FULLREPO_BRANCH:-fullrepo}` as the generated agent-context branch: agent-only paths and AI markers are allowed there, but definite secrets, runtime markers, browser artifacts, and local env files still block the push.

## Hook Strategy

The plugin includes a bounded SessionStart bootstrap hook, a read-only SessionStart context hook, a cwd-safety PreToolUse guard, advisory PostToolUse hooks, and a Stop hook.

`session_start_worktree_bootstrap.sh` is the only mutating SessionStart hook. It runs `fullrepo_sync.py --restore-local` only when canonical agent-only markers are missing and an existing local `origin/fullrepo` ref is already present. It never fetches, publishes, pushes, commits, or edits non-agent project files.

`session_start_context.sh` is read-only, fast, and offline. It adds a compact local repository context packet to the session: branch, HEAD, local upstream drift, tracked dirty files, worktree count, Serena sync-marker state, local fullrepo ref/exclude state, and whether startup markers suggest follow-up sync. It deliberately does not fetch, run deep Serena/fullrepo scans, or call `flow_post_task_state.py`; scoped `ry-init`, Stop, doctor, and explicit validation own the deeper checks.

`flow_post_task_state.py` includes branch-cleanup state. Merged local branches, merged remote branches, and merged workflow worktrees keep `needs_flow_sync` true until they are removed or reported as blockers. Protected branches such as `main` and `fullrepo` are excluded from cleanup candidates.

Bootstrap-only `.serena` files created by tool startup, such as an untracked `.serena/project.yml` plus runtime markers, are ignored by the flow state gate. They are not enough to force `flow-post-task-sync` in an otherwise clean or unborn repository.

The PostToolUse hook watches Bash `git commit` commands and emits non-blocking commit advice for conventional commit format, oversized subjects, suspicious sensitive paths, runtime markers, browser evidence, or very broad commits. It never rejects the command.

The PreToolUse cwd guard blocks Bash commands that would rename or remove the active Codex session directory or repository root. Codex runs hook commands with the session cwd; if that path is removed or renamed outside the active session, later hook processes may fail before their scripts start.

The Stop hook does not duplicate Serena memory sync. Serena owns `.serena/memories`, `.serena/plans`, and `.serena/research` freshness. The flow Stop hook waits until Serena is current, then asks Codex to run `instruction-docs-sync` when needed and `flow-post-task-sync` for docs, git, GitHub, and fullrepo synchronization. Stop-state checks use local-only fullrepo status and child process-group timeouts; network fullrepo sync stays in explicit post-task sync, doctor, or validation commands. The continuation prompt includes installed script paths so product repositories do not need to vendor this plugin.

`ry-init` is read-only for Serena knowledge by default. It may bootstrap `fullrepo` context, but it reports memory candidates instead of writing `.serena` unless the user explicitly requested memory sync or a stale-memory hook requires it.

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
