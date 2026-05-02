# rldyour-rules

`rldyour-rules` is the owner's quality-first engineering rule layer for Codex.

It does not configure MCP servers or hooks. MCP transports come from `rldyour-mcps`; workflow execution comes from `rldyour-flow`; code intelligence comes from `rldyour-serena-mcp`.

## Skills

- `quality-first-engineering`: default quality and no-compromise engineering policy.
- `architecture-boundaries`: frontend/client FSD and backend VSA default architecture rules.
- `implementation-discipline`: code synchronization, reuse, error handling, and no-entropy implementation rules.
- `dependency-compatibility-policy`: latest-compatible dependency and technology selection rules.
- `verification-quality-gates`: quality gate selection and no-fake-green policy.
- `project-instructions-policy`: `AGENTS.md`, `CLAUDE.md`, `REVIEW.md`, ADR, and durable documentation rules.
- `ry-rules-review`: explicit command-style rules audit for a diff, PR, branch, or scope.

## Behavior

The plugin is advisory-first. It should guide and correct implementation in scope without blocking normal progress. Hard bans still require correction: no hacks, no temporary workarounds, no swallowed errors, no secrets, and no fake checks.

User-facing conversation stays Russian. Repository documentation, memory files, plans, research archives, code comments, and commit messages stay English.

