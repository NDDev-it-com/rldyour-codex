---
name: ry-design
description: "End-to-end design/UI workflow with Figma, i18n, tokens, data classification, full validation. Use for $ry-design, сверстай, перенеси Figma, pixel-perfect."
---

# ry-design

## Purpose

Run the full rldyour design implementation workflow from source design to browser-validated code.

User-facing communication stays in Russian unless requested otherwise. Code, docs, tokens, comments, and commits stay in English.

## Auto Invocation

Use this skill without waiting for an explicit `$ry-design` call when the user asks for an end-to-end design result rather than a narrow subtask:

- Implement a Figma design, designer mockup, page, component, landing, dashboard, widget, feature UI, or redesign.
- Create UI that requires tokens, architecture placement, shadcn/ui or ReactBits components, and browser validation.
- Make frontend design work "pixel-perfect", "production-ready", "according to design", or visually and functionally complete.
- Coordinate multiple design skills in one task.

For very narrow tasks, prefer the matching subskill directly. Use `design-validation` after any meaningful visible implementation even when `$ry-design` is not selected.

For production-quality Figma/UI work, read `../../references/figma-delivery-contract.md` before implementation and before final delivery.

## Workflow

1. Establish scope: target page/component, Figma source, required states, responsive frames, business behavior, content/data ownership, i18n requirements, and acceptance criteria.
2. Use `figma-to-code` if Figma context exists. Figma MCP is the design source of truth.
3. Build the implementation manifest from `figma-delivery-contract.md`.
4. Classify each block as static/config/admin/CMS/API/session-backed before choosing hardcoded config, admin schema, API/domain model, or localized resource placement.
5. Use `design-system-implementation` to create or update centralized tokens, UI-kit primitives, and i18n-ready content surfaces before scattering raw values or text.
6. Use `fsd-frontend-architecture` to place code into strict FSD layers and public APIs.
7. Use shadcn/ui MCP for primitives, blocks, and registry-based components.
8. Use ReactBits.dev only for purposeful motion or interactive effects that match the design.
9. Implement code with Serena-first local code inspection when available.
10. Use `design-validation` and `rldyour-browser` to verify pixel-perfect layout, functionality, business logic, accessibility, desktop/mobile, provided Figma frame sizes, state matrix, screenshots, i18n, token/static scans, and runtime health.
11. Fix mismatches and revalidate until the result is correct or the blocker is explicit.
12. If durable architecture/design-system facts were created, update Serena memories through `serena-memory-sync`.

## Rules

- Centralized design system first: tokens, theme, primitives, variants, and shared assets must have a single source of truth.
- Centralized i18n first for visible copy. Static content is not admin-backed, but it is still localized unless the project explicitly has no i18n.
- Classify dynamic/static/admin-backed content before implementation; do not silently turn dynamic product data into JSX fixtures.
- Figma context is source material, not copy-paste code. Adapt to architecture and existing project conventions.
- Strict FSD by default: no deprecated `processes`, no cross-slice internals, public APIs required.
- shadcn/ui is the primary UI primitive source.
- ReactBits is for controlled motion and standout interactive details, not broad architecture.
- Browser validation is mandatory for meaningful frontend design work.
- The final answer is blocked until design validation passes or the exact external blocker is documented.
- Browser artifacts go under `browser/` and are not committed.
- Do not use placeholders when real Figma assets are available.
- Do not break business logic to match visuals.

## Output

For a completed design task, answer in Russian with:

- `Scope`: design/page/component implemented.
- `Figma`: source frame/context and assets used.
- `Content model`: dynamic/static/admin/i18n decisions.
- `Design system`: tokens/components/assets changed.
- `FSD`: placement decisions and public APIs.
- `Validation`: browser screenshots/checks and cleanup status.
- `Residual gaps`: any unresolved visual, asset, responsive, runtime, or business-logic gaps.
