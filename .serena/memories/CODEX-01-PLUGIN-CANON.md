<!-- Memory Metadata
Last updated: 2026-05-21
Last commit: be1134c fix(ci): classify github mcp runtime noise
Scope: .agents/plugins/marketplace.json, config/rldyour-contract.json, docs/contract-matrix.md, plugins/*/.codex-plugin/plugin.json, plugins/*/skills/*/SKILL.md, plugins/*/skills/*/agents/openai.yaml, plugins/*/hooks.json, system/agents/*.toml, scripts/validate_agent_tools.py, scripts/validate_plugin_versions.py, scripts/validate_skill_routing.py, scripts/validate_contract.py, scripts/plugin_cache_contract.py, scripts/smoke_codex_hook_listing.py
Area: CODEX
-->

# CODEX-01-PLUGIN-CANON

## Purpose

This memory records Codex-native plugin, skill, hook, and managed-subagent surfaces for `rldyour-codex`. It exists to prevent Claude Code formats from drifting into Codex plugin implementation.

## Source Of Truth

- `.agents/plugins/marketplace.json`: local marketplace catalog and plugin order.
- `config/rldyour-contract.json`: machine-readable Codex adapter contract for plugins, skills, slash-command absence, managed agents, hook lifecycle mapping, MCP servers, cache layout, and YOLO boundaries.
- `docs/contract-matrix.md`: human-readable matrix for the same adapter contract.
- `plugins/<plugin>/.codex-plugin/plugin.json`: Codex plugin manifest. Required manifest path is `.codex-plugin/plugin.json`.
- `plugins/<plugin>/skills/*/SKILL.md`: skill instructions and compact routing frontmatter.
- `plugins/<plugin>/skills/*/agents/openai.yaml`: Codex skill UI metadata and MCP dependencies.
- `plugins/rldyour-flow/hooks.json` and `plugins/rldyour-serena-mcp/hooks.json`: plugin hook declarations.
- `system/agents/*.toml`: managed Codex subagent roles installed to `${CODEX_HOME:-$HOME/.codex}/agents/*.toml`.
- `scripts/validate_agent_tools.py`: Codex-specific surface validator.
- `scripts/validate_plugin_versions.py`, `scripts/validate_contract.py`, and `scripts/validate_skill_routing.py`: manifest, adapter contract, and deterministic routing checks.
- `scripts/plugin_cache_contract.py`: versioned installed plugin cache path and parity contract.
- `scripts/smoke_codex_hook_listing.py`: live Codex app-server `hooks/list` trust/source smoke for installed bundled plugin hooks.
- `scripts/smoke_codex_hooks_migration.sh`: end-to-end deprecated-alias migration smoke for installed system config.

## Entry Points

- `uv run --with pyyaml python scripts/validate_agent_tools.py`: validates managed TOML agents, skill metadata, and absence of Claude-only artifacts.
- `python3 scripts/validate_plugin_versions.py`: validates marketplace release metadata, plugin interface fields, paths, and hook ownership.
- `python3 scripts/validate_contract.py`: validates the Codex adapter surface against real source files.
- `python3 scripts/validate_skill_routing.py`: validates prompt-to-skill routing policy.
- `python3 scripts/plugin_cache_contract.py verify`: validates installed cache parity under versioned plugin paths.
- `python3 scripts/smoke_codex_hook_listing.py`: validates live Codex `hooks/list` hook count, trust, enabled state, hash presence, and versioned source paths.
- `scripts/install_system_codex.sh --apply`: installs marketplace, plugin cache, managed agents, and active Codex config.

## Current Behavior

- Codex skills use `SKILL.md` for instructions and `agents/openai.yaml` for Codex UI/dependency metadata.
- `SKILL.md` frontmatter should stay compact: `name` and a Russian/English `description` are the durable routing surface. Long policy belongs in the body or `references/`.
- Claude-only skill frontmatter such as `allowed-tools`, `allowed_tools`, `disallowed-tools`, `maxTurns`, `model`, `effort`, `tools`, and `color` is rejected by `scripts/validate_agent_tools.py`.
- Managed subagents are TOML files, not plugin-root Markdown agents. Current managed roles must have `model = "gpt-5.5"` and `model_reasoning_effort = "medium"`.
- Managed subagents currently carry a temporary MCP startup-isolation policy. Each role keeps the lightweight inherited/core surface available (`sequential-thinking`, `serena`, `context7`, `grep`, `deepwiki`, `openaiDeveloperDocs`, and built-in `codex_apps`) and explicitly disables specialist MCP servers that have caused subagent startup fan-out or dependency friction (`semgrep`, `figma`, `playwright`, `chrome-devtools`, `dart-flutter`, and `shadcn`).
- Disabled specialist MCP overrides in standalone `system/agents/*.toml` files must include complete disabled transport metadata copied from `plugins/rldyour-mcps/.mcp.json` (`command` or `url`, args, and timeouts where defined). Codex deserializes standalone agent configs before any parent-layer merge, so partial disabled tables such as `mcp_servers.semgrep.enabled = false` can still produce `invalid transport` startup warnings.
- Built-in `codex_apps` is inherited from Codex Apps/connectors and must not be declared as a synthetic `[mcp_servers.codex_apps]` custom-agent transport table.
- `system/agents/serena-sync.toml` is the Codex-native memory-maintenance role. It may edit only `.serena/memories/` and closely related Serena metadata, not source code, plugin files, docs, configs, tests, scripts, or git history.
- Plugin hook support is used only by `rldyour-flow` and `rldyour-serena-mcp`.
- Codex intentionally has no slash commands in this adapter; public flows are exposed through skills and managed subagents, and `scripts/validate_contract.py` rejects accidental `commands/` directories.
- The canonical public repository URL for owned plugin manifests is `https://github.com/NDDev-it-com/rldyour-codex`, and owned plugin manifests declare `AGPL-3.0-or-later`.
- Plugin hook command entries use the official plugin runtime environment and call scripts through `PLUGIN_ROOT`; they must not use repo-cwd relative script paths or installed-cache search fallbacks.
- Flow `SessionStart` uses one plugin hook entry for `session_start_dispatcher.sh`, which serializes bootstrap and context because official Codex hook semantics allow concurrent execution of multiple matching command hooks. Its child scripts are intentionally fast/offline: bootstrap can use only an existing local fullrepo tracking ref, and context generation cannot call network or deep repository analyzers.
- Flow `PreToolUse` registers `pre_tool_use_cwd_guard.sh` for `Bash`. It denies common commands that would rename or remove the active Codex session cwd or repository root before Codex can lose its hook working directory.
- Flow `Stop` uses one plugin hook entry for `stop_lifecycle_dispatcher.sh`; it drains stdin to a temp file, invokes the Serena Stop memory gate first, invokes Flow post-task sync only after Serena exits cleanly, runs children in separate process groups with explicit timeouts, and surfaces timeout continuation instructions instead of letting the outer Codex hook timeout hide the cause. `rldyour-serena-mcp/hooks.json` intentionally does not register its own Stop hook to avoid cross-plugin Stop races.
- Serena and Flow hooks that may early-exit now drain Codex hook stdin before returning, preventing `Broken pipe` failures when Codex writes a larger hook payload.
- Official Codex docs verified for this implementation: Codex plugin manifests live at `.codex-plugin/plugin.json`; plugin hooks can point to `hooks.json`; Codex skills use `skills/`; Codex config uses `[features].hooks` for lifecycle hooks and `[features].plugin_hooks` to opt into bundled hooks from enabled plugins.
- Installed plugin cache paths are versioned as `${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/<plugin>/<version>`. Legacy `<plugin>/local` lookup remains only as a compatibility fallback in wrapper paths.
- Legacy config aliases (`codex_hooks`, `use_legacy_landlock`, `experimental_instructions_file`, `background_terminal_timeout`, `experimental_use_unified_exec_tool`, and deprecated `features.web_search*`) are migrated by installer/doctor/smoke into canonical equivalents.

## Contracts And Data

- Plugin manifests include `name`, `version`, `description`, bundled capability paths such as `skills`/`hooks`, and `interface` metadata.
- Plugin manifests must keep `license = "AGPL-3.0-or-later"` and canonical NDDev repository/homepage/interface URLs.
- Bundled hook JSON paths are relative to the plugin root, while command bodies resolve executable hook scripts through the `PLUGIN_ROOT` environment variable supplied by Codex at runtime.
- Current hook-enabled plugin versions after `6ec3fb9`: `rldyour-flow` `0.3.3` and `rldyour-serena-mcp` `0.2.4`.
- Marketplace entries use local `source.path` references to `./plugins/<plugin>`.
- `plugins/rldyour-mcps/.mcp.json` defines valid MCP dependency values for `agents/openai.yaml`.
- `scripts/validate_agent_tools.py` loads `.mcp.json`, parses YAML/TOML, rejects unknown MCP dependency names, rejects partial disabled managed-agent MCP overrides, rejects disabled transport drift from `.mcp.json`, and rejects explicit `mcp_servers.codex_apps` tables.
- `scripts/validate_contract.py` rejects drift in plugin set, skill names/count, slash-command absence, managed agent role mapping, hook command handler shape, MCP server list, manifest license/URL metadata, and repo-local YOLO defaults. JSON-derived contract values must be type-narrowed before comparison so Pyright strict checks prove the validator itself stays safe.
- Managed agent TOML field `name` must match the filename stem.

## Invariants

- Do not add `.claude-plugin/*` to this repository. Codex plugin manifests use `.codex-plugin/*`.
- Do not add `plugins/rldyour-*/agents/*.md`; that is a Claude Code plugin-root subagent format, not this Codex format.
- Do not encode tool allowlists in Codex `SKILL.md` frontmatter. Use `agents/openai.yaml` dependencies and project policy instead.
- Do not hardcode plugin or MCP lists in installer/doctor logic; derive plugin enablement from `.agents/plugins/marketplace.json` and MCP registration from `plugins/rldyour-mcps/.mcp.json`.
- Do not bypass `config/rldyour-contract.json` when changing the public Codex adapter surface.
- Do not strip `[features].plugin_hooks`; it is the official opt-in for bundled plugin hooks and is managed as `true` here.
- Do not reintroduce hook command wrappers that search `plugins/rldyour-*` under the session cwd or `${CODEX_HOME}/plugins/cache`; that was the source of cross-project hook execution fragility.

## Change Rules

- When adding a plugin, update `.agents/plugins/marketplace.json`, create `plugins/<plugin>/.codex-plugin/plugin.json`, add skill metadata under `skills/*/agents/openai.yaml`, and run marketplace validation.
- When adding a managed subagent, add a TOML file under `system/agents/`, ensure installer/doctor parity still passes, and avoid unsupported tool allowlist fields.
- When changing Codex surfaces, update this memory and run `validate_agent_tools.py`.
- When changing public adapter shape, update `config/rldyour-contract.json`, `docs/contract-matrix.md`, and run `python3 scripts/validate_contract.py`.
- When changing plugin hook commands, run `scripts/smoke_hooks.sh`, install into `${CODEX_HOME}`, and verify live hook trust with `scripts/doctor_system_codex.sh`.
- `66070a8` bumps the marketplace to `0.3.3` and closes the Codex startup warning where all installed managed subagent role files were ignored with `invalid transport`; the fix is complete disabled transport metadata in source and installed agent TOML files plus validator/doctor anti-regression checks.
- `cdad168` bumps the marketplace to `0.3.4` and makes Flow `SessionStart` offline and local-only so slow remotes or deep state analyzers cannot produce startup hook timeout context.
- `6ec3fb9` bumps the marketplace to `0.3.5` and hardens lifecycle execution: Flow PreToolUse blocks active cwd/repo-root rename or deletion through Codex Bash, Stop checks are local-only and process-group bounded, hook stdin is drained before early exits, and hook smoke covers large stdin, cwd rename blocking, and no-network Stop regressions.
- `2da696d` adds a machine-readable Codex adapter contract, aligns plugin manifest license/URLs with the public AGPL repository, switches install/doctor/validation cache parity to versioned plugin cache paths, adds live `hooks/list` smoke, batches skill frontmatter validation, and keeps legacy `local` cache only as fallback.

## Verification

- `uv run --with pyyaml python scripts/validate_agent_tools.py`: proves Codex-native agent and skill surfaces.
- `python3 scripts/validate_plugin_versions.py`: proves manifest and marketplace policy consistency.
- `python3 scripts/validate_skill_routing.py`: proves deterministic routing policy coverage.
- `python3 scripts/validate_contract.py`: proves the Codex adapter contract matches source.
- `python3 scripts/smoke_codex_hook_listing.py`: proves installed rldyour bundled plugin hooks are trusted/enabled in live Codex `hooks/list`.
- `scripts/validate_marketplace.sh`: includes all of the above and hook/taxonomy smoke coverage.
