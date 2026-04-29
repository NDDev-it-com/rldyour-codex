---
name: fsd-frontend-architecture
description: Strict Feature-Sliced Design placement rules for frontend design implementation. Use automatically when placing or refactoring React UI, pages, widgets, features, entities, shared UI primitives, design tokens, assets, model state, API calls, public APIs, imports, or generated Figma, shadcn/ui, or ReactBits code in a frontend project.
---

# FSD Frontend Architecture

## Purpose

Keep frontend design implementation structurally clean and scalable. Default to strict Feature-Sliced Design for React application code.

## Auto Invocation

Use this skill without waiting for an explicit `$fsd-frontend-architecture` call when the task involves:

- Deciding where frontend code belongs in `app`, `pages`, `widgets`, `features`, `entities`, or `shared`.
- Moving generated Figma, shadcn/ui, ReactBits, or custom UI code into production architecture.
- Adding public APIs, fixing imports, preventing cross-slice internals, or reducing duplicated UI structure.
- Separating reusable primitives from business features and page composition.
- Keeping a design implementation scalable instead of page-local and ad hoc.

Use it together with `design-system-implementation` whenever token or shared UI placement is involved.

## Layers

Use these layers only:

- `app`: routing, providers, root layouts, global styles, app-level initialization.
- `pages`: route-level screens and page-specific composition.
- `widgets`: large self-contained UI blocks or page sections that combine features/entities/shared.
- `features`: user actions that provide business value.
- `entities`: domain entities and their UI/model/api where appropriate.
- `shared`: reusable UI primitives, assets, tokens, config, API clients, libs without business logic.

Do not use the deprecated `processes` layer.

## Import Rule

Files can import only from lower layers:

- `app` can import from all lower layers.
- `pages` can import from `widgets`, `features`, `entities`, `shared`.
- `widgets` can import from `features`, `entities`, `shared`.
- `features` can import from `entities`, `shared`.
- `entities` can import from `shared`.
- `shared` imports only internal shared segments or external libraries.

Slices on the same layer must not import each other's internals. Use public APIs.

## Public API Rule

Every slice and relevant segment must expose a public API, usually `index.ts`.

External imports must target public APIs, not internal files:

- Good: `import { UserCard } from "@/entities/user"`.
- Bad: `import { UserCard } from "@/entities/user/ui/UserCard"`.

## Design Placement

Use this placement by default:

- Design tokens: `shared/config/theme` or the existing centralized theme location.
- shadcn primitives: `shared/ui`.
- ReactBits primitives/effects: `shared/ui` if generic, otherwise the owning widget/feature.
- Reusable icons/assets: `shared/assets`.
- Domain-specific assets: owning entity/feature/widget/page slice.
- Page-specific layout: `pages/<page>/ui`.
- Large reusable page sections: `widgets/<widget>/ui`.
- User actions: `features/<feature>/ui`, `features/<feature>/model`, `features/<feature>/api`.
- Domain UI/data: `entities/<entity>/ui`, `entities/<entity>/model`, `entities/<entity>/api`.

## Figma And Generated Code

Never paste generated Figma, shadcn, or ReactBits code blindly.

Before committing generated or copied code:

1. Remove demo-only code, unused props, unused variants, placeholder assets, and unrelated styles.
2. Replace raw design values with centralized tokens.
3. Split code into FSD-appropriate slices and segments.
4. Add or update public APIs.
5. Preserve existing project conventions.
6. Validate in browser.

## Output

For design implementation, report in Russian:

- `Placement`: layer/slice/segment decisions.
- `Public APIs`: new or changed exports.
- `Architecture constraints`: import boundaries or compromises.
- `Generated code adaptation`: what was removed, tokenized, or moved.
- `Validation`: checks proving the placement works.
