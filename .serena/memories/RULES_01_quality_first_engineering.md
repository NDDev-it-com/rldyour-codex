<!-- Memory Metadata
Last updated: 2026-05-02
Last commit: dbdd6ca chore(serena): record rules plugin knowledge
Scope: plugins/rldyour-rules, .agents/plugins/marketplace.json, README.md
Area: RULES
-->

# RULES_01_quality_first_engineering

## Purpose

`plugins/rldyour-rules` defines the owner's quality-first engineering policy layer for Codex. It is a skills-only plugin that guides implementation, architecture, dependency selection, verification, project instructions, and rules audits without adding MCP transports or hooks.

## Source Of Truth

- `plugins/rldyour-rules/.codex-plugin/plugin.json`: plugin manifest, skills path, interface metadata, capabilities, and marketplace-facing description.
- `plugins/rldyour-rules/skills/*/SKILL.md`: automatic trigger descriptions and concise execution rules.
- `plugins/rldyour-rules/skills/*/agents/openai.yaml`: UI metadata and `policy.allow_implicit_invocation: true` for every rules skill.
- `plugins/rldyour-rules/references/*.md`: detailed quality, architecture, dependency, verification, project-instruction, ADR, and source-backed policy.
- `plugins/rldyour-rules/README.md`: human-readable boundary and skill list.

## Entry Points

- `quality-first-engineering`: default quality policy, Sequential Thinking requirement for non-trivial decisions, low semantic entropy, source-of-truth rules, and hard bans.
- `architecture-boundaries`: FSD default for frontend/client UI and VSA default for backend, with existing project architecture as source of truth.
- `implementation-discipline`: synchronized implementation rules for affected contracts, generated artifacts, reuse, naming, errors, docs, and tests.
- `dependency-compatibility-policy`: latest-compatible dependency and technology policy using official docs, release notes, migration guides, compatibility checks, and lockfile discipline.
- `verification-quality-gates`: no-fake-green quality gate routing for tests, types, lint, build, LSP, browser, security, design, and deploy evidence.
- `project-instructions-policy`: durable `AGENTS.md`, `CLAUDE.md`, `REVIEW.md`, ADR, and repository documentation rules.
- `ry-rules-review`: explicit report-only rules audit for a diff, branch, PR, file scope, or requested implementation scope.

## Current Behavior

The plugin is advisory-first. It should guide and correct implementation inside the current scope without using a blocking hook. Hard bans still require correction in touched scope: no hacks, no temporary workarounds, no fake implementations, no swallowed errors, no secrets, and no fake green checks.

The owner chose FSD and VSA as defaults for new areas, not as mandatory rewrites of coherent existing projects. Existing project code remains the source of truth.

For non-trivial engineering decisions, the rules plugin requires structured reasoning through Sequential Thinking when available. The expected minimum pattern is understand, analyze, decide; deeper decisions should add investigation, evaluation, planning, and verification.

When serious technical debt is found outside scope, Codex should ask the owner in Russian with 2-3 concrete options before expanding scope.

`AGENTS.md` should be created or updated automatically when durable Codex project rules, setup commands, quality gates, architecture constraints, deploy contracts, or workflow guidance change. `CLAUDE.md` should be updated when it exists, when Claude Code compatibility is explicit, or when the owner asks for it.

Important architecture, technology, dependency, deployment, security, or irreversible design decisions should produce an ADR or equivalent decision record.

## Contracts And Data

User-facing conversation stays Russian. Repository docs, plugin docs, memories, plans, research archives, code comments, and commit messages stay English.

Every rules skill must keep `policy.allow_implicit_invocation: true`.

`rldyour-rules` depends behaviorally on existing plugins but does not own their runtime:

- `rldyour-serena-mcp`: code source-of-truth inspection and memory sync.
- `rldyour-explore`: current source-backed technical research.
- `rldyour-lsps`: language-server quality checks.
- `rldyour-browser`: browser-visible verification.
- `rldyour-security`: security-sensitive implementation guidance and review.
- `rldyour-design`: frontend design-system and FSD design workflows.
- `rldyour-flow`: SDLC orchestration and post-task sync.

`rldyour-rules` contains detailed reference files for policy, not just skill frontmatter:

- `references/rules-policy.md`: quality priority, no-hacks policy, technical debt scope, and Sequential Thinking policy.
- `references/architecture-policy.md`: FSD and VSA defaults plus existing-architecture preservation.
- `references/dependency-policy.md`: latest-compatible dependency selection and compatibility checks.
- `references/quality-gates.md`: evidence requirements and no-fake-green policy.
- `references/project-instructions-and-adrs.md`: `AGENTS.md`, `CLAUDE.md`, `REVIEW.md`, and ADR rules.

## Invariants

- Do not add hooks to `rldyour-rules` unless the owner explicitly asks for enforcement behavior.
- Do not duplicate MCP server definitions from `rldyour-mcps`.
- Do not store secrets, tokens, cookies, private keys, or credentials in rules docs or memories.
- Do not make FSD/VSA a forced rewrite policy for existing coherent projects.
- Do not let `AGENTS.md`, `CLAUDE.md`, `REVIEW.md`, or ADRs become chat logs, generic advice, or speculative backlog.
- Keep rules concise in `SKILL.md`; move detailed policy into `references/`.

## Change Rules

- Update `references/rules-policy.md` when changing global quality priority, hard bans, technical debt policy, or Sequential Thinking policy.
- Update `references/architecture-policy.md` when changing FSD/VSA placement rules.
- Update `references/dependency-policy.md` when changing dependency or compatibility rules.
- Update `references/quality-gates.md` when changing verification evidence rules.
- Update `references/project-instructions-and-adrs.md` when changing `AGENTS.md`, `CLAUDE.md`, `REVIEW.md`, or ADR behavior.
- Keep `README.md`, `plugin.json`, `SKILL.md` descriptions, and `agents/openai.yaml` aligned with automatic routing intent.
- Re-sync `plugins/rldyour-rules/` into the active Codex plugin cache after changes.

## Verification

- `jq empty plugins/rldyour-rules/.codex-plugin/plugin.json .agents/plugins/marketplace.json`: validates plugin and marketplace JSON.
- `uv run --with pyyaml python /Users/rldyourmnd/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/rldyour-rules/skills/<skill>`: validates each rules skill.
- `uv run --with pyyaml python -c '<parse agents/openai.yaml files>'`: validates `agents/openai.yaml` parse and implicit invocation.
- `rg -n 'TODO|\\[TODO|PLACEHOLDER|FIXME|HACK|ctx7sk|ghp_|github_pat|password|secret|access[_-]?token|private[_-]?key|bearer' plugins/rldyour-rules`: should show only policy text, not real credentials or placeholders.
- `diff -qr plugins/rldyour-rules /Users/rldyourmnd/.codex/plugins/cache/rldyour-codex/rldyour-rules/local`: verifies system cache matches the repository plugin.
