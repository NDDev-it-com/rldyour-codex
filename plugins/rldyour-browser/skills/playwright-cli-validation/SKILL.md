---
name: playwright-cli-validation
description: "Низкоуровневая browser automation через Playwright CLI. Используй для: screenshots, snapshots, headed sessions, traces, responsive, UI flow proof. EN triggers: Playwright CLI validation, screenshots, snapshots, headed browser, traces, responsive."
---

# Playwright CLI Validation

Use Playwright CLI for deterministic browser control and evidence:

- Named sessions: `PLAYWRIGHT_CLI_SESSION` or `playwright-cli -s=<session>`.
- Screenshots, snapshots, traces, and temporary outputs under `browser/`.
- Desktop/mobile viewport proof for UI-visible changes.
- `playwright-cli show --annotate` for human-visible headed inspection when useful.
- `NOT_PROVEN` instead of invented evidence when runtime is unavailable.

```bash
playwright-cli --help
playwright-cli -s="${RY_PROJECT_SLUG:-rldyour}" open "$URL"
playwright-cli -s="${RY_PROJECT_SLUG:-rldyour}" snapshot --filename browser/snapshot.yaml
playwright-cli -s="${RY_PROJECT_SLUG:-rldyour}" screenshot --filename browser/ui.png
```
