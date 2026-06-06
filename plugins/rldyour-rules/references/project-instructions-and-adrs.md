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

For default rldyour-managed product repositories, project-root `AGENTS.md` is agent-only context. Keep it local and in the `fullrepo` branch, and add it to `.git/info/exclude` through the rldyour fullrepo workflow instead of tracking it in normal branches. Project policy may explicitly set `normal_branch_policy.agent_files=allowed` or `instruction_docs.mode=tracked-normal-branch`; then `AGENTS.md` is a normal tracked project file.

## .claude/CLAUDE.md

Create or update `.claude/CLAUDE.md` in every fullrepo-managed project. This file is Claude Code project memory and must be optimized for Claude Code, not treated as a thin wrapper around `AGENTS.md`.

Include:

- Project commands and checks Claude Code should know every session.
- Project architecture, source-of-truth paths, naming conventions, and common workflows.
- Claude-specific diagnostics and controls when relevant: `/memory`, `/context`, `/hooks`, `/mcp`, `/permissions`, `/doctor`, `/status`.
- Claude-specific file locations when relevant: `.claude/settings.json`, `.claude/skills/`, `.claude/hooks/`, `.claude/agents/`.

Keep it concise and first-class. Do not make the file only `@AGENTS.md`. Do not create root `CLAUDE.md` by default; it is a legacy location in the rldyour workflow.

For default rldyour-managed product repositories, `.claude/CLAUDE.md` is agent-only context and follows the same `fullrepo` branch policy as project-root `AGENTS.md`. In tracked-normal-branch projects, it may be committed as a first-class project instruction file.

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

## Agent-Only Files And Fullrepo

Default rldyour-managed policy keeps agent-only files that reveal or preserve AI workflow state out of normal project branches. Store them locally, ignore them through `.git/info/exclude`, and publish them to the `fullrepo` branch through `rldyour-flow`. Foreign or colleague-owned repositories may opt into tracked AI instruction files through `.rldyour/project-policy.json`.

Default agent-only paths include:

- `AGENTS.md`, `.claude/CLAUDE.md`, root `CLAUDE.md` when migrating legacy projects, `REVIEW.md`, `GEMINI.md`, and `QWEN.md`.
- `.serena/project.yml`, `.serena/memories/`, `.serena/plans/`, `.serena/research/`, `.serena/newproj/`, and `.serena/deploy/`.
- `.claude/`, `.codex/`, `.cursor/rules/`, `.agents/skills/`, `.agents/commands/`, `.agents/hooks/`, `.github/instructions/`, and `.github/prompts/`.

Never publish runtime markers, caches, local env files, browser evidence, secrets, tokens, cookies, or credentials to `main` or `fullrepo`.
