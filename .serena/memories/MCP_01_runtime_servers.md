<!-- Memory Metadata
Last updated: 2026-05-05
Last commit: 8b7c897 fix(flow): gate sync on merged branch cleanup
Scope: plugins/rldyour-mcps/.mcp.json, plugins/rldyour-mcps/.codex-plugin/plugin.json, plugins/rldyour-mcps/README.md, plugins/rldyour-mcps/.env.example, README.md, config/mcp-runtime-versions.env, scripts/install_system_codex.sh, scripts/validate_marketplace.sh, scripts/smoke_mcp_runtime.sh, scripts/smoke_mcp_capabilities.py, scripts/smoke_mcp_capabilities.sh, scripts/bootstrap_check.sh, scripts/smoke_clean_bootstrap.sh, .github/workflows/validate.yml, ${CODEX_HOME:-$HOME/.codex}/config.toml
Area: MCP
-->

# MCP_01_runtime_servers

## Purpose

`plugins/rldyour-mcps` is the MCP transport runtime plugin for this marketplace. It only owns transport and MCP configuration, not behavior policy, skills, hooks, memories, or project workflows.

## Source Of Truth

- `plugins/rldyour-mcps/.mcp.json`: transport list, commands, args, URLs, timeouts, env contracts.
- `plugins/rldyour-mcps/.codex-plugin/plugin.json`: plugin metadata (`mcpServers: "./.mcp.json"`).
- `plugins/rldyour-mcps/README.md`: runtime responsibility and verification guidance.
- `plugins/rldyour-mcps/.env.example`: environment placeholder contract.
- `config/mcp-runtime-versions.env`: pinned package versions used by installer and checks.
- `scripts/install_system_codex.sh`: maps portable `.mcp.json` commands to installed executable paths.
- `scripts/validate_marketplace.sh`: MCP pinning, config sync, and runtime smoke checks.
- `scripts/smoke_mcp_runtime.sh`: installed-config + endpoint/command smoke.
- `scripts/smoke_mcp_capabilities.py/.sh`: MCP initialize/list_tools/safe probe smoke.
- `${CODEX_HOME:-$HOME/.codex}/config.toml`: installed MCP runtime.

## Installed MCP Set (12 servers)

1. `serena` (`uvx`)
2. `sequential-thinking` (`bunx`)
3. `playwright` (`bunx`)
4. `chrome-devtools` (`bunx`)
5. `context7` (`bunx`)
6. `deepwiki` (`url`)
7. `grep` (`url`)
8. `semgrep` (`uvx`)
9. `shadcn` (`bunx`)
10. `dart-flutter` (`dart`)
11. `figma` (`url`)
12. `openaiDeveloperDocs` (`url`)

Local command/runtime contracts from `.mcp.json`:

- `serena`: `uvx --from serena-agent==1.2.0 ... serena start-mcp-server ... --enable-web-dashboard False --open-web-dashboard False`
- `sequential-thinking`: `bunx @modelcontextprotocol/server-sequential-thinking@2025.12.18`
- `playwright`: `bunx @playwright/mcp@0.0.73 --headless --caps=network,storage,testing,devtools`
- `chrome-devtools`: `bunx chrome-devtools-mcp@0.24.0 --headless --isolated --no-usage-statistics --no-performance-crux`
- `context7`: `bunx @upstash/context7-mcp@2.2.4` (reads `CONTEXT7_API_KEY` via `env_vars`)
- `semgrep`: `uvx --from semgrep==1.161.0 semgrep mcp`
- `shadcn`: `bunx shadcn@4.6.0 mcp`
- `dart-flutter`: `dart mcp-server --force-roots-fallback`

Remote URL MCPs:

- `deepwiki`: `https://mcp.deepwiki.com/mcp`
- `grep`: `https://mcp.grep.app`
- `figma`: `https://mcp.figma.com/mcp`
- `openaiDeveloperDocs`: `https://developers.openai.com/mcp`

Timeouts:

- local servers: `startup_timeout_sec: 90`, `tool_timeout_sec` 120/180
- remote servers: `startup_timeout_sec: 60`, `tool_timeout_sec: 120`

## Config Synchronization

- `plugins/rldyour-mcps/.mcp.json` keeps portable commands (`uvx`, `bunx`, `dart`).
- `scripts/install_system_codex.sh --apply` replaces command names with absolute machine paths using:
  - `UVX_BIN`
  - `BUNX_BIN`
  - `DART_BIN`
  - fallback to `PATH`.
- `scripts/validate_marketplace.sh` runs MCP config sync and requires only:
  - same server names,
  - same command basenames,
  - same args/env/env_vars/urls/timeouts,
  - with executable path difference allowed.
- `@latest` is disallowed for MCP runtime definitions by validation.
- Pinned package specs in `.mcp.json` must be exact:
  - `serena-agent==1.2.0`
  - `@modelcontextprotocol/server-sequential-thinking@2025.12.18`
  - `@playwright/mcp@0.0.73`
  - `chrome-devtools-mcp@0.24.0`
  - `@upstash/context7-mcp@2.2.4`
  - `semgrep==1.161.0`
  - `shadcn@4.6.0`
- `config/mcp-runtime-versions.env` is expected to mirror MCP launcher pins and includes `CODEX_CLI_VERSION`/`MCP_PYTHON_SDK_VERSION`.

## Capability Smoke Contract

`scripts/smoke_mcp_capabilities.py` expects `list_tools` matches for all 12 servers and runs deterministic safe calls by default for:

- `serena`: `check_onboarding_performed`
- `sequential-thinking`: `sequentialthinking`
- `playwright`: `browser_navigate` + `browser_close`
- `chrome-devtools`: `new_page`
- `deepwiki`: `read_wiki_structure`
- `grep`: `searchGitHub`
- `semgrep`: `get_supported_languages`
- `shadcn`: `get_project_registries`
- `openaiDeveloperDocs`: `search_openai_docs`

Skip rules in capability smoke:

- `context7` call is skipped if `CONTEXT7_API_KEY` is absent.
- `figma` is skipped unless `--include-auth`.
- `dart-flutter` is list-only.

`scripts/smoke_mcp_runtime.sh` requires installed config/server name parity and checks:
- every `codex mcp get <server>`
- command executable presence (or `PATH` resolution)
- remote endpoint reachability (unless `--skip-url-check`).

## Invariants

- Keep runtime local commands on approved launchers only: `uvx`, `bunx`, `dart`.
- Keep `serena` headless flags explicit: `--enable-web-dashboard False`, `--open-web-dashboard False`, `--project-from-cwd --context=codex`.
- Keep `playwright` and `chrome-devtools` headless/isolated as currently configured.
- Keep URL MCPs explicit; avoid wrapping them in local wrappers.
- Do not place real tokens/keys in `.mcp.json`, memories, or repo files.
- Update `scripts/rldyour-mcps` docs and this memory with any transport or pin change.

## Verification

- `jq '{servers: (.mcpServers | keys)}' plugins/rldyour-mcps/.mcp.json`
- `jq empty plugins/rldyour-mcps/.mcp.json plugins/rldyour-mcps/.codex-plugin/plugin.json`
- `scripts/validate_marketplace.sh` (MCP config sync, pinning policy, smoke checks)
- `scripts/smoke_mcp_runtime.sh`
- `scripts/smoke_mcp_capabilities.sh`
- `codex mcp list`
- `codex mcp get serena`, `codex mcp get figma`, `codex mcp get openaiDeveloperDocs`
- `scripts/bootstrap_check.sh --apply`
- `scripts/smoke_clean_bootstrap.sh`
- `rg -n 'ctx7sk|password|secret|api[_-]?key|access[_-]?token|bearer|private[_-]?key' plugins/rldyour-mcps`
