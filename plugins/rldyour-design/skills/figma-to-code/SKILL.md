---
name: figma-to-code
description: "Implement Figma designs pixel-perfect with Figma MCP, tokens, FSD, i18n, dynamic/static content classification, shadcn/ui, browser validation. Use for Figma links, перенеси из фигмы, сверстай макет."
---

# Figma To Code

## Purpose

Transfer designer-provided Figma layouts into production frontend code as accurately as possible while preserving architecture, design-system consistency, and runtime behavior.

User-facing conversation stays in Russian unless requested otherwise. Repository documentation, code comments, commit messages, and design-token files stay in English.

## Auto Invocation

Use this skill without waiting for an explicit `$figma-to-code` call when the task is about:

- Implementing, copying, transferring, or recreating a Figma frame, component, layout, selection, or designer mockup.
- Matching a visual reference pixel-perfect or as close as possible in a browser.
- Extracting Figma variables, styles, components, assets, dimensions, or Code Connect hints into code.
- Turning design handoff material into React/frontend implementation.

Do not use it for design-system-only refactors that have no Figma source; use `design-system-implementation` instead.

## Source Of Truth

Figma MCP is the source of truth for:

- Selected frames, components, variants, variables, styles, layout data, dimensions, constraints, and assets.
- Figma screenshots or visual references used for pixel comparison.
- Code Connect hints when available; prefer connected project components over inventing new components.

If Figma MCP is unavailable, say so and use only explicitly provided fallback assets such as screenshots or specs. Do not pretend a design was inspected.

Read `../../references/figma-delivery-contract.md` for the mandatory implementation manifest, content classification, i18n, design-system, and final validation gate whenever the task is more than a one-off tiny visual tweak.

## Workflow

1. Parse the Figma URL or current selection. For a whole canvas or heavy frame, run `get_metadata` first, identify target frames/sections, and avoid one broad implementation pass.
2. Fetch exact Figma context for each target through `get_design_context`.
3. Capture `get_screenshot` for each target frame/section and keep it as the visual reference during implementation.
4. Fetch `get_variable_defs` for variables/styles and use Code Connect or design-system lookup when available.
5. Build the implementation manifest: scope, frame/state matrix, assets, tokens, content model, architecture, and validation plan.
6. Classify every visible block as `static-i18n`, `config-backed`, `cms-admin-backed`, `api-domain-backed`, or `user-session-backed`.
7. Map all user-visible text into centralized i18n/resources. Static content means "not admin-backed", not "inline hardcoded strings".
8. Map Figma variables/styles to centralized design tokens before writing page/widget code.
9. Inspect the existing codebase with Serena-first workflow to find architecture, existing design system, i18n setup, shadcn setup, data/API patterns, and component placement.
10. Choose FSD placement before writing code: `shared`, `entities`, `features`, `widgets`, `pages`, or `app`.
11. Use shadcn/ui MCP for primitives and registry blocks when they fit the design.
12. Use ReactBits.dev only for purposeful animation or interactive effects that match the design and do not harm performance or accessibility.
13. Implement the design by adapting Figma context into project-native code. Do not paste generated code blindly.
14. Validate in browser through `design-validation` and `browser-validation`: desktop, mobile, provided frame sizes, state matrix, screenshots under `browser/`, functional flow, business behavior, runtime health, i18n, and token/static scans.
15. Iterate until the result is visually and functionally aligned, or report the exact blocker.

## Pixel-Perfect Requirements

Match:

- Layout: frame size, grid, alignment, spacing, containers, breakpoints, overflow, and scroll behavior.
- Typography: font family, size, line height, weight, letter spacing, text transform, truncation, and responsive scaling.
- Visual tokens: colors, opacity, gradients, borders, radius, shadows, blur, z-index, and elevation.
- Assets: icons, images, illustrations, masks, aspect ratios, object fit, and exported file quality.
- States: hover, focus, active, disabled, selected, loading, error, empty, modal, drawer, and validation states.
- Interactions: navigation, transitions, motion, form behavior, dialogs, menus, and any designer-specified behavior.

## Data And i18n Requirements

- Do not implement repeated cards, tables, dashboards, forms, counters, filters, editable marketing content, pricing, FAQs, blog/news, testimonials, product catalogs, or account-specific UI as static JSX without proving it is truly static.
- Prefer existing admin/CMS/API/domain patterns for dynamic blocks. If no backend/admin exists, create the frontend contract, types, fixtures, loading/empty/error states, and mark backend/admin work as a residual product blocker.
- Do not inline user-visible copy in components. Use existing i18n namespaces, or create the smallest centralized i18n structure consistent with the project.
- Avoid sentence-fragment interpolation. Use complete translation strings, plural/context variants, and locale-aware formatting for runtime values.
- Test long localized strings and non-default content lengths during browser validation.

## Asset Rule

Extract or copy all required design assets when possible. Place reusable assets in the FSD-appropriate location, usually `shared/assets` or the owning slice when the asset is domain-specific.

Do not use placeholders if Figma assets are available. If an asset cannot be extracted, mark it as a blocker or unresolved gap.

## Done Gate

Do not mark the implementation complete until the `figma-delivery-contract.md` validation gate is satisfied. If a gate is blocked by missing Figma access, credentials, unavailable services, or product decisions, report that blocker explicitly instead of delivering as complete.

## Output

For implementation work, report in Russian:

- `Figma scope`: inspected frame/component and source context.
- `Content model`: dynamic/static/admin/i18n decisions.
- `Design system updates`: tokens/components/assets created or changed.
- `FSD placement`: where code was placed and why.
- `Browser validation`: screenshots/checks performed through `rldyour-browser`.
- `Mismatches fixed`: visual or functional gaps corrected.
- `Residual gaps`: missing assets, unavailable Figma context, unavailable credentials, or untested states.
