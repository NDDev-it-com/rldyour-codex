<!-- Memory Metadata
Last updated: 2026-05-19
Last commit: 8c11c76 chore(release): bump to 0.4.0
Scope: AGENTS.md, .claude/CLAUDE.md, system/AGENTS.md, plugins/rldyour-flow/skills/instruction-docs-sync/SKILL.md, plugins/rldyour-flow/scripts/instruction_docs_state.py, scripts/validate_instruction_docs.py
Area: DOCS
-->

# DOCS-01-INSTRUCTIONS

## Purpose

This memory records how durable project instruction docs are kept aligned for Codex and Claude Code without turning either file into a stale copy of the other.

## Source Of Truth

- `system/AGENTS.md`: tracked canonical template for global `~/.codex/AGENTS.md`.
- Root `AGENTS.md`: project Codex instructions restored/published through `fullrepo`.
- `.claude/CLAUDE.md`: Claude Code-native project memory restored/published through `fullrepo`.
- `plugins/rldyour-flow/skills/instruction-docs-sync/SKILL.md`: instruction docs sync workflow.
- `plugins/rldyour-flow/scripts/instruction_docs_state.py`: state detector for instruction docs sync.
- `scripts/validate_instruction_docs.py`: validation gate.

## Entry Points

- `$instruction-docs-sync`: update root `AGENTS.md` and `.claude/CLAUDE.md` from verified project facts.
- `plugins/rldyour-flow/scripts/instruction_docs_state.py --json | python3 -m json.tool`: inspect durable-change candidates and required docs.
- `python3 scripts/validate_instruction_docs.py --require-agent-docs`: validate restored agent-only instruction docs.
- `scripts/install_system_codex.sh --apply`: install `system/AGENTS.md` into `${CODEX_HOME:-$HOME/.codex}/AGENTS.md`.

## Current Behavior

- User-facing conversation with the owner is Russian; repository artifacts, instruction docs, and memories are English.
- Root `AGENTS.md` and `.claude/CLAUDE.md` are agent-only in normal branches and published through `fullrepo`.
- `system/AGENTS.md` is tracked because it is a product artifact and the canonical global Codex template.
- `AGENTS.md` is Codex-native and contains Codex plugin routing, tool priority, Serena workflow, fullrepo rules, managed subagents, and system Codex setup.
- `.claude/CLAUDE.md` remains Claude Code-native and should not be reduced to `@AGENTS.md`; shared facts may overlap, but CLI-specific commands and concepts stay separate.
- Instruction docs state that system Codex manages `[features].hooks = true`, `[features].plugin_hooks = true`, and `[features].multi_agent = true`; only `codex_hooks` remains a deprecated hook alias.
- Instruction docs now describe temporary managed-subagent MCP isolation: subagents keep the lightweight inherited core surface (`sequential-thinking`, `serena`, `context7`, `grep`, `deepwiki`, `openaiDeveloperDocs`, and built-in `codex_apps`) while specialist MCP servers remain parent-session tools. Disabled specialist MCP overrides must include full transport metadata copied from `.mcp.json`; `codex_apps` stays inherited from Apps/connectors and must not be declared as an `mcp_servers` transport table.
- Project instruction docs reflect the AGPL-3.0-or-later license, the public OSS posture (NDDev / Danil Silantyev (rldyourmnd) attribution), and the auto-running CI/CD model on the public `main` branch (push/PR/schedule/tag triggers). Project instruction docs do not include the AGPL license text itself; `LICENSE` carries the canonical FSF text.
- Public-facing documentation (`README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`) lives on `main` (not on `fullrepo`) and is rewritten for an OSS audience. Internal Codex/Claude agent docs (`AGENTS.md`, `.claude/CLAUDE.md`) remain agent-only and live on `fullrepo`.

## Contracts And Data

- Instruction docs should be updated after meaningful behavior changes in setup, install, bootstrap, doctor, validation, deploy, release, plugins, skills, hooks, MCP runtime, LSP/browser/design/security workflows, git/fullrepo behavior, managed agents, or project conventions.
- Do not store secrets, credentials, raw tokens, cookies, browser evidence, transient runtime markers, or speculative plans in instruction docs.
- Root `AGENTS.md`, `.claude/CLAUDE.md`, and `.serena` knowledge must stay out of normal branch commits unless explicitly intended as tracked product artifacts.

## Invariants

- Code/config/scripts are source of truth; instruction docs document verified facts only.
- Codex and Claude Code docs are both first-class and optimized for their own CLIs.
- `fullrepo` is the portable delivery mechanism for agent-only docs.
- Validation must pass with `--require-agent-docs` when fullrepo context is restored.

## Change Rules

- Update Serena memories first, then instruction docs, then run validation, then publish fullrepo.
- When Codex behavior changes, update `system/AGENTS.md` if the global template must change and run installer/doctor.
- When Claude Code-relevant behavior changes, update `.claude/CLAUDE.md` independently; do not rely on imports alone.

## Verification

- `plugins/rldyour-flow/scripts/instruction_docs_state.py --json | python3 -m json.tool`: shows instruction-doc state.
- `python3 scripts/validate_instruction_docs.py --require-agent-docs`: validates restored docs and required references.
- `scripts/sync_fullrepo_branch.sh --status`: verifies agent-only docs are part of the fullrepo snapshot state.
