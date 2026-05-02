---
name: ry-review
description: "Report-only deep review of diff, PR, or scope with research and reviewer tracks. Use for ry-review, review, audit diff, проверь реализацию, сделай ревью, найди проблемы."
---

# ry-review

## Purpose

Find real issues before merge or deploy. Default mode is report-only: do not edit files unless the user explicitly asks after seeing findings.

## Workflow

1. Determine review target: current diff, branch vs main, PR, file scope, or prompt scope.
2. Initialize missing context with `ry-init` if needed.
3. Use Serena to map changed symbols and affected integration graph.
4. Use `rldyour-explore` for current implementation best practices when the review depends on external technology behavior.
5. Run reviewer tracks. Use subagents when the review request or `ry-start` review phase calls for parallel review.
6. Consolidate findings by severity and confidence. Validate uncertain findings with code evidence.
7. Output Russian report with exact paths, impact, suggested fixes, and whether each finding is must-fix.

## Reviewer Tracks

Read `references/reviewer-protocol.md`. These tracks are orchestrated by `ry-review` or `ry-start`; they are not broad implicit-entry skills.

- `flow-architecture-review`
- `flow-quality-review`
- `flow-consistency-review`
- `flow-integration-review`
- `flow-verification-review`
- `flow-security-review` when sensitive or requested
