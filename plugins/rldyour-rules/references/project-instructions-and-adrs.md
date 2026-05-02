# Project Instructions And ADRs

## AGENTS.md

Create or update `AGENTS.md` when durable Codex instructions change:

- Setup commands.
- Quality gates.
- Architecture constraints.
- Project-specific coding rules.
- Deploy contracts.
- Review rules.
- Tooling and generated artifact rules.

Keep it concise. Codex reads it before work, so it should contain high-signal project rules only.

## CLAUDE.md

Update `CLAUDE.md` when:

- It already exists.
- The project explicitly uses Claude Code compatibility.
- The owner asks to create or maintain it.

Do not create generic `CLAUDE.md` by default in every project.

## REVIEW.md

Create or update `REVIEW.md` when review-specific rules are durable:

- Always-check areas.
- Architecture boundaries.
- Security-sensitive paths.
- Test expectations.
- Known generated files to ignore.
- Project-specific false positives.

## ADRs

Store ADRs in the project-standard location when one exists. Otherwise prefer `docs/adr/`.

Default ADR fields:

- Title.
- Status.
- Date.
- Context.
- Decision.
- Consequences.
- Alternatives considered.
- Verification.
- Related code paths.

ADRs must capture why the decision was made and what tradeoffs future agents must preserve.

