---
name: webwright-task
description: "Маршрутизирует старые Webwright-запросы в управляемые CloakBrowser workflows. Используй для: длинная web-задача, RPA, extraction. EN triggers: compatibility browser task, long-horizon web task."
---

# Webwright Task

This skill name is retained only as a compatibility route for existing prompts.
It must never start or import Webwright. Decompose long-horizon work into
managed Playwright CLI actions and approved Chrome DevTools MCP diagnostics.

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

Expected outputs:

- `plan.md` for task intent and steps.
- Screenshots and logs from preflighted managed actions as evidence.
- A command log that records the exact allowed provider used for every action.
- `NOT_PROVEN` when the managed CloakBrowser boundary is unavailable.

Use the managed Playwright CLI for browser control and screenshots. Use the
approved Chrome DevTools MCP transport for runtime, network, performance,
memory, or Lighthouse debugging.
