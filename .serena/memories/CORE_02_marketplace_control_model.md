<!-- Memory Metadata
Last updated: 2026-05-02
Last commit: 7f53801 chore(codex): add marketplace validation instructions
Scope: README.md, AGENTS.md, scripts/validate_marketplace.sh, .agents/plugins/marketplace.json, plugins/*/.codex-plugin/plugin.json, .gitignore, /Users/rldyourmnd/.codex/config.toml
Area: CORE
-->

# CORE_02_marketplace_control_model

## Purpose

This repository is a personal Codex marketplace named `rldyour-codex`. It is a controlled catalog for the owner's own plugins, MCP servers, skills, hooks, rules, and workflows. It is not a generic preset and does not treat anything as enabled or correct unless the owner explicitly decides it.

## Source Of Truth

- `README.md`: owner-facing control model, active catalog, planned plugin architecture, plugin creation rules, and local installation command.
- `AGENTS.md`: concise Codex project instructions loaded for repository work.
- `scripts/validate_marketplace.sh`: reusable full marketplace validation command.
- `.agents/plugins/marketplace.json`: active installable plugin catalog and plugin order.
- `plugins/<plugin>/.codex-plugin/plugin.json`: per-plugin manifest, linked capabilities, and plugin interface metadata.
- `.gitignore`: repository-level ignored runtime artifacts, browser evidence, env files, and Serena runtime state.
- `/Users/rldyourmnd/.codex/config.toml`: active local marketplace registration and enabled plugin list for system Codex.

## Entry Points

- `codex plugin marketplace add .`: registers this repository as the local marketplace.
- `.agents/plugins/marketplace.json`: active plugin list consumed by Codex marketplace tooling.
- `plugins/<plugin>/.codex-plugin/plugin.json`: manifest used by Codex to discover skills, MCP servers, hooks, and metadata.

## Current Behavior

The active marketplace contains nine plugins in this order:

- `rldyour-mcps`: Developer Tools, `AVAILABLE`, `ON_USE`, source path `./plugins/rldyour-mcps`.
- `rldyour-explore`: Research, `AVAILABLE`, `ON_USE`, source path `./plugins/rldyour-explore`.
- `rldyour-serena-mcp`: Developer Tools, `AVAILABLE`, `ON_USE`, source path `./plugins/rldyour-serena-mcp`.
- `rldyour-security`: Security, `AVAILABLE`, `ON_USE`, source path `./plugins/rldyour-security`.
- `rldyour-browser`: Developer Tools, `AVAILABLE`, `ON_USE`, source path `./plugins/rldyour-browser`.
- `rldyour-design`: Design, `AVAILABLE`, `ON_USE`, source path `./plugins/rldyour-design`.
- `rldyour-lsps`: Developer Tools, `AVAILABLE`, `ON_USE`, source path `./plugins/rldyour-lsps`.
- `rldyour-flow`: Developer Tools, `AVAILABLE`, `ON_USE`, source path `./plugins/rldyour-flow`.
- `rldyour-rules`: Developer Tools, `AVAILABLE`, `ON_USE`, source path `./plugins/rldyour-rules`.

Created plugins are listed in the active catalog. Planned plugins stay documented in `README.md` and are not added to `marketplace.json` until explicitly created.

Root `AGENTS.md` exists and records durable project instructions for Codex: language policy, source-of-truth paths, plugin boundaries, development rules, validation commands, cache sync, memory sync, and git workflow.

System Codex has this marketplace registered as a local source:

- `marketplaces.rldyour-codex.source_type`: `local`.
- `marketplaces.rldyour-codex.source`: `/Users/rldyourmnd/Desktop/codex_base/rldyour-codex`.
- Enabled rldyour plugins: `rldyour-mcps`, `rldyour-explore`, `rldyour-serena-mcp`, `rldyour-security`, `rldyour-browser`, `rldyour-design`, `rldyour-lsps`, `rldyour-flow`, and `rldyour-rules`.
- External curated plugins also enabled in system Codex: `github@openai-curated` and `gmail@openai-curated`.

## Contracts And Data

Marketplace root metadata:

- `name`: `rldyour-codex`.
- `interface.displayName`: `rldyour Codex`.
- Each plugin entry must keep `name`, `source.source`, `source.path`, `policy.installation`, `policy.authentication`, and `category`.
- Current plugin entries use `policy.installation: AVAILABLE` and `policy.authentication: ON_USE`.

Plugin manifests use `.codex-plugin/plugin.json`. Current plugin capability boundaries:

- Workflow plugins expose `skills: "./skills/"`.
- `rldyour-mcps` exposes `mcpServers: "./.mcp.json"` and no skills.
- `rldyour-serena-mcp` exposes `skills: "./skills/"` and `hooks: "./hooks.json"`.
- `rldyour-lsps` exposes `skills: "./skills/"` only. It does not define MCP servers, apps, or hooks.
- `rldyour-flow` exposes `skills: "./skills/"` and `hooks: "./hooks.json"`. It does not define MCP servers or apps.
- `rldyour-rules` exposes `skills: "./skills/"` only. It does not define MCP servers, apps, or hooks.

Current plugin manifest versions:

- `rldyour-mcps`: `0.1.4`.
- `rldyour-explore`: `0.1.1`.
- `rldyour-serena-mcp`: `0.1.1`.
- `rldyour-security`: `0.1.0`.
- `rldyour-browser`: `0.1.0`.
- `rldyour-design`: `0.1.0`.
- `rldyour-lsps`: `0.1.0`.
- `rldyour-flow`: `0.1.0`.
- `rldyour-rules`: `0.1.0`.

Repository documentation, plugin metadata, code comments, commits, memory files, plans, and research archives are written in English. User-facing conversation with the owner stays Russian unless requested otherwise.

`scripts/validate_marketplace.sh` is the canonical repository validation entry point. It validates marketplace JSON, plugin manifests, skill frontmatter, OpenAI skill metadata, shell scripts, Python syntax, LSP health, Serena state, Flow state, MCP registration, plugin cache sync, secret patterns, and whitespace.

## Invariants

- Do not add planned plugins to `.agents/plugins/marketplace.json` until they are actually created and ready.
- Do not store secrets, tokens, cookies, private keys, or raw credentials in this repository.
- Keep technical identifiers stable and ASCII.
- Keep each plugin's responsibility boundary explicit.
- Do not commit browser evidence or local Serena runtime/cache state.

## Change Rules

- Use `plugin-creator` guidance when adding or modifying plugin manifests or marketplace entries.
- Append new marketplace entries unless the owner explicitly asks to reorder.
- Keep `README.md` active catalog aligned with `.agents/plugins/marketplace.json`.
- Restart Codex after changing marketplace metadata, plugin manifests, hooks, skills, or `.mcp.json`.
- Re-sync changed plugin directories into the active Codex plugin cache when applying changes to the system Codex runtime.

## Verification

- `jq empty .agents/plugins/marketplace.json plugins/*/.codex-plugin/plugin.json`: validates marketplace and plugin manifests.
- `scripts/validate_marketplace.sh`: runs the full reusable marketplace validation suite.
- `jq -r '.plugins[] | [.name,.category,.policy.installation,.policy.authentication,.source.path] | @tsv' .agents/plugins/marketplace.json`: shows active plugin order and policy.
- `codex plugin marketplace add .`: registers or confirms this marketplace.
- `codex mcp list`: verifies runtime MCP registrations after marketplace/plugin changes are installed.
- `git status -sb --ignored`: verifies only expected ignored Serena runtime files remain untracked.
