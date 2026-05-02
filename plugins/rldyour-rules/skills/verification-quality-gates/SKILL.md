---
name: verification-quality-gates
description: "Verification and quality gate rules for Codex. Use automatically before finalizing code changes, reviews, refactors, dependency updates, browser-visible work, security-sensitive work, design work, deploy work, tests, lint, type checks, LSP diagnostics, проверки, тесты, линтер, типы, качество, browser check, security check."
---

# Verification Quality Gates

## Purpose

Finish work with real evidence, not assumptions. Verification should match the change type and risk.

## Gate Selection

- Run project-native tests, type checks, linters, format checks, and build checks that apply to touched code.
- Use `rldyour-lsps` for language-server routing and diagnostics when language support matters.
- Use `rldyour-browser` for frontend, UI-visible, browser behavior, responsive, visual, and business-flow changes.
- Use `rldyour-security` for auth, authorization, input/output handling, secrets, file handling, dependency/config, payment, admin, or external integration changes.
- Use `rldyour-design` for Figma, shadcn/ui, ReactBits, design tokens, FSD frontend placement, and design-system changes.
- Use `rldyour-flow` post-task sync when changes should be committed, pushed, documented, or memory-synchronized.

## No Fake Green

- If a check passes, report the exact command or evidence.
- If a check fails, fix root cause or report the blocker.
- If a check cannot run, state why and what risk remains.
- Do not replace missing verification with confidence language.

Read `references/quality-gates.md` for the full checklist.

