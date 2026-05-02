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
3. Read `references/init-context-pack.md` and use it as the required context-pack contract.
4. Use `serena-code-workflow`: check onboarding, list memories, read relevant memories, and use Serena semantic tools before raw reads.
5. Map the requested scope deeply enough to understand modules, layers, symbols, DB fields, schemas, APIs, generated artifacts, configs, tests, and integration paths.
6. Use `lsp-routing` or `lsp-health-check` when language server support affects understanding.
7. Use `tech-research` or `web-research` only for unclear technology, architecture, or current best-practice questions.
8. Synthesize a Russian report with exact source-of-truth paths, current behavior, data/contracts, integration points, quality gates, risks, gaps, and what Codex can now safely change.
9. If durable facts were discovered, let `serena-memory-sync` capture them.

## Scope Rules

- Empty scope means whole project.
- Sphere scope means the whole sphere plus integration points.
- Feature scope means trace all layers touched by that feature.
- Ambiguous scope means ask the user with 2-3 options.
- Do not stop at file lists. The initialized context must explain how relevant code works end to end.
- For database-backed or API work, include fields, schemas, migrations, payloads, and caller/client paths.
- For UI/client work, include routes/screens/components, state, API calls, design-system constraints, browser-visible behavior, and tests.

## Output

Report in Russian:

- Scope initialized.
- Git/GitHub/worktree state.
- Architecture and data flow.
- Key files and symbols.
- Data models, DB fields, schemas, API contracts, config/env keys, and generated artifacts.
- Integration points.
- Tests, LSP/check commands, browser/security/design evidence when relevant.
- Known risks and gaps.
- Ready-for tasks.
