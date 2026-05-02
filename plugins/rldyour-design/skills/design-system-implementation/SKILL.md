---
name: design-system-implementation
description: "Centralized frontend design system workflow with design tokens, shadcn/ui MCP, and ReactBits.dev. Use automatically for Russian or English design-system work: дизайн-система, дизайн токены, токены, UI primitives, theme tokens, CSS variables, Tailwind/shadcn theme config, variants, типографика, цвета, spacing, radii, shadows, motion tokens, Figma variables, ReactBits, visual consistency."
---

# Design System Implementation

## Purpose

Build and maintain a centralized design system so design implementation is consistent, scalable, and easy for future Codex sessions to modify with high confidence.

The design system is the source of truth for reusable visual decisions. Components should consume tokens instead of scattering raw values across pages and features.

## Auto Invocation

Use this skill without waiting for an explicit `$design-system-implementation` call when the task includes:

- Creating or modifying a design system, theme, tokens, CSS variables, Tailwind config, shadcn theme, or UI kit.
- Adding, adapting, or cleaning shadcn/ui primitives, registry blocks, component variants, or shared UI components.
- Adding ReactBits or custom animated components that need token normalization and reduced-motion handling.
- Replacing raw visual values with centralized tokens.
- Mapping Figma variables, styles, modes, or semantic names into code.

For a full Figma implementation, use it together with `figma-to-code`, `fsd-frontend-architecture`, and `design-validation`.

## Token System

Create or update centralized tokens for all relevant categories:

- Color: primitive palette, semantic colors, text, background, border, surface, state, brand, destructive, success, warning, info.
- Typography: font families, sizes, line heights, weights, letter spacing, headings, body, captions, buttons.
- Spacing: scale, layout gaps, section spacing, component padding, density.
- Radius: base radius, component radius, pill/full radius.
- Shadow/elevation: shadow levels, overlays, popovers, dialogs, focus rings.
- Border: widths, styles, semantic border colors.
- Layout: containers, max widths, columns, gutters, page padding.
- Breakpoints: responsive thresholds and naming.
- Z-index: layers for dropdowns, sticky bars, modals, toasts, tooltips.
- Motion: duration, easing, delay, stagger, reduced-motion behavior.
- Opacity/blur: overlays, disabled states, glass effects.
- Component states: hover, focus, active, disabled, selected, loading, error.

Preferred placement in strict FSD:

- `shared/config/theme`: token definitions, CSS variables, theme config, Tailwind/shadcn theme mapping.
- `shared/ui`: reusable primitives and shadcn-based components without business logic.
- `app`: global style imports, providers, theme initialization, and root CSS variable attachment.

If the project already has a design-token convention, extend it rather than creating a parallel system.

## Figma Variable Mapping

When Figma variables are available:

1. Extract variable names, modes, values, aliases, and usage context through Figma MCP.
2. Preserve traceability from Figma names to code tokens.
3. Prefer semantic tokens in code, with primitive values underneath when needed.
4. Avoid hardcoding Figma values inside page/widget/feature components when they represent reusable design decisions.
5. Document unresolved token gaps in the final report.

## shadcn/ui Rules

Use shadcn/ui MCP as the primary component and registry workflow:

- Search/browse existing registry items before writing common primitives from scratch.
- Install only the components/blocks needed for the task.
- Keep shadcn primitives in `shared/ui` or the existing project-specific UI-kit location.
- Adapt generated components to the centralized token system.
- Do not keep unused variants, demo-only code, or registry leftovers.
- Preserve accessibility behavior from shadcn primitives.

## ReactBits Rules

Use ReactBits.dev for purposeful motion and interactive effects only:

- Prefer TypeScript + Tailwind variants when the project uses TypeScript and Tailwind.
- Prefer shadcn-compatible install URLs when available; fallback to manually adapting source code.
- Inspect dependencies before adding them. Avoid heavy dependencies for minor visual effects.
- Normalize styling to project tokens and FSD placement.
- Respect reduced-motion users and performance budgets.
- Do not make ReactBits a separate design system. It is a source component library, not the project source of truth.

## Quality Rules

- No duplicated token definitions across pages/features.
- No raw colors, shadows, radii, motion timings, or typography values when a design token exists or should exist.
- No business logic in `shared/ui`.
- No component imports from another slice internals; use public APIs.
- No visual-only implementation that breaks business logic, accessibility, or browser validation.

## Output

Report in Russian:

- `Tokens`: new/changed token categories and source.
- `Components`: shadcn/ui or ReactBits components used and where they were placed.
- `FSD placement`: design-system files and public APIs touched.
- `Compatibility`: dependency, accessibility, performance, and reduced-motion notes.
- `Validation`: browser/design checks completed or blocked.
