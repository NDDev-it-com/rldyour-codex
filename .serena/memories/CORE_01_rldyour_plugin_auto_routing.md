<!-- Memory Metadata
Last updated: 2026-05-02
Last commit: ca06abf docs: sync flow catalog description
Scope: plugins/rldyour-flow, plugins/rldyour-*, AGENTS.md, system/AGENTS.md, /Users/rldyourmnd/.codex/config.toml
Area: CORE
-->

# CORE_01_rldyour_plugin_auto_routing

## Purpose

The rldyour Codex plugin set is designed around automatic skill routing for the owner's personal Codex runtime. Workflow plugins define `SKILL.md` descriptions, `Auto Invocation` sections, `agents/openai.yaml` metadata, and plugin manifest descriptions so Codex can select the correct workflow without the owner manually invoking `$skill` names.

## Source Of Truth

- `plugins/rldyour-*/.codex-plugin/plugin.json`: marketplace-facing plugin descriptions, capabilities, keywords, and default prompts.
- `plugins/rldyour-*/skills/*/SKILL.md`: primary automatic trigger surface through YAML frontmatter `description`.
- `plugins/rldyour-*/skills/*/agents/openai.yaml`: UI metadata and invocation policy.
- `plugins/rldyour-*/README.md`: human-readable trigger maps and plugin boundaries.
- `plugins/rldyour-mcps/.mcp.json`: MCP transport runtime layer used by workflow plugins.
- `/Users/rldyourmnd/.codex/config.toml`: active system Codex plugin enablement and MCP registrations.

## Entry Points

- `rldyour-explore`: auto-routes research requests. Use `tech-research` for technical docs, APIs, repository architecture, MCP/tool sources, and production GitHub patterns. Use `web-research` for current web information, source-backed facts, non-technical research, recommendations, and latest-state checks.
- `rldyour-browser`: auto-routes browser checks. Use `browser-validation` for visual/browser proof, screenshots, responsive checks, functional flows, and business behavior. Use `browser-debug` for console, network, runtime, hydration, layout, Lighthouse, performance, and memory diagnosis. Use `browser-tool-routing` when the browser workflow is unclear.
- `rldyour-security`: auto-routes security work. Use `owasp-top-10-implementation` for non-blocking secure implementation guidance. Use `ry-sec-review` for explicit security review, vulnerability audit, sensitive diff review, or source-to-sink security assessment.
- `rldyour-serena-mcp`: auto-routes code and memory work. Use `serena-code-workflow` for repository inspection, indexing, symbol-aware exploration, refactors, and non-trivial edits. Use `serena-memory-sync` after meaningful verified changes, Stop hook sync prompts, durable plans, or reusable research.
- `rldyour-design`: auto-routes design work. Use `ry-design` for end-to-end design implementation, with subskills for Figma-to-code, design systems, FSD placement, and design validation.
- `rldyour-lsps`: auto-routes language-server work. Use `lsp-routing` for choosing language-server workflows, `serena-lsp-integration` for Serena language key alignment, `lsp-health-check` for `$ry-lsp-check` verification, and `lsp-setup` for explicit brew-first setup.
- `rldyour-flow`: auto-routes SDLC command workflows. Use `ry-init` for scoped context-pack initialization, `ry-start` for feature/task lifecycle implementation with a context sufficiency gate, `ry-newp` for new-project planning, `ry-review` for report-only review, `ry-deploy` for server deployment verification, and `flow-post-task-sync` after meaningful work or Stop hook prompts.
- `rldyour-rules`: auto-routes quality-first engineering rules. Use `quality-first-engineering` for clean code and no-hacks policy, `architecture-boundaries` for FSD/VSA placement, `implementation-discipline` for synchronized implementation, `dependency-compatibility-policy` for latest-compatible dependencies, `verification-quality-gates` for evidence, `project-instructions-policy` for `AGENTS.md`/`CLAUDE.md`/ADR rules, and `ry-rules-review` for explicit rules audits.

## Current Behavior

The active rldyour marketplace contributes nine plugins: `rldyour-mcps`, `rldyour-explore`, `rldyour-serena-mcp`, `rldyour-security`, `rldyour-browser`, `rldyour-design`, `rldyour-lsps`, `rldyour-flow`, and `rldyour-rules`.

Most workflow skills in `rldyour-explore`, `rldyour-browser`, `rldyour-security`, `rldyour-serena-mcp`, `rldyour-design`, `rldyour-lsps`, `rldyour-flow`, and `rldyour-rules` keep `policy.allow_implicit_invocation: true`.

The six `rldyour-flow` reviewer track skills set `policy.allow_implicit_invocation: false` and are orchestrated by `ry-start` or `ry-review`: `flow-architecture-review`, `flow-quality-review`, `flow-consistency-review`, `flow-integration-review`, `flow-verification-review`, and `flow-security-review`.

The owner communicates with Codex in Russian. Plugin docs, memory files, code comments, token files, and commit messages remain English. Every callable rldyour skill must include compact Russian and English trigger phrases in `SKILL.md` frontmatter `description`, because Codex uses the description as the primary routing surface.

Commit `6af53aa feat(skills): optimize plugin routing metadata` compacted all 37 callable rldyour skill descriptions. The current maximum description length is 187 characters and the average length is 166.8 characters. `scripts/validate_marketplace.sh` now fails when a callable rldyour skill description is longer than 240 characters, is duplicated, lacks Cyrillic trigger text, or lacks English trigger text.

`rldyour-mcps` has no skills and cannot auto-invoke by itself. It is the runtime dependency layer for MCP tools used by automatic workflow plugins.

`rldyour-lsps` has no MCP transport definitions. It is a skills-only workflow layer for local LSP executables, project prerequisite checks, and Serena LSP integration guidance.

`rldyour-flow` has no MCP transport definitions. It is a skills-and-hooks workflow layer that coordinates existing workflow plugins, Serena memory freshness, project instruction docs, git history, GitHub sync, and branch/worktree cleanup.

Commit `e506ccb feat(flow): add context sufficiency hooks` added two non-blocking flow hook entry points:

- `SessionStart`: emits compact repository context through `hookSpecificOutput.additionalContext`.
- `PostToolUse` with matcher `Bash`: emits commit quality advice through `systemMessage` after `git commit` commands when warnings exist.

The same commit added `references/init-context-pack.md` and `references/context-sufficiency-gate.md` as the detailed contracts for deep `ry-init` initialization and safe `ry-start` pre-edit context.

`rldyour-rules` has no MCP transport definitions and no hooks. It is a skills-only policy layer that coordinates quality, architecture, dependency, verification, project-instruction, and ADR rules with existing workflow plugins.

`plugins/rldyour-flow/skills/ry-start/SKILL.md` contains an `Automatic Helper Routing` section. It explicitly routes Russian `ry-start` prompts to helper workflows: Serena/code/LSP/rules for code work, `tech-research` plus optional `web-research` for technical internet research, browser skills for browser-visible work, design skills for Figma/UI/design-system work, security skills for sensitive work, and verification/memory/post-task sync before final delivery.

Current skill directory counts verified from repository files:

- `rldyour-browser`: 3 skills.
- `rldyour-design`: 5 skills.
- `rldyour-explore`: 2 skills.
- `rldyour-flow`: 12 skills.
- `rldyour-lsps`: 4 skills.
- `rldyour-rules`: 7 skills.
- `rldyour-security`: 2 skills.
- `rldyour-serena-mcp`: 2 skills.

## Contracts And Data

The primary auto-routing contract is the frontmatter `description` in each `SKILL.md`. When changing automatic behavior, update `SKILL.md` first, then keep `plugin.json`, `agents/openai.yaml`, and README trigger maps aligned.

Every callable workflow skill should keep `policy.allow_implicit_invocation: true` unless it is an orchestrated-only reviewer track. The current orchestrated-only exception list is encoded in `scripts/validate_marketplace.sh`.

System Codex cache must be re-synced after plugin changes so the runtime uses the repository version after restart. Active cache roots are under `/Users/rldyourmnd/.codex/plugins/cache/rldyour-codex/<plugin>/local`.

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
- Keep compact Russian and English trigger phrases in every callable rldyour skill description; `scripts/validate_marketplace.sh` enforces this through the `Skill routing descriptions` step.
- Validate `agents/openai.yaml` parse, default prompt length, `$skill-name` prompt reference, short description length, MCP dependencies, and implicit invocation policy after UI metadata changes.
- Re-sync changed plugin directories into the active Codex plugin cache.
- Restart Codex after changing skill descriptions, manifests, hook definitions, or MCP server definitions.

## Verification

- `jq empty plugins/rldyour-*/.codex-plugin/plugin.json .agents/plugins/marketplace.json`: validates JSON metadata.
- `/opt/homebrew/bin/uv run --with pyyaml python <skill-creator>/scripts/quick_validate.py <skill-dir>`: validates skill frontmatter.
- `scripts/validate_marketplace.sh`: validates compact bilingual skill routing descriptions, OpenAI skill metadata, MCP dependencies, cache sync, scripts, LSP health, and secret patterns.
- `diff -qr plugins/<plugin> <codex-plugin-cache>/<plugin>/local`: verifies the system cache matches the repository plugin.
