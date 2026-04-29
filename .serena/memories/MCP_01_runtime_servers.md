<!-- Memory Metadata
Last updated: 2026-04-29
Last commit: b1bf776 docs(serena): record plugin auto routing
Scope: plugins/rldyour-mcps/.mcp.json, plugins/rldyour-mcps/.codex-plugin/plugin.json, plugins/rldyour-mcps/README.md, plugins/rldyour-mcps/.env.example
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

## Current Behavior

Local MCP servers use explicit runtimes:

- `uvx`: `serena`, `semgrep`.
- `bunx`: `sequential-thinking`, `playwright`, `chrome-devtools`, `context7`, `shadcn`.
- `dart`: `dart-flutter`.

Remote MCP servers use URL connections:

- `deepwiki`: `https://mcp.deepwiki.com/mcp`.
- `grep`: `https://mcp.grep.app`.
- `figma`: `https://mcp.figma.com/mcp`.

Startup timeouts are explicit to reduce startup race failures:

- Local MCP servers use `startup_timeout_sec: 90`.
- Remote MCP servers use `startup_timeout_sec: 60`.
- Tool timeouts are 120 or 180 seconds depending on expected workload.

Serena starts headless with `--open-web-dashboard False` and `--project-from-cwd --context=codex`.

Playwright starts headless with `--caps=network,storage,testing,devtools`.

Chrome DevTools starts headless and isolated with `--no-usage-statistics` and `--no-performance-crux`.

## Contracts And Data

Allowed local runtimes are `uv`, `uvx`, `bun`, `bunx`, and `dart`. This plugin must not use `npx`, `npm`, or direct `node` commands for local MCP servers.

`context7` reads `CONTEXT7_API_KEY` through `env_vars`; the key is not stored in `.mcp.json`. `.env.example` contains only a placeholder.

`sequential-thinking` sets `DISABLE_THOUGHT_LOGGING: "true"`.

`rldyour-mcps` is the runtime dependency layer for automatic workflow plugins such as `rldyour-explore`, `rldyour-browser`, `rldyour-security`, `rldyour-serena-mcp`, and `rldyour-design`.

## Invariants

- Do not add behavior rules, skills, hooks, memories, or workflow commands to `rldyour-mcps`.
- Do not store real MCP credentials, tokens, cookies, or API keys in plugin files.
- Keep Serena dashboard disabled by default unless the owner explicitly changes the runtime policy.
- Keep Playwright and Chrome DevTools headless by default.
- Keep remote MCP servers as explicit URL connections.

## Change Rules

- When adding a local MCP, use only approved runtimes and set explicit startup/tool timeouts.
- When adding a remote MCP, use explicit `url` and avoid local command wrappers.
- Document any new environment variable in `.env.example` with a placeholder only.
- Update `plugins/rldyour-mcps/README.md` and this memory when server names, runtimes, timeout policy, or secret handling changes.

## Verification

- `jq '{servers: (.mcpServers | keys)}' plugins/rldyour-mcps/.mcp.json`: lists configured MCP servers.
- `jq empty plugins/rldyour-mcps/.mcp.json plugins/rldyour-mcps/.codex-plugin/plugin.json`: validates JSON.
- `codex mcp list`: checks active MCP registration after plugin installation.
- `codex mcp get serena`, `codex mcp get figma`: checks representative local and remote MCP definitions.
- `rg -n 'ctx7sk|password|secret|api[_-]?key|access[_-]?token|bearer|private[_-]?key' plugins/rldyour-mcps`: should show only placeholders or security text, not real credentials.
