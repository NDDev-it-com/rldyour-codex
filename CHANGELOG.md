# Changelog

All notable changes to this project are documented in this file.

The format follows Keep a Changelog, and marketplace/plugin versions follow Semantic Versioning.

## [Unreleased]

### Added

- `docs/adr/0001-codex-marketplace-operating-model.md` records the core plugin, hook, fullrepo, CI, MCP, and ADR operating decisions.
- GitHub Actions full-SHA pin validation through `scripts/validate_action_pins.py`.
- Repository text security scan for secret-like patterns and hidden Unicode controls through `scripts/scan_text_security.py`.

### Changed

- Flow Stop hook state now ignores bootstrap-only untracked `.serena` files created by tool startup, preventing empty or unborn repositories from being forced into `flow-post-task-sync` loops.
- `flow-post-task-sync` guidance now resolves rldyour-flow helper scripts from the installed plugin cache when a product repository does not vendor this plugin.
- Flow `SessionStart` hook wiring now uses a single dispatcher so fullrepo bootstrap and session context run in deterministic order under Codex hook concurrency semantics.
- Serena memory analyzer taxonomy now includes `DESIGN`, `LSP`, and `RULES`, with smoke coverage against `CORE-01-INDEX.md`.
- Installer config handling now fails closed on malformed existing `config.toml` instead of silently regenerating from an empty config model.
- Rollback restore now writes backed-up files through temporary files before renaming them into place.
- GitHub Actions workflows now pin external actions to full commit SHAs.
- `dart-flutter` MCP runtime is documented and validated as an explicit external local Dart SDK exception.
- `rldyour-flow` plugin version updated to `0.2.6` for deterministic SessionStart dispatch and hook prologue hardening.
- `rldyour-serena-mcp` plugin version updated to `0.2.3` for expanded memory taxonomy coverage.

## [0.1.1] - 2026-05-16

### Added

- Formal release, rollback, dependency-update, routing-policy, and observability workflows for the rldyour Codex marketplace.
- `rldyour-design` Figma delivery contract for implementation manifests, dynamic/static/admin content classification, centralized i18n, token/UI-kit gates, and browser/static validation before final delivery.
- `fullrepo` branch workflow for portable agent-only files: restore, migrate, publish, status, smoke validation, and Flow/Serena lifecycle integration.
- Safe `--force-with-lease` fullrepo publishing after normal branch synchronization.
- Instruction docs sync workflow for first-class Codex `AGENTS.md` and Claude Code `.claude/CLAUDE.md` maintenance.
- Branch-aware local Git pre-push guard for rldyour-managed repositories, with strict product-branch protection and fullrepo-aware AI context publishing.
- Flow branch-cleanup state and smoke coverage so merged workflow branches, remote branches, and merged worktree candidates keep post-task sync pending until cleanup is done or explicitly reported.
- `fullrepo` bootstrap init command and smoke coverage for first-run repository initialization, remote context restore, local AI-file publishing, and current-branch AI-file index cleanup.
- Serena memory freshness helper and smoke coverage for source-branch freshness, stale memory failures, and `fullrepo` snapshot skip behavior.
- Codex-native Serena sync impact analyzer, numbered memory taxonomy smoke coverage, managed `serena-sync` guidance, and agent surface validation for Codex TOML/OpenAI skill metadata.
- `scripts/worktree_add.sh` and Flow SessionStart worktree bootstrap so new Codex worktrees restore agent-only context from `origin/fullrepo` before deep work starts.

### Changed

- System Codex install now writes `[features].hooks = true`, `[features].plugin_hooks = true`, and `[features].multi_agent = true` so bundled rldyour plugin hooks load from enabled plugins across current Codex CLI releases where plugin hooks remain explicit opt-in.
- System Codex install now explicitly writes `suppress_unstable_features_warning = true` so under-development feature noise is stable and intentional.
- System Codex install migration now normalizes current Codex deprecated config aliases: `codex_hooks`, legacy `features.web_search*`, `experimental_instructions_file`, `background_terminal_timeout`, `experimental_use_unified_exec_tool`, `memories.no_memories_if_mcp_or_web_search`, and deprecated `use_legacy_landlock`, with dedicated smoke coverage in `scripts/smoke_codex_hooks_migration.sh`.
- Flow post-task state now treats stale Serena memories and stale fullrepo snapshots as pending sync instead of false green states.
- Doctor and validation now use stricter parsed-config/current-state checks for system config, Serena memory freshness, and fullrepo sync.
- System Codex install and doctor now derive rldyour plugin enablement from `.agents/plugins/marketplace.json` and MCP server checks from `plugins/rldyour-mcps/.mcp.json` instead of parallel hardcoded lists.
- Hook smoke validation now parses plugin `hooks.json` wiring and executes the configured command wrappers in addition to direct hook script lifecycle checks.
- GitHub validation now includes scheduled and manual MCP safe-call smoke coverage for deterministic unauthenticated MCP tool invocations.
- Fullrepo bootstrap-init smoke now covers `.claude/CLAUDE.md` restore, ignore, and current-branch index cleanup alongside `AGENTS.md` and Serena memories.
- Clean bootstrap smoke now restores agent-only context with `scripts/sync_fullrepo_branch.sh --bootstrap-init` before running strict system doctor checks.
- MCP runtime smoke now checks remote URL servers with a Streamable HTTP `initialize` POST preflight, parses JSON and SSE initialize responses, accepts auth-gated `401`/`403` endpoints, and keeps retry/timeout controls.
- MCP capability smoke now probes Grep with a fast code-pattern query that matches the current `searchGitHub` tool contract and gives transient remote calls five attempts by default.
- Marketplace validation now enforces parity between `config/mcp-runtime-versions.env` and local MCP launcher package specs in `plugins/rldyour-mcps/.mcp.json`.
- System doctor keeps the fullrepo current-state gate strict locally while treating it as advisory on GitHub Actions `main` runs, where the separate `fullrepo` workflow validates published agent-only snapshots.
- System Codex install now writes the official Codex config schema hint at the top of generated `config.toml`, and doctor/migration smoke verify it.
- System Codex install now reproduces the owner-selected `gpt-5.5`/`xhigh` model defaults and approved MCP tool overrides from a clean `CODEX_HOME`.
- Plugin release validation now enforces Codex marketplace policy fields, plugin interface metadata, relative bundled capability paths, default prompt limits, and brand color format.
- System Codex install now manages `~/.codex/agents/*.toml` subagent role configs from `system/agents/*.toml`, enables `features.multi_agent`, and verifies managed subagents use `gpt-5.5` with medium reasoning.
- Runtime Codex CLI pin updated from `0.128.0` to `0.130.0`.
- MCP Python SDK pin updated from `1.27.0` to `1.27.1` for the latest compatibility fixes.
- MCP runtime pins updated for Serena Agent `1.3.0`, Semgrep `1.163.0`, Playwright MCP `0.0.75`, Chrome DevTools MCP `0.26.0`, Context7 MCP `2.2.5`, and shadcn `4.7.0`.
- `rldyour-serena-mcp` plugin version updated to `0.2.2` for Codex-native memory taxonomy, impact analysis, and managed `serena-sync` routing.
- `rldyour-flow` plugin version updated to `0.2.5` for read-only `ry-init` memory discipline, fullrepo bootstrap init behavior, and SessionStart worktree bootstrap.
- `ry-init` is now explicitly read-only for Serena memories by default; it reports memory candidates instead of writing `.serena` unless the user requested memory sync or a stale-memory hook requires it.
- `serena-memory-sync` no longer auto-runs for read-only init, log audits, server snapshots, report-only reviews, or exploratory debugging without an explicit memory-sync request.
- Global and project instructions now state the explicit fullrepo-managed task sync order: Serena/docs, checks, normal branch push, fullrepo publish, and safe cleanup.
- `@upstash/context7-mcp` runtime pin updated from `2.2.3` to `2.2.5`.
- `rldyour-flow` now treats `fullrepo` as part of `ry-init` and `flow-post-task-sync`.
- `rldyour-flow` now detects missing or stale instruction docs and routes post-task sync through `$instruction-docs-sync`.
- `rldyour-serena-mcp` memory sync now supports fullrepo-managed `.serena` knowledge without committing AI files to normal branches.
- `rldyour-rules` now documents the agent-only file policy for `AGENTS.md`, `.claude/CLAUDE.md`, `.serena`, and related AI workflow paths.
- `validate.yml` now runs `scripts/check_mcp_runtime_versions.py --fail-on-outdated --json` in a dedicated `dependency-pins` job on `push`, `pull_request`, and manual dispatch; this catches MCP runtime pin drift in normal CI alongside the scheduled `dependency-check` workflow.

## [0.1.0] - 2026-05-03

### Added

- Initial controlled Codex marketplace with rldyour plugins, MCP runtime definitions, system install scripts, validation scripts, hooks, LSP policy, browser/design/security/research workflows, and Serena project knowledge.
