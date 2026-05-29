---
name: design-validation
description: "Проверяет дизайн-реализацию в браузере: Figma parity, i18n/token/static scans и responsive states. EN: design validation, browser, pixel-perfect."
---

# Design Validation

## Purpose

Prove that design work is visually accurate, functionally correct, responsive, accessible enough for the scope, and aligned with business behavior.

This skill depends on `rldyour-browser`, especially `browser-validation`.

Read `../../references/figma-delivery-contract.md` when validating a Figma-driven or production-quality UI task.

## Auto Invocation

Use this skill without waiting for an explicit `$design-validation` call when the task has changed or created:

- Frontend UI, layout, styling, responsive behavior, visual states, animations, or interactions.
- Figma-to-code implementation, shadcn/ui components, ReactBits components, or design-system tokens.
- User-visible page, widget, feature, form, modal, menu, navigation, or stateful component behavior.

If browser tools cannot run, state the blocker and perform the strongest available static checks instead. Do not mark meaningful design work as complete without either browser evidence or an explicit validation blocker.

## Required Checks

For every meaningful design implementation, validate:

- Figma match: visual comparison against the inspected frame or supplied reference.
- Pixel-perfect details: spacing, typography, colors, radii, shadows, layout, assets, states.
- Design-system consistency: tokens, shared primitives, shadcn variants, no duplicate raw values.
- Functionality: interactions, form flows, navigation, modals, menus, state transitions.
- Business logic: required fields, permissions, calculations, data visibility, edge cases.
- Responsiveness: desktop plus mobile by default, and every provided Figma frame size.
- Runtime health: console errors, failed network requests, hydration/runtime issues when relevant.
- Accessibility basics: semantic controls, labels, keyboard reachability, focus visibility.
- Motion: purposeful, performant, reduced-motion friendly when ReactBits or custom animation is used.
- Content and i18n: no unapproved user-visible literal strings, complete translation keys, long localized text, plural/context variants, and locale-aware runtime formatting when applicable.
- Token discipline: no raw colors, shadows, radii, typography values, arbitrary Tailwind values, or duplicated one-off styles outside token/theme files unless explicitly justified.
- Dynamic content: loading, empty, error, permission, long-list, and realistic data states for blocks classified as admin/CMS/API/session-backed.

## Browser Evidence

Use `browser/` for all browser artifacts:

- `browser/<feature>-figma-reference.png` when a reference screenshot is created.
- `browser/<feature>-desktop.png`.
- `browser/<feature>-mobile.png`.
- `browser/<feature>-state-<name>.png`.
- `browser/<feature>-trace.zip` or similar only when useful.

Do not commit browser artifacts. Delete them after the task unless the owner explicitly asks to keep them.

## Validation Workflow

1. Use Playwright MCP for browser flow reproduction, screenshots, accessibility snapshots, and assertions.
2. Use Chrome DevTools MCP for console/network/runtime/layout/performance diagnosis when relevant.
3. Compare against Figma context and screenshots.
4. Run or manually perform static scans for raw visible text, raw design values, placeholders, duplicate generated components, and missing assets in the touched scope.
5. Fix mismatches and re-run checks.
6. Report remaining mismatches or blockers explicitly.

## Done Criteria

Design implementation is not done until:

- The main Figma frame or provided design reference is represented in the browser.
- Critical visual states and responsive frames are checked.
- Functional and business behavior affected by the design is checked.
- i18n, token, UI-kit reuse, dynamic/static content, and placeholder checks are complete for the touched scope.
- Runtime blockers are absent or documented.
- Screenshots/evidence are either cleaned or intentionally kept by owner request.

Do not finish a meaningful design task with only static review if browser tools can run. If browser validation is unavailable, state the exact tool/environment blocker and run the strongest project-native build, lint, type, and static scans instead.

## Output

Report in Russian:

- `Visual checks`: frames/viewports/states checked.
- `Screenshots`: artifact paths under `browser/` and cleanup status.
- `Functional checks`: flows and business rules verified.
- `Static checks`: i18n/token/raw-value/placeholder scans and results.
- `Runtime checks`: console/network/performance status if checked.
- `Fixed mismatches`: visual or behavioral issues corrected.
- `Residual gaps`: exact missing Figma access, assets, credentials, states, or browser constraints.
