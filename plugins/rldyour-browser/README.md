# rldyour-browser

`rldyour-browser` is a skills-only browser workflow plugin for Codex.

It does not configure MCP servers directly. The Playwright MCP and Chrome DevTools MCP transports belong to `rldyour-mcps`; this plugin defines how Codex should use them.

User-facing conversation stays in Russian unless the owner asks otherwise. Repository documentation is written in English.

## Scope

- Use Playwright MCP as the primary tool for user-flow reproduction, functional checks, business-logic verification, screenshots, accessibility snapshots, storage/network/testing assertions, and pixel-perfect UI validation.
- Use Chrome DevTools MCP as the primary tool for console errors, network analysis, DOM/runtime debugging, layout inspection, Lighthouse, performance traces, and deeper browser diagnosis.
- Use both tools together when the right workflow is: reproduce with Playwright, diagnose with Chrome DevTools, then re-validate with Playwright.
- Store all browser artifacts under `browser/`.
- Treat `browser/` artifacts as temporary and ignored by git. Delete screenshots, videos, traces, PDFs, and temporary evidence after the task unless the owner explicitly asks to keep them.

## Skills

- `browser-tool-routing`: chooses Playwright, Chrome DevTools, or both based on the task.
- `browser-validation`: verifies UI, pixel-perfect behavior, functionality, and business logic in the browser.
- `browser-debug`: diagnoses runtime, console, network, layout, and performance problems through Chrome DevTools, with Playwright reproduction when useful.

## Artifact Rule

All MCP browser screenshots and related artifacts must go under `browser/`. Do not scatter screenshots into the repo root, feature folders, or plugin directories.

Ignored artifact examples:

- `browser/*.png`
- `browser/*.jpg`
- `browser/*.webp`
- `browser/*.mp4`
- `browser/*.webm`
- `browser/*.zip`
- `browser/*.trace`
- `browser/*.har`
- `browser/*.pdf`

The directory exists only as a local working area. Commit text summaries, not binary evidence, unless the owner explicitly asks otherwise.

## Sources

- Playwright MCP introduction: https://playwright.dev/mcp/introduction
- Playwright MCP capabilities: https://playwright.dev/mcp/capabilities
- Playwright MCP configuration: https://playwright.dev/mcp/configuration/options
- Chrome DevTools MCP: https://github.com/ChromeDevTools/chrome-devtools-mcp
- Chrome DevTools MCP announcement: https://developer.chrome.com/blog/chrome-devtools-mcp
