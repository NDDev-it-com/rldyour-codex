<!-- Memory Metadata
Last updated: 2026-05-02
Last commit: 03a05d1 feat(codex): add system install workflow
Scope: system/AGENTS.md, scripts/install_system_codex.sh, scripts/doctor_system_codex.sh, scripts/validate_marketplace.sh, README.md, AGENTS.md, /Users/rldyourmnd/.codex/AGENTS.md, /Users/rldyourmnd/.codex/config.toml
Area: CORE
-->

# CORE_05_system_install_workflow

## Purpose

The system install workflow turns this repository into a portable source of truth for the owner's global Codex setup on any machine. It installs a global `AGENTS.md`, applies rldyour-owned Codex config sections, registers the local marketplace, syncs plugin cache, and verifies the installed state.

## Source Of Truth

- `system/AGENTS.md`: canonical global Codex instruction template.
- `scripts/install_system_codex.sh`: installer with dry-run default and apply mode.
- `scripts/doctor_system_codex.sh`: installed system verification script.
- `scripts/validate_marketplace.sh`: repository and cache validation suite.
- `README.md`: human install commands.
- `AGENTS.md`: repository-level instructions for maintaining this marketplace.
- `/Users/rldyourmnd/.codex/AGENTS.md`: installed global Codex instructions on the current machine.
- `/Users/rldyourmnd/.codex/config.toml`: installed Codex config on the current machine.

## Entry Points

- `scripts/install_system_codex.sh --dry-run`: preview install actions without writing.
- `scripts/install_system_codex.sh --apply`: write global Codex state to `CODEX_HOME`.
- `scripts/doctor_system_codex.sh`: verify installed system state.
- `scripts/validate_marketplace.sh`: validate repository marketplace state and plugin cache.

## Current Behavior

`scripts/install_system_codex.sh` defaults to dry-run. It writes only when `--apply` is passed.

Apply mode:

- Backs up existing `CODEX_HOME/AGENTS.md` and `CODEX_HOME/config.toml` into `CODEX_HOME/backups/rldyour-codex/<timestamp>/` when they exist.
- Installs `system/AGENTS.md` as `CODEX_HOME/AGENTS.md`.
- Runs `codex plugin marketplace add <repo-root>` when the `codex` command is available.
- Patches rldyour-owned sections in `CODEX_HOME/config.toml`: marketplace, repo trust, curated GitHub/Gmail plugins, nine rldyour plugins, `codex_hooks`, and eleven MCP servers.
- Resolves local executable paths for `uvx`, `bunx`, and `dart` from the current machine.
- Syncs each `plugins/rldyour-*` directory into `CODEX_HOME/plugins/cache/rldyour-codex/<plugin>/local`.

`scripts/doctor_system_codex.sh` verifies:

- Installed `CODEX_HOME/AGENTS.md` matches `system/AGENTS.md`.
- No global `AGENTS.override.md` is present.
- `CODEX_HOME/config.toml` has hooks enabled, marketplace source, repo trust, required plugins, and MCP sections.
- `scripts/validate_marketplace.sh` passes.
- `codex mcp list` contains all eleven MCP servers.
- Plugin cache directories match repository plugin directories.

## Contracts And Data

`system/AGENTS.md` is a compact global router/policy file. It must not duplicate full plugin skill bodies because Codex skills provide progressive workflow loading.

The installer manages only rldyour-owned config sections and the curated GitHub/Gmail plugin enablement. It does not write secrets, OAuth tokens, cookies, or raw API keys.

`CONTEXT7_API_KEY` is referenced by name only. Figma, GitHub, Gmail, and other auth remain runtime auth outside this repository.

`--trust-home` is optional and disabled by default. The default installer trusts only the repository path, not the entire home directory.

## Invariants

- Do not make `--apply` the default.
- Do not overwrite `~/.codex/config.toml` without creating a backup.
- Do not commit installed `~/.codex` files, auth state, logs, or plugin cache output.
- Do not store raw credentials in `system/AGENTS.md`, scripts, memories, or README files.
- Restart Codex after changing global AGENTS, config, installed plugins, hooks, skills, or MCP runtime definitions.

## Change Rules

- Update `system/AGENTS.md`, `scripts/install_system_codex.sh`, `scripts/doctor_system_codex.sh`, `README.md`, root `AGENTS.md`, and this memory together when changing global install behavior.
- Run `scripts/install_system_codex.sh --dry-run` before apply-mode testing.
- Run `scripts/install_system_codex.sh --apply` only when installing to the current machine is intended.
- Run `scripts/doctor_system_codex.sh` after apply-mode testing.
- Run `scripts/validate_marketplace.sh` before committing repository changes.

## Verification

- `scripts/install_system_codex.sh --dry-run`: previews install actions and managed counts.
- `scripts/install_system_codex.sh --apply`: installs current system state with backups.
- `scripts/doctor_system_codex.sh`: verifies installed system state.
- `scripts/validate_marketplace.sh`: validates repository, skills, hooks, scripts, MCP registration, cache sync, secret patterns, and whitespace.
- `cmp -s system/AGENTS.md /Users/rldyourmnd/.codex/AGENTS.md`: verifies installed global AGENTS matches the template.
