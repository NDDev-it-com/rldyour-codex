---
name: browser-validation
description: Browser validation workflow for UI implementation, pixel-perfect checks, functional behavior, responsive states, and business-logic verification. Use automatically after frontend changes, browser-visible feature work, visual fixes, form/flow changes, route changes, client-side logic changes, and whenever the user asks to check in browser, verify visually, take screenshots, validate UI, or prove implementation in a real browser. Playwright MCP is primary; Chrome DevTools MCP is used when console/network/runtime evidence is needed.
---

# Browser Validation

## Purpose

Validate browser-facing work with real browser evidence, not assumptions. The goal is to prove the implementation is visually correct, functionally correct, and consistent with business logic.

User-facing reports stay in Russian unless requested otherwise. Store browser artifacts under `browser/` and do not commit them.

## Auto Invocation

Use this skill without waiting for an explicit `$browser-validation` call when the task asks to:

- Check, validate, verify, or prove a browser-visible implementation.
- Verify UI visually, pixel-perfect, responsive, mobile/desktop, or against a design/reference.
- Test navigation, forms, modals, tabs, dialogs, auth-like flows, route changes, loading/error/empty states, or business behavior.
- Capture screenshots or browser evidence under `browser/`.
- Confirm that a frontend fix works after code changes.

If the validation exposes console, network, runtime, layout, hydration, or performance problems, add `browser-debug`.

## When To Use

Use this skill after:

- UI, layout, styling, responsive, animation, or design-system changes.
- User-flow, form, route, navigation, modal, upload, auth, checkout-like, or wizard changes.
- Client-side business logic, validation, error-state, loading-state, or empty-state changes.
- Changes that affect browser-visible data, browser storage, network requests, hydration, or runtime state.

If the user asks for pixel-perfect, production-quality, or "check in browser", this skill applies.

## Required Validation Layers

Validate the implementation across these layers when relevant:

- Pixel-perfect: screenshots, spacing, typography, colors, alignment, visual hierarchy, responsive layout, overflow, scroll, focus, hover/active/disabled states.
- Functionality: navigation, form input, validation, buttons, modals, tabs, dialogs, uploads, state changes, errors, loading, empty states.
- Business logic: permissions, roles, required fields, calculations, step order, state transitions, saved values, data visibility, and edge cases.
- Runtime health: console errors/warnings, failed network requests, hydration/runtime exceptions, unexpected redirects, stale state.
- Accessibility basics: meaningful roles/names where interaction depends on them, keyboard reachability for important flows, visible focus when relevant.
- Mobile/responsive: at least desktop plus mobile when UI/layout changed.

## Playwright Workflow

1. Start from a clean or explicit test state.
2. Navigate to the changed page/flow.
3. Capture an accessibility snapshot to understand the page structure.
4. Exercise the main user flow and changed edge cases.
5. Use testing capability assertions when useful: visible element/text/list/value checks.
6. Capture screenshots into `browser/` for key states: initial, changed state, error/empty/loading state, desktop/mobile, and final state.
7. Check network/storage tools when behavior depends on API responses, cookies, localStorage, sessionStorage, or persisted state.
8. Use Chrome DevTools if console/network/runtime/performance diagnosis is needed.
9. Re-run the relevant flow after fixes.
10. Delete transient artifacts in `browser/` unless the owner asks to keep them.

## Pixel-Perfect Standard

Do not call UI done if:

- Important content overflows, clips, jumps, or is misaligned.
- Mobile layout is broken for a changed responsive surface.
- Loading, error, empty, disabled, hover/focus, or modal states are visibly inconsistent when they are part of the feature.
- Typography, spacing, and contrast are visibly inconsistent with the local design language.
- The page works only by accident because a business rule or state transition was not tested.

When a design reference exists, compare against it directly. When no reference exists, compare against the existing product style and nearby components.

## Artifact Rule

All screenshots and browser artifacts must be written under `browser/`.

Use descriptive names:

- `browser/<feature>-desktop-before.png`
- `browser/<feature>-desktop-after.png`
- `browser/<feature>-mobile.png`
- `browser/<feature>-error-state.png`
- `browser/<feature>-trace.zip`

Do not commit these files. They are local evidence. Remove them after the task unless the owner explicitly asks to keep them.

## Output

For implementation work, report in Russian:

- `Browser checks`: flows and viewports tested.
- `Visual evidence`: screenshot filenames created under `browser/` and whether they were deleted or kept.
- `Functional evidence`: interactions/assertions verified.
- `Runtime evidence`: console/network/storage/performance status if checked.
- `Fixes made`: browser-driven corrections applied.
- `Residual risks`: flows not tested, unavailable credentials, external dependency, or manual checks still needed.

If browser validation cannot run, state the blocker and the exact fallback used.
