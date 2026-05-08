<!-- Memory Metadata
Last updated: 2026-05-08
Last commit: 622c421 fix(mcp): validate remote streamable http preflight
Scope: .serena/memories, AGENTS.md, .claude/CLAUDE.md, README.md, .agents/plugins/marketplace.json, plugins/*/.codex-plugin/plugin.json, plugins/rldyour-mcps/.mcp.json, config/mcp-runtime-versions.env, scripts/release_manifest.py, scripts/validate_marketplace.sh, scripts/smoke_codex_hooks_migration.sh, scripts/smoke_mcp_runtime.sh, scripts/smoke_mcp_capabilities.py, scripts/smoke_mcp_capabilities.sh, scripts/sync_fullrepo_branch.sh
Area: CORE
-->

# CORE_00_memory_index

## Purpose

This is the entry point for the `rldyour-codex` Serena memory set. Use it first to choose the smallest relevant memory files, then verify implementation details against the source files listed in each memory.

## Current Project Snapshot

- Repository: `rldyour-codex`
- Normal branch: `main`
- Current source HEAD: `622c421e79beadb24bf16dcd0ade3e6cda107fcd`
- Current fullrepo snapshot is generated from `main` HEAD plus agent-only files; verify the exact local/remote SHA with `scripts/sync_fullrepo_branch.sh --status`.
- Marketplace version: `0.1.0`
- Active rldyour plugins: `9`
- Callable rldyour skills: `38`
- Configured MCP servers: `12`
- Runtime Codex CLI pin: `0.129.0`
- `rldyour-flow` plugin version: `0.2.4`

## Source Priority

Use code and configuration as the source of truth. Memories are compact indexes of verified facts, not independent authority.

- Marketplace catalog: `.agents/plugins/marketplace.json`
- Plugin capabilities: `plugins/<plugin>/.codex-plugin/plugin.json`
- Skill routing: `plugins/<plugin>/skills/*/SKILL.md`, `plugins/<plugin>/skills/*/agents/openai.yaml`, `config/skill-routing-policy.json`
- MCP runtime: `plugins/rldyour-mcps/.mcp.json`, `config/mcp-runtime-versions.env`
- System install/runtime: `scripts/install_system_codex.sh`, `scripts/smoke_codex_hooks_migration.sh`, `scripts/doctor_system_codex.sh`, `${CODEX_HOME:-$HOME/.codex}/config.toml`
- Fullrepo and flow sync: `scripts/sync_fullrepo_branch.sh`, `plugins/rldyour-flow/scripts/fullrepo_sync.py`, `plugins/rldyour-flow/scripts/flow_post_task_state.py`, `plugins/rldyour-flow/scripts/git_sync_audit.sh`
- Local Git guard: `plugins/rldyour-flow/scripts/local_git_ai_guard.sh`, `scripts/install_local_git_hooks.sh`, `scripts/smoke_local_git_guard.sh`
- Serena knowledge freshness: `plugins/rldyour-serena-mcp/scripts/serena_memory_state.py`, `plugins/rldyour-serena-mcp/scripts/commit_serena_knowledge.sh`

## Memory Map

- `CORE_01_rldyour_plugin_auto_routing.md`: plugin routing, skill counts, implicit invocation policy, routing validation.
- `CORE_02_marketplace_control_model.md`: active catalog, manifest boundaries, installed plugin set, marketplace change rules.
- `CORE_03_research_browser_security_plugins.md`: explore/browser/security domain contracts and validation.
- `CORE_04_system_codex_runtime.md`: installed Codex profile, permissions, plugin registration, MCP config, restart-sensitive files.
- `CORE_05_system_install_workflow.md`: install/dry-run/apply/doctor/rollback workflow and portability rules.
- `CORE_06_release_observability.md`: release metadata, diagnostics, CI gates, dependency freshness checks.
- `DESIGN_01_rldyour_design_plugin.md`: design/Figma/FSD/shadcn/browser-validation workflow.
- `FLOW_01_sdlc_workflow.md`: `ry-init`, `ry-start`, `ry-review`, `ry-deploy`, post-task synchronization, reviewer orchestration.
- `LSP_01_language_server_workflow.md`: language-server routing, health check, macOS/Linux fallback policy, Serena LSP integration.
- `MCP_01_runtime_servers.md`: exact MCP server registry, pins, commands, timeouts, env contracts.
- `MCP_02_serena_workflow_hooks.md`: Serena hooks, stop-sync freshness, knowledge/runtime path split.
- `RULES_01_quality_first_engineering.md`: engineering policy, verification gates, architecture/dependency/security rules.

## Cross-Cutting Invariants

- User-facing chat is Russian unless explicitly requested otherwise; repository artifacts stay English.
- `rldyour-mcps` is transport-only and must not own behavior policy or skills.
- `rldyour-flow` and `rldyour-serena-mcp` are the only rldyour plugins with hooks.
- Agent-only project context lives in fullrepo-managed files such as root `AGENTS.md`, `.claude/CLAUDE.md`, `.serena/`, `.claude/`, `.codex/`, `.cursor/rules`, and `.agents/skills`.
- Normal branches keep agent-only context ignored; fullrepo publishes it with `scripts/sync_fullrepo_branch.sh --publish`.
- Repository initialization uses `scripts/sync_fullrepo_branch.sh --bootstrap-init`: restore existing `fullrepo` when available, publish local agent-only files when no `fullrepo` exists, install excludes, and remove tracked agent-only files from the current branch index when migration is needed.
- `ry-init` is read-only for Serena memories by default. It reports `Memory candidates (not written)` instead of writing `.serena` unless the user explicitly requested memory sync or a Stop/stale-memory hook requires it.
- Product repositories can install `scripts/install_local_git_hooks.sh --repo <project> --apply`; the local pre-push guard keeps product refs strict and treats `refs/heads/${RLDYOUR_FULLREPO_BRANCH:-fullrepo}` as the AI-context ref while still blocking definite secrets and runtime/local-only files.
- `branch_cleanup_state` is a finish gate: merged local branches, merged remote branches, and merged workflow worktrees keep Flow sync pending until cleaned or explicitly reported as blockers. Protected branches such as `main` and `fullrepo` are excluded.
- Fullrepo status compares the expected tree from current `HEAD` plus agent-only files against local/remote `fullrepo`; stale snapshots keep Flow sync pending.
- MCP package specs must stay pinned; `@latest` is invalid in runtime definitions.
- Remote URL MCP runtime smoke uses Streamable HTTP JSON-RPC `initialize` POST preflight, not raw GET reachability; auth-gated `401`/`403` can pass, but POST `405` fails.
- Do not store secrets, tokens, cookies, private keys, raw credentials, or browser evidence in memories.

## Minimum Verification After Memory Changes

- `python3 plugins/rldyour-serena-mcp/scripts/serena_memory_state.py | python3 -m json.tool`
- `python3 plugins/rldyour-flow/scripts/flow_post_task_state.py | python3 -m json.tool`
- `python3 plugins/rldyour-flow/scripts/instruction_docs_state.py --root . --json | python3 -m json.tool`
- `python3 scripts/validate_instruction_docs.py --require-agent-docs`
- `scripts/smoke_local_git_guard.sh`
- `scripts/smoke_flow_branch_cleanup.sh`
- `scripts/smoke_codex_hooks_migration.sh`
- `scripts/validate_marketplace.sh`
- `scripts/sync_fullrepo_branch.sh --publish`
