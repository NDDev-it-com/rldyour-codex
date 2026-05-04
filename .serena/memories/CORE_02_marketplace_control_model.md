<!-- Memory Metadata
Last updated: 2026-05-04
Last commit: 3128913 chore(mcp): update chrome devtools runtime pin
Scope: README.md, AGENTS.md, system/AGENTS.md, VERSION, CHANGELOG.md, docs, .github/workflows/validate.yml, .github/workflows/dependency-check.yml, .github/dependabot.yml, config/mcp-runtime-versions.env, config/skill-routing-policy.json, scripts/validate_marketplace.sh, scripts/validate_plugin_versions.py, scripts/validate_skill_routing.py, scripts/release_manifest.py, scripts/check_mcp_runtime_versions.py, scripts/collect_diagnostics.sh, scripts/rollback_system_codex.sh, scripts/install_system_codex.sh, scripts/doctor_system_codex.sh, scripts/bootstrap_check.sh, scripts/smoke_mcp_runtime.sh, scripts/smoke_mcp_capabilities.py, scripts/smoke_mcp_capabilities.sh, scripts/smoke_hooks.sh, scripts/smoke_clean_bootstrap.sh, scripts/smoke_fullrepo_sync.sh, scripts/sync_fullrepo_branch.sh, plugins/rldyour-flow/scripts/fullrepo_sync.py, pyrightconfig.json, .agents/plugins/marketplace.json, plugins/*/.codex-plugin/plugin.json, plugins/rldyour-mcps/.mcp.json, .gitignore, /Users/rldyourmnd/.codex/config.toml
Area: CORE
-->

# CORE_02_marketplace_control_model

## Purpose

This repository is a personal Codex marketplace named `rldyour-codex`. It is a controlled catalog for the owner's own plugins, MCP servers, skills, hooks, rules, and workflows. It is not a generic preset and does not treat anything as enabled or correct unless the owner explicitly decides it.

## Source Of Truth

- `README.md`: owner-facing control model, active catalog, planned plugin architecture, plugin creation rules, and local installation command.
- `AGENTS.md`: concise Codex project instructions loaded for repository work.
- `system/AGENTS.md`: canonical tracked template for the owner's global `~/.codex/AGENTS.md`.
- `VERSION`: marketplace release version.
- `CHANGELOG.md`: human-readable marketplace release history.
- `docs/release-process.md`: release/versioning procedure.
- `docs/rollback-restore.md`: first-class rollback and restore workflow.
- `docs/dependency-updates.md`: pinned MCP runtime update policy.
- `docs/observability.md`: diagnostics and failure-triage model.
- `scripts/validate_marketplace.sh`: reusable full marketplace validation command.
- `scripts/validate_plugin_versions.py`: SemVer, release document, marketplace, and plugin manifest version validation.
- `scripts/validate_skill_routing.py`: deterministic Russian/English prompt routing policy validation.
- `scripts/release_manifest.py`: machine-readable release snapshot generator.
- `scripts/check_mcp_runtime_versions.py`: upstream freshness check for pinned MCP/Codex runtime packages.
- `scripts/collect_diagnostics.sh`: local sanitized diagnostics bundle collector.
- `scripts/rollback_system_codex.sh`: read-only-by-default backup listing and explicit restore command for system Codex files.
- `scripts/install_system_codex.sh`: dry-run-first installer for global Codex state.
- `scripts/doctor_system_codex.sh`: installed system Codex verification command.
- `scripts/bootstrap_check.sh`: end-to-end bootstrap smoke command.
- `scripts/smoke_mcp_runtime.sh`: installed MCP runtime smoke command.
- `scripts/smoke_mcp_capabilities.sh`: MCP initialize, list-tools, and safe call-tool smoke command.
- `scripts/smoke_hooks.sh`: repository and installed hook smoke plus lifecycle smoke command.
- `scripts/smoke_clean_bootstrap.sh`: committed clean-clone bootstrap smoke command.
- `scripts/smoke_fullrepo_sync.sh`: fullrepo branch publish, migrate-main, restore, and exclude-rule smoke command.
- `scripts/sync_fullrepo_branch.sh`: operational fullrepo status, restore, publish, and migration wrapper.
- `plugins/rldyour-flow/scripts/fullrepo_sync.py`: canonical fullrepo sync implementation for agent-only files.
- `config/mcp-runtime-versions.env`: pinned runtime package versions for reproducible MCP startup and CI.
- `config/skill-routing-policy.json`: prompt-to-skill routing policy test fixture.
- `.github/workflows/validate.yml`: Ubuntu/macOS CI workflow for validation on push, pull request, and manual dispatch.
- `.github/workflows/dependency-check.yml`: scheduled and manual MCP runtime pin freshness workflow.
- `.github/dependabot.yml`: GitHub Actions update checks.
- `pyrightconfig.json`: Python script scope for this repository.
- `.agents/plugins/marketplace.json`: active installable plugin catalog and plugin order.
- `plugins/<plugin>/.codex-plugin/plugin.json`: per-plugin manifest, linked capabilities, and plugin interface metadata.
- `.gitignore`: repository-level ignored runtime artifacts, browser evidence, env files, and Serena runtime state.
- `/Users/rldyourmnd/.codex/config.toml`: active local marketplace registration, YOLO permission defaults, enabled plugin list, and MCP runtime config for system Codex.

## Entry Points

- `codex plugin marketplace add .`: registers this repository as the local marketplace.
- `.agents/plugins/marketplace.json`: active plugin list consumed by Codex marketplace tooling.
- `plugins/<plugin>/.codex-plugin/plugin.json`: manifest used by Codex to discover skills, MCP servers, hooks, and metadata.
- `scripts/sync_fullrepo_branch.sh --restore`: restores complete agent-only context from `origin/fullrepo` during initialization.
- `scripts/sync_fullrepo_branch.sh --publish`: publishes complete agent-only context after normal branch sync.

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

The GitHub repository is `rldyourmnd/rldyour-codex`, private, with default branch `main`. Commit `018cc6e` added the generated `fullrepo` branch workflow for complete agent-only context snapshots.

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
- `rldyour-serena-mcp`: `0.2.1`.
- `rldyour-security`: `0.1.1`.
- `rldyour-browser`: `0.1.1`.
- `rldyour-design`: `0.1.1`.
- `rldyour-lsps`: `0.1.1`.
- `rldyour-flow`: `0.2.1`.
- `rldyour-rules`: `0.1.3`.

`rldyour-flow` `0.2.1` exposes deep `ry-init` context packs, `ry-start` context sufficiency gates, advisory SessionStart context, advisory PostToolUse commit advice, reviewer workflows, deployment workflow, instruction docs sync, post-task sync, and fullrepo agent-only context synchronization.

`rldyour-serena-mcp` `0.2.1` keeps memory freshness current when agent-only instruction/workflow files are moved out of `main` and into `fullrepo`.

Root `README.md` describes the active catalog, planned architecture, system install workflow, the portable MCP source-of-truth rule for `plugins/rldyour-mcps/.mcp.json`, and the owner-requested YOLO defaults applied by the installer.

`README.md`, `AGENTS.md`, and `system/AGENTS.md` now document release, rollback, dependency check, diagnostics, observability, and fullrepo commands. These additions are operational wrappers around the runtime; they do not change the active MCP server set or YOLO policy.

Repository documentation, plugin metadata, code comments, commits, memory files, plans, and research archives are written in English. User-facing conversation with the owner stays Russian unless requested otherwise.

`scripts/validate_marketplace.sh` is the canonical repository validation entry point. It validates marketplace JSON, release metadata, generated release manifest syntax, plugin manifests, skill frontmatter, compact bilingual routing descriptions, deterministic routing policy cases, strict OpenAI skill metadata, MCP dependency names, shell scripts, Python syntax, LSP health, Serena state, Flow state, MCP registration, MCP config sync, MCP package pinning, MCP runtime smoke, MCP capability smoke, plugin cache sync, hook smoke, hook lifecycle smoke, fullrepo sync smoke, secret patterns, and whitespace.

Current active plugin count is nine rldyour plugins plus two curated external plugins in system Codex. Current callable rldyour skill count is 38.

`scripts/install_system_codex.sh --dry-run` is the safe default system install preview. `scripts/install_system_codex.sh --apply` writes global Codex state with backups, including YOLO permission defaults and twelve MCP servers loaded from `plugins/rldyour-mcps/.mcp.json`. `scripts/doctor_system_codex.sh` verifies installed global AGENTS, config, YOLO defaults, plugins, MCP, cache, and repository validation.

`scripts/bootstrap_check.sh --dry-run` is the non-mutating bootstrap preview. `scripts/bootstrap_check.sh --apply` is the end-to-end current-machine bootstrap smoke flow: install preview, install apply, marketplace validation, MCP runtime smoke, hook smoke, system doctor, Serena state, Flow state, and git status.

`scripts/smoke_clean_bootstrap.sh` is the committed-state bootstrap proof. It requires a clean working tree, clones the current repository into a temporary path, installs into a temporary `CODEX_HOME`, runs doctor in list-only MCP capability mode with a temporary `SERENA_HOME`, verifies fullrepo status JSON, runs fullrepo smoke, verifies `codex mcp list`, and removes the temporary workspace by default.

`.github/workflows/validate.yml` runs on push to `main` and `fullrepo`, pull requests to `main`, and manual dispatch. It uses a matrix for `ubuntu-latest` and `macos-latest`, installs pinned Codex CLI from `config/mcp-runtime-versions.env`, applies the marketplace, runs marketplace validation, runs doctor, and runs clean bootstrap smoke. It writes a job summary on success and uploads `diagnostics/ci` as an artifact on failure.

`.github/workflows/dependency-check.yml` runs weekly and manually. It runs `python3 scripts/check_mcp_runtime_versions.py --fail-on-outdated --json`, writes a job summary, and uploads `dependency-check.json`.

CI validation uses portable mode for machine-specific checks: `RLDYOUR_SKIP_LSP_HEALTH=1` disables full LSP health on GitHub runners, while local validation still runs LSP health by default.

## Invariants

- Do not add planned plugins to `.agents/plugins/marketplace.json` until they are actually created and ready.
- Do not store secrets, tokens, cookies, private keys, or raw credentials in this repository.
- Keep technical identifiers stable and ASCII.
- Keep each plugin's responsibility boundary explicit.
- Keep compact Russian and English trigger phrases in each callable rldyour skill `SKILL.md` description so routing works with the owner's Russian prompts and English technical terms.
- Do not commit browser evidence or local Serena runtime/cache state.
- In normal product repositories, do not commit agent-only AI workflow files to normal branches after adopting the fullrepo workflow; restore and publish them through `fullrepo`.
- Do not publish secrets, local credentials, diagnostics, browser evidence, Serena caches, or runtime hook markers to `main` or `fullrepo`.

## Change Rules

- Use `plugin-creator` guidance when adding or modifying plugin manifests or marketplace entries.
- Append new marketplace entries unless the owner explicitly asks to reorder.
- Keep `README.md` active catalog aligned with `.agents/plugins/marketplace.json`.
- Restart Codex after changing marketplace metadata, plugin manifests, hooks, skills, or `.mcp.json`.
- Re-sync changed plugin directories into the active Codex plugin cache when applying changes to the system Codex runtime.
- Use `scripts/bootstrap_check.sh --apply` when validating a full new-machine or resynced-machine setup path.
- Use `scripts/smoke_clean_bootstrap.sh` when validating that committed source can bootstrap from a clean clone.
- Use `scripts/smoke_fullrepo_sync.sh` when validating fullrepo pattern, migration, restore, or publish changes.
- Use `scripts/sync_fullrepo_branch.sh --status` before final sync and `scripts/sync_fullrepo_branch.sh --publish` after normal branch push when agent-only context changed.
- Keep local MCP package specs pinned. `@latest` is not allowed in `plugins/rldyour-mcps/.mcp.json`.
- Keep `VERSION`, `CHANGELOG.md`, plugin manifest versions, and `docs/release-process.md` aligned for release changes.
- Do not commit `diagnostics/` or `dist/`; both are ignored local/runtime output directories.

## Verification

- `jq empty .agents/plugins/marketplace.json plugins/*/.codex-plugin/plugin.json`: validates marketplace and plugin manifests.
- `scripts/validate_marketplace.sh`: runs the full reusable marketplace validation suite.
- `python3 scripts/validate_plugin_versions.py`: validates SemVer release metadata and plugin manifest versions.
- `python3 scripts/validate_skill_routing.py`: validates deterministic Russian/English prompt routing policy cases.
- `python3 scripts/release_manifest.py`: emits the release snapshot JSON.
- `python3 scripts/check_mcp_runtime_versions.py --fail-on-outdated`: verifies pinned MCP runtime versions are current.
- `scripts/collect_diagnostics.sh`: writes a sanitized local diagnostics bundle.
- `scripts/rollback_system_codex.sh --list`: lists installer backups available for restore.
- `scripts/install_system_codex.sh --dry-run`: previews system Codex installation.
- `scripts/doctor_system_codex.sh`: validates installed system Codex state.
- `scripts/bootstrap_check.sh --apply`: validates full install and runtime smoke flow.
- `scripts/smoke_mcp_runtime.sh`: validates installed MCP runtime behavior.
- `scripts/smoke_mcp_capabilities.sh`: validates MCP initialize, expected tool discovery, and safe call-tool behavior.
- `scripts/smoke_hooks.sh`: validates repository and installed hook execution plus temporary git lifecycle transitions.
- `scripts/smoke_clean_bootstrap.sh`: validates clean clone to temporary system install.
- `scripts/smoke_fullrepo_sync.sh`: validates fullrepo publish, migrate-main, restore, and exclude behavior.
- `scripts/sync_fullrepo_branch.sh --status`: reports fullrepo state.
- `scripts/sync_fullrepo_branch.sh --publish`: publishes complete agent-only context snapshot.
- `.github/workflows/validate.yml`: validates marketplace and runtime smoke in GitHub Actions on Ubuntu and macOS.
- `.github/workflows/dependency-check.yml`: monitors pinned MCP runtime package freshness.
- `jq -r '.plugins[] | [.name,.category,.policy.installation,.policy.authentication,.source.path] | @tsv' .agents/plugins/marketplace.json`: shows active plugin order and policy.
- `codex plugin marketplace add .`: registers or confirms this marketplace.
- `codex mcp list`: verifies runtime MCP registrations after marketplace/plugin changes are installed.
- `git status -sb --ignored`: verifies only expected ignored Serena runtime files remain untracked.
