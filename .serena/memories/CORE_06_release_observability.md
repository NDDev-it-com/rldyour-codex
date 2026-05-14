<!-- Memory Metadata
Last updated: 2026-05-14
Last commit: b3dc114 test(codex): strengthen integration smoke gates
Scope: CHANGELOG.md, README.md, docs/dependency-updates.md, config/skill-routing-policy.json, scripts/validate_instruction_docs.py, scripts/validate_marketplace.sh, scripts/check_serena_memory_freshness.py, scripts/smoke_serena_memory_freshness.sh, scripts/smoke_codex_hooks_migration.sh, scripts/smoke_mcp_runtime.sh, scripts/smoke_mcp_capabilities.py, scripts/smoke_mcp_capabilities.sh, scripts/smoke_fullrepo_sync.sh, plugins/rldyour-flow/scripts/instruction_docs_state.py, plugins/rldyour-flow/scripts/flow_post_task_state.py, plugins/rldyour-flow/skills/instruction-docs-sync, AGENTS.md, .claude/CLAUDE.md, system/AGENTS.md
Area: CORE
-->

# CORE_06_release_observability

## Purpose

Operational layer for release readiness, observability, runtime checks, and rollback recovery in this repository.

## Source Of Truth

- `VERSION`
- `CHANGELOG.md`
- `docs/release-process.md`
- `docs/rollback-restore.md`
- `docs/observability.md`
- `docs/dependency-updates.md`
- `scripts/validate_plugin_versions.py`
- `scripts/check_mcp_runtime_versions.py`
- `scripts/check_serena_memory_freshness.py`
- `scripts/smoke_serena_memory_freshness.sh`
- `scripts/release_manifest.py`
- `scripts/collect_diagnostics.sh`
- `scripts/smoke_local_git_guard.sh`
- `scripts/smoke_flow_branch_cleanup.sh`
- `scripts/smoke_codex_hooks_migration.sh`
- `scripts/smoke_mcp_runtime.sh`
- `scripts/smoke_mcp_capabilities.py/.sh`
- `plugins/rldyour-flow/scripts/flow_post_task_state.py`
- `plugins/rldyour-flow/scripts/instruction_docs_state.py`
- `.github/workflows/validate.yml`
- `.github/workflows/dependency-check.yml`

## Versioning and Artifacts

- Marketplace release version is `VERSION` (independent from plugin manifest versions).
- Plugin behavior versions are in each `plugins/<plugin>/.codex-plugin/plugin.json`.
- `scripts/validate_plugin_versions.py` enforces SemVer and checks that:
  - release docs exist (`docs/release-process.md`, `docs/rollback-restore.md`, `docs/observability.md`, `docs/dependency-updates.md`)
  - marketplace plugin entries align with manifests
  - `CHANGELOG.md` has required sections.

## Release Evidence

`scripts/release_manifest.py` emits machine snapshot containing:

- repository version and git metadata (`head`, `branch`, `dirty`, `remote`, `fullrepo_sha`)
- marketplace metadata and plugin manifest list
- MCP runtime versions from `config/mcp-runtime-versions.env`
- `plugins/rldyour-mcps/.mcp.json` server specs

Use for release evidence and operational tagging flow.

## Runtime Pin & Dependency Contract

- MCP runtime versions are pinned in `config/mcp-runtime-versions.env` and `.mcp.json`.
- `scripts/check_mcp_runtime_versions.py` compares pins against upstream.
- `scripts/validate_marketplace.sh` checks parity between env pins and local launcher package specs in `.mcp.json`.
- `--fail-on-outdated` is CI-grade mode.
- `docs/dependency-updates.md` defines the manual update flow and validation gate order.
- `scripts/smoke_mcp_runtime.sh` treats unexpected URL MCP HTTP statuses and malformed initialize responses as failures. Remote URL servers are validated with a Streamable HTTP JSON-RPC `initialize` POST preflight; auth-gated `401`/`403` endpoints may pass, but POST `405` does not.
- `scripts/smoke_mcp_capabilities.py` requires env vars by default; CI/offline list-only paths pass `--allow-missing-env` explicitly.

## Rollback and Recovery

- Install rollback:
  - `scripts/rollback_system_codex.sh --list`
  - `scripts/rollback_system_codex.sh --restore <backup> [--dry-run]`
- Git-tag rollback path is documented in `docs/rollback-restore.md` using `git checkout v<version>` and re-install.
- For agent-only context restore failures:
  - `scripts/sync_fullrepo_branch.sh --restore`
  - `scripts/sync_fullrepo_branch.sh --status`

## Observability

### Local

- `scripts/collect_diagnostics.sh`
- `scripts/collect_diagnostics.sh --include-doctor` (adds doctor output)
- artifacts in ignored `diagnostics/` directory

### CI

- `.github/workflows/validate.yml` runs on `main`/`fullrepo` push and PR to `main`, matrix `ubuntu-latest` and `macos-latest`
  - uses temporary `CODEX_HOME=/tmp/rldyour-codex-home`
  - keeps marketplace MCP capability smoke in list-only mode for push/PR portability
  - writes `GITHUB_STEP_SUMMARY`
  - writes and uploads `diagnostics/ci` on failure
- `.github/workflows/validate.yml` also runs weekly and manually through `workflow_dispatch`; those runs include an Ubuntu `mcp-safe-calls` job that probes deterministic unauthenticated MCP `call_tool` paths after a temporary system install.
- `validate_marketplace.sh` skips Serena memory freshness on `fullrepo` because fullrepo snapshot commits intentionally differ from source commits recorded in memory metadata.
- `scripts/doctor_system_codex.sh` keeps fullrepo current-state strict locally but reports it as a warning on GitHub Actions `main` runs; the separate `fullrepo` branch workflow is the CI authority for published agent-only snapshots.
- `.github/workflows/dependency-check.yml` runs pinned-version freshness weekly + manual (`--fail-on-outdated`).

## Verification

- `scripts/validate_marketplace.sh`
- `scripts/doctor_system_codex.sh`
- `scripts/smoke_codex_hooks_migration.sh`
- `scripts/smoke_mcp_runtime.sh`
- `scripts/smoke_mcp_capabilities.sh`
- `scripts/smoke_serena_memory_freshness.sh`
- `python3 scripts/validate_plugin_versions.py`
- `python3 scripts/check_mcp_runtime_versions.py --fail-on-outdated`
- `python3 scripts/release_manifest.py`
- `scripts/smoke_fullrepo_sync.sh`
- `scripts/smoke_local_git_guard.sh`
- `scripts/smoke_flow_branch_cleanup.sh`
- `scripts/smoke_clean_bootstrap.sh`
- `scripts/collect_diagnostics.sh`
- `python3 scripts/release_manifest.py > diagnostics/release-manifest.json` (when running local release checks)

## Invariants

- Keep release operations reproducible and command-driven.
- Do not mutate config/state in CI-only checks.
- Keep diagnostics/runtimes/doctor outputs free of secrets and env-dumps.
- `collect_diagnostics.sh` output is ignored and should remain outside commit history.
- Fullrepo operations in release/recovery flow are safe only when non-agent workspace state is clean.
