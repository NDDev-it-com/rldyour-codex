<!-- Memory Metadata
Last updated: 2026-05-16
Last commit: 1132859 feat(serena): harden codex memory sync brain
Scope: ${CODEX_HOME:-$HOME/.codex}/config.toml, ${CODEX_HOME:-$HOME/.codex}/AGENTS.md, ${CODEX_HOME:-$HOME/.codex}/agents/*.toml, ${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex, system/AGENTS.md, system/agents/*.toml, scripts/install_system_codex.sh, scripts/doctor_system_codex.sh, plugins/rldyour-mcps/.mcp.json
Area: CODEX
-->

# CODEX-02-SYSTEM-RUNTIME

## Purpose

This memory records the installed system Codex runtime state owned by this repository: config shape, permissions/model defaults, managed agents, plugin cache, MCP registration, and restart-sensitive files.

## Source Of Truth

- `system/AGENTS.md`: canonical global Codex instruction template.
- `system/agents/*.toml`: canonical managed subagent configs.
- `scripts/install_system_codex.sh`: writes global config, AGENTS, agents, marketplace registration, MCP servers, approved tool overrides, and plugin cache.
- `scripts/doctor_system_codex.sh`: verifies installed runtime state.
- `plugins/rldyour-mcps/.mcp.json`: MCP server definitions.
- `.agents/plugins/marketplace.json`: enabled rldyour plugin set.
- `config/mcp-runtime-versions.env`: pinned Codex CLI and MCP launcher versions.
- `${CODEX_HOME:-$HOME/.codex}/config.toml`: active system Codex config.
- `${CODEX_HOME:-$HOME/.codex}/agents/*.toml`: installed managed agent configs.
- `${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/<plugin>/local`: installed plugin cache used by Codex.

## Entry Points

- `scripts/install_system_codex.sh --dry-run`: preview managed system changes.
- `scripts/install_system_codex.sh --apply`: apply managed system state.
- `scripts/doctor_system_codex.sh`: verify active system state and plugin cache parity.
- `codex mcp list`: inspect registered MCP servers.

## Current Behavior

- System Codex is intentionally configured for owner-controlled YOLO execution: `approval_policy = "never"`, `sandbox_mode = "danger-full-access"`, `default_permissions = ":danger-no-sandbox"`, `profile = "rldyour-yolo"`.
- Parent model defaults are `model = "gpt-5.5"` and `model_reasoning_effort = "xhigh"`.
- Generated `config.toml` starts with the official schema hint `#:schema https://developers.openai.com/codex/config-schema.json`.
- `[features].hooks = true` and `[features].multi_agent = true` are managed; deprecated/unstable hook feature keys such as `codex_hooks` and `plugin_hooks` must be absent.
- Managed subagents are installed from `system/agents/*.toml`; all rldyour-managed roles use `gpt-5.5` with `medium` reasoning.
- Active managed roles are `architecture-reviewer`, `browser-tester`, `consistency-reviewer`, `quality-reviewer`, `research-explorer`, `security-audit`, `serena-sync`, and `test-reviewer`.
- Installer/doctor derive rldyour plugin enablement from `.agents/plugins/marketplace.json` and MCP registration from `plugins/rldyour-mcps/.mcp.json`.
- After plugin/hook/skill/agent changes, plugin cache must be synced through `scripts/install_system_codex.sh --apply`, and Codex should be restarted for runtime reload.

## Contracts And Data

- `${CODEX_HOME:-$HOME/.codex}/AGENTS.md` is generated from `system/AGENTS.md`.
- `${CODEX_HOME:-$HOME/.codex}/agents/*.toml` must match `system/agents/*.toml` exactly.
- `scripts/doctor_system_codex.sh` checks config schema hint, feature flags, model defaults, managed agents, marketplace-derived plugin enablement, MCP registration, plugin cache parity, and fullrepo current-state.
- Plugin cache parity matters for runtime because installed hooks and skills execute from `${CODEX_HOME}` in normal Codex sessions.

## Invariants

- Do not reintroduce deprecated hook feature keys.
- Do not hardcode parallel plugin/MCP lists in installer or doctor scripts.
- Do not change YOLO permission defaults without explicit owner request.
- Restart Codex after changing global `AGENTS.md`, `config.toml`, managed agents, installed plugins, hooks, skills, or MCP runtime definitions.

## Change Rules

- After editing `system/AGENTS.md`, `system/agents/*.toml`, plugin manifests, hooks, or skills, run installer apply, then doctor.
- If doctor fails only on fullrepo current-state while normal branch is dirty or unpublished, finish normal branch and fullrepo sync before treating it as a real runtime failure.
- Keep managed agent model and reasoning settings aligned with repository policy unless the owner explicitly changes them.

## Verification

- `scripts/install_system_codex.sh --dry-run`: preview install.
- `scripts/install_system_codex.sh --apply`: sync active system runtime and plugin cache.
- `scripts/doctor_system_codex.sh`: installed-state verification.
- `diff -qr plugins/<plugin> "${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/<plugin>/local"`: targeted plugin cache parity check.
