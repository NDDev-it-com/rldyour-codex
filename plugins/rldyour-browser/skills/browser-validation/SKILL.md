---
name: browser-validation
description: "Валидирует UI и сценарии через Playwright CLI evidence. Используй для: проверь UI, браузер, скриншот, регрессия, адаптив, бизнес-логика, визуально. EN triggers: validate UI, browser check, regression, responsive, screenshot."
---

# Browser Validation

Validate browser-facing work with repeatable Playwright CLI evidence. Store artifacts under `browser/` and do not commit them.

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

1. Use a named session with `PLAYWRIGHT_CLI_SESSION` or the exact managed CLI
   path plus `-s=<session>`.
2. Open the target URL and set the relevant viewport.
3. Capture a snapshot and screenshots under `browser/`.
4. Exercise changed flows, state transitions, validation rules, loading/error/empty states, and responsive behavior.
5. Use Playwright CLI console/request commands for ordinary runtime checks.
6. Use `browser-debug` with Chrome DevTools MCP for console/network/runtime/performance/memory/Lighthouse diagnosis.
7. Re-run the same commands after fixes.

Example:

```bash
$HOME/.local/bin/cloakbrowser-cdp-health
PLAYWRIGHT_CLI_SESSION="${RY_PROJECT_SLUG:-rldyour}" $HOME/.local/bin/playwright-cli open "$URL"
$HOME/.local/bin/cloakbrowser-cdp-health
$HOME/.local/bin/playwright-cli -s="${RY_PROJECT_SLUG:-rldyour}" snapshot
$HOME/.local/bin/cloakbrowser-cdp-health
$HOME/.local/bin/playwright-cli -s="${RY_PROJECT_SLUG:-rldyour}" screenshot
$HOME/.local/bin/cloakbrowser-cdp-health
$HOME/.local/bin/playwright-cli -s="${RY_PROJECT_SLUG:-rldyour}" console error
$HOME/.local/bin/cloakbrowser-cdp-health
$HOME/.local/bin/playwright-cli -s="${RY_PROJECT_SLUG:-rldyour}" requests
```

Report exact evidence paths and mark unavailable runtime as `NOT_PROVEN` with a bounded reason.
