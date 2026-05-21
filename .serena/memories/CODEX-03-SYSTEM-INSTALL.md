<!-- Memory Metadata
Last updated: 2026-05-21
Last commit: 761e03f chore(release): 0.4.2
Scope: scripts/install_system_codex.sh, scripts/doctor_system_codex.sh, scripts/plugin_cache_contract.py, scripts/smoke_codex_hook_listing.py, scripts/validate_contract.py, scripts/validate_runtime_prereqs.py, scripts/validate_runtime.sh, scripts/rollback_system_codex.sh, scripts/collect_diagnostics.sh, scripts/bootstrap_check.sh, scripts/smoke_clean_bootstrap.sh, scripts/smoke_codex_hooks_migration.sh, system/AGENTS.md, system/agents/*.toml, pyproject.toml, scripts/validate_marketplace.sh, config/rldyour-contract.json
Area: CODEX
-->

# CODEX-03-SYSTEM-INSTALL

## Purpose

This memory records how the repository installs, verifies, rolls back, and diagnoses the owner's system Codex runtime.

## Source Of Truth

- `scripts/install_system_codex.sh`: installer and cache sync.
- `scripts/doctor_system_codex.sh`: installed-state doctor.
- `scripts/plugin_cache_contract.py`: manifest-versioned plugin cache contract for installer, doctor, and marketplace validation.
- `scripts/smoke_codex_hook_listing.py`: live Codex `hooks/list` smoke for installed bundled plugin hooks.
- `scripts/validate_contract.py`: source-tree Codex adapter contract validator.
- `scripts/validate_runtime_prereqs.py`: strict launcher prerequisite validator for enabled MCP/Codex runtime surfaces.
- `scripts/validate_runtime.sh`: focused installer/runtime/hook/fullrepo validation slice.
- `scripts/rollback_system_codex.sh`: backup listing and restore.
- `scripts/collect_diagnostics.sh`: local diagnostics bundle.
- `scripts/bootstrap_check.sh`: bootstrap sanity checks.
- `scripts/smoke_clean_bootstrap.sh`: clean temporary install smoke.
- `scripts/smoke_codex_hooks_migration.sh`: hook feature migration smoke.
- `system/AGENTS.md` and `system/agents/*.toml`: installed templates.

## Entry Points

- `scripts/install_system_codex.sh --dry-run`: preview global file/config/cache changes.
- `scripts/install_system_codex.sh --apply`: apply managed global Codex state.
- `scripts/install_system_codex.sh --apply --strict-runtime`: apply managed global Codex state only when required launchers for enabled runtime surfaces are present.
- `scripts/doctor_system_codex.sh --quick`: verify installed state without running the full marketplace validation path.
- `scripts/doctor_system_codex.sh --strict-runtime`: verify installed state and fail on missing launchers for enabled runtime surfaces.
- `scripts/doctor_system_codex.sh --full`: verify installed state and run the full marketplace validation path.
- `scripts/rollback_system_codex.sh --list`: list installer backups.
- `scripts/rollback_system_codex.sh --restore <backup>`: restore backed up global files.
- `scripts/collect_diagnostics.sh`: write ignored diagnostics bundle for triage.
- `python3 scripts/plugin_cache_contract.py verify`: check installed versioned cache parity.
- `python3 scripts/smoke_codex_hook_listing.py`: verify installed hooks are visible, trusted, enabled, and sourced from versioned cache paths.

## Current Behavior

- Installer writes global `AGENTS.md`, managed agents, Codex config sections, marketplace registration, MCP servers, approved tool overrides, and versioned plugin cache.
- Installer preserves unrelated config where supported but owns rldyour-managed sections.
- Installer removes legacy `codex_hooks` aliases and writes `[features].hooks = true`, `[features].plugin_hooks = true`, and `[features].multi_agent = true`.
- Installer derives plugin and MCP runtime data from repository source files instead of static lists.
- Installer derives plugin cache targets from plugin manifest `name` and `version` through `scripts/plugin_cache_contract.py`.
- Installer strict runtime mode (`--strict` or `--strict-runtime`) validates enabled MCP/Codex launcher prerequisites through `scripts/validate_runtime_prereqs.py` before writing managed config.
- Installer refuses malformed existing `config.toml` instead of silently falling back to an empty config model.
- Rollback restores backed-up files through temporary files before renaming them into place.
- Doctor supports quick, strict-runtime, and full modes. Quick mode validates installed config and runtime prerequisites without the full marketplace path; full mode includes repository marketplace validation, versioned cache parity, and live hook trust.
- Doctor validates that installed managed subagent TOML files match source, preserve the temporary MCP isolation policy, include complete disabled transport metadata copied from `.mcp.json`, and do not declare built-in `codex_apps` under `mcp_servers`.
- Doctor's fullrepo current-state gate is strict locally and advisory only in GitHub Actions `main` context.
- Doctor intentionally fails the local fullrepo current-state gate while normal-branch code/config changes are dirty; rerun after normal commit/push/fullrepo publish for final green state.
- `scripts/collect_diagnostics.sh` writes local ignored artifacts; do not commit diagnostics bundles.
- `scripts/validate_runtime.sh --strict-runtime` installs into a temporary `CODEX_HOME`, runs quick strict doctor, validates execpolicy rules, runs `scripts/smoke_codex_hook_listing.py`, then runs hook/fullrepo bootstrap smokes.

## Contracts And Data

- Installer backups are the only supported rollback source for global Codex files changed by installer apply.
- Plugin cache must mirror `plugins/<plugin>` under `${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/<plugin>/<version>`.
- Legacy `<plugin>/local` paths are fallback-only compatibility paths in wrapper scripts; installer, doctor, marketplace validation, and runtime smoke use versioned paths.
- Strict runtime mode checks launcher availability for enabled local MCP servers and the Codex CLI surface; it should fail rather than silently installing a config that cannot start required local tooling.
- The clean bootstrap smoke must be able to restore fullrepo agent-only context before strict doctor checks.
- Official Codex hook support uses `[features].hooks` for lifecycle hooks. Bundled hooks from enabled plugins require `[features].plugin_hooks = true`; `codex_hooks` is the deprecated alias that must be removed.

## Invariants

- Do not run destructive git or filesystem actions from install/doctor scripts.
- Do not install secrets or machine-local credentials into tracked files.
- Do not bypass marketplace validation in full doctor mode except for explicit CI advisory logic already encoded in the script.
- Restart Codex after successful apply when global config, plugin cache, hooks, skills, or managed agents changed.
- Do not install owner YOLO defaults from repo-local `.codex/config.toml` or `config.toml`; YOLO is owner-local installer policy and `scripts/validate_contract.py` rejects repo-local YOLO defaults.

## Change Rules

- When installer output shape changes, update doctor and relevant smoke tests in the same commit.
- When official Codex feature flags change, update installer, doctor, migration smoke, global/project instructions, and this memory from source-backed docs.
- When adding managed agents, update installer, doctor, `validate_agent_tools.py`, and system templates if needed.
- When changing adapter surface, update `config/rldyour-contract.json`, `docs/contract-matrix.md`, `scripts/validate_contract.py` coverage, and release validation wiring.
- When changing plugin cache layout, update `scripts/plugin_cache_contract.py`, installer, doctor, marketplace validation, hook smoke installed-root resolution, and fallback wrapper tests.
- When changing managed agent MCP policy, run installer apply, quick strict doctor, agent-tool validation, and a Codex startup smoke to catch standalone role deserialization warnings.
- When changing fullrepo or clean bootstrap behavior, update `scripts/smoke_clean_bootstrap.sh` and fullrepo memories.

## Verification

- `scripts/install_system_codex.sh --dry-run`
- `scripts/install_system_codex.sh --apply --strict-runtime`
- `scripts/doctor_system_codex.sh --quick --strict-runtime`
- `scripts/doctor_system_codex.sh --strict-runtime`
- `scripts/validate_runtime.sh --strict-runtime`
- `python3 scripts/plugin_cache_contract.py verify`
- `python3 scripts/smoke_codex_hook_listing.py`
- `python3 scripts/validate_contract.py`
- `scripts/smoke_clean_bootstrap.sh`
- `scripts/smoke_codex_hooks_migration.sh`
- `scripts/rollback_system_codex.sh --list`
