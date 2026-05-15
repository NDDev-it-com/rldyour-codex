<!-- Memory Metadata
Last updated: 2026-05-16
Last commit: 1132859 feat(serena): harden codex memory sync brain
Scope: plugins/rldyour-rules, AGENTS.md, system/AGENTS.md, scripts/validate_marketplace.sh, scripts/validate_instruction_docs.py
Area: RULES
-->

# RULES-01-QUALITY-FIRST

## Purpose

`rldyour-rules` owns quality-first engineering policy for this Codex marketplace: implementation discipline, architecture boundaries, dependency compatibility, verification gates, project-instruction policy, and rules review.

## Source Of Truth

- `plugins/rldyour-rules/skills/quality-first-engineering/SKILL.md`: no hacks/technical-debt policy.
- `plugins/rldyour-rules/skills/implementation-discipline/SKILL.md`: code/API/schema/config/test discipline.
- `plugins/rldyour-rules/skills/architecture-boundaries/SKILL.md`: FSD/VSA/clean architecture boundaries.
- `plugins/rldyour-rules/skills/dependency-compatibility-policy/SKILL.md`: source-backed dependency policy.
- `plugins/rldyour-rules/skills/verification-quality-gates/SKILL.md`: matching checks before delivery.
- `plugins/rldyour-rules/skills/project-instructions-policy/SKILL.md`: durable docs and ADR policy.
- `plugins/rldyour-rules/skills/ry-rules-review/SKILL.md`: rules-focused review.
- `AGENTS.md` and `system/AGENTS.md`: project/global enforcement instructions.

## Entry Points

- `$quality-first-engineering`: apply clean/scalable/no-hack policy.
- `$implementation-discipline`: implementation rules for code/config/tests.
- `$architecture-boundaries`: layer/import/public API boundaries.
- `$dependency-compatibility-policy`: current source-backed dependency changes.
- `$verification-quality-gates`: choose and run relevant checks.
- `$project-instructions-policy`: maintain durable docs.
- `$ry-rules-review`: audit against rldyour rules.

## Current Behavior

- Quality and correctness have higher priority than speed.
- Code/config/scripts/tests are source of truth; docs and memories must reflect verified behavior.
- Dependencies should be current, compatible, and source-backed; do not upgrade blindly.
- Browser-visible changes require browser validation when feasible.
- Security-sensitive work applies OWASP-oriented guidance and review when requested or risk-bearing.
- After meaningful durable changes, synchronize Serena memories and instruction docs before final sync.

## Contracts And Data

- No hardcoded secrets or raw credentials.
- No swallowed errors; handle boundary errors with meaningful messages.
- No fake green checks; blocked checks must be reported.
- Comments explain why, not obvious what.
- Prefer focused behavior tests and edge cases; mock only external services.

## Invariants

- Do not revert user changes unless explicitly requested.
- Do not use destructive git commands without clear explicit request.
- Keep edits scoped to the task and surrounding patterns.
- Keep agent-only context out of normal branches and publish it through `fullrepo`.

## Change Rules

- When rules change, update relevant skill docs, `AGENTS.md`/`system/AGENTS.md` if durable, and route tests if trigger behavior changes.
- When validation gates change, update `RELEASE-01-VALIDATION.md` and marketplace validation.

## Verification

- `scripts/validate_marketplace.sh`: main gate.
- `python3 scripts/validate_instruction_docs.py --require-agent-docs`: instruction docs gate.
- Task-specific tests/lint/types/browser/security checks chosen by touched scope.
