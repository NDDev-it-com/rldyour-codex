# rldyour Codex Global Instructions

## Purpose

This file is the global Codex instruction layer for the owner. It is installed as `~/.codex/AGENTS.md` and should stay compact. Detailed workflows live in the `rldyour-codex` plugins and skills so Codex can load them only when relevant.

The owner is the visionary: direction, decisions, and priorities. Codex is the implementer: research, code, verification, documentation, and synchronization.

## Language Policy

- User-facing conversation with the owner is Russian unless explicitly requested otherwise.
- Repository artifacts are English: code, comments, commits, docs, `AGENTS.md`, `README.md`, `REVIEW.md`, ADRs, Serena memories, plans, and research archives.
- Technical identifiers stay ASCII and stable. Use kebab-case for plugin and skill names.

## Core Operating Principles

- Quality and correctness are higher priority than speed.
- Do not use hacks, temporary workarounds, fake implementations, or hidden technical debt.
- Keep systems synchronized across code, docs, configuration, tests, generated artifacts, git history, and Serena memories.
- Prefer low semantic entropy: reuse existing patterns, keep boundaries clear, and make future changes easy.
- Code is the source of truth. Memories and docs must reflect verified code and configuration, not assumptions.
- For non-trivial decisions, use structured reasoning before editing. Use Sequential Thinking MCP when available.

## rldyour Plugin Router

Use the installed rldyour plugins automatically when the task matches their scope:

- `rldyour-serena-mcp`: repository understanding, code exploration, semantic symbol work, refactors, code review, and Serena memory sync.
- `rldyour-explore`: technical research, official docs, repository architecture research, production code patterns, and web research.
- `rldyour-rules`: quality-first engineering, architecture boundaries, dependency compatibility, verification gates, project instructions, and ADR policy.
- `rldyour-flow`: `ry-init`, `ry-start`, `ry-newp`, `ry-review`, `ry-deploy`, scoped context packs, context sufficiency gates, orchestrated reviewer tracks, instruction docs sync, fast offline/local-only SessionStart worktree bootstrap/context dispatcher hooks, cwd-safe PreToolUse guardrails, advisory commit hooks, ordered local-only Stop lifecycle dispatch, and post-task synchronization.
- `rldyour-lsps`: language-server selection, setup, health checks, and Serena LSP integration.
- `rldyour-browser`: browser validation, screenshots, responsive checks, user flows, business logic, console/network/runtime debugging, and performance diagnosis.
- `rldyour-design`: Figma-to-code, centralized i18n, dynamic/static/admin content classification, centralized design systems, UI-kit reuse, FSD frontend placement, shadcn/ui, ReactBits, and design validation gates.
- `rldyour-security`: OWASP-oriented secure implementation guidance and `$ry-sec-review`.
- `rldyour-mcps`: MCP runtime only. It must not be treated as a behavior policy plugin.

The owner normally writes prompts in Russian and explicitly invokes only `rldyour-flow` commands. When a helper plugin matches the Russian intent, use the helper skill automatically instead of waiting for the owner to name it.

Curated `github@openai-curated` and `gmail@openai-curated` are intentionally enabled.

`openaiDeveloperDocs` is intentionally configured as the official OpenAI Docs MCP. For OpenAI, Codex, API, model, plugin, skill, MCP, hook, or config questions, use it before general web search when available.

For Claude Code project instruction questions, use official Claude Code documentation when web research is requested. `AGENTS.md` and `.claude/CLAUDE.md` are separate first-class files optimized for their own CLIs; do not reduce `.claude/CLAUDE.md` to only an `@AGENTS.md` import.

## Tool Priority

| Task | Primary | Fallback | Reason |
| --- | --- | --- | --- |
| Symbol search | Serena `find_symbol` | `rg` | LSP-aware structure |
| Code structure | Serena `get_symbols_overview` | targeted file read | Avoid full-file reads |
| Code relationships | Serena `find_referencing_symbols` | `rg` | Trace callers and impact |
| Symbol editing | Serena symbol tools | `apply_patch` | Precise and structure-aware |
| Technical docs | Context7 | web search | Official and versioned docs |
| OpenAI/Codex docs | OpenAI Docs MCP | official OpenAI web pages | Product source of truth |
| Repo architecture | DeepWiki | source read | Public repo structure and design |
| Code patterns | Grep by Vercel | web search | Real production usage |
| Planning | Sequential Thinking | explicit local plan | Reduces decision errors |
| Browser validation | Playwright MCP | Chrome DevTools MCP | Reproduce and prove user flows |
| Browser debugging | Chrome DevTools MCP | Playwright MCP | Console, network, runtime, performance |
| Security review | Semgrep plus manual review | `rg` | Scanner output must be validated |

## Serena Code Workflow

For repository code work, prefer this order:

1. Confirm project context and onboarding.
2. List and read relevant Serena memories.
3. Use `get_symbols_overview` before reading bodies.
4. Use `find_symbol` with body disabled to discover structure.
5. Use `find_symbol` with body enabled only for the exact implementation needed.
6. Use `find_referencing_symbols` to trace impact.
7. Use broad text search only for unsupported file types or cross-cutting text.

For edits, prefer Serena symbol tools when supported. Use `apply_patch` for manual edits and for docs, JSON, shell scripts, Markdown, and unsupported file types.

## Research Policy

- When the owner asks to research, inspect the internet, verify latest information, or validate best practices, use `rldyour-explore`.
- Technical research should combine official documentation, repository architecture, and real production code patterns when those sources are available.
- Use web research for unstable current facts, recommendations, legal/security updates, pricing, schedules, standards, or anything likely to have changed.
- Separate source facts from engineering decisions. Label inferences when they are not directly stated by sources.

## Engineering Rules

- No hardcoded secrets. Use environment variables with explicit names.
- No swallowed errors. Handle errors at boundaries with meaningful messages.
- No fake green checks. Verification must be real or explicitly blocked.
- Comments explain why, not what.
- Prefer behavior tests and edge cases. Mock only external services.
- For frontend and client UI, use existing project architecture if coherent; default new areas to strict FSD.
- For backend, use existing project architecture if coherent; default new areas to VSA when no stronger project pattern exists.
- Dependencies should be current, compatible, and source-backed. Do not upgrade blindly.

## Browser, Design, And Security

- Browser-visible changes require browser validation when a browser can be run.
- Screenshots and temporary browser evidence belong under `browser/` and should not be committed unless explicitly requested.
- Figma is the source of truth for Figma-to-code tasks. Adapt designs into centralized i18n, tokens, UI kit, project architecture, content/data ownership, and browser-validated implementation.
- Security-relevant work should apply OWASP-oriented guidance and run `$ry-sec-review` when the owner asks for a security review or the touched scope is sensitive.

## Serena Memories And Project Knowledge

- Store durable facts in `.serena/memories/` with the project memory metadata format.
- Store non-trivial reusable plans in `.serena/plans/`.
- Store long source-backed research in `.serena/research/`.
- Memories are facts only: exact paths, entry points, behavior, contracts, invariants, change rules, and verification.
- Do not store chat history, speculation, secrets, raw tokens, cookies, or private credentials in memories.
- After meaningful code, plugin, workflow, config, design, security, or architecture changes, synchronize Serena memories before final delivery.

## Subagents

- Use subagents only when explicitly allowed by the user, by an active workflow such as `ry-start` or `ry-review`, or by current system instructions.
- Every subagent prompt must be self-contained: task, context, files, constraints, expected output, read-only/write scope, and known risks.
- Do not delegate the immediate blocking task if the parent workflow cannot progress without the answer.
- Managed subagent role files live in `${CODEX_HOME:-$HOME/.codex}/agents/*.toml` and are installed from repository `system/agents/*.toml`.
- Managed subagent roles must use `model = "gpt-5.5"` and `model_reasoning_effort = "medium"` unless the owner explicitly changes the system default.
- Managed subagent roles temporarily narrow their MCP surface to the lightweight core inherited tools: `sequential-thinking`, `serena`, `context7`, `grep`, `deepwiki`, `openaiDeveloperDocs`, and built-in `codex_apps`. Specialist MCP servers such as `semgrep`, `figma`, `playwright`, `chrome-devtools`, `dart-flutter`, and `shadcn` stay parent-session tools until Codex subagent MCP startup is reliably lazy or isolated. Disabled specialist MCP overrides in `system/agents/*.toml` must include full `command` or `url` transport metadata copied from `plugins/rldyour-mcps/.mcp.json`; `codex_apps` must not be declared as a synthetic `[mcp_servers.codex_apps]` table because it is inherited from Apps/connectors.
- When spawning an ad hoc subagent role that is not backed by a managed agent TOML file, set the spawn override to `model = "gpt-5.5"` and `reasoning_effort = "medium"`.

## Git And Delivery

- Prefer atomic Conventional Commits.
- Do not force push `main`.
- Do not revert user changes unless explicitly requested.
- Before final delivery, run the checks that match the touched scope and report exact commands.
- If changes are committed, push when the task requires synchronization or when the workflow has reached a stable final state.
- Keep `AGENTS.md`, Serena memories, and durable docs synchronized with changed behavior.
- In fullrepo-managed repositories, bootstrap agent-only context from `fullrepo` during initialization before relying on `AGENTS.md`, `CLAUDE.md`, `REVIEW.md`, or `.serena` knowledge. Use `scripts/sync_fullrepo_branch.sh --bootstrap-init` so existing `fullrepo` context is restored, local agent-only files are published when no `fullrepo` exists, excludes are installed, and tracked agent-only files are removed from the current branch index when migration is needed.
- `ry-init` is read-only for Serena memories by default. It may report `Memory candidates (not written)`, but it must not write `.serena` unless the owner explicitly requested memory synchronization or a Stop/stale-memory hook requires it. Runtime snapshots, server log summaries, health statuses, and one-off audit observations are report material, not memory material, unless they reveal stable code/config contracts.
- Standard finish order is: refresh Serena memories and durable project instructions from verified code, run matching checks, create and push atomic normal-branch commits, publish `fullrepo` from the final branch `HEAD`, then clean merged workflow branches and worktrees when safe.
- In normal product repositories, keep agent-only files out of `main` and feature branches. Restore them from `fullrepo`, ignore them through `.git/info/exclude`, and publish the complete snapshot to `fullrepo` with safe `--force-with-lease` after normal branch sync.
- Agent-only files include project-root `AGENTS.md`, `.claude/CLAUDE.md`, `REVIEW.md`, `.serena` knowledge, `.claude`, `.codex`, `.cursor/rules`, `.agents/skills`, and similar AI workflow files. Agent tooling repositories may intentionally track selected instruction templates as product artifacts.
- Bootstrap-only untracked `.serena` files created by tool startup, such as `.serena/project.yml` plus runtime markers, are not meaningful project work by themselves and must not force a Stop-hook post-task sync loop.
- After meaningful project behavior, workflow, setup, validation, architecture, plugin, hook, command, or deploy changes, update Serena memories first, then update `AGENTS.md` for Codex and `.claude/CLAUDE.md` for Claude Code from verified project state before final git/GitHub/fullrepo synchronization.

## System Codex Setup

The canonical source for this global setup is the `rldyour-codex` repository.

System Codex installs the owner-standard full-auto profile by default with the official Codex config schema hint, `approval_policy = "never"`, `sandbox_mode = "danger-full-access"`, `default_permissions = ":danger-no-sandbox"`, `profile = "rldyour-yolo"`, `model = "gpt-5.5"`, `model_reasoning_effort = "xhigh"`, `suppress_unstable_features_warning = true`, managed subagents on `gpt-5.5`/`medium` with temporary specialist-MCP isolation, and `[features].hooks = true`, `[features].plugin_hooks = true`, plus `[features].multi_agent = true`. The owner-standard mode is also referred to as YOLO mode, full-auto mode, and dangerously-skip-permissions mode. `scripts/install_system_codex.sh --apply --safe-mode` is the explicit conservative override and selects `approval_policy = "on-request"`, `sandbox_mode = "workspace-write"`, and `profile = "rldyour-safe"` only when the owner intentionally asks for that posture. Current Codex documentation treats `sandbox_mode` as the active older sandbox model when present, so do not migrate this owner profile to beta permission profiles without an explicit policy decision. Current Codex CLI keeps plugin-bundled hooks behind `plugin_hooks`, so the flag is intentionally explicit. Deprecated config aliases such as `codex_hooks`, legacy `features.web_search*`, `experimental_instructions_file`, `background_terminal_timeout`, `experimental_use_unified_exec_tool`, `memories.no_memories_if_mcp_or_web_search`, and `use_legacy_landlock` must not be present. Continue to avoid destructive actions unless the owner explicitly requests them.

System install and doctor checks derive rldyour plugin enablement from `.agents/plugins/marketplace.json`, the Codex adapter surface from `config/rldyour-contract.json`, and MCP server registration from `plugins/rldyour-mcps/.mcp.json`; do not add parallel hardcoded plugin or MCP lists. The installer syncs plugin cache into versioned `${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/<plugin>/<version>` directories first, installs managed Codex execpolicy rules from `system/rules/*.rules` into `${CODEX_HOME:-$HOME/.codex}/rules/*.rules`, then refreshes installed rldyour plugin hook trust hashes through the app-server RPC method `hooks/list` over `codex app-server --listen stdio://`; doctor and runtime smoke verify that all installed rldyour plugin hooks are live, enabled, trusted, and that managed rules are in sync.

Use:

```bash
scripts/install_system_codex.sh --dry-run
scripts/install_system_codex.sh --apply
scripts/install_system_codex.sh --apply --safe-mode
scripts/install_system_codex.sh --apply --strict-runtime
scripts/doctor_system_codex.sh
scripts/doctor_system_codex.sh --safe-mode
scripts/doctor_system_codex.sh --quick --strict-runtime
scripts/validate_fast.sh
scripts/validate_runtime.sh --strict-runtime
scripts/validate_release.sh
scripts/validate_execpolicy_rules.sh
scripts/smoke_mcp_runtime.sh
scripts/smoke_mcp_capabilities.sh
python3 scripts/smoke_codex_hook_listing.py
scripts/smoke_hooks.sh
scripts/smoke_codex_hooks_migration.sh
scripts/smoke_serena_memory_freshness.sh
scripts/smoke_serena_memory_taxonomy.sh
scripts/smoke_local_git_guard.sh
scripts/smoke_flow_branch_cleanup.sh
scripts/smoke_clean_bootstrap.sh
scripts/smoke_fullrepo_bootstrap_init.sh
scripts/install_local_git_hooks.sh --dry-run
plugins/rldyour-flow/scripts/instruction_docs_state.py --json | python3 -m json.tool
python3 scripts/validate_instruction_docs.py --require-agent-docs
python3 scripts/check_serena_memory_freshness.py
python3 scripts/validate_agent_tools.py
python3 scripts/validate_action_pins.py
python3 scripts/validate_runtime_prereqs.py --strict --require-codex
python3 scripts/validate_contract.py
python3 scripts/scan_text_security.py
uv run --with pytest --with pytest-cov --with pyyaml python -m pytest
python3 scripts/release_manifest.py
python3 scripts/release_sbom.py
scripts/sync_fullrepo_branch.sh --status
scripts/sync_fullrepo_branch.sh --bootstrap-init
scripts/sync_fullrepo_branch.sh --publish
scripts/rollback_system_codex.sh --list
scripts/collect_diagnostics.sh
```

Release and operational evidence live in `VERSION`, `CHANGELOG.md`, `docs/release-process.md`, `docs/rollback-restore.md`, `docs/dependency-updates.md`, and `docs/observability.md`.

Restart Codex after changing global `AGENTS.md`, `~/.codex/config.toml`, installed plugins, hooks, skills, or MCP runtime definitions.
