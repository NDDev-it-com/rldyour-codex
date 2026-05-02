<!-- Memory Metadata
Last updated: 2026-05-02
Last commit: 5006272 feat(codex): add lsp and flow workflow plugins
Scope: plugins/rldyour-explore, plugins/rldyour-browser, plugins/rldyour-security, plugins/rldyour-serena-mcp, plugins/rldyour-design, plugins/rldyour-lsps, plugins/rldyour-flow, plugins/rldyour-mcps
Area: CORE
-->

# CORE_01_rldyour_plugin_auto_routing

## Purpose

The rldyour Codex plugin set is designed around automatic skill routing. Workflow plugins define `SKILL.md` descriptions, `Auto Invocation` sections, `agents/openai.yaml` metadata, and plugin manifest descriptions so Codex can select the correct workflow without the owner manually invoking `$skill` names.

## Source Of Truth

- `plugins/rldyour-*/.codex-plugin/plugin.json`: marketplace-facing plugin descriptions, capabilities, keywords, and default prompts.
- `plugins/rldyour-*/skills/*/SKILL.md`: primary automatic trigger surface through YAML frontmatter `description`.
- `plugins/rldyour-*/skills/*/agents/openai.yaml`: UI metadata and `policy.allow_implicit_invocation: true`.
- `plugins/rldyour-*/README.md`: human-readable trigger maps and plugin boundaries.
- `plugins/rldyour-mcps/.mcp.json`: MCP transport runtime layer used by workflow plugins.

## Entry Points

- `rldyour-explore`: auto-routes research requests. Use `tech-research` for technical docs, APIs, repository architecture, MCP/tool sources, and production GitHub patterns. Use `web-research` for current web information, source-backed facts, non-technical research, recommendations, and latest-state checks.
- `rldyour-browser`: auto-routes browser checks. Use `browser-validation` for visual/browser proof, screenshots, responsive checks, functional flows, and business behavior. Use `browser-debug` for console, network, runtime, hydration, layout, Lighthouse, performance, and memory diagnosis. Use `browser-tool-routing` when the browser workflow is unclear.
- `rldyour-security`: auto-routes security work. Use `owasp-top-10-implementation` for non-blocking secure implementation guidance. Use `ry-sec-review` for explicit security review, vulnerability audit, sensitive diff review, or source-to-sink security assessment.
- `rldyour-serena-mcp`: auto-routes code and memory work. Use `serena-code-workflow` for repository inspection, indexing, symbol-aware exploration, refactors, and non-trivial edits. Use `serena-memory-sync` after meaningful verified changes, Stop hook sync prompts, durable plans, or reusable research.
- `rldyour-design`: auto-routes design work. Use `ry-design` for end-to-end design implementation, with subskills for Figma-to-code, design systems, FSD placement, and design validation.
- `rldyour-lsps`: auto-routes language-server work. Use `lsp-routing` for choosing language-server workflows, `serena-lsp-integration` for Serena language key alignment, `lsp-health-check` for `$ry-lsp-check` verification, and `lsp-setup` for explicit brew-first setup.
- `rldyour-flow`: auto-routes SDLC command workflows. Use `ry-init` for scoped initialization, `ry-start` for feature/task lifecycle implementation, `ry-newp` for new-project planning, `ry-review` for report-only review, `ry-deploy` for server deployment verification, and `flow-post-task-sync` after meaningful work or Stop hook prompts.

## Current Behavior

All workflow skills in `rldyour-explore`, `rldyour-browser`, `rldyour-security`, `rldyour-serena-mcp`, `rldyour-design`, `rldyour-lsps`, and `rldyour-flow` keep `policy.allow_implicit_invocation: true`.

The owner communicates with Codex in Russian. Plugin docs, memory files, code comments, token files, and commit messages remain English. Skill descriptions are written in English but explicitly account for Russian or English user requests where relevant.

`rldyour-mcps` has no skills and cannot auto-invoke by itself. It is the runtime dependency layer for MCP tools used by automatic workflow plugins.

`rldyour-lsps` has no MCP transport definitions. It is a skills-only workflow layer for local LSP executables, project prerequisite checks, and Serena LSP integration guidance.

`rldyour-flow` has no MCP transport definitions. It is a skills-and-hooks workflow layer that coordinates existing workflow plugins, Serena memory freshness, project instruction docs, git history, GitHub sync, and branch/worktree cleanup.

## Contracts And Data

The primary auto-routing contract is the frontmatter `description` in each `SKILL.md`. When changing automatic behavior, update `SKILL.md` first, then keep `plugin.json`, `agents/openai.yaml`, and README trigger maps aligned.

Every callable skill contributed by these workflow plugins must keep `policy.allow_implicit_invocation: true`.

System Codex cache must be re-synced after plugin changes so the runtime uses the repository version after restart.

## Invariants

- Do not move MCP transport definitions into workflow plugins unless explicitly requested.
- Do not store secrets, raw tokens, cookies, or credentials in plugin metadata, README files, skills, memories, or marketplace metadata.
- Do not use `rldyour-mcps` for behavior policy; keep behavior in skills, rules, hooks, or future workflow plugins.
- Keep user-facing responses in Russian and repository artifacts in English unless the owner explicitly changes that rule.
- Keep browser artifacts under `browser/` and out of commits unless explicitly requested.

## Change Rules

- Use `skill-creator` guidance when adding or updating skills.
- Use `plugin-creator` guidance when adding or changing plugin manifests or marketplace metadata.
- Validate `SKILL.md` files after description changes.
- Validate `agents/openai.yaml` parse and `allow_implicit_invocation` after UI metadata changes.
- Re-sync changed plugin directories into the active Codex plugin cache.

## Verification

- `jq empty plugins/rldyour-*/.codex-plugin/plugin.json .agents/plugins/marketplace.json`: validates JSON metadata.
- `/opt/homebrew/bin/uv run --with pyyaml python <skill-creator>/scripts/quick_validate.py <skill-dir>`: validates skill frontmatter.
- `/opt/homebrew/bin/uv run --with pyyaml python -c '<parse agents/openai.yaml files>'`: validates OpenAI skill metadata and implicit invocation policy.
- `diff -qr plugins/<plugin> <codex-plugin-cache>/<plugin>/local`: verifies the system cache matches the repository plugin.
