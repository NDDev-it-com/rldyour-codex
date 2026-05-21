<!-- Memory Metadata
Last updated: 2026-05-20
Last commit: 761e03f chore(release): 0.4.2
Scope: plugins/rldyour-mcps/.mcp.json, config/mcp-runtime-versions.env, scripts/smoke_mcp_runtime.sh, scripts/smoke_mcp_capabilities.sh, scripts/smoke_mcp_capabilities.py, scripts/check_mcp_runtime_versions.py, scripts/validate_runtime_prereqs.py, scripts/doctor_system_codex.sh, scripts/install_system_codex.sh
Area: MCP
-->

# MCP-01-TRANSPORT

## Purpose

`rldyour-mcps` owns MCP transport definitions only. This memory records the runtime registry, pins, smoke contracts, and boundary rules.

## Source Of Truth

- `plugins/rldyour-mcps/.mcp.json`: MCP server registry used by installer and doctor.
- `config/mcp-runtime-versions.env`: pinned launcher/package versions.
- `scripts/check_mcp_runtime_versions.py`: pin freshness/parity check.
- `scripts/validate_runtime_prereqs.py`: strict launcher prerequisite check for enabled local MCP servers.
- `scripts/smoke_mcp_runtime.sh`: runtime startup and remote preflight smoke.
- `scripts/smoke_mcp_capabilities.sh` and `scripts/smoke_mcp_capabilities.py`: capability-level smoke.
- `scripts/install_system_codex.sh` and `scripts/doctor_system_codex.sh`: install/verify MCP registration.

## Entry Points

- `codex mcp list`: inspect active Codex MCP registration.
- `scripts/smoke_mcp_runtime.sh`: verify installed server startup/remote preflight.
- `scripts/smoke_mcp_capabilities.sh`: verify representative tool calls.
- `python3 scripts/check_mcp_runtime_versions.py`: verify pinned runtime versions.
- `python3 scripts/validate_runtime_prereqs.py --strict --require-codex`: verify enabled local launchers and Codex CLI availability.

## Current Behavior

- Configured MCP servers: `chrome-devtools`, `context7`, `dart-flutter`, `deepwiki`, `figma`, `grep`, `openaiDeveloperDocs`, `playwright`, `semgrep`, `sequential-thinking`, `serena`, and `shadcn`.
- Managed subagents intentionally use a temporary narrower MCP policy: `sequential-thinking`, `serena`, `context7`, `grep`, `deepwiki`, `openaiDeveloperDocs`, and built-in `codex_apps` remain available, while specialist MCP servers are disabled in subagent TOML files to avoid eager startup fan-out and launcher friction. This is a subagent policy, not a removal from the parent-session MCP registry.
- A disabled managed-agent MCP table is still a declared MCP server table to Codex. It must include a valid transport (`command` or `url`) and registry-matching transport fields from `plugins/rldyour-mcps/.mcp.json`; otherwise Codex can reject the entire standalone role file with `invalid transport`.
- `codex_apps` is an Apps/connectors capability, not a transport definition in `plugins/rldyour-mcps/.mcp.json`, so managed agents leave it inherited instead of declaring `[mcp_servers.codex_apps]`.
- Current pins from `config/mcp-runtime-versions.env`: Codex CLI `0.132.0`, Node major `24`, Bun `1.3.14`, Dart SDK `3.11.0`, MCP Python SDK `1.27.1`, Serena Agent `1.5.1`, Semgrep `1.163.0`, Playwright MCP `0.0.75`, Chrome DevTools MCP `1.0.1`, Context7 MCP `2.2.5`, shadcn `4.7.0`, sequential-thinking `2025.12.18`.
- `dart-flutter` is the explicit reproducibility exception: it launches through the local Dart SDK and is declared as `DART_FLUTTER_MCP_RUNTIME=external-local-dart-sdk` instead of a package-version pin.
- Strict runtime validation maps enabled local MCP servers to launcher prerequisites (`uvx`, `bunx`, `dart`, and optional `codex`) and fails in strict mode when a required launcher is missing.
- Remote URL MCP smoke uses Streamable HTTP JSON-RPC `initialize` POST preflight; auth-gated `401`/`403` may pass, but unsupported POST behavior fails.
- Serena MCP is started with `--project-from-cwd`, `--context=codex`, web dashboard disabled, and Python `3.13` through `uvx`.
- Serena Agent `1.5.1` exposes `initial_instructions`, `onboarding`, `list_memories`, and `get_current_config` in the Codex context; `check_onboarding_performed` is no longer an exposed active tool in the installed Codex context. Capability smoke uses `list_memories` as the deterministic safe Serena call because `get_current_config` logs a variable multi-line configuration block in CI.
- OpenAI docs are available through `openaiDeveloperDocs` and should be preferred over general web search for OpenAI/Codex product facts.

## Contracts And Data

- MCP launcher package specs must be pinned; `@latest` is invalid in runtime definitions.
- `config/mcp-runtime-versions.env` and local package specs in `.mcp.json` must stay in parity.
- GitHub Actions and devcontainer setup must consume shared runtime pins from `config/mcp-runtime-versions.env` instead of drifting to tool defaults.
- If `dart-flutter` uses command `dart`, marketplace validation requires `DART_FLUTTER_MCP_RUNTIME=external-local-dart-sdk`.
- Environment variable references in `.mcp.json` are names only; do not commit secret values.
- `rldyour-mcps` must not add behavior skills. Domain behavior belongs to the domain plugins.
- Managed subagent disabled MCP overrides must copy transport fields from `.mcp.json`; validator and doctor reject drift.

## Invariants

- Do not duplicate MCP server lists in installer/doctor/skills; derive from `.mcp.json`.
- Do not treat built-in Apps/connectors such as `codex_apps` as `.mcp.json` transport entries.
- Do not store credentials or tokens in `.mcp.json`, memories, docs, or diagnostics.
- Use official/current documentation MCPs before general web search for technical product facts.

## Change Rules

- When adding or renaming an MCP server, update `.mcp.json`, metadata dependencies in affected `agents/openai.yaml` files, validation, and this memory.
- When bumping package pins, update `config/mcp-runtime-versions.env`, `.mcp.json`, `CHANGELOG.md`, and run runtime/capability smoke when feasible.

## Verification

- `codex mcp list`: active registration.
- `scripts/smoke_mcp_runtime.sh`: startup and remote preflight.
- `scripts/smoke_mcp_capabilities.sh`: representative tool calls.
- `python3 scripts/check_mcp_runtime_versions.py`: pin parity/freshness.
- `python3 scripts/validate_runtime_prereqs.py --strict --require-codex`: strict launcher prerequisite validation.
- `scripts/doctor_system_codex.sh`: installed MCP config verification.
