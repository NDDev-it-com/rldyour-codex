---
name: browser-tool-routing
description: "Маршрутизирует browser tasks между Webwright, Playwright CLI и Chrome DevTools MCP. Используй для: браузер, UI, визуально, скриншот, Figma, фото, консоль, сеть, перфоманс, Lighthouse. EN triggers: browser tool routing, UI validation, screenshots, visual QA, console, network, performance."
---

# Browser Tool Routing

Choose the provider before browser work:

- Webwright: high-level long-horizon web tasks, reusable scripts, RPA, extraction, comparison, and evidence-first workflows.
- Playwright CLI: low-level browser flow validation, deterministic screenshots, snapshots, headed sessions, traces, console/request checks, and final UI proof.
- Chrome DevTools MCP: console/network/runtime/performance/memory/Lighthouse debugging and live Chrome inspection.

RU triggers: проверь UI, проверь в браузере, визуально, pixel-perfect, сравни с Figma, сравни с фото, скриншот, консоль, сеть, перфоманс, Lighthouse.
EN triggers: validate UI, browser check, visual QA, pixel-perfect, compare with Figma, compare with reference image, screenshot, console, network, performance, Lighthouse.

Use Webwright for long-horizon web task execution and reusable `final_script.py` workflows. Use Playwright CLI for low-level browser flow validation, screenshot capture under `browser/`, snapshots, responsive matrices, and post-fix proof. Use Chrome DevTools MCP for console, network, runtime, layout, performance, memory, Lighthouse, and live Chrome debugging.

For unknown browser defects, reproduce with Playwright CLI first and then diagnose with Chrome DevTools MCP when runtime evidence is relevant.
