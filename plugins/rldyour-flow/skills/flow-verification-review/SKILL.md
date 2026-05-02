---
name: flow-verification-review
description: "Orchestrated verification review for ry-start/ry-review. Use explicitly for tests, quality gates, browser/server evidence; триггеры: проверь тесты, проверки."
---

# Flow Verification Review

Review whether the implementation has enough automated and manual verification:

- Tests exist for new public behavior and critical paths.
- Edge cases and error paths are covered.
- LSP/type/lint/project checks are appropriate.
- Browser validation exists for UI-visible work.
- Server/deploy evidence exists for deployment changes.

Do not run destructive tests or modify files. Report missing evidence and exact checks to add.
