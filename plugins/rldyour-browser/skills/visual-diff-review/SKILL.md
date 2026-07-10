---
name: visual-diff-review
description: "Проводит visual QA для Figma, screenshots и reference images. Используй для: pixel-perfect, сравни с Figma, сравни с фото, diff. EN triggers: visual diff, pixel-perfect, compare Figma, reference image."
---

# Visual Diff Review

Use this workflow for pixel-perfect checks, Figma parity, screenshot comparisons, or photo/reference-image comparisons.

## Mandatory CloakBrowser Boundary

Before every browser action, execute exactly
`$HOME/.local/bin/cloakbrowser-cdp-health`. If the command is missing or exits
nonzero, stop immediately and report `NOT_PROVEN`.

After a successful preflight, use only:

- Exact `$HOME/.local/bin/playwright-cli`; never use `run-code` or `--filename`.
- Chrome DevTools MCP only when its managed-wrapper transport is exactly
  `/bin/sh -c 'exec "$HOME/.local/bin/chrome-devtools-mcp" --headless --isolated --no-usage-statistics --no-performance-crux'`.

Never use a Webwright runtime (including Python Webwright), stock Browser, raw
Browser, in-app Browser, `browser_agent`, `node_repl`, `computer-use`,
Playwright MCP, raw Playwright, `bunx`, `npx`, direct provider packages,
alternate CDP endpoints, alternate executables, alternate configs, or any
fallback. Repeat the exact health preflight before each Playwright CLI command
and before each Chrome DevTools MCP tool call.

Required evidence:

- Reference source: Figma frame export, photo, screenshot, or accepted product reference.
- actual screenshot captured with Playwright CLI under `browser/`.
- Diff image or measured deviation report.
- Responsive viewport evidence when layout is responsive.
- Chrome DevTools MCP diagnosis for computed styles, layout, network, runtime, performance, or memory when deviations require debugging.

For multi-page or reusable visual workflows, sequence preflighted managed
Playwright CLI actions; use approved Chrome DevTools MCP only for diagnosis.
