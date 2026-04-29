# rldyour-explore

`rldyour-explore` is a skills-only research workflow plugin for Codex.

It does not configure MCP servers directly. Context7, DeepWiki, Grep by Vercel, and web/browser capabilities are provided by the active Codex environment and `rldyour-mcps`; this plugin defines when and how Codex should use research workflows.

User-facing conversation stays in Russian unless the owner asks otherwise. Repository documentation is written in English.

## Auto Invocation

The plugin is optimized for automatic skill selection. Codex should route research work to these skills when a task asks to research, investigate, study the internet, look up current information, inspect documentation, find best practices, compare approaches, verify facts with sources, or close unknowns before implementation.

`policy.allow_implicit_invocation` is enabled for every skill. The primary trigger surface is each `SKILL.md` frontmatter `description`; plugin manifest descriptions and `agents/openai.yaml` metadata mirror the same intent for marketplace and UI discovery.

## Trigger Map

- Technical docs, APIs, frameworks, SDKs, migrations, MCP/tool sources, repository architecture, or production GitHub patterns: use `tech-research`.
- Current information, authoritative source links, latest status, non-technical research, recommendations, pricing, legal/security updates, standards, or web-only evidence: use `web-research`.
- Technical implementation that needs both MCP evidence and fresh web context: use `tech-research` first, then `web-research`.

## Skills

- `tech-research`: Context7 for official docs, DeepWiki for repository architecture, and Grep by Vercel for real GitHub usage patterns.
- `web-research`: source-backed internet research through web search/browser with scope definition, source quality checks, and concise conclusions.
