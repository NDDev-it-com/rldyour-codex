# rldyour-browser

`rldyour-browser` is a skills-only browser workflow plugin for Codex.

It does not configure MCP servers directly. Browser automation is restricted to
two managed providers:

- Playwright CLI handles low-level browser flow validation, screenshots, snapshots, traces, headed sessions, responsive matrices, and post-fix proof.
- Chrome DevTools MCP handles console, network, runtime, layout, performance, memory, Lighthouse, and live Chrome debugging.

User-facing conversation stays in Russian unless the owner asks otherwise. Repository documentation is written in English.

## Scope

- Use managed Playwright CLI for deterministic browser evidence and
  decomposed long-horizon workflows.
- Use Chrome DevTools MCP when the task requires DevTools diagnosis or live Chrome inspection.
- Store all browser artifacts under `browser/` and do not commit them.

## Mandatory Engine And Wrapper Boundary

Before every browser action, run exactly
`$HOME/.local/bin/cloakbrowser-cdp-health`. Missing or nonzero health stops the
workflow with `NOT_PROVEN`. After successful preflight, the only providers are:

- Playwright CLI: exact `$HOME/.local/bin/playwright-cli`, without `run-code`
  or `--filename`.
- Chrome DevTools MCP: `$HOME/.local/bin/chrome-devtools-mcp` through the exact
  `/bin/sh -c 'exec "$HOME/.local/bin/chrome-devtools-mcp" --headless --isolated --no-usage-statistics --no-performance-crux'`
  transport.

This plugin routes tasks; bootstrap owns the mandatory CloakBrowser engine and
this adapter does not install provider packages. Webwright runtime, Python
Webwright, stock Chromium, Codex in-app browser, raw browser, `browser_agent`,
`node_repl`, `computer-use`,
Playwright MCP, raw Playwright, `bunx`, `npx`, direct provider packages,
alternate CDP endpoints/executables/configs, and all fallbacks are forbidden.
The boundary must fail closed; it cannot substitute another browser runtime.

The system installer also writes
`[plugins."browser@openai-bundled"] enabled = false`. If app-managed
`mcp_servers.node_repl` or `mcp_servers.computer-use` transport metadata is
present, the installer preserves that metadata but forces `enabled = false`.
These raw/in-app/computer-use surfaces are never browser fallbacks. Doctor
rejects any active or reinjected copy and requires reinstall plus a Codex
restart.

## Skills

- `browser-tool-routing`: chooses managed Playwright CLI, approved Chrome DevTools MCP, or a staged combination.
- `browser-validation`: verifies UI, visual behavior, functionality, and business logic with Playwright CLI evidence.
- `playwright-cli-validation`: low-level screenshot/snapshot/session provider workflow.
- `webwright-task`: compatibility-only route from historical prompts to the two managed providers; it never runs Webwright.
- `visual-diff-review`: Figma/photo/reference-image deviation workflow.
- `browser-debug`: Chrome DevTools MCP diagnosis with Playwright CLI reproduction when useful.

## Sources

- Playwright CLI: https://github.com/microsoft/playwright-cli
- Chrome DevTools MCP: https://github.com/ChromeDevTools/chrome-devtools-mcp
- Chrome DevTools MCP announcement: https://developer.chrome.com/blog/chrome-devtools-mcp
