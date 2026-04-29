---
name: ry-design
description: End-to-end design implementation command for Codex. Use when the user invokes $ry-design or asks to implement a design, transfer a Figma layout, create frontend UI, build a design system, or produce pixel-perfect frontend work. Orchestrates Figma MCP, centralized tokens, strict FSD placement, shadcn/ui MCP, ReactBits.dev, browser validation, and Serena memory sync when useful.
---

# ry-design

## Purpose

Run the full rldyour design implementation workflow from source design to browser-validated code.

User-facing communication stays in Russian unless requested otherwise. Code, docs, tokens, comments, and commits stay in English.

## Workflow

1. Establish scope: target page/component, Figma source, required states, responsive frames, business behavior, and acceptance criteria.
2. Use `figma-to-code` if Figma context exists. Figma MCP is the design source of truth.
3. Use `design-system-implementation` to create or update centralized tokens before scattering raw design values.
4. Use `fsd-frontend-architecture` to place code into strict FSD layers and public APIs.
5. Use shadcn/ui MCP for primitives, blocks, and registry-based components.
6. Use ReactBits.dev only for purposeful motion or interactive effects that match the design.
7. Implement code with Serena-first local code inspection when available.
8. Use `design-validation` and `rldyour-browser` to verify pixel-perfect layout, functionality, business logic, desktop/mobile, screenshots, and runtime health.
9. Fix mismatches and revalidate until the result is correct or the blocker is explicit.
10. If durable architecture/design-system facts were created, update Serena memories through `serena-memory-sync`.

## Rules

- Centralized design system first: tokens, theme, primitives, variants, and shared assets must have a single source of truth.
- Figma context is source material, not copy-paste code. Adapt to architecture and existing project conventions.
- Strict FSD by default: no deprecated `processes`, no cross-slice internals, public APIs required.
- shadcn/ui is the primary UI primitive source.
- ReactBits is for controlled motion and standout interactive details, not broad architecture.
- Browser validation is mandatory for meaningful frontend design work.
- Browser artifacts go under `browser/` and are not committed.
- Do not use placeholders when real Figma assets are available.
- Do not break business logic to match visuals.

## Output

For a completed design task, answer in Russian with:

- `Scope`: design/page/component implemented.
- `Figma`: source frame/context and assets used.
- `Design system`: tokens/components/assets changed.
- `FSD`: placement decisions and public APIs.
- `Validation`: browser screenshots/checks and cleanup status.
- `Residual gaps`: any unresolved visual, asset, responsive, runtime, or business-logic gaps.
