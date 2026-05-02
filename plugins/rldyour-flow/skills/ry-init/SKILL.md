---
name: ry-init
description: "Initialize scoped project context with Serena-first discovery and sync. Use for ry-init, init scope, understand project, инициализируй, загрузи контекст, изучи проект/модуль."
---

# ry-init

## Purpose

Build a verified mental model of the requested project scope before implementation. If the scope is a sphere such as backend or mobile UI, inspect the entire sphere and all integration points needed to understand how it works end to end.

## Workflow

1. Run `plugins/rldyour-flow/scripts/git_sync_audit.sh` when available.
2. Inspect dirty work, old branches, and worktrees. If code is correct and consistent, synchronize it into `main`, push, and remove merged branches/worktrees. If risky, explain the issue in Russian and ask the user with concrete options.
3. Use `serena-code-workflow`: check onboarding, list memories, read relevant memories, and use Serena semantic tools before raw reads.
4. Use `lsp-routing` or `lsp-health-check` when language server support affects understanding.
5. Use `tech-research` or `web-research` only for unclear technology, architecture, or current best-practice questions.
6. Synthesize a Russian report with exact source-of-truth paths, current behavior, integration points, risks, and what Codex can now safely change.
7. If durable facts were discovered, let `serena-memory-sync` capture them.

## Scope Rules

- Empty scope means whole project.
- Sphere scope means the whole sphere plus integration points.
- Feature scope means trace all layers touched by that feature.
- Ambiguous scope means ask the user with 2-3 options.

## Output

Report in Russian:

- Scope initialized.
- Git/GitHub/worktree state.
- Architecture and data flow.
- Key files and symbols.
- Integration points.
- Known risks and gaps.
- Ready-for tasks.
