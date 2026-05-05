<!-- Memory Metadata
Last updated: 2026-05-05
Last commit: b4038bd fix(lsp): support linuxbrew portability
Scope: plugins/rldyour-lsps, pyrightconfig.json, .agents/plugins/marketplace.json, README.md
Area: LSP
-->

# LSP_01_language_server_workflow

## Purpose

Keep a concise, verified record of language-server workflow behavior and Serena integration limits for future sessions.

## Source-of-Truth

- `plugins/rldyour-lsps/.codex-plugin/plugin.json`
- `plugins/rldyour-lsps/references/lsp-server-matrix.md`
- `plugins/rldyour-lsps/references/serena-lsp-integration.md`
- `plugins/rldyour-lsps/references/install-profiles.md`
- `plugins/rldyour-lsps/scripts/check_lsps.sh`
- `plugins/rldyour-lsps/scripts/install_lsps_brew.sh`
- `plugins/rldyour-lsps/skills/*/SKILL.md`
- `pyrightconfig.json`

## Skills

- `lsp-routing`: select correct LSP stack and decide Serena-backed vs external tool paths.
- `serena-lsp-integration`: map supported languages to Serena keys and indexing practices.
- `lsp-health-check`: run and interpret diagnostics for required commands and project prerequisites.
- `lsp-setup`: explicit install/update path, brew-first.

## Verified Tool Model

- Supported Serena keys in this system: `python`, `typescript`, `rust`, `dart`, `go`, `cpp`, `yaml`, `bash`, `json`, `toml`, `markdown`.
- C and C++ map to `cpp`; JavaScript maps to `typescript`.
- HTML, CSS, Docker, and Qt QML are treated as external areas unless upstream Serena support changes.
- `plugins/rldyour-lsps/scripts/check_lsps.sh` checks command presence with `command -v` first, then checks common macOS Homebrew and Linuxbrew paths for tools such as `clangd` and `qmlls`.
- Current check script reports separate `missing` and `warnings` counters and exits non-zero only when missing required commands > 0.
- For the current HEAD repository state, the check reports `missing: 0` and `warnings: 0` after the `b4038bd` Linuxbrew portability fix.
- The setup rule is explicit install-only on request; long-lived LSP stdio sessions should use stable local executables, not `bunx/uvx` setup calls.

## Verification Commands

- `plugins/rldyour-lsps/scripts/check_lsps.sh`
- `plugins/rldyour-lsps/scripts/install_lsps_brew.sh` (only after explicit user request)
- `jq empty pyrightconfig.json`
- `shellcheck plugins/rldyour-lsps/scripts/check_lsps.sh plugins/rldyour-lsps/scripts/install_lsps_brew.sh`
- `scripts/validate_marketplace.sh` (includes LSP health integration)
- `diff -qr plugins/rldyour-lsps ${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/rldyour-lsps/local`
