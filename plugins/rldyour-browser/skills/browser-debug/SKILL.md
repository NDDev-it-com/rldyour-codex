---
name: browser-debug
description: "Debug browser-only failures with Chrome DevTools/Playwright. Use for console/network/runtime/layout/hydration/Lighthouse bugs; triggers: ошибка в браузере, консоль, сеть, не работает UI."
---

# Browser Debug

## Purpose

Diagnose browser-only failures with runtime evidence. Use Chrome DevTools MCP for deep inspection and Playwright MCP for deterministic reproduction and validation.

User-facing reports stay in Russian unless requested otherwise. Browser artifacts belong under `browser/`.

## Auto Invocation

Use this skill without waiting for an explicit `$browser-debug` call when the task mentions:

- Browser-only bug, broken UI in browser, hydration issue, runtime exception, console error, or source-map issue.
- Network failure, unexpected API response, redirect, cache, CORS, CSP, auth/session browser behavior, or failed request.
- Layout issue, overflow, rendering mismatch, computed style problem, DOM state mismatch, or responsive breakage.
- Lighthouse, Core Web Vitals, performance trace, slow rendering, memory issue, long task, or layout shift.
- A failed `browser-validation` flow where evidence is needed to find root cause.

Use `browser-validation` after fixing the issue to prove the user flow works.

## When To Use

Use this skill when:

- A page works in code review but fails in the browser.
- Console errors, hydration failures, source-map issues, or runtime exceptions appear.
- API calls fail, return unexpected payloads, redirect incorrectly, cache incorrectly, or trigger CORS/CSP issues.
- Layout/rendering differs from expected output and accessibility snapshots are not enough.
- Performance, Lighthouse, Core Web Vitals, slow rendering, long tasks, memory, or bundle/runtime regressions matter.
- A Playwright validation flow fails and the cause is unclear.

## Debug Workflow

1. Reproduce with Playwright when possible: navigate, perform the minimal failing flow, capture screenshot and snapshot under `browser/`.
2. Inspect with Chrome DevTools: console messages, network requests, DOM/runtime state, layout/computed styles, screenshots, performance trace, Lighthouse, or memory snapshot as relevant.
3. Classify the failure: code bug, data/API issue, config issue, environment issue, flaky timing, browser compatibility, design mismatch, or test expectation issue.
4. Trace back to source files with Serena/code tools and implement the smallest correct fix.
5. Re-run Playwright validation for the affected flow.
6. Re-check Chrome DevTools evidence if the issue involved console, network, runtime, layout, or performance.
7. Clean `browser/` artifacts unless the owner asks to keep evidence.

## Chrome DevTools Evidence

Collect only evidence that matters:

- Console: errors, warnings, stack traces, source file hints.
- Network: failed requests, status codes, response shape, payload mismatch, cache/redirect/CORS/CSP problems.
- DOM/runtime: rendered state, computed values, hydration/runtime state, script execution.
- Layout: bounding boxes, overflow, scroll containers, computed style, media query behavior.
- Performance: Lighthouse, trace, long tasks, layout shifts, slow network/CPU behavior.
- Memory: snapshots only when leaks, retained objects, or runaway growth are plausible.

## Playwright Revalidation

Use Playwright after fixes to prove:

- The original failing flow now works.
- Important visual states render correctly.
- Assertions pass for visible text/elements/form values.
- No new console/network/runtime failure is visible for the checked path.

## Artifact Rule

All screenshots, traces, videos, PDFs, and temporary browser evidence must be written under `browser/`.

Do not commit these artifacts. If the final answer needs evidence, mention filenames and observations. Delete artifacts after the task unless the owner explicitly asks to keep them.

## Output

For debugging work, report in Russian:

- `Reproduction`: exact browser steps and whether Playwright reproduced the issue.
- `Evidence`: console/network/runtime/layout/performance facts from Chrome DevTools.
- `Root cause`: file/path/symbol and why it caused the issue.
- `Fix`: what changed.
- `Revalidation`: Playwright and Chrome DevTools checks after the fix.
- `Residual risks`: unavailable environment, untested browsers, missing credentials, or flaky external dependency.
