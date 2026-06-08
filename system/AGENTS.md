# rldyour Codex Global Instructions

## Purpose

This file is the compact global Codex instruction layer installed as
`~/.codex/AGENTS.md`. Detailed workflows live in rldyour plugins, skills,
references, docs, and Serena memories so Codex only loads them when relevant.

The owner sets direction and priorities. Codex implements: research, code,
verification, documentation, git synchronization, and release follow-through.

## Language

- User-facing conversation with the owner is Russian unless explicitly requested otherwise.
- Repository artifacts are English: code, comments, commits, docs, ADRs, Serena memories, plans, and research archives.
- Technical identifiers stay ASCII, stable, and kebab-case where applicable.

## Operating Rules

- Quality and correctness outrank speed.
- No hacks, fake implementations, swallowed errors, hidden debt, or fake green checks.
- Code/config/tests are the source of truth. Docs and memories must reflect verified state.
- Keep semantic entropy low: reuse local patterns, keep boundaries clear, avoid duplicate policy sources.
- Use current source-backed dependency and product facts; do not upgrade or migrate blindly.
- Do not commit secrets, runtime markers, browser artifacts, caches, or accidental local state.
- Do not revert user changes unless explicitly requested.

## Plugin Router

Use installed rldyour plugins automatically when the task matches their scope:

- `rldyour-flow`: `ry-init`, `ry-start`, `ry-review`, `ry-repair`, `ry-deploy`, instruction docs sync, post-task sync, fullrepo publish, and lifecycle hooks.
- `rldyour-serena-mcp`: code understanding, semantic inspection/refactor, and Serena memory sync.
- `rldyour-explore`: official docs, upstream research, web evidence, and current-version checks.
- `rldyour-rules`: quality, architecture, dependency policy, verification gates, ADR and instruction policy.
- `rldyour-lsps`: language-server routing, health checks, and Serena/LSP integration.
- `rldyour-browser`: browser validation/debugging, screenshots, user flows, console/network/runtime.
- `rldyour-design`: Figma-to-code, design systems, tokens, i18n, FSD, shadcn/ui, ReactBits.
- `rldyour-security`: OWASP-oriented implementation guidance and defensive `$ry-sec-review`.
- `rldyour-mcps`: MCP runtime only; never treat it as a behavior policy plugin.

Curated `github@openai-curated` and `gmail@openai-curated` are intentionally enabled.
For OpenAI, Codex, API, model, plugin, skill, MCP, hook, or config facts, use the official
OpenAI Docs MCP before general web search when it is available.

## Tool Priority

- Code structure: Serena overview/symbol tools first; targeted file reads and `rg` for docs, JSON, shell, or unsupported text.
- Technical docs: Context7/OpenAI Docs MCP/official sources first; web search only when needed.
- Repo architecture: DeepWiki/source reads when appropriate.
- Planning: Sequential Thinking when available for non-trivial decisions.
- Browser-visible changes: Playwright CLI validation and Chrome DevTools MCP diagnosis when relevant.
- Security-sensitive changes: project security scripts, CI security artifacts, and manual review where applicable.

## Codex System Contract

- Owner-standard profile is full-auto/YOLO: `approval_policy = "never"` and `sandbox_mode = "danger-full-access"`.
- Safe mode is explicit only: `scripts/install_system_codex.sh --apply --safe-mode`.
- Do not mix Codex permission profiles (`default_permissions` or `[permissions]`) with legacy `sandbox_mode` in the same active config layer.
- Current profile files are `$CODEX_HOME/<name>.config.toml`; do not restore legacy `profile = "..."` or `[profiles.*]`.
- Required features: `[features].hooks = true` and `[features].multi_agent = true`.
- Parent model default is `gpt-5.5` with `model_reasoning_effort = "xhigh"`.
- Managed subagents use `gpt-5.5` with `model_reasoning_effort = "medium"` unless explicitly changed by the owner.
- Deprecated aliases such as `codex_hooks`, `plugin_hooks`, legacy web-search flags, `experimental_instructions_file`, `background_terminal_timeout`, `experimental_use_unified_exec_tool`, `use_legacy_landlock`, legacy profile selectors, and active `default_permissions` with `sandbox_mode` must not be present.

## Native Boundaries

- Codex workflows are plugins and skills, not copied Claude/OpenCode slash-command files.
- Plugin manifests live in `.codex-plugin/plugin.json`.
- Repo marketplace lives in `.agents/plugins/marketplace.json`.
- Skills live in `plugins/<plugin>/skills/*/SKILL.md`; OpenAI metadata lives in sibling `agents/openai.yaml`.
- Source MCP definitions live in `plugins/rldyour-mcps/.mcp.json`; runtime Codex MCP config is TOML `[mcp_servers.*]`.
- Plugin-bundled hooks are discoverable from manifests, but hook execution still requires trusted hook hashes refreshed by the installer through `hooks/list`.
- Flow owns the ordered Stop lifecycle. Serena memory sync is child-dispatched by Flow and must not be registered as a competing Stop hook.

## Subagents

- Use subagents only when explicitly allowed by the user, an active workflow, or current system instructions.
- Subagent prompts must be self-contained: task, context, constraints, expected output, read/write scope, risks.
- Do not spawn subagents for trivial one-file work.
- Managed role files live in `${CODEX_HOME:-$HOME/.codex}/agents/*.toml` and are installed from `system/agents/*.toml`.
- Temporary specialist-MCP isolation is intentional: disabled specialist servers must copy full transport metadata from `plugins/rldyour-mcps/.mcp.json`; `codex_apps` is inherited and must not be declared as a synthetic MCP server.

## Memories And Docs

- Store durable facts only in `.serena/memories/`: paths, entry points, behavior, contracts, invariants, update triggers, verification.
- Store reusable plans in `.serena/plans/` and long source-backed research in `.serena/research/`.
- Do not store chat logs, speculation, secrets, raw tokens, cookies, or credentials.
- After meaningful code/config/workflow/release changes, sync Serena memories first, then durable instruction docs if verified project facts changed.
- `AGENTS.md` and `.claude/CLAUDE.md` are separate first-class files optimized for their CLIs; do not collapse Claude docs into an `@AGENTS.md` import.

## Git And Delivery

- Prefer atomic Conventional Commits.
- Split unrelated implementation, validators/tests, docs/instructions, metadata/generated artifacts, and Serena/fullrepo sync when independently reviewable.
- Do not force-push `main`. Do not rewrite pushed history without explicit owner approval.
- Run checks matching the touched scope and report exact commands.
- If changes are committed, push when synchronization or release workflow requires it.
- In fullrepo-managed repositories, keep agent-only files out of normal branches; restore/publish them through `fullrepo`.
- Standard finish order: Serena memories and instruction docs, checks, atomic normal-branch commits, push, publish `fullrepo` with safe force-with-lease, cleanup merged workflow branches/worktrees when safe.

## Key Commands

Use repository-local scripts when present:

```bash
scripts/install_system_codex.sh --dry-run
scripts/install_system_codex.sh --apply
scripts/install_system_codex.sh --apply --safe-mode
scripts/doctor_system_codex.sh --quick --strict-runtime
scripts/validate_fast.sh
scripts/validate_runtime.sh --strict-runtime
scripts/validate_release.sh
scripts/validate_execpolicy_rules.sh
python3 scripts/validate_agent_tools.py
python3 scripts/validate_contract.py
python3 scripts/validate_skill_routing.py
python3 scripts/validate_plugin_versions.py
python3 scripts/validate_instruction_docs.py --require-agent-docs
python3 scripts/check_serena_memory_freshness.py
uv run --with pytest --with pytest-cov --with pyyaml python -m pytest
scripts/sync_fullrepo_branch.sh --status
scripts/sync_fullrepo_branch.sh --bootstrap-init
scripts/sync_fullrepo_branch.sh --publish
```

Restart Codex after changing global `AGENTS.md`, `~/.codex/config.toml`, installed plugins, hooks, skills, managed agents, rules, or MCP runtime definitions.
