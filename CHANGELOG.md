# Changelog

All notable changes to this project are documented in this file.

The format follows Keep a Changelog, and marketplace/plugin versions follow Semantic Versioning.

## [Unreleased]

### Added

- Formal release, rollback, dependency-update, routing-policy, and observability workflows for the rldyour Codex marketplace.
- `fullrepo` branch workflow for portable agent-only files: restore, migrate, publish, status, smoke validation, and Flow/Serena lifecycle integration.
- Safe `--force-with-lease` fullrepo publishing after normal branch synchronization.
- Instruction docs sync workflow for first-class Codex `AGENTS.md` and Claude Code `.claude/CLAUDE.md` maintenance.
- Branch-aware local Git pre-push guard for rldyour-managed repositories, with strict product-branch protection and fullrepo-aware AI context publishing.
- Flow branch-cleanup state and smoke coverage so merged workflow branches, remote branches, and merged worktree candidates keep post-task sync pending until cleanup is done or explicitly reported.
- `fullrepo` bootstrap init command and smoke coverage for first-run repository initialization, remote context restore, local AI-file publishing, and current-branch AI-file index cleanup.

### Changed

- System Codex install now writes `[features].hooks = true` and removes the deprecated `codex_hooks` feature key from managed config.
- System Codex install migration now normalizes dotted, quoted, and inline-table legacy hooks feature keys, with dedicated smoke coverage in `scripts/smoke_codex_hooks_migration.sh`.
- MCP capability smoke now probes Grep with a fast code-pattern query that matches the current `searchGitHub` tool contract and gives transient remote calls a third retry.
- Runtime Codex CLI pin updated from `0.128.0` to `0.129.0`.
- `rldyour-flow` plugin version updated to `0.2.4` for read-only `ry-init` memory discipline and fullrepo bootstrap init behavior.
- `ry-init` is now explicitly read-only for Serena memories by default; it reports memory candidates instead of writing `.serena` unless the user requested memory sync or a stale-memory hook requires it.
- `serena-memory-sync` no longer auto-runs for read-only init, log audits, server snapshots, report-only reviews, or exploratory debugging without an explicit memory-sync request.
- Global and project instructions now state the explicit fullrepo-managed task sync order: Serena/docs, checks, normal branch push, fullrepo publish, and safe cleanup.
- `chrome-devtools-mcp` runtime pin updated from `0.23.0` to `0.24.0`.
- `@upstash/context7-mcp` runtime pin updated from `2.2.3` to `2.2.4`.
- `rldyour-flow` now treats `fullrepo` as part of `ry-init` and `flow-post-task-sync`.
- `rldyour-flow` now detects missing or stale instruction docs and routes post-task sync through `$instruction-docs-sync`.
- `rldyour-serena-mcp` memory sync now supports fullrepo-managed `.serena` knowledge without committing AI files to normal branches.
- `rldyour-rules` now documents the agent-only file policy for `AGENTS.md`, `.claude/CLAUDE.md`, `.serena`, and related AI workflow paths.

## [0.1.0] - 2026-05-03

### Added

- Initial controlled Codex marketplace with rldyour plugins, MCP runtime definitions, system install scripts, validation scripts, hooks, LSP policy, browser/design/security/research workflows, and Serena project knowledge.
