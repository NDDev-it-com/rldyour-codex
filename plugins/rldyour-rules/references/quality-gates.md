# Verification And Quality Gates

## General Gates

Run the checks that match the touched stack and risk:

- Type checking.
- Linting.
- Unit tests.
- Integration tests.
- E2E tests.
- Build.
- Formatting checks when project-standard.
- Generated artifact checks.
- Migration checks.
- Security checks.
- Browser checks for UI-visible work.
- Deploy checks for server changes.

## Evidence Rules

- Report exact commands and outcomes.
- If checks cannot run, report the blocker and residual risk.
- Do not claim confidence as a substitute for checks.
- Do not ignore warnings that indicate broken contracts, stale generated files, missing migrations, or unsafe behavior.

## Review Focus

Before finalizing, verify:

- Design fits the system.
- Functionality satisfies user and developer needs.
- Complexity is not higher than necessary.
- Tests would fail if behavior breaks.
- Names communicate domain meaning.
- Comments explain why, not what.
- Style follows project standards.
- Changed docs match changed behavior.
- Every human-written line in the touched scope is understood.
- The change improves or preserves overall code health.

