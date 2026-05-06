<!-- Memory Metadata
Last updated: 2026-05-06
Last commit: d675a30 fix(flow): ignore remote head in git sync audit
Scope: system/AGENTS.md, README.md, AGENTS.md, .claude/CLAUDE.md, scripts/validate_instruction_docs.py, scripts/validate_marketplace.sh, scripts/smoke_fullrepo_sync.sh, plugins/rldyour-flow/scripts/instruction_docs_state.py, ${CODEX_HOME:-$HOME/.codex}/AGENTS.md, ${CODEX_HOME:-$HOME/.codex}/config.toml
Area: CORE
-->

# CORE_05_system_install_workflow

## Purpose

This repository owns the canonical install/doctor/rollback workflow for this Codex setup. The workflow writes:

- global `~/.codex/AGENTS.md`
- `~/.codex/config.toml` managed sections
- plugin cache from `plugins/rldyour-*`
- `plugins` + MCP runtime config synchronization

## Source Of Truth

- `system/AGENTS.md` (template source)
- `scripts/install_system_codex.sh`
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
  - codex hooks enabled
- required marketplace plugin registrations
- required MCP server configuration
- plugin cache parity against repository plugins
- fullrepo status script availability
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

## Invariants

- Keep global configuration write scope explicit and reversible.
- Do not install secrets or tokens.
- Do not run destructive fullrepo mutations from install script.
- Restart Codex after template/config/cache changes so runtime reloads plugin and hook state.
- Run required checks before considering installation or rollback complete.
