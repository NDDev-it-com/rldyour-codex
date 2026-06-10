---
name: ry-rules-review
description: "Аудит реализации против rldyour rules. Используй для: /rldyour-rules:ry-rules-review, проверь по правилам, аудит правил, проверь жесткие правила, качество по правилам. EN triggers: rules review, hard rules audit, check against rules, rldyour rules check, policy compliance audit, rules audit."
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
