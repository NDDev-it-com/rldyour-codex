# Architecture Policy

## Existing Projects

Existing project architecture is the source of truth. Apply these defaults to new areas and refactors, but do not force a rewrite when the project already has a coherent architecture.

## Frontend And Client UI Default: FSD

Use Feature-Sliced Design for new frontend, web UI, mobile UI, and desktop UI areas when practical.

Default layers:

- `app`: application setup, providers, routing, global styles.
- `pages`: route-level composition.
- `widgets`: large reusable UI blocks composed from features and entities.
- `features`: user actions and business interactions.
- `entities`: business entities and entity model/UI.
- `shared`: business-agnostic UI, lib, config, API clients, assets.

Rules:

- Do not use `processes` by default.
- Lower layers must not import higher layers.
- Slices should expose public APIs.
- Avoid deep imports into slice internals.
- Keep `shared` free of business-specific concepts.
- Use separate public APIs for `shared/ui` and `shared/lib` components when a single barrel would harm tree-shaking or clarity.
- Use `@x` cross-imports only when an entity relationship needs it and the project accepts the pattern.

## Backend Default: VSA

Use Vertical Slice Architecture for backend features when practical.

Rules:

- Organize around use cases, commands, queries, routes, or handlers.
- Keep validation, handler logic, domain orchestration, persistence interaction, and response mapping easy to trace for one use case.
- Minimize coupling between slices.
- Keep shared code small, stable, and cross-cutting.
- Avoid pass-through services and repositories that add no abstraction value.
- Use common layers only for cross-cutting concerns or proven repeated abstractions.

## ADR Triggers

Create an ADR for:

- New architecture style or major boundary change.
- New framework, database, message broker, auth strategy, deployment model, or critical dependency.
- Intentional deviation from FSD/VSA defaults.
- Breaking public API or contract change.
- Long-lived tradeoff that future Codex sessions must understand.

