---
name: implementation-discipline
description: "Реализация: рефакторинг, naming, schemas, tests, errors, reuse. Используй для: доработка, контракты. EN: implementation discipline."
---

# Implementation Discipline

## Purpose

Make every change precise, synchronized, maintainable, and consistent with the system around it.

## Workflow

- Understand the current implementation before editing. Use Serena semantic tools first when available.
- Trace all affected integration points before finalizing: routes, clients, schemas, DTOs, migrations, generated types, config, docs, and tests.
- Preserve existing public contracts unless the task explicitly requires a breaking change.
- Keep changes atomic and readable. Separate mechanical refactors from behavior changes.
- Keep git history logical: separate implementation, tests/validators,
  docs/instructions, license/metadata, generated artifacts, and Serena knowledge
  sync when they are independently reviewable.
- Prefer clear names over comments. Use comments only for why, constraints, non-obvious algorithms, or external contract reasons.
- Remove obsolete code, stale branches, stale docs, dead feature flags, and outdated tests when they are in scope.
- Keep generated files synchronized with their source commands or state why generation is unavailable.

## Reuse And Abstraction

- Reuse existing stable utilities, primitives, domain types, and patterns.
- Extract common code when there is real duplication or a stable concept, not just because two lines look similar.
- Do not introduce a broad abstraction for a single speculative future case.
- If two areas solve the same problem differently, choose the project-consistent pattern or ask before normalizing wider scope.

Read `references/rules-policy.md` for the full implementation discipline checklist.
