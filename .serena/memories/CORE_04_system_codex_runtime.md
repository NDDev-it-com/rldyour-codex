<!-- Memory Metadata
Last updated: 2026-05-03
Last commit: 72329c8 feat(system): add bootstrap and runtime smoke checks
Scope: /Users/rldyourmnd/.codex/AGENTS.md, /Users/rldyourmnd/.codex/config.toml, /Users/rldyourmnd/.codex/plugins/cache/rldyour-codex, system/AGENTS.md, scripts/install_system_codex.sh, scripts/doctor_system_codex.sh, scripts/validate_marketplace.sh, scripts/bootstrap_check.sh, scripts/smoke_mcp_runtime.sh, scripts/smoke_hooks.sh, pyrightconfig.json, plugins/rldyour-*, .agents/plugins/marketplace.json, AGENTS.md, README.md
Area: CORE
-->

# CORE_04_system_codex_runtime

## Purpose

This memory records the verified system Codex runtime state for the local `rldyour-codex` marketplace. It explains which repository settings are installed into the owner runtime, where the active cache lives, and which runtime facts future sessions must preserve.

## Source Of Truth

- `/Users/rldyourmnd/.codex/config.toml`: active Codex model, trusted projects, enabled plugins, feature flags, marketplace source, and MCP registrations.
- `/Users/rldyourmnd/.codex/plugins/cache/rldyour-codex/<plugin>/local`: active cached plugin copies used by system Codex after marketplace installation.
- `.agents/plugins/marketplace.json`: repository marketplace catalog.
- `plugins/rldyour-*/.codex-plugin/plugin.json`: repository plugin manifests.
- `plugins/rldyour-mcps/.mcp.json`: repository MCP server definitions.
- `AGENTS.md`: project-level Codex instructions for this repository.
- `system/AGENTS.md`: tracked canonical global Codex instructions template.
- `/Users/rldyourmnd/.codex/AGENTS.md`: installed global Codex instructions on this machine.
- `scripts/install_system_codex.sh`: installs global AGENTS, patches rldyour-owned config sections, registers marketplace, and syncs plugin cache.
- `scripts/doctor_system_codex.sh`: verifies installed system state.
- `scripts/validate_marketplace.sh`: local validation entry point for runtime and repository consistency.
- `scripts/smoke_mcp_runtime.sh`: runtime MCP smoke check for installed config, `codex mcp get`, command availability, and remote endpoint reachability.
- `scripts/smoke_hooks.sh`: non-mutating smoke check for repository and installed Serena/Flow hook scripts.
- `scripts/bootstrap_check.sh`: end-to-end bootstrap check for dry-run and apply-mode system setup validation.
- `pyrightconfig.json`: minimal Python project configuration for this scripts-focused repository.

## Entry Points

- `codex plugin marketplace add .`: registers this repository as the local `rldyour-codex` marketplace.
- `codex mcp list`: shows active MCP registrations from system Codex.
- `scripts/validate_marketplace.sh`: validates repository metadata, skills, hooks/scripts, local tool availability, MCP registration, MCP config sync, plugin cache sync, secret patterns, and whitespace.
- `scripts/install_system_codex.sh --dry-run`: previews global Codex installation actions.
- `scripts/install_system_codex.sh --apply`: installs global Codex state into `CODEX_HOME`.
- `scripts/doctor_system_codex.sh`: validates installed global Codex state.
- `scripts/bootstrap_check.sh --dry-run`: previews install and validates repository-local JSON, shell scripts, and repo hook smoke.
- `scripts/bootstrap_check.sh --apply`: runs install preview, install apply, marketplace validation, MCP runtime smoke, hook smoke, system doctor, state checks, and git status.
- `scripts/smoke_mcp_runtime.sh`: checks every configured MCP server through installed Codex runtime metadata and endpoint/command availability.
- `scripts/smoke_hooks.sh`: checks the hook scripts that will be used after restart from both repository sources and installed plugin cache.
- `/Users/rldyourmnd/.codex/config.toml`: direct runtime configuration file for the current machine.
- `/Users/rldyourmnd/.codex/plugins/cache/rldyour-codex`: installed plugin cache root.

## Current Behavior

System Codex is configured with `model = "gpt-5.5"` and `model_reasoning_effort = "xhigh"`.

System Codex is intentionally configured for owner-controlled YOLO execution:

- `profile = "rldyour-yolo"`.
- `approval_policy = "never"`.
- `sandbox_mode = "danger-full-access"`.
- `default_permissions = ":danger-no-sandbox"`.
- `[profiles.rldyour-yolo]` repeats the same approval, sandbox, and default permission values so the named profile remains self-contained.

Trusted projects in system config:

- `/Users/rldyourmnd`.
- `/Users/rldyourmnd/Desktop/codex_base/rldyour-codex`.

Enabled plugin set in system config:

- `gmail@openai-curated`.
- `github@openai-curated`.
- `rldyour-mcps@rldyour-codex`.
- `rldyour-explore@rldyour-codex`.
- `rldyour-serena-mcp@rldyour-codex`.
- `rldyour-security@rldyour-codex`.
- `rldyour-browser@rldyour-codex`.
- `rldyour-design@rldyour-codex`.
- `rldyour-lsps@rldyour-codex`.
- `rldyour-flow@rldyour-codex`.
- `rldyour-rules@rldyour-codex`.

System Codex has `[features] codex_hooks = true`, so hook-capable plugins can run their Codex lifecycle hooks after restart.

`/Users/rldyourmnd/.codex/AGENTS.md` exists and matches `system/AGENTS.md`. The global instructions describe `rldyour-flow` scoped context packs, context sufficiency gates, advisory session/commit hooks, reviewer tracks, post-task synchronization, `openaiDeveloperDocs` routing for OpenAI/Codex documentation, and the owner-requested YOLO execution defaults.

The registered marketplace is local:

- `marketplaces.rldyour-codex.source_type`: `local`.
- `marketplaces.rldyour-codex.source`: `/Users/rldyourmnd/Desktop/codex_base/rldyour-codex`.

The active plugin cache contains local copies for all nine rldyour plugins:

- `rldyour-browser`.
- `rldyour-design`.
- `rldyour-explore`.
- `rldyour-flow`.
- `rldyour-lsps`.
- `rldyour-mcps`.
- `rldyour-rules`.
- `rldyour-security`.
- `rldyour-serena-mcp`.

The full validation script currently validates 37 skills, compact bilingual routing descriptions for all 37 callable skills, strict metadata for 37 `agents/openai.yaml` files, known MCP dependency names, MCP registration, MCP config sync, MCP runtime smoke, plugin cache sync, hook smoke, secret patterns, and whitespace.

The LSP health check reports no missing commands and zero warnings. `pyrightconfig.json` makes the Python script scope explicit for Pyright and removes the previous Python project-config warning.

After commit `72329c8`, `scripts/install_system_codex.sh --apply` synced all repository rldyour plugins into `/Users/rldyourmnd/.codex/plugins/cache/rldyour-codex/<plugin>/local`, patched YOLO permission defaults, and installed all twelve MCP servers. `scripts/doctor_system_codex.sh` verifies those cache directories match repository plugin sources.

`scripts/bootstrap_check.sh --apply` passed on the current machine after commit `72329c8`. It ran install preview, install apply, marketplace validation, MCP runtime smoke, hook smoke, system doctor, Serena state, Flow state, and `git status -sb`.

`scripts/doctor_system_codex.sh` passed on the current machine with zero warnings and zero failures after `scripts/install_system_codex.sh --apply`. It verifies Context7 through the runtime `codex mcp list` output and reports `context7 runtime environment registered` when `CONTEXT7_API_KEY` is visible as a masked runtime environment variable.

## Contracts And Data

System MCP registrations are installed in `/Users/rldyourmnd/.codex/config.toml`, not only in repository `.mcp.json`.

`plugins/rldyour-mcps/.mcp.json` is the portable MCP source of truth. The installed config resolves portable command names to local executable paths. `scripts/validate_marketplace.sh` compares repository and installed MCP definitions, allowing only that command-path resolution difference.

Active local command paths:

- `/opt/homebrew/bin/uvx`: `serena`, `semgrep`.
- `/Users/rldyourmnd/.local/bin/bunx`: `sequential-thinking`, `playwright`, `chrome-devtools`, `context7`, `shadcn`.
- `/opt/homebrew/bin/dart`: `dart-flutter`.

Remote MCP URLs:

- `deepwiki`: `https://mcp.deepwiki.com/mcp`.
- `grep`: `https://mcp.grep.app`.
- `figma`: `https://mcp.figma.com/mcp`.
- `openaiDeveloperDocs`: `https://developers.openai.com/mcp`.

`scripts/smoke_mcp_runtime.sh` treats HTTP responses below 500 as reachable for remote MCP endpoints. This accepts method/auth negotiation responses such as HTTP 405 while still failing server-side outages.

`scripts/smoke_hooks.sh` resolves both repository plugin layout (`plugins/<plugin>`) and installed cache layout (`<plugin>/local`) so it validates the same hook scripts Codex will load after restart.

Environment variables and auth:

- `context7` references `CONTEXT7_API_KEY` through `env_vars`; no raw key should be stored in repository files or memories.
- `sequential-thinking` sets `DISABLE_THOUGHT_LOGGING`.
- `figma` is registered as the remote MCP URL `https://mcp.figma.com/mcp`. Do not store Figma OAuth tokens or bearer tokens in this repository or in memories.
- `openaiDeveloperDocs` is registered as the remote MCP URL `https://developers.openai.com/mcp`; it does not require a repository secret.

## Invariants

- Do not commit `/Users/rldyourmnd/.codex/config.toml` or cached plugin copies.
- Do not store raw API keys, OAuth tokens, cookies, private keys, or bearer tokens in this repository or in memories.
- Keep repository plugin sources as the editable source of truth; use the system cache only as installed runtime output.
- Restart Codex after changing installed plugin manifests, skill descriptions, hook registrations, or MCP runtime definitions.
- Keep hooks enabled only through explicit system config, not through hidden repository side effects.
- Keep `system/AGENTS.md` as the tracked source and `~/.codex/AGENTS.md` as installed output.
- After changing plugin hooks, run `scripts/install_system_codex.sh --apply` and restart Codex so the installed cache and active hook registry are reloaded.
- YOLO permission defaults are intentional owner policy. Do not weaken or remove them unless the owner explicitly changes that policy.

## Change Rules

- Modify repository plugin files first, validate them, then re-install or re-sync into system Codex.
- When changing MCP server definitions, update `plugins/rldyour-mcps/.mcp.json`, re-apply system Codex runtime config, then verify with `scripts/validate_marketplace.sh`, `scripts/doctor_system_codex.sh`, and `codex mcp list`.
- When changing hooks, update the repository hook files and `hooks.json`, verify cache sync, then restart Codex.
- When changing system-only config, record only sanitized facts in memories.
- Use `scripts/install_system_codex.sh --dry-run` before `--apply` on a new machine.
- Use `scripts/bootstrap_check.sh --dry-run` for a non-mutating repository-local bootstrap preview. Use `scripts/bootstrap_check.sh --apply` when the current machine should be installed and verified end-to-end.

## Verification

- `codex mcp list`: verifies enabled MCP server names, commands, URLs, status, and auth mode.
- `codex mcp get openaiDeveloperDocs`: verifies the official OpenAI Docs MCP endpoint.
- `scripts/validate_marketplace.sh`: verifies the full repository, installed MCP config, and installed-cache consistency contract.
- `scripts/doctor_system_codex.sh`: verifies the installed system Codex state.
- `scripts/bootstrap_check.sh --apply`: verifies the clone-to-installed-runtime flow on the current machine.
- `scripts/smoke_mcp_runtime.sh`: verifies installed MCP server names, `codex mcp get`, local MCP command executables, and remote MCP endpoint reachability.
- `scripts/smoke_hooks.sh`: verifies repository and installed Serena/Flow hooks with non-mutating sample payloads.
- `diff -qr plugins/<plugin> /Users/rldyourmnd/.codex/plugins/cache/rldyour-codex/<plugin>/local`: verifies a cached plugin matches the repository source.
- `jq empty .agents/plugins/marketplace.json plugins/*/.codex-plugin/plugin.json`: validates repository marketplace and plugin manifests.
- `rg -n 'ctx7sk|ghp_|github_pat|password|secret|access[_-]?token|private[_-]?key|bearer' .serena/memories plugins .agents`: should show only policy text and placeholders, not real credentials.
