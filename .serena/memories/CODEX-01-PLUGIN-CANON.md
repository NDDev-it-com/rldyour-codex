<!-- Memory Metadata
Last updated: 2026-05-17
Last commit: e2f5b80 fix(codex): stabilize plugin hook execution
Scope: .agents/plugins/marketplace.json, plugins/*/.codex-plugin/plugin.json, plugins/*/skills/*/SKILL.md, plugins/*/skills/*/agents/openai.yaml, plugins/*/hooks.json, system/agents/*.toml, scripts/validate_agent_tools.py, scripts/validate_plugin_versions.py, scripts/validate_skill_routing.py
Area: CODEX
-->

# CODEX-01-PLUGIN-CANON

## Purpose

This memory records Codex-native plugin, skill, hook, and managed-subagent surfaces for `rldyour-codex`. It exists to prevent Claude Code formats from drifting into Codex plugin implementation.

## Source Of Truth

- `.agents/plugins/marketplace.json`: local marketplace catalog and plugin order.
- `plugins/<plugin>/.codex-plugin/plugin.json`: Codex plugin manifest. Required manifest path is `.codex-plugin/plugin.json`.
- `plugins/<plugin>/skills/*/SKILL.md`: skill instructions and compact routing frontmatter.
- `plugins/<plugin>/skills/*/agents/openai.yaml`: Codex skill UI metadata and MCP dependencies.
- `plugins/rldyour-flow/hooks.json` and `plugins/rldyour-serena-mcp/hooks.json`: plugin hook declarations.
- `system/agents/*.toml`: managed Codex subagent roles installed to `${CODEX_HOME:-$HOME/.codex}/agents/*.toml`.
- `scripts/validate_agent_tools.py`: Codex-specific surface validator.
- `scripts/validate_plugin_versions.py` and `scripts/validate_skill_routing.py`: manifest and deterministic routing checks.
- `scripts/smoke_codex_hooks_migration.sh`: end-to-end deprecated-alias migration smoke for installed system config.

## Entry Points

- `uv run --with pyyaml python scripts/validate_agent_tools.py`: validates managed TOML agents, skill metadata, and absence of Claude-only artifacts.
- `python3 scripts/validate_plugin_versions.py`: validates marketplace release metadata, plugin interface fields, paths, and hook ownership.
- `python3 scripts/validate_skill_routing.py`: validates prompt-to-skill routing policy.
- `scripts/install_system_codex.sh --apply`: installs marketplace, plugin cache, managed agents, and active Codex config.

## Current Behavior

- Codex skills use `SKILL.md` for instructions and `agents/openai.yaml` for Codex UI/dependency metadata.
- `SKILL.md` frontmatter should stay compact: `name` and a Russian/English `description` are the durable routing surface. Long policy belongs in the body or `references/`.
- Claude-only skill frontmatter such as `allowed-tools`, `allowed_tools`, `disallowed-tools`, `maxTurns`, `model`, `effort`, `tools`, and `color` is rejected by `scripts/validate_agent_tools.py`.
- Managed subagents are TOML files, not plugin-root Markdown agents. Current managed roles must have `model = "gpt-5.5"` and `model_reasoning_effort = "medium"`.
- `system/agents/serena-sync.toml` is the Codex-native memory-maintenance role. It may edit only `.serena/memories/` and closely related Serena metadata, not source code, plugin files, docs, configs, tests, scripts, or git history.
- Plugin hook support is used only by `rldyour-flow` and `rldyour-serena-mcp`.
- Plugin hook command entries use the official plugin runtime environment and call scripts through `PLUGIN_ROOT`; they must not use repo-cwd relative script paths or installed-cache search fallbacks.
- Official Codex docs verified for this implementation: Codex plugin manifests live at `.codex-plugin/plugin.json`; plugin hooks can point to `hooks.json`; Codex skills use `skills/`; Codex config uses `[features].hooks` for lifecycle hooks and `[features].plugin_hooks` to opt into bundled hooks from enabled plugins.
- Legacy config aliases (`codex_hooks`, `use_legacy_landlock`, `experimental_instructions_file`, `background_terminal_timeout`, `experimental_use_unified_exec_tool`, and deprecated `features.web_search*`) are migrated by installer/doctor/smoke into canonical equivalents.

## Contracts And Data

- Plugin manifests include `name`, `version`, `description`, bundled capability paths such as `skills`/`hooks`, and `interface` metadata.
- Bundled hook JSON paths are relative to the plugin root, while command bodies resolve executable hook scripts through the `PLUGIN_ROOT` environment variable supplied by Codex at runtime.
- Marketplace entries use local `source.path` references to `./plugins/<plugin>`.
- `plugins/rldyour-mcps/.mcp.json` defines valid MCP dependency values for `agents/openai.yaml`.
- `scripts/validate_agent_tools.py` loads `.mcp.json`, parses YAML/TOML, and rejects unknown MCP dependency names.
- Managed agent TOML field `name` must match the filename stem.

## Invariants

- Do not add `.claude-plugin/*` to this repository. Codex plugin manifests use `.codex-plugin/*`.
- Do not add `plugins/rldyour-*/agents/*.md`; that is a Claude Code plugin-root subagent format, not this Codex format.
- Do not encode tool allowlists in Codex `SKILL.md` frontmatter. Use `agents/openai.yaml` dependencies and project policy instead.
- Do not hardcode plugin or MCP lists in installer/doctor logic; derive plugin enablement from `.agents/plugins/marketplace.json` and MCP registration from `plugins/rldyour-mcps/.mcp.json`.
- Do not strip `[features].plugin_hooks`; it is the official opt-in for bundled plugin hooks and is managed as `true` here.
- Do not reintroduce hook command wrappers that search `plugins/rldyour-*` under the session cwd or `${CODEX_HOME}/plugins/cache`; that was the source of cross-project hook execution fragility.

## Change Rules

- When adding a plugin, update `.agents/plugins/marketplace.json`, create `plugins/<plugin>/.codex-plugin/plugin.json`, add skill metadata under `skills/*/agents/openai.yaml`, and run marketplace validation.
- When adding a managed subagent, add a TOML file under `system/agents/`, ensure installer/doctor parity still passes, and avoid unsupported tool allowlist fields.
- When changing Codex surfaces, update this memory and run `validate_agent_tools.py`.
- When changing plugin hook commands, run `scripts/smoke_hooks.sh`, install into `${CODEX_HOME}`, and verify live hook trust with `scripts/doctor_system_codex.sh`.
- `6b6dfd3` is a release-level maintenance commit (VERSION/CHANGELOG) and does not change plugin manifests, hooks, install logic, or managed-agent behavior in this memory scope.

## Verification

- `uv run --with pyyaml python scripts/validate_agent_tools.py`: proves Codex-native agent and skill surfaces.
- `python3 scripts/validate_plugin_versions.py`: proves manifest and marketplace policy consistency.
- `python3 scripts/validate_skill_routing.py`: proves deterministic routing policy coverage.
- `scripts/validate_marketplace.sh`: includes all of the above and hook/taxonomy smoke coverage.
