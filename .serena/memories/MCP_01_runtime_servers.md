<!-- Memory Metadata
Last updated: 2026-05-04
Last commit: 3128913 chore(mcp): update chrome devtools runtime pin
Scope: plugins/rldyour-mcps/.mcp.json, plugins/rldyour-mcps/.codex-plugin/plugin.json, plugins/rldyour-mcps/README.md, plugins/rldyour-mcps/.env.example, README.md, config/mcp-runtime-versions.env, scripts/install_system_codex.sh, scripts/validate_marketplace.sh, scripts/smoke_mcp_runtime.sh, scripts/smoke_mcp_capabilities.py, scripts/smoke_mcp_capabilities.sh, scripts/bootstrap_check.sh, scripts/smoke_clean_bootstrap.sh, .github/workflows/validate.yml, /Users/rldyourmnd/.codex/config.toml
Area: MCP
-->

# MCP_01_runtime_servers

## Purpose

`plugins/rldyour-mcps` is the MCP transport runtime layer for the rldyour Codex workflow plugins. It connects approved MCP servers and does not define behavior policy, skills, hooks, project memories, or workflow commands.

## Source Of Truth

- `plugins/rldyour-mcps/.mcp.json`: MCP server transport definitions, commands, URLs, timeouts, and environment variable requirements.
- `plugins/rldyour-mcps/.codex-plugin/plugin.json`: plugin manifest with `mcpServers: "./.mcp.json"` and no `skills`.
- `plugins/rldyour-mcps/README.md`: runtime rules, responsibility boundary, startup rules, language rules, and verification commands.
- `plugins/rldyour-mcps/.env.example`: placeholder-only environment variable shape.
- `config/mcp-runtime-versions.env`: pinned local MCP launcher package versions and MCP Python SDK version.
- `scripts/install_system_codex.sh`: projects portable `.mcp.json` definitions into active system Codex config.
- `scripts/validate_marketplace.sh`: validates repository MCP definitions against the installed system Codex MCP config.
- `scripts/smoke_mcp_runtime.sh`: validates installed MCP runtime definitions through Codex and endpoint/command probes.
- `scripts/smoke_mcp_capabilities.py`: validates MCP initialize, expected tool discovery, and safe call-tool probes.
- `scripts/smoke_mcp_capabilities.sh`: wrapper that runs capability smoke with pinned `mcp` Python SDK.
- `/Users/rldyourmnd/.codex/config.toml`: active system MCP registrations after marketplace installation.

## Entry Points

- `serena`: semantic code navigation and editing through `uvx`.
- `sequential-thinking`: structured reasoning through `bunx`.
- `playwright`: browser automation through `bunx`.
- `chrome-devtools`: browser diagnosis through `bunx`.
- `context7`: documentation lookup through `bunx` and `CONTEXT7_API_KEY`.
- `deepwiki`: remote repository architecture MCP.
- `grep`: remote Grep by Vercel MCP.
- `semgrep`: static analysis through `uvx --from semgrep semgrep mcp`.
- `shadcn`: shadcn/ui registry workflow through `bunx`.
- `dart-flutter`: Dart/Flutter MCP through `dart`.
- `figma`: remote Figma MCP through OAuth.
- `openaiDeveloperDocs`: official OpenAI and Codex documentation MCP.

## Current Behavior

Local MCP servers use explicit runtimes:

- `uvx`: `serena`, `semgrep`.
- `bunx`: `sequential-thinking`, `playwright`, `chrome-devtools`, `context7`, `shadcn`.
- `dart`: `dart-flutter`.

Repository `.mcp.json` intentionally stores portable commands (`uvx`, `bunx`, `dart`). Active system Codex config resolves them to absolute local paths:

- `/opt/homebrew/bin/uvx` for `serena` and `semgrep`.
- `/Users/rldyourmnd/.local/bin/bunx` for `sequential-thinking`, `playwright`, `chrome-devtools`, `context7`, and `shadcn`.
- `/opt/homebrew/bin/dart` for `dart-flutter`.

`scripts/install_system_codex.sh --apply` is the supported way to project portable `.mcp.json` definitions into the active system config. The installer reads `plugins/rldyour-mcps/.mcp.json` directly, then replaces portable commands with local executable paths. This avoids a duplicated hardcoded MCP server list in the installer.

`scripts/validate_marketplace.sh` has an `MCP config sync` step that compares repository `.mcp.json` with `/Users/rldyourmnd/.codex/config.toml`. It requires the same server names, command basenames, URLs, args, `env_vars`, `env`, startup timeouts, and tool timeouts. Absolute command-path resolution is the only expected difference.

`scripts/validate_marketplace.sh` has an `MCP pinning policy` step. It rejects `@latest`, requires exact `uvx --from package==version` package specs, and requires pinned bunx package specs.

Pinned local package specs in `.mcp.json`:

- `serena`: `serena-agent==1.2.0`.
- `sequential-thinking`: `@modelcontextprotocol/server-sequential-thinking@2025.12.18`.
- `playwright`: `@playwright/mcp@0.0.73`.
- `chrome-devtools`: `chrome-devtools-mcp@0.24.0`.
- `context7`: `@upstash/context7-mcp@2.2.3`.
- `semgrep`: `semgrep==1.161.0`.
- `shadcn`: `shadcn@4.6.0`.

`config/mcp-runtime-versions.env` stores the same pinned runtime package versions plus `CODEX_CLI_VERSION=0.128.0` and `MCP_PYTHON_SDK_VERSION=1.27.0`.

After commit `3128913 chore(mcp): update chrome devtools runtime pin`, `chrome-devtools-mcp` is pinned to `0.24.0` in both `config/mcp-runtime-versions.env` and `plugins/rldyour-mcps/.mcp.json`. `scripts/install_system_codex.sh --apply` projected that pin into `/Users/rldyourmnd/.codex/config.toml`, and `codex mcp get chrome-devtools` reports `chrome-devtools-mcp@0.24.0`.

`scripts/smoke_mcp_runtime.sh` checks that repository `.mcp.json` and installed `CODEX_HOME/config.toml` have the same server names, runs `codex mcp get <server>` for each server, verifies local command executables, and probes remote MCP URLs unless `--skip-url-check` is passed. It accepts remote HTTP responses below 500 as reachable endpoint negotiation responses.

`scripts/smoke_mcp_capabilities.py` uses the MCP Python SDK to create stdio or streamable HTTP sessions, call `initialize`, run `list_tools`, and compare discovered tool names against expected tools for all twelve configured MCP servers. Default full mode also runs safe deterministic `call_tool` probes where available:

- `serena`: `check_onboarding_performed`.
- `sequential-thinking`: `sequentialthinking`.
- `playwright`: `browser_navigate` to a `data:` URL and `browser_close`.
- `chrome-devtools`: `new_page` to a `data:` URL.
- `deepwiki`: `read_wiki_structure`.
- `grep`: `searchGitHub`.
- `semgrep`: `get_supported_languages`.
- `shadcn`: `get_project_registries`.
- `openaiDeveloperDocs`: `search_openai_docs`.

`context7` safe call is skipped when `CONTEXT7_API_KEY` is not present in the shell environment. `figma` is skipped by default because it requires OAuth; use `--include-auth` only when authenticated probing is intended. `dart-flutter` is list-only because no repository-independent safe project call is used by the smoke script.

Remote MCP servers use URL connections:

- `deepwiki`: `https://mcp.deepwiki.com/mcp`.
- `grep`: `https://mcp.grep.app`.
- `figma`: `https://mcp.figma.com/mcp`.
- `openaiDeveloperDocs`: `https://developers.openai.com/mcp`.

Startup timeouts are explicit to reduce startup race failures:

- Local MCP servers use `startup_timeout_sec: 90`.
- Remote MCP servers use `startup_timeout_sec: 60`.
- Tool timeouts are 120 or 180 seconds depending on expected workload.

Serena starts headless with `--enable-web-dashboard False`, `--open-web-dashboard False`, and `--project-from-cwd --context=codex`.

Playwright starts headless with `--caps=network,storage,testing,devtools`.

Chrome DevTools starts headless and isolated with `--no-usage-statistics` and `--no-performance-crux`.

`codex mcp list` verified that all twelve rldyour MCP servers are enabled in system Codex. `codex mcp get openaiDeveloperDocs` verifies the official OpenAI Docs MCP as a `streamable_http` remote endpoint. `figma` uses OAuth. `context7` reads `CONTEXT7_API_KEY` through an environment-variable reference. The real Context7 API key is not committed.

On the owner machine, Semgrep CLI is also installed through Homebrew at `/opt/homebrew/bin/semgrep` for direct local use. The repository MCP runtime remains pinned to `uvx --from semgrep==1.161.0 semgrep mcp`; do not replace that portable MCP definition with the Homebrew CLI unless the owner explicitly changes the reproducibility policy.

Semgrep authentication and Pro Engine availability are runtime state, not repository secrets. Verified local behavior: `semgrep show identity` and `uvx --from semgrep==1.161.0 semgrep show deployment` succeed without exposing tokens; `semgrep scan --pro` works for both the Homebrew CLI and the pinned `uvx` Semgrep runtime. The Semgrep MCP daemon may still print that DeepSemgrep/daemon mode is not running when the Semgrep deployment does not expose that capability; this does not by itself mean normal Semgrep MCP tools or `scan --pro` are broken.

## Contracts And Data

Allowed local runtimes are `uv`, `uvx`, `bun`, `bunx`, and `dart`. This plugin must not use `npx`, `npm`, or direct `node` commands for local MCP servers.

`context7` reads `CONTEXT7_API_KEY` through `env_vars`; the key is not stored in `.mcp.json`. `.env.example` contains only a placeholder.

`sequential-thinking` sets `DISABLE_THOUGHT_LOGGING: "true"`.

`openaiDeveloperDocs` is the preferred MCP source for OpenAI, Codex, model, API, plugin, skill, MCP, hook, and configuration documentation.

Do not store Semgrep auth output, deployment IDs, usernames, tokens, or organization details in repository files or memories. Only store the operational contract: repository MCP config is pinned and portable; local Semgrep auth/Pro state is managed outside the repository.

`rldyour-mcps` is the runtime dependency layer for automatic workflow plugins such as `rldyour-explore`, `rldyour-browser`, `rldyour-security`, `rldyour-serena-mcp`, and `rldyour-design`.

`scripts/smoke_clean_bootstrap.sh` validates this MCP runtime layer from committed source by installing into a temporary `CODEX_HOME`, running doctor with list-only capability smoke and a temporary `SERENA_HOME`, and verifying `codex mcp list`. The temporary `SERENA_HOME` prevents clean-bootstrap probes from writing temporary clone paths into `/Users/rldyourmnd/.serena/serena_config.yml`.

`.github/workflows/validate.yml` runs MCP registration, pinning, runtime smoke, and list-only capability smoke in CI through `scripts/validate_marketplace.sh` and `scripts/doctor_system_codex.sh`.

## Invariants

- Do not add behavior rules, skills, hooks, memories, or workflow commands to `rldyour-mcps`.
- Do not store real MCP credentials, tokens, cookies, or API keys in plugin files.
- Keep Serena dashboard disabled by default unless the owner explicitly changes the runtime policy.
- Keep Playwright and Chrome DevTools headless by default.
- Keep remote MCP servers as explicit URL connections.

## Change Rules

- When adding a local MCP, use only approved runtimes and set explicit startup/tool timeouts.
- Pin local launcher package versions. Do not use `@latest`.
- When adding a remote MCP, use explicit `url` and avoid local command wrappers.
- Document any new environment variable in `.env.example` with a placeholder only.
- After changing `.mcp.json`, update `config/mcp-runtime-versions.env` when package versions change, run `scripts/install_system_codex.sh --dry-run`, `scripts/install_system_codex.sh --apply`, and `scripts/doctor_system_codex.sh` so the installed runtime is synchronized.
- Run `scripts/smoke_mcp_runtime.sh` after MCP runtime changes to prove installed Codex can resolve every configured server.
- Run `scripts/smoke_mcp_capabilities.sh` after MCP runtime changes to prove tools can initialize and expose expected capabilities.
- Update `plugins/rldyour-mcps/README.md` and this memory when server names, runtimes, timeout policy, or secret handling changes.

## Verification

- `jq '{servers: (.mcpServers | keys)}' plugins/rldyour-mcps/.mcp.json`: lists configured MCP servers.
- `jq empty plugins/rldyour-mcps/.mcp.json plugins/rldyour-mcps/.codex-plugin/plugin.json`: validates JSON.
- `codex mcp list`: checks active MCP registration after plugin installation.
- `codex mcp get serena`, `codex mcp get figma`, `codex mcp get openaiDeveloperDocs`: checks representative local and remote MCP definitions.
- `scripts/validate_marketplace.sh`: checks installed MCP config synchronization and prints `MCP config in sync: 12 servers` when repository and system config match.
- `scripts/smoke_mcp_runtime.sh`: checks installed MCP runtime server metadata, local commands, and remote endpoints.
- `scripts/smoke_mcp_capabilities.sh`: checks MCP initialize, expected tool discovery, and safe call-tool probes.
- `scripts/smoke_clean_bootstrap.sh`: checks clean clone to temporary system install path.
- `.github/workflows/validate.yml`: checks MCP runtime state in GitHub Actions.
- `rg -n 'ctx7sk|password|secret|api[_-]?key|access[_-]?token|bearer|private[_-]?key' plugins/rldyour-mcps`: should show only placeholders or security text, not real credentials.
