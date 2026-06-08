---
name: webwright-task
description: "Запускает Webwright для длинных web tasks, RPA и воспроизводимых browser workflows. Используй для: найти, сравнить, выгрузить, повторить, reusable script. EN triggers: Webwright task, long-horizon web task, RPA, extraction, final_script.py."
---

# Webwright Task

Use Webwright for high-level long-horizon browser tasks and reusable web workflows. The release-grade install path is a pinned Webwright checkout from Microsoft GitHub.

Expected outputs:

- `plan.md` for task intent and steps.
- Screenshots and logs as evidence.
- `final_script.py` for the rerunnable workflow.
- `NOT_PROVEN` when the pinned Webwright checkout or browser runtime is unavailable.

Use Playwright CLI for low-level browser control or screenshots. Use Chrome DevTools MCP for runtime, network, performance, memory, or Lighthouse debugging.
