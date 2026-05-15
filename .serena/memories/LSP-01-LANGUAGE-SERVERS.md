<!-- Memory Metadata
Last updated: 2026-05-16
Last commit: 1132859 feat(serena): harden codex memory sync brain
Scope: plugins/rldyour-lsps, plugins/rldyour-lsps/scripts/check_lsps.sh, plugins/rldyour-serena-mcp, pyrightconfig.json, README.md
Area: LSP
-->

# LSP-01-LANGUAGE-SERVERS

## Purpose

`rldyour-lsps` owns language-server routing, setup policy, health checks, and Serena LSP integration guidance for code understanding and refactors.

## Source Of Truth

- `plugins/rldyour-lsps/skills/lsp-routing/SKILL.md`: language-server usage routing.
- `plugins/rldyour-lsps/skills/lsp-health-check/SKILL.md`: diagnostics and prerequisite checks.
- `plugins/rldyour-lsps/skills/lsp-setup/SKILL.md`: install/update/repair policy.
- `plugins/rldyour-lsps/skills/serena-lsp-integration/SKILL.md`: Serena project language settings.
- `plugins/rldyour-lsps/scripts/check_lsps.sh`: health-check script.
- `pyrightconfig.json`: Python type-check configuration for repository scripts.

## Entry Points

- `$lsp-routing`: choose LSP-backed diagnostics/symbol flow during implementation.
- `$lsp-health-check`: check installed LSP health and Serena prerequisites.
- `$lsp-setup`: install or repair language servers when explicitly requested.
- `$serena-lsp-integration`: configure Serena project language settings.
- `plugins/rldyour-lsps/scripts/check_lsps.sh`: local LSP health command.

## Current Behavior

- Serena symbolic tools are preferred for supported code structure and references.
- Direct `rg`/file reads are still appropriate for shell, Markdown, JSON, YAML, TOML, and other text/config surfaces where LSP tools are not useful.
- LSP setup is brew-first where applicable, with toolchain fallbacks documented by the skill.

## Contracts And Data

- LSP setup should not silently install broad toolchains without explicit need.
- Serena project settings should match actual repository languages and generated/source boundaries.
- Diagnostics are evidence; they do not replace targeted source inspection.

## Invariants

- Prefer semantic tools for code symbols and relationships before broad file reads when supported.
- Do not perform risky semantic refactors without reference tracing or matching tests.

## Change Rules

- When adding a language profile, update the corresponding skill and `check_lsps.sh` if it has executable health checks.
- When changing Serena LSP integration behavior, update `SERENA-01-MEMORY-SYNC.md` only if it affects memory/code workflow contracts.

## Verification

- `plugins/rldyour-lsps/scripts/check_lsps.sh`: local LSP health.
- `scripts/validate_marketplace.sh`: shell/Python/skill validation.
