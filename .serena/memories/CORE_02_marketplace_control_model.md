<!-- Memory Metadata
Last updated: 2026-05-03
Last commit: 72329c8 feat(system): add bootstrap and runtime smoke checks
Scope: README.md, AGENTS.md, system/AGENTS.md, scripts/validate_marketplace.sh, scripts/install_system_codex.sh, scripts/doctor_system_codex.sh, scripts/bootstrap_check.sh, scripts/smoke_mcp_runtime.sh, scripts/smoke_hooks.sh, pyrightconfig.json, .agents/plugins/marketplace.json, plugins/*/.codex-plugin/plugin.json, .gitignore, /Users/rldyourmnd/.codex/config.toml
Area: CORE
-->

# CORE_02_marketplace_control_model

## Purpose

This repository is a personal Codex marketplace named `rldyour-codex`. It is a controlled catalog for the owner's own plugins, MCP servers, skills, hooks, rules, and workflows. It is not a generic preset and does not treat anything as enabled or correct unless the owner explicitly decides it.

## Source Of Truth

- `README.md`: owner-facing control model, active catalog, planned plugin architecture, plugin creation rules, and local installation command.
- `AGENTS.md`: concise Codex project instructions loaded for repository work.
- `system/AGENTS.md`: canonical tracked template for the owner's global `~/.codex/AGENTS.md`.
- `scripts/validate_marketplace.sh`: reusable full marketplace validation command.
- `scripts/install_system_codex.sh`: dry-run-first installer for global Codex state.
- `scripts/doctor_system_codex.sh`: installed system Codex verification command.
- `scripts/bootstrap_check.sh`: end-to-end bootstrap smoke command.
- `scripts/smoke_mcp_runtime.sh`: installed MCP runtime smoke command.
- `scripts/smoke_hooks.sh`: repository and installed hook smoke command.
- `pyrightconfig.json`: Python script scope for this repository.
- `.agents/plugins/marketplace.json`: active installable plugin catalog and plugin order.
- `plugins/<plugin>/.codex-plugin/plugin.json`: per-plugin manifest, linked capabilities, and plugin interface metadata.
- `.gitignore`: repository-level ignored runtime artifacts, browser evidence, env files, and Serena runtime state.
- `/Users/rldyourmnd/.codex/config.toml`: active local marketplace registration, YOLO permission defaults, enabled plugin list, and MCP runtime config for system Codex.

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

`system/AGENTS.md` exists and is installed into `/Users/rldyourmnd/.codex/AGENTS.md` on the current machine. It is a compact global Codex router/policy file, not a full copy of every plugin workflow.

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

- `rldyour-mcps`: `0.1.5`.
- `rldyour-explore`: `0.1.2`.
- `rldyour-serena-mcp`: `0.1.2`.
- `rldyour-security`: `0.1.1`.
- `rldyour-browser`: `0.1.1`.
- `rldyour-design`: `0.1.1`.
- `rldyour-lsps`: `0.1.1`.
- `rldyour-flow`: `0.1.2`.
- `rldyour-rules`: `0.1.1`.

`rldyour-flow` `0.1.2` exposes deep `ry-init` context packs, `ry-start` context sufficiency gates, advisory SessionStart context, advisory PostToolUse commit advice, reviewer workflows, deployment workflow, and post-task sync.

Root `README.md` describes the active catalog, planned architecture, system install workflow, the portable MCP source-of-truth rule for `plugins/rldyour-mcps/.mcp.json`, and the owner-requested YOLO defaults applied by the installer.

Repository documentation, plugin metadata, code comments, commits, memory files, plans, and research archives are written in English. User-facing conversation with the owner stays Russian unless requested otherwise.

`scripts/validate_marketplace.sh` is the canonical repository validation entry point. It validates marketplace JSON, plugin manifests, skill frontmatter, compact bilingual routing descriptions, strict OpenAI skill metadata, MCP dependency names, shell scripts, Python syntax, LSP health, Serena state, Flow state, MCP registration, MCP config sync, MCP runtime smoke, plugin cache sync, hook smoke, secret patterns, and whitespace.

`scripts/install_system_codex.sh --dry-run` is the safe default system install preview. `scripts/install_system_codex.sh --apply` writes global Codex state with backups, including YOLO permission defaults and twelve MCP servers. `scripts/doctor_system_codex.sh` verifies installed global AGENTS, config, YOLO defaults, plugins, MCP, cache, and repository validation.

`scripts/bootstrap_check.sh --dry-run` is the non-mutating bootstrap preview. `scripts/bootstrap_check.sh --apply` is the end-to-end current-machine bootstrap smoke flow: install preview, install apply, marketplace validation, MCP runtime smoke, hook smoke, system doctor, Serena state, Flow state, and git status.

## Invariants

- Do not add planned plugins to `.agents/plugins/marketplace.json` until they are actually created and ready.
- Do not store secrets, tokens, cookies, private keys, or raw credentials in this repository.
- Keep technical identifiers stable and ASCII.
- Keep each plugin's responsibility boundary explicit.
- Keep compact Russian and English trigger phrases in each callable rldyour skill `SKILL.md` description so routing works with the owner's Russian prompts and English technical terms.
- Do not commit browser evidence or local Serena runtime/cache state.

## Change Rules

- Use `plugin-creator` guidance when adding or modifying plugin manifests or marketplace entries.
- Append new marketplace entries unless the owner explicitly asks to reorder.
- Keep `README.md` active catalog aligned with `.agents/plugins/marketplace.json`.
- Restart Codex after changing marketplace metadata, plugin manifests, hooks, skills, or `.mcp.json`.
- Re-sync changed plugin directories into the active Codex plugin cache when applying changes to the system Codex runtime.
- Use `scripts/bootstrap_check.sh --apply` when validating a full new-machine or resynced-machine setup path.

## Verification

- `jq empty .agents/plugins/marketplace.json plugins/*/.codex-plugin/plugin.json`: validates marketplace and plugin manifests.
- `scripts/validate_marketplace.sh`: runs the full reusable marketplace validation suite.
- `scripts/install_system_codex.sh --dry-run`: previews system Codex installation.
- `scripts/doctor_system_codex.sh`: validates installed system Codex state.
- `scripts/bootstrap_check.sh --apply`: validates full install and runtime smoke flow.
- `scripts/smoke_mcp_runtime.sh`: validates installed MCP runtime behavior.
- `scripts/smoke_hooks.sh`: validates repository and installed hook execution.
- `jq -r '.plugins[] | [.name,.category,.policy.installation,.policy.authentication,.source.path] | @tsv' .agents/plugins/marketplace.json`: shows active plugin order and policy.
- `codex plugin marketplace add .`: registers or confirms this marketplace.
- `codex mcp list`: verifies runtime MCP registrations after marketplace/plugin changes are installed.
- `git status -sb --ignored`: verifies only expected ignored Serena runtime files remain untracked.
