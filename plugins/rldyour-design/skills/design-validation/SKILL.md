---
name: design-validation
description: Mandatory browser validation for design implementation. Use after Figma-to-code work, design-system changes, shadcn/ui or ReactBits integration, responsive layout changes, and any visual/frontend implementation. Delegates browser evidence to rldyour-browser workflows and requires screenshots under browser/.
---

# Design Validation

## Purpose

Prove that design work is visually accurate, functionally correct, responsive, accessible enough for the scope, and aligned with business behavior.

This skill depends on `rldyour-browser`, especially `browser-validation`.

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
4. Fix mismatches and re-run checks.
5. Report remaining mismatches or blockers explicitly.

## Done Criteria

Design implementation is not done until:

- The main Figma frame or provided design reference is represented in the browser.
- Critical visual states and responsive frames are checked.
- Functional and business behavior affected by the design is checked.
- Runtime blockers are absent or documented.
- Screenshots/evidence are either cleaned or intentionally kept by owner request.

## Output

Report in Russian:

- `Visual checks`: frames/viewports/states checked.
- `Screenshots`: artifact paths under `browser/` and cleanup status.
- `Functional checks`: flows and business rules verified.
- `Runtime checks`: console/network/performance status if checked.
- `Fixed mismatches`: visual or behavioral issues corrected.
- `Residual gaps`: exact missing Figma access, assets, credentials, states, or browser constraints.
