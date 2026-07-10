---
name: browser-tool-routing
description: "Маршрутизирует browser tasks: Webwright, Playwright CLI, Chrome DevTools MCP. Используй для: UI, визуально, скриншот, Figma, консоль, сеть, перфоманс. EN triggers: browser routing, UI validation, screenshots, visual QA, console, network."
---

# Browser Tool Routing

Choose the provider before browser work:

- Webwright: high-level long-horizon web tasks, reusable scripts, RPA, extraction, comparison, and evidence-first workflows.
- Playwright CLI: low-level browser flow validation, deterministic screenshots, snapshots, headed sessions, traces, console/request checks, and final UI proof.
- Chrome DevTools MCP: console/network/runtime/performance/memory/Lighthouse debugging and live Chrome inspection.

Mandatory execution boundary:

- Webwright must run through `$HOME/.local/bin/webwright`.
- Playwright CLI must run through `$HOME/.local/bin/playwright-cli`.
- Chrome DevTools MCP must run through `$HOME/.local/bin/chrome-devtools-mcp`
  using the exact managed `/bin/sh -c` transport.
- All three bootstrap-owned wrappers must use CloakBrowser as their browser
  engine. There is no stock Chromium, Codex in-app browser, raw browser, direct
  provider-package executable, or alternate browser-engine fallback.
- If a managed wrapper or CloakBrowser health gate is unavailable, fail closed
  and report `NOT_PROVEN`; do not bypass the managed runtime.

RU triggers: проверь UI, проверь в браузере, визуально, pixel-perfect, сравни с Figma, сравни с фото, скриншот, консоль, сеть, перфоманс, Lighthouse.
EN triggers: validate UI, browser check, visual QA, pixel-perfect, compare with Figma, compare with reference image, screenshot, console, network, performance, Lighthouse.

Use Webwright for long-horizon web task execution and reusable `final_script.py` workflows. Use Playwright CLI for low-level browser flow validation, screenshot capture under `browser/`, snapshots, responsive matrices, and post-fix proof. Use Chrome DevTools MCP for console, network, runtime, layout, performance, memory, Lighthouse, and live Chrome debugging.

Decision tree:

1. If the user asks for a long-horizon web task, extraction, comparison, booking/search flow, export, or reusable script, use Webwright.
2. If the user asks to validate UI, reproduce clicks/forms, capture screenshots, compare Figma/photo/screenshot, or prove final UI state, use Playwright CLI.
3. If the user asks for console, network, runtime exception, computed style, layout debug, Lighthouse, performance, memory, or live Chrome inspection, use Chrome DevTools MCP.
4. If the browser issue is unknown, reproduce with Playwright CLI first, then diagnose with Chrome DevTools MCP when runtime evidence is relevant.
5. Never use Webwright as a DevTools replacement.
6. Never use a browser-control MCP surface for Playwright; the approved provider is Playwright CLI.
7. Never route browser work to an in-app browser, raw browser process, stock
   Chromium, or a direct provider package.

For unknown browser defects, reproduce with Playwright CLI first and then diagnose with Chrome DevTools MCP when runtime evidence is relevant.
