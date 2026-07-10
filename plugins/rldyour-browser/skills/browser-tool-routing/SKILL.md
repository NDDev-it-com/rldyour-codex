---
name: browser-tool-routing
description: "Маршрутизирует browser tasks только через managed Playwright CLI и Chrome DevTools MCP. Используй для: UI, визуально, скриншот, Figma, консоль, сеть, перфоманс. EN triggers: browser routing, UI validation, screenshots, visual QA, console, network."
---

# Browser Tool Routing

Choose the allowed provider before browser work:

- Playwright CLI: low-level browser flow validation, deterministic screenshots, snapshots, headed sessions, traces, console/request checks, and final UI proof.
- Chrome DevTools MCP: console/network/runtime/performance/memory/Lighthouse debugging and live Chrome inspection.

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

This boundary must fail closed: stock Chromium, the in-app browser, and every
raw browser path are forbidden.

- The compatibility skill `webwright-task` routes old prompts into these two
  managed providers and never runs Webwright.
- The Codex system config must keep `browser@openai-bundled`, `node_repl`, and
  `computer-use` on `enabled = false`. If one becomes active, stop browser work,
  rerun the system installer, restart Codex, and revalidate with doctor.

RU triggers: проверь UI, проверь в браузере, визуально, pixel-perfect, сравни с Figma, сравни с фото, скриншот, консоль, сеть, перфоманс, Lighthouse.
EN triggers: validate UI, browser check, visual QA, pixel-perfect, compare with Figma, compare with reference image, screenshot, console, network, performance, Lighthouse.

Use managed Playwright CLI for browser flow validation, screenshot capture
under `browser/`, snapshots, responsive matrices, long-horizon workflows, and
post-fix proof. Use approved Chrome DevTools MCP for console, network, runtime,
layout, performance, memory, Lighthouse, and live Chrome debugging.

Decision tree:

1. If the user asks for a long-horizon web task, extraction, comparison,
   booking/search flow, export, or reusable procedure, use managed Playwright
   CLI actions.
2. If the user asks to validate UI, reproduce clicks/forms, capture screenshots,
   compare Figma/photo/screenshot, or prove final UI state, use managed
   Playwright CLI.
3. If the user asks for console, network, runtime exception, computed style,
   layout debug, Lighthouse, performance, memory, or live Chrome inspection,
   use approved Chrome DevTools MCP.
4. If the browser issue is unknown, reproduce with managed Playwright CLI first,
   then diagnose with approved Chrome DevTools MCP when runtime evidence is
   relevant.
5. Never use a browser-control MCP surface for Playwright; the approved provider
   is the exact managed Playwright CLI executable.

For unknown browser defects, reproduce with Playwright CLI first and then diagnose with Chrome DevTools MCP when runtime evidence is relevant.
