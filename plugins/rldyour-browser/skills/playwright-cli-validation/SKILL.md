---
name: playwright-cli-validation
description: "Низкоуровневая browser automation через Playwright CLI. Используй для: screenshots, snapshots, headed sessions, traces, responsive, UI proof. EN triggers: Playwright CLI validation, screenshots, snapshots, traces."
---

# Playwright CLI Validation

Use Playwright CLI for deterministic browser control and evidence:

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

- Named sessions: `PLAYWRIGHT_CLI_SESSION` or the exact managed CLI path plus
  `-s=<session>`.
- Screenshots, snapshots, traces, and temporary outputs under `browser/`.
- Desktop/mobile viewport proof for UI-visible changes.
- Managed CLI `show --annotate` for human-visible headed inspection when useful.
- `NOT_PROVEN` instead of invented evidence when runtime is unavailable.

```bash
$HOME/.local/bin/cloakbrowser-cdp-health
$HOME/.local/bin/playwright-cli --help
$HOME/.local/bin/cloakbrowser-cdp-health
$HOME/.local/bin/playwright-cli -s="${RY_PROJECT_SLUG:-rldyour}" open "$URL"
$HOME/.local/bin/cloakbrowser-cdp-health
$HOME/.local/bin/playwright-cli -s="${RY_PROJECT_SLUG:-rldyour}" snapshot
$HOME/.local/bin/cloakbrowser-cdp-health
$HOME/.local/bin/playwright-cli -s="${RY_PROJECT_SLUG:-rldyour}" screenshot
```
