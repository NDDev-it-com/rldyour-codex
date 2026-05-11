<!-- Memory Metadata
Last updated: 2026-05-11
Last commit: 7825a59 chore(codex): reproduce managed system defaults
Scope: system/AGENTS.md, README.md, AGENTS.md, .claude/CLAUDE.md, scripts/install_system_codex.sh, scripts/smoke_codex_hooks_migration.sh, scripts/doctor_system_codex.sh, scripts/validate_instruction_docs.py, scripts/validate_marketplace.sh, scripts/smoke_mcp_runtime.sh, scripts/smoke_fullrepo_sync.sh, plugins/rldyour-flow/scripts/instruction_docs_state.py, ${CODEX_HOME:-$HOME/.codex}/AGENTS.md, ${CODEX_HOME:-$HOME/.codex}/config.toml
Area: CORE
-->

# CORE_05_system_install_workflow

## Purpose

This repository owns the canonical install/doctor/rollback workflow for this Codex setup. The workflow writes:

- global `~/.codex/AGENTS.md`
- `~/.codex/config.toml` managed sections
- owner-selected model defaults and MCP tool approval overrides
- plugin cache from `plugins/rldyour-*`
- `plugins` + MCP runtime config synchronization

## Source Of Truth

- `system/AGENTS.md` (template source)
- `scripts/install_system_codex.sh`
- `scripts/smoke_codex_hooks_migration.sh`
- `scripts/doctor_system_codex.sh`
- `scripts/rollback_system_codex.sh`
- `scripts/bootstrap_check.sh`
- `scripts/sync_fullrepo_branch.sh`
- `plugins/rldyour-mcps/.mcp.json`
- `config/mcp-runtime-versions.env`
- `.github/workflows/validate.yml`

## Install Contract

### `scripts/install_system_codex.sh`

- Default mode: dry-run.
- `--apply` writes:
  - `CODEX_HOME/AGENTS.md` from `system/AGENTS.md`
  - patched `CODEX_HOME/config.toml`
  - `[features].hooks = true`
  - `model = "gpt-5.5"`
  - `model_reasoning_effort = "xhigh"`
  - approved MCP tool overrides for sequential-thinking, DeepWiki, and Grep
  - deprecated/unstable hook key removal for `codex_hooks` and `plugin_hooks` from `[features]`, quoted keys, dotted root keys, and inline root feature tables
  - unrelated feature flags preserved when hook keys are normalized
  - plugin cache for every `plugins/rldyour-*` into `CODEX_HOME/plugins/cache/rldyour-codex/<plugin>/local`
- optional:
  - `--codex-home PATH`
  - `--trust-home` (explicit opt-in only; default false)
- backs up existing `AGENTS.md` and `config.toml` into:
  - `$CODEX_HOME/backups/rldyour-codex/<timestamp>/`

### `scripts/doctor_system_codex.sh`

Validates:

- installed `AGENTS.md` equals repository `system/AGENTS.md`
- config contains:
  - profile and permissions (`rldyour-yolo`, `never`, `danger-full-access`, `:danger-no-sandbox`)
  - owner-selected model defaults (`gpt-5.5`, `xhigh`)
  - `[features].hooks = true`
  - no legacy `codex_hooks` key and no unstable `plugin_hooks` key under `[features]`
  - approved MCP tool overrides
- required marketplace plugin registrations
- required MCP server configuration
- plugin cache parity against repository plugins
- fullrepo status script availability
- no dirty non-agent files during doctor checks
- on `main`, remote fullrepo tree matches current `HEAD` plus agent-only files when agent-only files exist
- `scripts/validate_marketplace.sh` pass

### `scripts/bootstrap_check.sh`

- `--dry-run`: dry install + local checks + hook/fullrepo smoke
- `--apply`: install + validate script suite + doctor + state checks
- Useful for new-machine sanity flow.

## Fullrepo + Runtime Contract

- Fullrepo/agent-only context restore path uses:
  - `scripts/sync_fullrepo_branch.sh --bootstrap-init`
  - `scripts/sync_fullrepo_branch.sh --status`
  - `scripts/sync_fullrepo_branch.sh --publish`
- Bootstrap is required before relying on agent-only files. It restores existing `origin/fullrepo`, publishes local agent-only files when no remote branch exists, installs `.git/info/exclude`, and removes tracked agent-only files from the current branch index when migration is needed.
- `install_system_codex.sh` does not mutate installed fullrepo branch; it only ensures local cache and runtime config.

## Rollback Contract

- `scripts/rollback_system_codex.sh --list`: list available install backups.
- `scripts/rollback_system_codex.sh --restore <backup> [--dry-run]`:
  - restore `AGENTS.md` and `config.toml` from backup
  - prints `Dry-run` plan without filesystem writes when requested.
- Pre-restore of current state is created automatically during real restore.

## Verification Commands

- `scripts/install_system_codex.sh --dry-run`
- `scripts/install_system_codex.sh --apply`
- `scripts/smoke_codex_hooks_migration.sh`
- `scripts/doctor_system_codex.sh`
- `scripts/validate_marketplace.sh`
- `scripts/smoke_mcp_runtime.sh`
- `scripts/smoke_mcp_capabilities.sh`
- `scripts/smoke_hooks.sh`
- `scripts/smoke_clean_bootstrap.sh`
- `scripts/smoke_fullrepo_bootstrap_init.sh`
- `scripts/bootstrap_check.sh --apply`
- `scripts/sync_fullrepo_branch.sh --status`
- `scripts/sync_fullrepo_branch.sh --bootstrap-init`
- `scripts/rollback_system_codex.sh --list`

`scripts/smoke_mcp_runtime.sh` retries remote URL checks by default and validates URL MCPs with a Streamable HTTP JSON-RPC `initialize` POST preflight. `401`/`403` are accepted for auth-gated endpoints; POST `405` is a failure, because `405` is only valid for optional GET SSE. Use `--skip-url-check` only for intentionally offline validation.

## Invariants

- Keep global configuration write scope explicit and reversible.
- Do not install secrets or tokens.
- Do not treat transient runtime/UI state such as `[tui.model_availability_nux]` as source-of-truth.
- Do not run destructive fullrepo mutations from install script.
- Use the stable Codex `hooks` feature flag; do not reintroduce deprecated `codex_hooks` or under-development `plugin_hooks`.
- Restart Codex after template/config/cache changes so runtime reloads plugin and hook state.
- Run required checks before considering installation or rollback complete.
