---
name: browser-debug
description: "Отлаживает browser-only failures через Chrome DevTools MCP и Playwright CLI. Используй для: консоль, сеть, runtime, layout, memory, performance, Lighthouse. EN triggers: browser debug, console, network, runtime, performance."
---

# Browser Debug

Diagnose browser-only failures with runtime evidence. Use managed Playwright CLI
for deterministic reproduction and the approved Chrome DevTools MCP transport
for console, network, runtime, performance, memory, Lighthouse, and live Chrome
inspection.

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

Workflow:

1. Reproduce with Playwright CLI when deterministic flow evidence or screenshots are needed.
2. Inspect console, network, runtime state, DOM/layout, performance traces, Lighthouse, and memory/heap data with Chrome DevTools MCP.
3. Fix the root cause.
4. Revalidate with Playwright CLI, then repeat Chrome DevTools MCP checks for runtime, network, performance, or memory defects.

For long-horizon tasks, decompose the workflow into preflighted managed
Playwright CLI actions and approved Chrome DevTools MCP diagnostics.
