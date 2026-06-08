# rldyour-browser

`rldyour-browser` is a skills-only browser workflow plugin for Codex.

It does not configure MCP servers directly. Browser automation is provider-routed:

- Webwright handles high-level long-horizon web tasks, RPA, extraction, comparison, and reusable `final_script.py` workflows.
- Playwright CLI handles low-level browser flow validation, screenshots, snapshots, traces, headed sessions, responsive matrices, and post-fix proof.
- Chrome DevTools MCP handles console, network, runtime, layout, performance, memory, Lighthouse, and live Chrome debugging.

User-facing conversation stays in Russian unless the owner asks otherwise. Repository documentation is written in English.

## Scope

- Use Webwright when the expected output is a rerunnable web workflow with `plan.md`, logs, screenshots, and `final_script.py`.
- Use Playwright CLI when the expected output is deterministic browser evidence under `browser/`.
- Use Chrome DevTools MCP when the task requires DevTools diagnosis or live Chrome inspection.
- Store all browser artifacts under `browser/` and do not commit them.

## Skills

- `browser-tool-routing`: chooses Webwright, Playwright CLI, Chrome DevTools MCP, or a staged combination.
- `browser-validation`: verifies UI, visual behavior, functionality, and business logic with Playwright CLI evidence.
- `playwright-cli-validation`: low-level screenshot/snapshot/session provider workflow.
- `webwright-task`: long-horizon reusable browser-task workflow.
- `visual-diff-review`: Figma/photo/reference-image deviation workflow.
- `browser-debug`: Chrome DevTools MCP diagnosis with Playwright CLI reproduction when useful.

## Sources

- Webwright: https://github.com/microsoft/Webwright
- Playwright CLI: https://github.com/microsoft/playwright-cli
- Chrome DevTools MCP: https://github.com/ChromeDevTools/chrome-devtools-mcp
- Chrome DevTools MCP announcement: https://developer.chrome.com/blog/chrome-devtools-mcp
