<!-- Memory Metadata
Last updated: 2026-05-18
Last commit: 6ec3fb9 fix(hooks): harden lifecycle execution
Scope: .serena/memories, .agents/plugins/marketplace.json, plugins/*/.codex-plugin/plugin.json, plugins/*/skills/*/SKILL.md, plugins/*/skills/*/agents/openai.yaml, plugins/rldyour-mcps/.mcp.json, system/AGENTS.md, system/agents/*.toml, pyproject.toml, tests/, .github/workflows/*.yml, .github/actions/setup-codex-runtime/action.yml, docs/adr/*.md, scripts/validate_marketplace.sh
Area: CORE
-->

# CORE-01-INDEX

## Purpose

This is the entry point for the `rldyour-codex` Serena memory set. Read this memory first, then read only the scoped topic memories needed for the task and verify details against source files.

## Source Of Truth

- `.agents/plugins/marketplace.json`: active local marketplace catalog.
- `plugins/<plugin>/.codex-plugin/plugin.json`: Codex plugin manifests, versions, interface metadata, and bundled capability paths.
- `plugins/<plugin>/skills/*/SKILL.md`: skill routing contract and operational instructions.
- `plugins/<plugin>/skills/*/agents/openai.yaml`: Codex skill UI/dependency metadata.
- `plugins/rldyour-mcps/.mcp.json`: MCP transport source of truth.
- `config/mcp-runtime-versions.env`: pinned MCP launcher and Codex CLI versions.
- `system/AGENTS.md`: tracked global Codex instruction template.
- `system/agents/*.toml`: tracked managed Codex subagent role configs.
- `.serena/memories/*.md`: fact-only project knowledge published through `fullrepo`.

## Entry Points

- `scripts/validate_marketplace.sh`: full repository validation gate.
- `scripts/install_system_codex.sh --apply`: install global Codex config, managed agents, plugins, hooks, MCP registration, and plugin cache.
- `scripts/doctor_system_codex.sh`: verify installed runtime and fullrepo/current-state gates.
- `scripts/sync_fullrepo_branch.sh --bootstrap-init|--publish|--status`: restore or publish agent-only context.
- `python3 plugins/rldyour-serena-mcp/scripts/serena_memory_state.py`: memory freshness and analyzer state.
- `uv run --with pytest --with pytest-cov --with pyyaml python -m pytest`: unit and coverage gate.
- `python3 scripts/release_sbom.py`: generated SPDX 2.3 release SBOM evidence.

## Current Behavior

- Active rldyour plugins: `rldyour-mcps`, `rldyour-explore`, `rldyour-serena-mcp`, `rldyour-security`, `rldyour-browser`, `rldyour-design`, `rldyour-lsps`, `rldyour-flow`, `rldyour-rules`.
- Marketplace release version is `0.3.5`.
- `rldyour-flow` is version `0.3.3` and owns SDLC commands, fullrepo, instruction docs, fast offline/local-only SessionStart dispatch, cwd-safe PreToolUse guardrails, ordered local-only Stop lifecycle dispatch, and post-task sync.
- `rldyour-serena-mcp` is version `0.2.4` and owns Serena-first code workflow plus memory freshness, expanded taxonomy, sync hooks, and acknowledgement.
- The repository currently has 38 rldyour skills, 12 MCP server definitions, and 8 managed Codex subagent TOML files validated by scripts.
- The Python test harness enforces a 75% coverage threshold through `pyproject.toml`.
- Managed subagents currently use temporary MCP isolation: the lightweight inherited/core surface stays available (`sequential-thinking`, `serena`, `context7`, `grep`, `deepwiki`, `openaiDeveloperDocs`, and built-in `codex_apps`), while specialist MCP servers remain parent-session tools until Codex subagent MCP startup is stable enough to widen safely. Disabled specialist MCP overrides include full transport metadata from `plugins/rldyour-mcps/.mcp.json`, and `codex_apps` stays inherited from Apps/connectors rather than declared as an `mcp_servers` transport.
- Fullrepo unit-test fixtures configure local git identity inside temporary repositories and clones, so GitHub-hosted runners do not depend on global git author settings.
- CI noise classification treats `uv` package download progress lines as known setup noise while still failing strict jobs on unrelated stderr.
- GitHub CI/CD is manual-only for this repository's spend policy. The latest full explicit GitHub pipeline on commit `cdad168` passed `validate.yml` run `25999559961` with macOS parity, `security-static.yml` run `25999559930`, `dependency-check.yml` run `25999559948`, and `release.yml` run `25999559947`, and published release `0.3.4` with deterministic bundle/SBOM/attestation output. Local validation for `6ec3fb9` / version `0.3.5` passed before memory sync and main push; GitHub Actions for `0.3.5` should be launched only on explicit owner request.
- System install manages Codex hook runtime with `[features].hooks = true` and `[features].plugin_hooks = true`, so enabled rldyour plugin hook declarations are actually loaded.
- Normal `main` excludes root `AGENTS.md`, `.claude/CLAUDE.md`, `.serena` knowledge, and similar agent-only files through `.git/info/exclude`; `fullrepo` carries the portable agent context snapshot.
- Normal-branch GitHub CI may run without tracked fullrepo-managed `.serena/memories`; memory taxonomy smoke still tests analyzer/fixture contracts, and the final live freshness state check is skipped until memories are present as tracked fullrepo context.
- Project memories use the numbered taxonomy `AREA-01-SLUG.md`; `CORE-01-INDEX.md` is the map.

## Contracts And Data

- Memory metadata must start with the exact HTML block containing `Last updated`, `Last commit`, `Scope`, and `Area`.
- `Last commit` should mention the current normal-branch commit when a memory is updated for a code/config change.
- Codex skills must not use Claude-only frontmatter keys such as `allowed-tools`; Codex dependencies live in `agents/openai.yaml`.
- Codex managed subagents live in `system/agents/*.toml`; plugin-root `plugins/rldyour-*/agents/*.md` is a rejected Claude Code surface.
- Disabled MCP overrides in managed subagent TOML files must include `command` or `url` transport metadata copied from `.mcp.json`; `scripts/validate_agent_tools.py` and `scripts/doctor_system_codex.sh` reject partial disabled tables and transport drift.
- `plugin_hooks` is an official Codex feature flag and is managed as enabled here; `codex_hooks` is the deprecated alias that must be removed.

## Invariants

- User-facing conversation with the owner is Russian unless explicitly requested otherwise; repository artifacts and memories are English.
- Code, config, scripts, tests, and official docs are source of truth; old memories are not authority.
- `rldyour-mcps` is transport-only and must not own behavior policy or skills.
- Only `rldyour-flow` and `rldyour-serena-mcp` currently declare plugin hooks.
- Do not store secrets, credentials, raw tokens, cookies, or transient runtime logs in memories.

## Change Rules

- When plugin, hook, skill, managed agent, workflow, install, validation, release, or agent-instruction behavior changes, update the relevant memory files and this index in the same sync pass.
- Prefer adding a focused numbered memory over expanding a broad catch-all memory.
- Run source-backed checks before marking memories current.

## Verification

- `scripts/validate_marketplace.sh`: validates manifests, skills, hooks, scripts, agent surfaces, smoke tests, memory freshness helper, and release metadata.
- `uv run --with pyyaml python scripts/validate_agent_tools.py`: rejects Codex/Claude surface drift.
- `python3 plugins/rldyour-serena-mcp/scripts/serena_memory_state.py | python3 -m json.tool`: shows HEAD, newest synced memory commit, analyzer targets, and staleness reason.
- `scripts/smoke_serena_memory_taxonomy.sh`: proves numbered memory taxonomy, analyzer routing, stop-hook advisory, nested memory scanning, and fullrepo-managed memory acknowledgement.

## Memory Map

- `CORE-02-MARKETPLACE.md`: marketplace catalog, plugin manifest, version, and boundary rules.
- `CORE-03-DOMAIN-PLUGINS.md`: research, browser, security, and other domain-plugin routing.
- `CODEX-01-PLUGIN-CANON.md`: Codex-specific plugin, skill, hook, managed agent, and validation surfaces.
- `CODEX-02-SYSTEM-RUNTIME.md`: installed Codex config, model/permission defaults, MCP registration, plugin cache, and managed agents.
- `CODEX-03-SYSTEM-INSTALL.md`: install, doctor, rollback, bootstrap, and restart-sensitive behavior.
- `MCP-01-TRANSPORT.md`: MCP runtime servers, pins, startup/tool timeouts, and capability smoke.
- `SERENA-01-MEMORY-SYNC.md`: Serena memory analyzer, freshness state, hooks, taxonomy, and acknowledgement.
- `HOOKS-01-LIFECYCLE.md`: Codex lifecycle hook event contracts and repository hook wiring.
- `FLOW-01-SDLC.md`: ry-* workflow, fullrepo, worktree, instruction-doc, git/GitHub, and cleanup state.
- `DOCS-01-INSTRUCTIONS.md`: AGENTS.md and .claude/CLAUDE.md synchronization policy.
- `RELEASE-01-VALIDATION.md`: validation, release, changelog, dependency, and diagnostics gates.
- `TECHDEBT-01-NOW.md`: durable mistakes, anti-regression rules, and known operational traps.
- `DESIGN-01-RLDYOUR-DESIGN.md`: Figma/design-system/browser-validation workflow.
- `LSP-01-LANGUAGE-SERVERS.md`: LSP routing, health, setup, and Serena LSP integration.
- `RULES-01-QUALITY-FIRST.md`: engineering rules, architecture boundaries, dependency policy, and verification gates.
