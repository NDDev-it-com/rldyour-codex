---
name: browser-debug
description: "Отлаживает browser-only failures через Chrome DevTools MCP и Playwright CLI. Используй для: консоль, сеть, runtime, layout, memory, performance, Lighthouse. EN triggers: browser debug, console, network, runtime, performance."
---

# Browser Debug

Diagnose browser-only failures with runtime evidence. Chrome DevTools MCP is the primary provider for console/network/runtime/performance/memory/Lighthouse and live Chrome inspection. Webwright does not replace Chrome DevTools MCP.

Workflow:

1. Reproduce with Playwright CLI when deterministic flow evidence or screenshots are needed.
2. Inspect console, network, runtime state, DOM/layout, performance traces, Lighthouse, and memory/heap data with Chrome DevTools MCP.
3. Fix the root cause.
4. Revalidate with Playwright CLI, then repeat Chrome DevTools MCP checks for runtime, network, performance, or memory defects.

Use Webwright for reusable long-horizon web tasks, not for DevTools diagnosis.
