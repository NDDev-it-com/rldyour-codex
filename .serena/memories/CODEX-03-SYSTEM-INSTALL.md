<!-- Memory Metadata
Last updated: 2026-05-16
Last commit: 2c326a0 fix(codex): enable bundled plugin hooks
Scope: scripts/install_system_codex.sh, scripts/doctor_system_codex.sh, scripts/rollback_system_codex.sh, scripts/collect_diagnostics.sh, scripts/bootstrap_check.sh, scripts/smoke_clean_bootstrap.sh, scripts/smoke_codex_hooks_migration.sh, system/AGENTS.md, system/agents/*.toml
Area: CODEX
-->

# CODEX-03-SYSTEM-INSTALL

## Purpose

This memory records how the repository installs, verifies, rolls back, and diagnoses the owner's system Codex runtime.

## Source Of Truth

- `scripts/install_system_codex.sh`: installer and cache sync.
- `scripts/doctor_system_codex.sh`: installed-state doctor.
- `scripts/rollback_system_codex.sh`: backup listing and restore.
- `scripts/collect_diagnostics.sh`: local diagnostics bundle.
- `scripts/bootstrap_check.sh`: bootstrap sanity checks.
- `scripts/smoke_clean_bootstrap.sh`: clean temporary install smoke.
- `scripts/smoke_codex_hooks_migration.sh`: hook feature migration smoke.
- `system/AGENTS.md` and `system/agents/*.toml`: installed templates.

## Entry Points

- `scripts/install_system_codex.sh --dry-run`: preview global file/config/cache changes.
- `scripts/install_system_codex.sh --apply`: apply managed global Codex state.
- `scripts/doctor_system_codex.sh`: verify installed state.
- `scripts/rollback_system_codex.sh --list`: list installer backups.
- `scripts/rollback_system_codex.sh --restore <backup>`: restore backed up global files.
- `scripts/collect_diagnostics.sh`: write ignored diagnostics bundle for triage.

## Current Behavior

- Installer writes global `AGENTS.md`, managed agents, Codex config sections, marketplace registration, MCP servers, approved tool overrides, and plugin cache.
- Installer preserves unrelated config where supported but owns rldyour-managed sections.
- Installer removes legacy `codex_hooks` aliases and writes `[features].hooks = true`, `[features].plugin_hooks = true`, and `[features].multi_agent = true`.
- Installer derives plugin and MCP runtime data from repository source files instead of static lists.
- Doctor validates the installed result and runs repository marketplace validation as part of the stricter local gate.
- Doctor's fullrepo current-state gate is strict locally and advisory only in GitHub Actions `main` context.
- `scripts/collect_diagnostics.sh` writes local ignored artifacts; do not commit diagnostics bundles.

## Contracts And Data

- Installer backups are the only supported rollback source for global Codex files changed by installer apply.
- Plugin cache must mirror `plugins/<plugin>` under `${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/<plugin>/local`.
- The clean bootstrap smoke must be able to restore fullrepo agent-only context before strict doctor checks.
- Official Codex hook support uses `[features].hooks` for lifecycle hooks. Bundled hooks from enabled plugins require `[features].plugin_hooks = true`; `codex_hooks` is the deprecated alias that must be removed.

## Invariants

- Do not run destructive git or filesystem actions from install/doctor scripts.
- Do not install secrets or machine-local credentials into tracked files.
- Do not bypass marketplace validation in doctor except for explicit CI advisory logic already encoded in the script.
- Restart Codex after successful apply when global config, plugin cache, hooks, skills, or managed agents changed.

## Change Rules

- When installer output shape changes, update doctor and relevant smoke tests in the same commit.
- When official Codex feature flags change, update installer, doctor, migration smoke, global/project instructions, and this memory from source-backed docs.
- When adding managed agents, update installer, doctor, `validate_agent_tools.py`, and system templates if needed.
- When changing fullrepo or clean bootstrap behavior, update `scripts/smoke_clean_bootstrap.sh` and fullrepo memories.

## Verification

- `scripts/install_system_codex.sh --dry-run`
- `scripts/install_system_codex.sh --apply`
- `scripts/doctor_system_codex.sh`
- `scripts/smoke_clean_bootstrap.sh`
- `scripts/smoke_codex_hooks_migration.sh`
- `scripts/rollback_system_codex.sh --list`
