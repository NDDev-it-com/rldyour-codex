<!-- Memory Metadata
Last updated: 2026-05-14
Last commit: b3dc114 test(codex): strengthen integration smoke gates
Scope: README.md, AGENTS.md, system/AGENTS.md, system/agents/*.toml, VERSION, CHANGELOG.md, docs, .github/workflows/validate.yml, .github/workflows/dependency-check.yml, .github/dependabot.yml, config/mcp-runtime-versions.env, config/skill-routing-policy.json, scripts/validate_marketplace.sh, scripts/validate_plugin_versions.py, scripts/validate_skill_routing.py, scripts/release_manifest.py, scripts/check_mcp_runtime_versions.py, scripts/collect_diagnostics.sh, scripts/rollback_system_codex.sh, scripts/install_system_codex.sh, scripts/smoke_codex_hooks_migration.sh, scripts/doctor_system_codex.sh, scripts/bootstrap_check.sh, scripts/smoke_mcp_runtime.sh, scripts/smoke_mcp_capabilities.py, scripts/smoke_mcp_capabilities.sh, scripts/smoke_hooks.sh, scripts/smoke_clean_bootstrap.sh, scripts/smoke_fullrepo_sync.sh, scripts/sync_fullrepo_branch.sh, plugins/rldyour-flow/scripts/fullrepo_sync.py, pyrightconfig.json, .agents/plugins/marketplace.json, plugins/*/.codex-plugin/plugin.json, plugins/rldyour-mcps/.mcp.json, .gitignore, ${CODEX_HOME:-$HOME/.codex}/config.toml, ${CODEX_HOME:-$HOME/.codex}/agents/*.toml
Area: CORE
-->

# CORE_02_marketplace_control_model

## Purpose

This marketplace memory records the verified catalog and control model for `rldyour-codex`. It stores runtime-relevant facts for marketplace registration, plugin boundaries, and deterministic install/runtime synchronization.

## Source Of Truth

- `README.md`: control model, active catalog, system install workflow, fullrepo lifecycle.
- `AGENTS.md`: repository Codex instructions for project scope.
- `.agents/plugins/marketplace.json`: authoritative marketplace catalog.
- `plugins/<plugin>/.codex-plugin/plugin.json`: plugin manifests and boundaries.
- `plugins/rldyour-mcps/.mcp.json`: MCP source-of-truth transport list for system runtime.
- `system/AGENTS.md`: canonical global instruction template for installed `~/.codex/AGENTS.md`.
- `system/agents/*.toml`: canonical managed Codex custom subagent role configs for installed `~/.codex/agents/*.toml`.
- `config/mcp-runtime-versions.env`: pinned MCP/Codex package versions.
- `scripts/install_system_codex.sh`: dry-run/apply installer.
- `scripts/doctor_system_codex.sh`: installed-system verification.
- `scripts/validate_marketplace.sh`: full marketplace/runtime consistency validation.
- `scripts/bootstrap_check.sh`: bootstrap validation entrypoint.
- `scripts/smoke_codex_hooks_migration.sh`, `scripts/smoke_mcp_runtime.sh`, `scripts/smoke_mcp_capabilities.sh`, `scripts/smoke_clean_bootstrap.sh`: feature-flag and runtime smoke checks.
- `scripts/smoke_hooks.sh`: hook smoke for repo and installed cache layouts.
- `scripts/sync_fullrepo_branch.sh`, `plugins/rldyour-flow/scripts/fullrepo_sync.py`: agent-only workflow-file synchronization.
- `scripts/check_mcp_runtime_versions.py`: pinned runtime freshness check.
- `${CODEX_HOME:-$HOME/.codex}/config.toml`: installed runtime config.
- `${CODEX_HOME:-$HOME/.codex}/agents/*.toml`: installed managed subagent configs.
- `${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex`: installed plugin cache.

## Current Catalog

The active catalog has nine rldyour plugins, loaded in repository order from `.agents/plugins/marketplace.json`:

- `rldyour-mcps` (version `0.1.5`)
- `rldyour-explore` (version `0.1.2`)
- `rldyour-serena-mcp` (version `0.2.1`)
- `rldyour-security` (version `0.1.1`)
- `rldyour-browser` (version `0.1.1`)
- `rldyour-design` (version `0.2.0`)
- `rldyour-lsps` (version `0.1.1`)
- `rldyour-flow` (version `0.2.4`)
- `rldyour-rules` (version `0.1.3`)

Each plugin entry keeps `policy.installation: AVAILABLE` and `policy.authentication: ON_USE`.

Plugin boundary contracts from manifests:

- `rldyour-mcps`: `mcpServers: "./.mcp.json"` only.
- All non-MCP plugins use `skills: "./skills/"`.
- `rldyour-serena-mcp` and `rldyour-flow` additionally expose `hooks: "./hooks.json"`.

## Installed Runtime Model

Current installed plugin set in runtime config:

- `gmail@openai-curated`
- `github@openai-curated`
- `rldyour-mcps@rldyour-codex`
- `rldyour-explore@rldyour-codex`
- `rldyour-serena-mcp@rldyour-codex`
- `rldyour-security@rldyour-codex`
- `rldyour-browser@rldyour-codex`
- `rldyour-design@rldyour-codex`
- `rldyour-lsps@rldyour-codex`
- `rldyour-flow@rldyour-codex`
- `rldyour-rules@rldyour-codex`

Installed cache layout is `plugins/cache/rldyour-codex/<plugin>/local` for each rldyour plugin.

## Runtime and Policy Facts

- `system/AGENTS.md` is installed as `${CODEX_HOME:-$HOME/.codex}/AGENTS.md`; repository sources should remain authoritative only for project instructions.
- `scripts/install_system_codex.sh --apply` is the only supported path for changing:
  - marketplace registration,
  - marketplace-derived rldyour plugin enablement,
  - MCP registrations,
  - plugin cache sync,
  - official Codex config schema hint,
  - owner-selected model defaults and approved MCP tool overrides,
  - YOLO/system permission profile.
- `scripts/doctor_system_codex.sh` validates installed AGENTS/config alignment, the Codex config schema hint, marketplace-derived enabled plugins, `.mcp.json`-derived MCP registrations, cache parity, and repository validation status.
- `scripts/validate_plugin_versions.py` enforces marketplace policy fields, manifest metadata (`author`, `homepage`, `repository`, `license`, `keywords`), interface metadata, bundled capability paths, default prompt limits, and `brandColor` format.
- `scripts/validate_plugin_versions.py` also enforces core plugin boundary invariants: only `rldyour-mcps` may declare `mcpServers`, `rldyour-mcps` must stay transport-only, and only `rldyour-flow` plus `rldyour-serena-mcp` may declare hooks.
- `scripts/validate_marketplace.sh` derives accepted MCP dependency names for `agents/openai.yaml` from `plugins/rldyour-mcps/.mcp.json`, not a parallel hardcoded list.
- Legacy plugin names and old aliases are not present in the active catalog or runtime config.
- `@latest` MCP package specs are disallowed by marketplace validation.

## Invariants

- Marketplace catalog changes must be backed by real plugin files and valid manifests.
- Runtime config, managed subagent configs, and plugin cache are generated from repository sources; installed files are not the source of truth.
- Keep normal branches free of agent-only context; publish `AGENTS.md`, `.claude/CLAUDE.md`, and `.serena` knowledge through `fullrepo`.
- Keep curated `github@openai-curated` and `gmail@openai-curated` enabled unless the owner explicitly changes the system runtime.

## Change Rules

- Use `plugin-creator` guidance for manifest or catalog changes.
- Do not add planned plugins to catalog until files exist in `plugins/`.
- Keep `README.md` and `system/AGENTS.md` aligned with current plugin/runtime behavior.
- `scripts/install_system_codex.sh --apply` should be followed by restart so Codex and hooks reload.
- Reinstalling/rerendering plugin cache requires the install/apply path.
- After agent-only context changes, run `scripts/sync_fullrepo_branch.sh --status` and publish fullrepo flow as documented.

## Verification

- `jq empty .agents/plugins/marketplace.json plugins/*/.codex-plugin/plugin.json`: validates catalog and manifests.
- `scripts/validate_marketplace.sh`: validates plugin manifests, skills, MCP sync/pinning, hooks, caches, and whitespace.
- `python3 scripts/validate_plugin_versions.py`: validates release metadata, marketplace policy fields, manifest metadata, interface metadata, bundled paths, default prompt limits, and brand color format.
- `python3 scripts/validate_skill_routing.py`: validates routing fixture constraints.
- `scripts/install_system_codex.sh --dry-run`: preview install changes.
- `scripts/doctor_system_codex.sh`: verify installed config and plugin cache.
- `scripts/bootstrap_check.sh --apply`: preview/apply install + smoke route.
- `scripts/smoke_codex_hooks_migration.sh`, `scripts/smoke_mcp_runtime.sh`, `scripts/smoke_mcp_capabilities.sh`, `scripts/smoke_hooks.sh`, `scripts/smoke_clean_bootstrap.sh`: feature-flag, runtime, and lifecycle smoke checks.
- `scripts/smoke_hooks.sh` parses each plugin `hooks.json` entry and executes the configured command wrappers for repo and installed-cache layouts before running direct hook lifecycle checks.
- `scripts/smoke_local_git_guard.sh`: local Git pre-push guard smoke for product refs, fullrepo refs, mixed pushes, suspicious wording, definite secrets generated at runtime without storing secret-looking literals, runtime paths, and previous-hook chaining.
- `scripts/smoke_flow_branch_cleanup.sh`: verifies merged local/remote workflow branches keep Flow sync pending until branch cleanup is complete.
- `scripts/smoke_fullrepo_bootstrap_init.sh`: verifies first-run publish, restore, ignore, and current-branch index cleanup for `AGENTS.md`, `.claude/CLAUDE.md`, and Serena memories.
- `scripts/sync_fullrepo_branch.sh --publish`: publish agent-only context after meaningful instruction/runtime changes.
- `python3 scripts/check_mcp_runtime_versions.py --fail-on-outdated`: verify pinned package versions.
- `rg -n 'ctx7sk|ghp_|github_pat|password|secret|access[_-]?token|private[_-]?key|bearer' .serena/memories plugins .agents`: scan for accidental credential text.
