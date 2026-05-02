---
name: ry-start
description: Full feature/task lifecycle for Codex. Use automatically when the user invokes ry-start or asks in Russian or English to implement, build, fix, change, develop, investigate and then implement, сделать фичу, реализуй, доработай, исправь, начни задачу, сделай качественно, сделай полный цикл. Performs scoped init when needed, deep code and internet research, plan, verified implementation, worktree/PR, atomic commits, quality gates, reviewer subagents, browser/security checks, and post-task sync.
---

# ry-start

## Purpose

Implement a task to a high-quality, scalable, synchronized state. Speed is secondary to correctness, consistency, maintainability, and clean git history.

## Workflow

1. If context is missing, run a scoped `ry-init` automatically.
2. Understand the prompt. For ambiguity, ask concise Russian questions with options.
3. Research code through Serena memories and semantic tools.
4. Research current docs, patterns, and alternatives through `rldyour-explore`.
5. Write a detailed plan. Verify each plan item against code using Serena before editing.
6. Create or use a feature branch/worktree. Use stacked PRs only when the task naturally splits into independent logical PRs.
7. Implement strictly by plan, adapting only after code evidence. Make frequent atomic Conventional Commits.
8. Fix all issues in touched scope plus affected integration path. If wider technical debt is found, ask whether to expand scope.
9. Run quality gates using project scripts, `rldyour-lsps`, and detected stack checks.
10. Trigger browser validation for UI/browser-visible work unless auth blocks it; if auth blocks, report the limitation and use available evidence.
11. Trigger security review for security-sensitive changes or explicit user request.
12. Run review phase with subagents for architecture, quality, consistency, integration, verification, and security when applicable.
13. Run `flow-post-task-sync` before final response.

## Subagent Permission

Invoking `ry-start` is the owner's explicit permission to use parallel reviewer subagents during the review phase. Prompts must be self-contained and read-only for reviewers.

## Non-Negotiables

- No hacks, temporary workarounds, or untracked debt in touched scope.
- No fake green checks. If a check cannot run, say why.
- No silent destructive git actions. Branch/worktree cleanup requires verified merged state.
- No secrets in commits, logs, docs, memories, or prompts.

