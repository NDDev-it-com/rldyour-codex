---
name: browser-validation
description: "Валидирует UI и сценарии через Playwright CLI evidence. Используй для: проверь UI, браузер, скриншот, регрессия, адаптив, бизнес-логика, визуально. EN triggers: validate UI, browser check, regression, responsive, screenshot."
---

# Browser Validation

Validate browser-facing work with repeatable Playwright CLI evidence. Store artifacts under `browser/` and do not commit them.

Workflow:

1. Use a named session with `PLAYWRIGHT_CLI_SESSION` or `playwright-cli -s=<session>`.
2. Open the target URL and set the relevant viewport.
3. Capture a snapshot and screenshots under `browser/`.
4. Exercise changed flows, state transitions, validation rules, loading/error/empty states, and responsive behavior.
5. Use Playwright CLI console/request commands for ordinary runtime checks.
6. Use `browser-debug` with Chrome DevTools MCP for console/network/runtime/performance/memory/Lighthouse diagnosis.
7. Re-run the same commands after fixes.

Example:

```bash
PLAYWRIGHT_CLI_SESSION="${RY_PROJECT_SLUG:-rldyour}" playwright-cli open "$URL"
playwright-cli -s="${RY_PROJECT_SLUG:-rldyour}" snapshot --filename browser/snapshot.yaml
playwright-cli -s="${RY_PROJECT_SLUG:-rldyour}" screenshot --filename browser/ui-desktop.png
playwright-cli -s="${RY_PROJECT_SLUG:-rldyour}" console error
playwright-cli -s="${RY_PROJECT_SLUG:-rldyour}" requests
```

Report exact evidence paths and mark unavailable runtime as `NOT_PROVEN` with a bounded reason.
