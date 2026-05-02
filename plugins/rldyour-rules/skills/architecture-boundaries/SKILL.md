---
name: architecture-boundaries
description: "Architecture boundary rules for Codex. Use automatically for frontend, backend, mobile UI, desktop UI, API, module placement, layering, FSD, Feature-Sliced Design, Vertical Slice Architecture, VSA, clean architecture, public API, imports, slices, modules, архитектура, слои, FSD, VSA, фронтенд, бекенд, модуль, границы."
---

# Architecture Boundaries

## Purpose

Keep systems easy to understand, change, and scale by using stable architecture boundaries and project-consistent placement.

## Default Architecture

- Existing project architecture is the source of truth. Do not rewrite architecture just to satisfy a generic rule.
- New frontend, web UI, mobile UI, and desktop UI areas default to Feature-Sliced Design when the stack allows it.
- New backend areas default to Vertical Slice Architecture when the application is use-case, command, query, route, or handler oriented.
- Important architecture or technology decisions require an ADR or equivalent decision record.

## Frontend And Client UI

- Prefer FSD layers: `app`, `pages`, `widgets`, `features`, `entities`, `shared`.
- Do not use `processes` by default because it is deprecated in modern FSD.
- Imports should point only to lower layers, except `app` and `shared` rules and explicit project exceptions.
- Use public APIs for slices. Avoid deep imports into slice internals.
- Keep `shared` business-agnostic. Business concepts belong in `entities`, `features`, `widgets`, or `pages`.

## Backend

- Group use-case code vertically when practical: command/query/route input, validation, handler, domain logic, persistence, and response contract should be easy to trace together.
- Minimize cross-slice coupling. Shared backend code must be stable, genuinely reusable, and not a dumping ground.
- Avoid generic service/repository layers when they only pass data through and add no useful abstraction.
- Cross-cutting concerns such as auth, logging, observability, transactions, and error mapping must be explicit and consistently placed.

Read `references/architecture-policy.md` when deciding placement or documenting an ADR.

