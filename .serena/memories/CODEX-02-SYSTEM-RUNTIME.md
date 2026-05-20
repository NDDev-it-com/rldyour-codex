<!-- Memory Metadata
Last updated: 2026-05-20
Last commit: 697f44d chore(codex): refresh system runtime pins
Scope: ${CODEX_HOME:-$HOME/.codex}/config.toml, ${CODEX_HOME:-$HOME/.codex}/AGENTS.md, ${CODEX_HOME:-$HOME/.codex}/agents/*.toml, ${CODEX_HOME:-$HOME/.codex}/rules/*.rules, ${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex, system/AGENTS.md, system/agents/*.toml, system/rules/*.rules, scripts/install_system_codex.sh, scripts/doctor_system_codex.sh, scripts/validate_execpolicy_rules.sh, plugins/rldyour-mcps/.mcp.json
Area: CODEX
-->

# CODEX-02-SYSTEM-RUNTIME

## Purpose

This memory records the installed system Codex runtime state owned by this repository: config shape, permissions/model defaults, managed agents, plugin cache, MCP registration, and restart-sensitive files.

## Source Of Truth

- `system/AGENTS.md`: canonical global Codex instruction template.
- `system/agents/*.toml`: canonical managed subagent configs.
- `system/rules/*.rules`: canonical managed Codex execpolicy rule files.
- `scripts/install_system_codex.sh`: writes global config, AGENTS, agents, execpolicy rules, marketplace registration, MCP servers, approved tool overrides, plugin cache, and trusted hook hashes.
- `scripts/doctor_system_codex.sh`: verifies installed runtime state.
- `scripts/validate_execpolicy_rules.sh`: validates managed rule decisions with `codex execpolicy check`.
- `plugins/rldyour-mcps/.mcp.json`: MCP server definitions.
- `.agents/plugins/marketplace.json`: enabled rldyour plugin set.
- `config/mcp-runtime-versions.env`: pinned Codex CLI and MCP launcher versions.
- `${CODEX_HOME:-$HOME/.codex}/config.toml`: active system Codex config.
- `${CODEX_HOME:-$HOME/.codex}/agents/*.toml`: installed managed agent configs.
- `${CODEX_HOME:-$HOME/.codex}/rules/*.rules`: installed managed execpolicy rules.
- `${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/<plugin>/local`: installed plugin cache used by Codex.

## Entry Points

- `scripts/install_system_codex.sh --dry-run`: preview managed system changes.
- `scripts/install_system_codex.sh --apply`: apply managed system state.
- `scripts/doctor_system_codex.sh`: verify active system state and plugin cache parity.
- `scripts/validate_execpolicy_rules.sh`: verify destructive, secrets, git, release, and allow examples for managed rules.
- `codex mcp list`: inspect registered MCP servers.

## Current Behavior

- System Codex is intentionally configured for owner-controlled YOLO execution: `approval_policy = "never"`, `sandbox_mode = "danger-full-access"`, `default_permissions = ":danger-no-sandbox"`, `profile = "rldyour-yolo"`.
- Current official Codex documentation treats `sandbox_mode` as the active older sandbox model when present, so the owner YOLO profile is not migrated to beta permission profiles without an explicit policy decision.
- YOLO execution is paired with managed Codex execpolicy rails installed from `system/rules/*.rules` into `${CODEX_HOME:-$HOME/.codex}/rules/*.rules`. These rules forbid obvious destructive and secret-read commands, prompt for risky git/release operations, and allow common read-only inspection commands.
- Parent model defaults are `model = "gpt-5.5"` and `model_reasoning_effort = "xhigh"`.
- Generated `config.toml` starts with the official schema hint `#:schema https://developers.openai.com/codex/config-schema.json`.
- `[features].hooks = true`, `[features].plugin_hooks = true`, and `[features].multi_agent = true` are managed. `hooks` enables lifecycle hooks, `plugin_hooks` opts into bundled hooks from enabled plugins, and `multi_agent` enables Codex subagent tools.
- Managed subagents are installed from `system/agents/*.toml`; all rldyour-managed roles use `gpt-5.5` with `medium` reasoning.
- Managed subagents currently include a temporary MCP isolation policy because Codex can eagerly initialize MCP servers per spawned session/subagent. Subagents keep the lightweight inherited core surface (`sequential-thinking`, `serena`, `context7`, `grep`, `deepwiki`, `openaiDeveloperDocs`, and built-in `codex_apps`) while specialist MCP servers (`semgrep`, `figma`, `playwright`, `chrome-devtools`, `dart-flutter`, `shadcn`) remain parent-session tools.
- Since `66070a8`, disabled specialist MCP overrides in managed subagent TOML files include complete transport metadata copied from `plugins/rldyour-mcps/.mcp.json`. This prevents Codex from ignoring standalone custom-agent role files with `invalid transport` warnings when an override disables a server but still declares an MCP table.
- Current runtime pins installed by `scripts/install_system_codex.sh --apply --strict-runtime`: Codex CLI `0.132.0`, Serena Agent `1.5.1`, Chrome DevTools MCP `1.0.1`, Bun `1.3.14`, Node major `24`, Semgrep `1.163.0`, Playwright MCP `0.0.75`, Context7 MCP `2.2.5`, and shadcn `4.7.0`.
- `codex_apps` is not represented as an `mcp_servers` table in managed agents. It remains available through the inherited Apps/connectors surface.
- Active managed roles are `architecture-reviewer`, `browser-tester`, `consistency-reviewer`, `quality-reviewer`, `research-explorer`, `security-audit`, `serena-sync`, and `test-reviewer`.
- Installer/doctor derive rldyour plugin enablement from `.agents/plugins/marketplace.json` and MCP registration from `plugins/rldyour-mcps/.mcp.json`.
- Installer refreshes installed rldyour plugin hook trust after cache sync by reading `currentHash` from the app-server RPC method `hooks/list` over `codex app-server --listen stdio://` and upserting `hooks.state` through `config/batchWrite`.
- Doctor includes a live hook trust gate: all installed rldyour plugin hooks returned by the `hooks/list` app-server RPC method must be present, enabled, and `trustStatus = trusted`.
- Doctor verifies installed managed execpolicy rules exactly match `system/rules/*.rules`.
- After plugin/hook/skill/agent changes, plugin cache must be synced through `scripts/install_system_codex.sh --apply`, and Codex should be restarted for runtime reload.

## Contracts And Data

- `${CODEX_HOME:-$HOME/.codex}/AGENTS.md` is generated from `system/AGENTS.md`.
- `${CODEX_HOME:-$HOME/.codex}/agents/*.toml` must match `system/agents/*.toml` exactly.
- `${CODEX_HOME:-$HOME/.codex}/rules/*.rules` must match `system/rules/*.rules` exactly.
- `scripts/doctor_system_codex.sh` checks config schema hint, `hooks`/`plugin_hooks`/`multi_agent` feature flags, model defaults, managed agents, managed subagent temporary MCP isolation with complete disabled transport metadata, managed execpolicy rules, marketplace-derived plugin enablement, MCP registration, plugin cache parity, installed rldyour plugin hook trust, and fullrepo current-state.
- `${CODEX_HOME:-$HOME/.codex}/config.toml` stores `hooks.state.<hook key>.trusted_hash` values that must match the installed hook definitions after plugin cache changes.
- Plugin cache parity matters for runtime because installed hooks and skills execute from `${CODEX_HOME}` in normal Codex sessions.

## Invariants

- Do not reintroduce deprecated hook aliases such as `codex_hooks`.
- Do not remove `[features].plugin_hooks = true`; without it, enabled rldyour plugin hook declarations can remain installed but not loaded as bundled plugin hooks.
- Do not leave installed rldyour plugin hooks in `modified` or `untrusted` trust state after cache sync; run installer apply and doctor to refresh and verify `hooks.state`.
- Do not hardcode parallel plugin/MCP lists in installer or doctor scripts.
- Do not change YOLO permission defaults without explicit owner request.
- Do not migrate the owner profile from `sandbox_mode = "danger-full-access"` to beta permission profiles without an explicit owner policy decision.
- Do not remove managed execpolicy rules while `approval_policy = "never"` and `sandbox_mode = "danger-full-access"` remain the owner-selected defaults.
- Do not add synthetic `[mcp_servers.codex_apps]` entries to managed agent TOML files.
- Do not leave disabled managed-agent MCP tables without `command` or `url`; copy transport metadata from `plugins/rldyour-mcps/.mcp.json`.
- Restart Codex after changing global `AGENTS.md`, `config.toml`, managed agents, installed plugins, hooks, skills, or MCP runtime definitions.

## Change Rules

- After editing `system/AGENTS.md`, `system/agents/*.toml`, `system/rules/*.rules`, plugin manifests, hooks, or skills, run installer apply, then doctor.
- If doctor fails only on fullrepo current-state while normal branch is dirty or unpublished, finish normal branch and fullrepo sync before treating it as a real runtime failure.
- Keep managed agent model, reasoning settings, and temporary MCP isolation aligned with repository policy unless the owner explicitly changes them.

## Verification

- `scripts/install_system_codex.sh --dry-run`: preview install.
- `scripts/install_system_codex.sh --apply`: sync active system runtime and plugin cache.
- `scripts/doctor_system_codex.sh`: installed-state verification.
- `python3 scripts/validate_agent_tools.py`: source-tree managed agent, skill, and temporary subagent MCP policy verification.
- `scripts/validate_execpolicy_rules.sh`: managed execpolicy rule decision validation.
- App-server RPC method `hooks/list` over `codex app-server --listen stdio://`: live source of current hook keys, hashes, enabled flags, and trust status.
- `diff -qr plugins/<plugin> "${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/<plugin>/local"`: targeted plugin cache parity check.
