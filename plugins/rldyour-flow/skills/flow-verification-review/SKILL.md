---
name: flow-verification-review
description: Verification and manual testing reviewer workflow for ry-start and ry-review. Use for test coverage, quality gates, manual checks, browser/server evidence, missing tests, edge cases, проверь тесты, проверь ручные тесты, проверь quality gates, хватает ли проверок. Read-only by default and suitable for subagent prompts.
---

# Flow Verification Review

Review whether the implementation has enough automated and manual verification:

- Tests exist for new public behavior and critical paths.
- Edge cases and error paths are covered.
- LSP/type/lint/project checks are appropriate.
- Browser validation exists for UI-visible work.
- Server/deploy evidence exists for deployment changes.

Do not run destructive tests or modify files. Report missing evidence and exact checks to add.

