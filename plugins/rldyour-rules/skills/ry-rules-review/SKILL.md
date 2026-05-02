---
name: ry-rules-review
description: "Explicit rldyour rules audit command. Use automatically when the user invokes ry-rules-review, asks to review against rules, audit code quality, check architecture rules, check no hacks, check technical debt, проверить по правилам, проверь качество по правилам, аудит правил, ревью правил, hard rules review."
---

# ry-rules-review

## Purpose

Review a diff, PR, branch, file scope, or implementation against `rldyour-rules`.

## Workflow

1. Determine target: current diff, branch vs `main`, PR, file scope, or user-provided scope.
2. Use Serena-first code inspection for affected symbols and integration paths.
3. Apply `quality-first-engineering`, `architecture-boundaries`, `implementation-discipline`, `dependency-compatibility-policy`, `verification-quality-gates`, and `project-instructions-policy`.
4. Use `rldyour-explore` when the review depends on current technology behavior, dependency versions, or architecture best practices.
5. Report findings in Russian, ordered by severity and confidence.
6. Default mode is report-only. Modify files only if the user explicitly asks to fix findings.

## Finding Format

- Severity: `critical`, `high`, `medium`, `low`.
- Confidence: `0-100`.
- Location: exact file and line when possible.
- Rule: which rldyour rule is violated.
- Evidence: concrete code, config, test, or docs evidence.
- Impact: what becomes incorrect, fragile, unscalable, insecure, or harder to maintain.
- Fix: actionable correction.
- Disposition: `must-fix`, `should-fix`, `ask-user`, or `defer`.

Read `references/rules-policy.md` and only load other references when they match the reviewed issue.

