<!-- Memory Metadata
Last updated: 2026-05-03
Last commit: 72329c8 feat(system): add bootstrap and runtime smoke checks
Scope: system/AGENTS.md, scripts/install_system_codex.sh, scripts/doctor_system_codex.sh, scripts/validate_marketplace.sh, scripts/bootstrap_check.sh, scripts/smoke_mcp_runtime.sh, scripts/smoke_hooks.sh, pyrightconfig.json, README.md, AGENTS.md, plugins/rldyour-mcps/.mcp.json, plugins/rldyour-explore, /Users/rldyourmnd/.codex/AGENTS.md, /Users/rldyourmnd/.codex/config.toml
Area: CORE
-->

# CORE_05_system_install_workflow

## Purpose

The system install workflow turns this repository into a portable source of truth for the owner's global Codex setup on any machine. It installs a global `AGENTS.md`, applies rldyour-owned Codex config sections, registers the local marketplace, syncs plugin cache, and verifies the installed state.

## Source Of Truth

- `system/AGENTS.md`: canonical global Codex instruction template.
- `scripts/install_system_codex.sh`: installer with dry-run default and apply mode.
- `scripts/doctor_system_codex.sh`: installed system verification script.
- `scripts/validate_marketplace.sh`: repository, installed MCP config, and cache validation suite.
- `scripts/bootstrap_check.sh`: dry-run and apply-mode end-to-end bootstrap verification.
- `scripts/smoke_mcp_runtime.sh`: installed MCP runtime smoke verification.
- `scripts/smoke_hooks.sh`: repository and installed hook smoke verification.
- `pyrightconfig.json`: Python script project configuration used by LSP health checks.
- `README.md`: human install commands.
- `AGENTS.md`: repository-level instructions for maintaining this marketplace.
- `/Users/rldyourmnd/.codex/AGENTS.md`: installed global Codex instructions on the current machine.
- `/Users/rldyourmnd/.codex/config.toml`: installed Codex config on the current machine.

## Entry Points

- `scripts/install_system_codex.sh --dry-run`: preview install actions without writing.
- `scripts/install_system_codex.sh --apply`: write global Codex state to `CODEX_HOME`.
- `scripts/doctor_system_codex.sh`: verify installed system state.
- `scripts/validate_marketplace.sh`: validate repository marketplace state, installed MCP config, and plugin cache.
- `scripts/bootstrap_check.sh --dry-run`: preview install actions and validate repository-local bootstrap prerequisites.
- `scripts/bootstrap_check.sh --apply`: install and verify system Codex end-to-end on the current machine.
- `scripts/smoke_mcp_runtime.sh [--codex-home PATH] [--skip-url-check]`: validate MCP runtime registrations and endpoint or command availability.
- `scripts/smoke_hooks.sh [--codex-home PATH] [--repo-only] [--installed-only]`: validate Serena and Flow hook execution without mutating project state.

## Current Behavior

`scripts/install_system_codex.sh` defaults to dry-run. It writes only when `--apply` is passed.

Apply mode:

- Backs up existing `CODEX_HOME/AGENTS.md` and `CODEX_HOME/config.toml` into `CODEX_HOME/backups/rldyour-codex/<timestamp>/` when they exist.
- Installs `system/AGENTS.md` as `CODEX_HOME/AGENTS.md`.
- Runs `codex plugin marketplace add <repo-root>` when the `codex` command is available.
- Patches rldyour-owned sections in `CODEX_HOME/config.toml`: owner-requested YOLO defaults, marketplace, repo trust, curated GitHub/Gmail plugins, nine rldyour plugins, `codex_hooks`, and twelve MCP servers.
- Resolves local executable paths for `uvx`, `bunx`, and `dart` from the current machine.
- Syncs each `plugins/rldyour-*` directory into `CODEX_HOME/plugins/cache/rldyour-codex/<plugin>/local`.

`README.md` now instructs maintainers to run `scripts/install_system_codex.sh --dry-run`, `scripts/install_system_codex.sh --apply`, and `scripts/doctor_system_codex.sh` after changing marketplace metadata, plugin manifests, hooks, skills, or `.mcp.json`.

`README.md` also documents `scripts/bootstrap_check.sh --apply`, `scripts/smoke_mcp_runtime.sh`, and `scripts/smoke_hooks.sh` as runtime smoke checks for new or resynced machines.

`scripts/bootstrap_check.sh` defaults to non-mutating dry-run mode. In dry-run mode it runs install preview, JSON validation, shellcheck, and repository-only hook smoke. In apply mode it runs install preview, install apply, `scripts/validate_marketplace.sh`, MCP runtime smoke, hook smoke, `scripts/doctor_system_codex.sh`, Serena state, Flow state, and `git status -sb`.

`scripts/doctor_system_codex.sh` verifies:

- Installed `CODEX_HOME/AGENTS.md` matches `system/AGENTS.md`.
- No global `AGENTS.override.md` is present.
- `CODEX_HOME/config.toml` has hooks enabled, marketplace source, repo trust, YOLO permission defaults, required plugins, and MCP sections.
- `scripts/validate_marketplace.sh` passes.
- `codex mcp list` contains all twelve MCP servers.
- Plugin cache directories match repository plugin directories.

`scripts/validate_marketplace.sh` has an `MCP config sync` step. It reads `plugins/rldyour-mcps/.mcp.json` and `CODEX_HOME/config.toml`, then checks server names, command basenames, URLs, args, `env_vars`, `env`, startup timeouts, and tool timeouts. It accepts absolute installed command paths when their basename matches the portable repository command.

`scripts/validate_marketplace.sh` now validates `pyrightconfig.json`, runs `scripts/smoke_mcp_runtime.sh`, and runs `scripts/smoke_hooks.sh` after plugin cache sync.

`plugins/rldyour-lsps/scripts/check_lsps.sh` reports zero missing commands and zero warnings for this repository because `pyrightconfig.json` defines the Python script scope.

## Contracts And Data

`system/AGENTS.md` is a compact global router/policy file. It must not duplicate full plugin skill bodies because Codex skills provide progressive workflow loading. It currently routes `rldyour-flow` to `ry-init`, `ry-start`, `ry-newp`, `ry-review`, `ry-deploy`, scoped context packs, context sufficiency gates, orchestrated reviewer tracks, advisory session/commit hooks, and post-task synchronization.

The installer manages only rldyour-owned config sections and the curated GitHub/Gmail plugin enablement. It does not write secrets, OAuth tokens, cookies, or raw API keys.

The installer also manages the owner-requested YOLO defaults:

- top-level `profile = "rldyour-yolo"`;
- top-level `approval_policy = "never"`;
- top-level `sandbox_mode = "danger-full-access"`;
- top-level `default_permissions = ":danger-no-sandbox"`;
- `[profiles.rldyour-yolo]` with the same approval, sandbox, and default permission values.

`CONTEXT7_API_KEY` is referenced by name only. Figma, GitHub, Gmail, and other auth remain runtime auth outside this repository. `openaiDeveloperDocs` uses the official remote endpoint `https://developers.openai.com/mcp` and does not require a repository secret.

`plugins/rldyour-mcps/.mcp.json` is the portable MCP source of truth. Installed `CODEX_HOME/config.toml` is the machine-specific projection of that source.

`scripts/smoke_mcp_runtime.sh` compares repository MCP server names to installed system config, runs `codex mcp get <server>` for every server, checks local command executables, and optionally checks remote MCP URLs. Remote HTTP responses below 500 are accepted as reachable endpoint negotiation responses.

`scripts/smoke_hooks.sh` runs non-mutating smoke payloads for Serena `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop` skip gate, Flow `SessionStart`, Flow `PostToolUse`, and Flow `Stop` skip gate. It checks both repository plugin paths and installed cache paths under `CODEX_HOME/plugins/cache/rldyour-codex/<plugin>/local`.

`--trust-home` is optional and disabled by default. The default installer trusts only the repository path, not the entire home directory.

## Invariants

- Do not make `--apply` the default.
- Do not overwrite `~/.codex/config.toml` without creating a backup.
- Do not commit installed `~/.codex` files, auth state, logs, or plugin cache output.
- Do not store raw credentials in `system/AGENTS.md`, scripts, memories, or README files.
- Restart Codex after changing global AGENTS, config, installed plugins, hooks, skills, or MCP runtime definitions.
- Keep YOLO defaults only because the owner explicitly requested unattended full-access execution.

## Change Rules

- Update `system/AGENTS.md`, `scripts/install_system_codex.sh`, `scripts/doctor_system_codex.sh`, `README.md`, root `AGENTS.md`, and this memory together when changing global install behavior.
- Run `scripts/install_system_codex.sh --dry-run` before apply-mode testing.
- Run `scripts/install_system_codex.sh --apply` only when installing to the current machine is intended.
- Run `scripts/doctor_system_codex.sh` after apply-mode testing.
- Run `scripts/bootstrap_check.sh --dry-run` before documenting a zero-machine bootstrap flow.
- Run `scripts/bootstrap_check.sh --apply` when proving the current machine can install and verify the full system state end-to-end.
- After changing `.mcp.json`, run the installer and doctor workflow before final delivery so portable and installed MCP state cannot drift.
- Run `scripts/validate_marketplace.sh` before committing repository changes.

## Verification

- `scripts/install_system_codex.sh --dry-run`: previews install actions and managed counts.
- `scripts/install_system_codex.sh --apply`: installs current system state with backups.
- `scripts/doctor_system_codex.sh`: verifies installed system state.
- `scripts/validate_marketplace.sh`: validates repository, skills, hooks, scripts, MCP registration, MCP config sync, cache sync, secret patterns, and whitespace.
- `scripts/bootstrap_check.sh --apply`: proves install, runtime smoke, hook smoke, doctor, and state checks work together.
- `scripts/smoke_mcp_runtime.sh`: verifies installed MCP runtime definitions through Codex and endpoint/command probes.
- `scripts/smoke_hooks.sh`: verifies hook scripts execute in repository and installed cache layouts.
- `codex mcp get openaiDeveloperDocs`: verifies the installed OpenAI Docs MCP endpoint.
- `cmp -s system/AGENTS.md /Users/rldyourmnd/.codex/AGENTS.md`: verifies installed global AGENTS matches the template.
