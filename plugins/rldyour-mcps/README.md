# rldyour-mcps

`rldyour-mcps` is the controlled MCP server set the owner uses in Codex.

User-facing conversation stays in Russian unless the owner asks otherwise. Repository documentation, plugin metadata, code comments, commits, memory files, plans, and research archives are written in English. Technical identifiers stay ASCII and kebab-case to keep Codex, MCP clients, and tooling compatible.

## Responsibility Boundary

This plugin is responsible only for connecting MCP servers.

It does not define global agent behavior, store project memory, provide workflow commands, replace security policy, or add skills. This means it has no `SKILL.md` trigger surface and cannot auto-invoke by itself. Automatic behavior belongs to dedicated skills in plugins such as `rldyour-explore`, `rldyour-browser`, `rldyour-security`, `rldyour-serena-mcp`, `rldyour-design`, `rldyour-rules`, `rldyour-flow`, and future MCP-specific workflow plugins.

This plugin is the runtime dependency layer those automatic skills use when they need MCP tools.

## Runtime Rule

All local MCP servers must run only through owner-approved runtimes:

- `uv` / `uvx`;
- `bun` / `bunx`;
- `dart`.

This plugin does not use `npx`, `npm`, or direct `node` commands for MCP servers. Remote MCP servers with `url` remain URL connections and do not start local processes.

Local MCP launcher packages are pinned for reproducibility. Do not use `@latest` or unpinned `uvx --from` package specs in `.mcp.json`. Update versions intentionally in both `.mcp.json` and `config/mcp-runtime-versions.env`, then run MCP capability smoke.

## Stable Startup Rule

Codex starts MCP servers as a batch during session startup. `startup_timeout_sec` covers not only process launch, but also the MCP handshake: `initialize` and the first tool list. Every MCP in this plugin therefore has an explicit timeout instead of relying on Codex's shorter default.

Local MCP servers use `startup_timeout_sec = 90`. Remote MCP servers use `startup_timeout_sec = 60`. This reduces random failures near the end of startup when multiple `uvx` / `bunx` servers resolve dependencies or wait on network calls at the same time.

## Language Rule

- User-facing conversation with the owner is Russian unless requested otherwise.
- Repository documentation and plugin metadata are English.
- MCP names, package names, commands, environment variables, and URLs are not translated.
- If an MCP returns English data, the agent briefly explains the result to the owner in Russian.

## Security Rule

- Secrets are never written to `.mcp.json`, `plugin.json`, README files, or marketplace metadata.
- MCP write tools are used only when the task explicitly requires state changes.
- Destructive actions require separate owner confirmation.
- Remote MCP servers are used only through explicitly configured URLs.
- Local MCP servers run only through `uv`, `uvx`, `bun`, `bunx`, or `dart`.

## Connected MCP Servers

| MCP | Purpose | Runtime |
| --- | --- | --- |
| `serena` | Semantic navigation, analysis, and precise code editing | `uvx`, headless |
| `sequential-thinking` | Structured reasoning and planning | `bunx` |
| `playwright` | Browser automation, UI checks, network/storage/testing/devtools workflows | `bunx`, headless |
| `chrome-devtools` | Page diagnostics through Chrome DevTools | `bunx`, headless, isolated |
| `context7` | Current library documentation | `bunx`, `CONTEXT7_API_KEY` |
| `deepwiki` | Repository documentation and explanations | remote URL |
| `grep` | Search across public GitHub repositories | remote URL |
| `github` | GitHub repositories, issues, pull requests, users, and context | `github-mcp-server stdio`, `GITHUB_PERSONAL_ACCESS_TOKEN` |
| `semgrep` | Static analysis and security checks | `uvx --from semgrep==1.163.0 semgrep mcp` |
| `shadcn` | shadcn/ui registry work | `bunx` |
| `dart-flutter` | Dart/Flutter MCP for Dart and Flutter projects | `dart` |
| `figma` | Figma design context | remote URL, OAuth |
| `openaiDeveloperDocs` | Official OpenAI and Codex product documentation | remote URL |

## Secrets

Do not write keys into `.mcp.json`.

Context7 requires this environment variable:

```bash
export CONTEXT7_API_KEY="ctx7sk_..."
```

The owner's current key is intentionally not stored in this repository.

GitHub MCP requires the official `github-mcp-server` binary on `PATH` and this
environment variable:

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="<github-token>"
```

The server is restricted to `context,repos,issues,pull_requests,users` so
repository, issue, and PR workflows have parity without exposing every GitHub
toolset by default.

The CI/runtime pin for this binary is `GITHUB_MCP_SERVER_VERSION` in
`config/mcp-runtime-versions.env`. GitHub Actions installs the matching release
archive from `github/github-mcp-server` and verifies its published SHA-256
checksum before strict runtime validation.

## Codex Verification

After installing or updating the plugin, check:

```bash
codex mcp list
codex mcp get serena
codex mcp get figma
scripts/smoke_mcp_runtime.sh
scripts/smoke_mcp_capabilities.sh
```

Expected state:

- `serena` starts through `uvx` with the web dashboard disabled.
- `playwright` starts through `bunx` with `--caps=network,storage,testing,devtools`.
- `figma` uses OAuth.
- `context7` reads its key only from `CONTEXT7_API_KEY`.
- `semgrep` starts through the current official `semgrep mcp`, not the archived `semgrep-mcp`.
- `openaiDeveloperDocs` uses the official OpenAI Docs MCP endpoint for OpenAI and Codex product documentation.
- Runtime smoke checks remote URL servers with a Streamable HTTP `initialize` POST preflight. Auth-gated endpoints may return `401`/`403`; `405` is treated as a GET/SSE compatibility signal, not a passing POST result.
- Local MCP servers do not use `npx`, `npm`, or direct `node` commands.

## Local Dependencies

Before use, verify these commands are available:

```bash
uv --version
uvx --version
bun --version
bunx --help
dart --version
github-mcp-server --help
```

## Figma

Figma uses the remote MCP endpoint:

```text
https://mcp.figma.com/mcp
```

After plugin installation, browser/OAuth authorization may be required. If Codex does not request it automatically, use the MCP login mechanism for the `figma` server.

## Serena

Serena is configured without starting or opening the web dashboard:

```text
uvx --from serena-agent==1.5.1 --python 3.13 --prerelease allow serena start-mcp-server --project-from-cwd --context=codex --enable-web-dashboard False --open-web-dashboard False
```

If the dashboard is needed manually, change this runtime policy intentionally and re-run the system installer.

## Sources

- Serena: https://oraios.github.io/serena/02-usage/030_clients.html
- Serena dashboard: https://oraios.github.io/serena/02-usage/060_dashboard.html
- Context7: https://www.mintlify.com/upstash/context7/mcp/configuration
- Codex MCP configuration: https://developers.openai.com/codex/mcp
- Playwright MCP: https://playwright.dev/mcp/configuration/options
- Chrome DevTools MCP: https://github.com/ChromeDevTools/chrome-devtools-mcp
- DeepWiki MCP: https://mcp.deepwiki.com/
- Grep by Vercel: https://vercel.com/blog/grep-a-million-github-repositories-via-mcp-1H5Bmvo4XKswf0TpZIOmEI
- Semgrep MCP: https://semgrep.dev/docs/mcp
- Semgrep MCP legacy repo: https://github.com/semgrep/mcp
- shadcn MCP: https://ui.shadcn.com/docs/mcp
- Dart/Flutter MCP: https://docs.flutter.dev/ai/mcp-server
- Figma MCP: https://help.figma.com/hc/en-us/articles/39888629089175-Codex-and-Figma-Set-up-the-MCP-server
- OpenAI Docs MCP: https://developers.openai.com/learn/docs-mcp
- MCP Streamable HTTP transport: https://modelcontextprotocol.io/specification/2025-11-25/basic/transports
- MCP lifecycle initialization: https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle
