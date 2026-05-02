---
name: implementation-discipline
description: "Implementation discipline rules for Codex. Use automatically when writing, changing, refactoring, deleting, synchronizing, or reviewing code, APIs, schemas, configs, generated types, migrations, tests, imports, naming, error handling, reuse, duplication, реализация, доработка, рефакторинг, синхронизация кода, переиспользование, нейминг, ошибки."
---

# Implementation Discipline

## Purpose

Make every change precise, synchronized, maintainable, and consistent with the system around it.

## Workflow

- Understand the current implementation before editing. Use Serena semantic tools first when available.
- Trace all affected integration points before finalizing: routes, clients, schemas, DTOs, migrations, generated types, config, docs, and tests.
- Preserve existing public contracts unless the task explicitly requires a breaking change.
- Keep changes atomic and readable. Separate mechanical refactors from behavior changes.
- Prefer clear names over comments. Use comments only for why, constraints, non-obvious algorithms, or external contract reasons.
- Remove obsolete code, stale branches, stale docs, dead feature flags, and outdated tests when they are in scope.
- Keep generated files synchronized with their source commands or state why generation is unavailable.

## Reuse And Abstraction

- Reuse existing stable utilities, primitives, domain types, and patterns.
- Extract common code when there is real duplication or a stable concept, not just because two lines look similar.
- Do not introduce a broad abstraction for a single speculative future case.
- If two areas solve the same problem differently, choose the project-consistent pattern or ask before normalizing wider scope.

Read `references/rules-policy.md` for the full implementation discipline checklist.

