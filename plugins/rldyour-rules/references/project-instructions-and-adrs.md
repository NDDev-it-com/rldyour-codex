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

Project-root `AGENTS.md` is tracked normally on `main` as ordinary source. Project policy may explicitly set `normal_branch_policy.agent_files=strict` to keep agent files out of product branches; the default `allowed` tracks `AGENTS.md` as a normal project file.

## .claude/CLAUDE.md

Create or update `.claude/CLAUDE.md` in every project. This file is Claude Code project memory and must be optimized for Claude Code, not treated as a thin wrapper around `AGENTS.md`.

Include:

- Project commands and checks Claude Code should know every session.
- Project architecture, source-of-truth paths, naming conventions, and common workflows.
- Claude-specific diagnostics and controls when relevant: `/memory`, `/context`, `/hooks`, `/mcp`, `/permissions`, `/doctor`, `/status`.
- Claude-specific file locations when relevant: `.claude/settings.json`, `.claude/skills/`, `.claude/hooks/`, `.claude/agents/`.

Keep it concise and first-class. Do not make the file only `@AGENTS.md`. Do not create root `CLAUDE.md` by default; it is a legacy location in the rldyour workflow.

`.claude/CLAUDE.md` is tracked normally on `main` as a first-class project instruction file, the same as project-root `AGENTS.md`.

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

## Agent Context On Main

Agent context is tracked normally on `main` as ordinary source, with no separate agent-only branch or overlay. A project may opt into strict agent-file protection through `.rldyour/project-policy.json` (`normal_branch_policy.agent_files=strict`); by default these files are tracked.

Agent-context paths include:

- `AGENTS.md`, `.claude/CLAUDE.md`, root `CLAUDE.md` when migrating legacy projects, `REVIEW.md`, `GEMINI.md`, and `QWEN.md`.
- `.serena/project.yml`, `.serena/memories/`, `.serena/plans/`, `.serena/research/`, `.serena/newproj/`, and `.serena/deploy/`.
- `.claude/`, `.codex/`, `.cursor/rules/`, `.agents/skills/`, `.agents/commands/`, `.agents/hooks/`, `.github/instructions/`, and `.github/prompts/`.

Never commit runtime markers, caches, local env files, browser evidence, secrets, tokens, cookies, or credentials to `main`.
