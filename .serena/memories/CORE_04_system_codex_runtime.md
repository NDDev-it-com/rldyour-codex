<!-- Memory Metadata
Last updated: 2026-05-02
Last commit: ca06abf docs: sync flow catalog description
Scope: /Users/rldyourmnd/.codex/AGENTS.md, /Users/rldyourmnd/.codex/config.toml, /Users/rldyourmnd/.codex/plugins/cache/rldyour-codex, system/AGENTS.md, scripts/install_system_codex.sh, scripts/doctor_system_codex.sh, scripts/validate_marketplace.sh, plugins/rldyour-*, .agents/plugins/marketplace.json, AGENTS.md
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

## Entry Points

- `codex plugin marketplace add .`: registers this repository as the local `rldyour-codex` marketplace.
- `codex mcp list`: shows active MCP registrations from system Codex.
- `scripts/validate_marketplace.sh`: validates repository metadata, skills, hooks/scripts, local tool availability, MCP registration, cache sync, secret patterns, and whitespace.
- `scripts/install_system_codex.sh --dry-run`: previews global Codex installation actions.
- `scripts/install_system_codex.sh --apply`: installs global Codex state into `CODEX_HOME`.
- `scripts/doctor_system_codex.sh`: validates installed global Codex state.
- `/Users/rldyourmnd/.codex/config.toml`: direct runtime configuration file for the current machine.
- `/Users/rldyourmnd/.codex/plugins/cache/rldyour-codex`: installed plugin cache root.

## Current Behavior

System Codex is configured with `model = "gpt-5.5"` and `model_reasoning_effort = "xhigh"`.

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

`/Users/rldyourmnd/.codex/AGENTS.md` exists and matches `system/AGENTS.md`. Commit `e506ccb feat(flow): add context sufficiency hooks` updated the global instructions to describe `rldyour-flow` scoped context packs, context sufficiency gates, advisory session/commit hooks, reviewer tracks, and post-task synchronization.

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

The full validation script currently validates 37 skills, compact bilingual routing descriptions for all 37 callable skills, strict metadata for 37 `agents/openai.yaml` files, known MCP dependency names, and cache sync for every rldyour plugin. The LSP health check reports no missing commands and one expected project warning: this marketplace repository has Python scripts but no `pyproject.toml` or `pyrightconfig.json`.

After commit `e506ccb`, `scripts/install_system_codex.sh --apply` synced the updated `rldyour-flow` plugin into `/Users/rldyourmnd/.codex/plugins/cache/rldyour-codex/rldyour-flow/local`. `diff -qr plugins/rldyour-flow /Users/rldyourmnd/.codex/plugins/cache/rldyour-codex/rldyour-flow/local` returns clean.

`scripts/doctor_system_codex.sh` passed on the current machine with zero warnings and zero failures after `scripts/install_system_codex.sh --apply`. It verifies Context7 through the runtime `codex mcp list` output and reports `context7 runtime environment registered` when `CONTEXT7_API_KEY` is visible as a masked runtime environment variable.

## Contracts And Data

System MCP registrations are installed in `/Users/rldyourmnd/.codex/config.toml`, not only in repository `.mcp.json`.

Active local command paths:

- `/opt/homebrew/bin/uvx`: `serena`, `semgrep`.
- `/Users/rldyourmnd/.local/bin/bunx`: `sequential-thinking`, `playwright`, `chrome-devtools`, `context7`, `shadcn`.
- `/opt/homebrew/bin/dart`: `dart-flutter`.

Remote MCP URLs:

- `deepwiki`: `https://mcp.deepwiki.com/mcp`.
- `grep`: `https://mcp.grep.app`.
- `figma`: `https://mcp.figma.com/mcp`.

Environment variables and auth:

- `context7` references `CONTEXT7_API_KEY` through `env_vars`; no raw key should be stored in repository files or memories.
- `sequential-thinking` sets `DISABLE_THOUGHT_LOGGING`.
- `figma` is registered as the remote MCP URL `https://mcp.figma.com/mcp`. Do not store Figma OAuth tokens or bearer tokens in this repository or in memories.

## Invariants

- Do not commit `/Users/rldyourmnd/.codex/config.toml` or cached plugin copies.
- Do not store raw API keys, OAuth tokens, cookies, private keys, or bearer tokens in this repository or in memories.
- Keep repository plugin sources as the editable source of truth; use the system cache only as installed runtime output.
- Restart Codex after changing installed plugin manifests, skill descriptions, hook registrations, or MCP runtime definitions.
- Keep hooks enabled only through explicit system config, not through hidden repository side effects.
- Keep `system/AGENTS.md` as the tracked source and `~/.codex/AGENTS.md` as installed output.
- After changing plugin hooks, run `scripts/install_system_codex.sh --apply` and restart Codex so the installed cache and active hook registry are reloaded.

## Change Rules

- Modify repository plugin files first, validate them, then re-install or re-sync into system Codex.
- When changing MCP server definitions, update `plugins/rldyour-mcps/.mcp.json`, re-apply system Codex runtime config, then verify with `codex mcp list`.
- When changing hooks, update the repository hook files and `hooks.json`, verify cache sync, then restart Codex.
- When changing system-only config, record only sanitized facts in memories.
- Use `scripts/install_system_codex.sh --dry-run` before `--apply` on a new machine.

## Verification

- `codex mcp list`: verifies enabled MCP server names, commands, URLs, status, and auth mode.
- `scripts/validate_marketplace.sh`: verifies the full repository and installed-cache consistency contract.
- `scripts/doctor_system_codex.sh`: verifies the installed system Codex state.
- `diff -qr plugins/<plugin> /Users/rldyourmnd/.codex/plugins/cache/rldyour-codex/<plugin>/local`: verifies a cached plugin matches the repository source.
- `jq empty .agents/plugins/marketplace.json plugins/*/.codex-plugin/plugin.json`: validates repository marketplace and plugin manifests.
- `rg -n 'ctx7sk|ghp_|github_pat|password|secret|access[_-]?token|private[_-]?key|bearer' .serena/memories plugins .agents`: should show only policy text and placeholders, not real credentials.
