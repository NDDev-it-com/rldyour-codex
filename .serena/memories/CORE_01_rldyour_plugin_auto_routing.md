<!-- Memory Metadata
Last updated: 2026-05-08
Last commit: 260345a docs: record runtime consistency fixes
Scope: plugins/rldyour-flow, plugins/rldyour-explore, plugins/rldyour-serena-mcp, plugins/rldyour-rules, plugins/rldyour-*, AGENTS.md, system/AGENTS.md, scripts/validate_marketplace.sh, scripts/validate_skill_routing.py, config/skill-routing-policy.json, scripts/smoke_mcp_runtime.sh, scripts/smoke_hooks.sh, scripts/smoke_fullrepo_sync.sh, scripts/sync_fullrepo_branch.sh, ${CODEX_HOME:-$HOME/.codex}/config.toml
Area: CORE
-->

# CORE_01_rldyour_plugin_auto_routing

## Purpose

Keep the current routing contract for the rldyour marketplace: active plugins, automatic skill selection inputs, and validation gates that keep runtime behavior aligned with repository state.

## Source-of-Truth

- `.agents/plugins/marketplace.json`
- `config/skill-routing-policy.json`
- `scripts/validate_skill_routing.py`
- `scripts/validate_marketplace.sh`
- `plugins/*/.codex-plugin/plugin.json`
- `plugins/*/skills/*/SKILL.md`
- `plugins/*/skills/*/agents/openai.yaml`

## Current Topology

- Active plugins: `rldyour-mcps`, `rldyour-explore`, `rldyour-serena-mcp`, `rldyour-security`, `rldyour-browser`, `rldyour-design`, `rldyour-lsps`, `rldyour-flow`, `rldyour-rules`.
- `rldyour-mcps` is MCP transport only (`.mcp.json`), no callable skills.
- All other listed plugins are workflow plugins and define skills via `skills/*/SKILL.md`.
- Current callable skill count: `38`.

## Automatic Routing Behavior

- The primary routing signal is each skill frontmatter `description` in `SKILL.md`.
- `scripts/validate_marketplace.sh` enforces:
  - valid frontmatter,
  - unique descriptions,
  - description length <= 240,
  - presence of Cyrillic + Latin triggers,
  - and valid `agents/openai.yaml` metadata.
- `scripts/validate_skill_routing.py` enforces the 10 policy cases in `config/skill-routing-policy.json`.

## Implicit Invocation Policy

- Default: `policy.allow_implicit_invocation: true`.
- Orchestrator-only exceptions remain the six Flow review skills:
  - `flow-architecture-review`
  - `flow-consistency-review`
  - `flow-integration-review`
  - `flow-quality-review`
  - `flow-security-review`
  - `flow-verification-review`
- These are set to `false` and are intended to be invoked by `ry-start`/`ry-review`.

## Plugin Boundaries (routing relevance)

- `rldyour-mcps` supplies transport definitions for `serena`, `playwright`, `chrome-devtools`, `context7`, `deepwiki`, `grep`, `semgrep`, `shadcn`, `dart-flutter`, `figma`, `openaiDeveloperDocs`, and `sequential-thinking`.
- `rldyour-flow` and `rldyour-serena-mcp` are the only domain plugins with hooks (`hooks.json`).
- `rldyour-rules` is advisory policy and has no hooks.
- `rldyour-lsps` is the LSP workflow boundary and includes explicit health-check/setup/Serena-mapping skills.

## Verification Commands

- `python3 scripts/validate_skill_routing.py`
- `scripts/validate_marketplace.sh` (primary gate; includes JSON, skill routing, market metadata, OpenAI metadata, scripts, LSP health, and plugin cache checks)
- `diff -qr plugins/<plugin> ${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/<plugin>/local` after any plugin edit
