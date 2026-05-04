<!-- Memory Metadata
Last updated: 2026-05-05
Last commit: b4038bd fix(lsp): support linuxbrew portability
Scope: plugins/rldyour-lsps, pyrightconfig.json, .agents/plugins/marketplace.json, README.md
Area: LSP
-->

# LSP_01_language_server_workflow

## Purpose

`plugins/rldyour-lsps` defines the rldyour language-server workflow layer for Codex. It routes LSP-related tasks, verifies local executables, documents brew-first setup, and explains how Serena MCP should use LSP-backed language keys.

## Source Of Truth

- `plugins/rldyour-lsps/.codex-plugin/plugin.json`: skills-only plugin manifest, marketplace metadata, trigger description, and capabilities.
- `plugins/rldyour-lsps/skills/lsp-routing/SKILL.md`: automatic routing for LSP, diagnostics, type checking, symbol navigation, semantic refactors, and listed languages.
- `plugins/rldyour-lsps/skills/serena-lsp-integration/SKILL.md`: Serena language key mapping, unsupported file type boundaries, and `serena project index` guidance.
- `plugins/rldyour-lsps/skills/lsp-health-check/SKILL.md`: `$ry-lsp-check` workflow and command expectations.
- `plugins/rldyour-lsps/skills/lsp-setup/SKILL.md`: explicit brew-first setup policy.
- `plugins/rldyour-lsps/references/lsp-server-matrix.md`: language matrix, primary commands, Serena keys, prerequisites, and source pointers.
- `plugins/rldyour-lsps/references/serena-lsp-integration.md`: Serena-native keys, external areas, and `.serena/project.yml` policy.
- `plugins/rldyour-lsps/references/install-profiles.md`: install policy, brew package set, and toolchain exceptions.
- `plugins/rldyour-lsps/scripts/check_lsps.sh`: deterministic command and project prerequisite health check.
- `plugins/rldyour-lsps/scripts/install_lsps_brew.sh`: explicit brew-first install profile.
- `pyrightconfig.json`: repository-level Python configuration for script directories.

## Entry Points

- `lsp-routing`: use for LSP selection and language-server workflow decisions.
- `serena-lsp-integration`: use for `.serena/project.yml`, `ls_specific_settings`, Serena language keys, and semantic tool availability.
- `lsp-health-check`: use when the owner asks if LSPs work, asks to verify diagnostics, or invokes `$ry-lsp-check`.
- `lsp-setup`: use only after an explicit install/update/repair request.
- `plugins/rldyour-lsps/scripts/check_lsps.sh [project-root]`: local command and prerequisite verification.
- `plugins/rldyour-lsps/scripts/install_lsps_brew.sh`: installs the approved brew-first dependency set.

## Current Behavior

The plugin has no `mcpServers`, apps, or hooks. It is intentionally not an MCP runtime layer.

The supported workflow covers Python, Rust, Dart, Flutter, TypeScript, JavaScript, Go, C, C++, Qt and QML, YAML, Docker, HTML, CSS, Shell, JSON, TOML, and Markdown.

Serena-native keys documented by the plugin are `python`, `typescript`, `typescript_vts`, `rust`, `dart`, `go`, `cpp`, `yaml`, `bash`, `json`, `toml`, and `markdown`. C maps to `cpp`; JavaScript maps to `typescript`. HTML, CSS, Docker, and QML are treated as external LSP areas unless current Serena upstream support proves otherwise.

The active system was verified with `plugins/rldyour-lsps/scripts/check_lsps.sh` after setup. Required commands are present: `pyright-langserver`, `ruff`, `typescript-language-server`, `rust-analyzer`, `dart`, `gopls`, `clangd`, `yaml-language-server`, `bash-language-server`, `shellcheck`, `vscode-html-language-server`, `vscode-css-language-server`, `vscode-json-language-server`, `docker-language-server`, `taplo`, `marksman`, and `qmlls`.

The current repository has a minimal `pyrightconfig.json` that includes `scripts`, `plugins/rldyour-flow/scripts`, and `plugins/rldyour-serena-mcp/scripts`; excludes cache and dependency directories; sets `pythonVersion` to `3.13`; and uses `typeCheckingMode: "basic"`.

`plugins/rldyour-lsps/scripts/check_lsps.sh` exits with failure only for missing required executable commands. Project prerequisite warnings are reported but do not fail the command. On the current repository it reports `missing: 0` and `warnings: 0`.

After commit `b4038bd fix(lsp): support linuxbrew portability`, the LSP health check reports `missing: 0` and `warnings: 0`. The health script resolves tools through `command -v` first, then falls back to common macOS Homebrew and Linuxbrew locations for tools such as `clangd` and `qmlls`. User-local, Bun, SDK, Snap, macOS Homebrew, and Linuxbrew paths are all acceptable runtime projections. The current repository prerequisite check succeeds because `pyrightconfig.json` is present and defines the Python script scope.

## Contracts And Data

Long-lived LSP sessions must use stable local executables. First-run `bunx` or `uvx` package-installing commands must not be used as long-lived `stdio` LSP runtimes because setup logs can corrupt protocol handshakes.

Installation is explicit only. `lsp-setup` may run the brew-first installer after the owner asks to install, update, repair, or ensure system tools.

The brew-first install script manages `go`, `gopls`, `shellcheck`, `vscode-langservers-extracted`, `docker-language-server`, `taplo`, `marksman`, `qtdeclarative`, and `qtlanguageserver`. When `rustup` is available, it also runs `rustup component add rust-src rust-analyzer`.

`.serena/project.yml` must not be silently mutated by this plugin. It may be inspected, explained, or changed only on explicit setup request. Future full project initialization belongs to `rldyour-flow`.

`pyrightconfig.json` is intentionally repository-level because this marketplace stores Python utility scripts without a Python package or `pyproject.toml`.

Serena should use its built-in language keys first for supported languages. External LSP health checks supplement Serena for technologies that are not documented as Serena-native in this plugin, such as HTML, CSS, Docker, and QML.

## Invariants

- Keep this plugin skills-only unless the owner explicitly adds a real integration surface.
- Do not duplicate MCP server definitions from `rldyour-mcps`.
- Do not claim Serena-native support for HTML, CSS, Docker, or QML without verified upstream support.
- Do not store machine-local executable paths in committed project files unless the repository intentionally depends on that layout.
- Keep user-facing answers Russian and plugin documentation English.
- Keep `policy.allow_implicit_invocation: true` for all four LSP skills.

## Change Rules

- Update `references/lsp-server-matrix.md` before changing skill routing for a language.
- Update `references/install-profiles.md` and `scripts/install_lsps_brew.sh` together when adding or removing installable system tools.
- Update `references/serena-lsp-integration.md` when Serena language key behavior changes.
- Run `shellcheck` for both scripts after shell edits.
- Re-sync `plugins/rldyour-lsps/` into `${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/rldyour-lsps/local/` after plugin changes.

## Verification

- `jq empty plugins/rldyour-lsps/.codex-plugin/plugin.json .agents/plugins/marketplace.json`: validates plugin and marketplace JSON.
- `uv run --with pyyaml python ${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py plugins/rldyour-lsps/skills/<skill>`: validates each LSP skill.
- `shellcheck plugins/rldyour-lsps/scripts/check_lsps.sh plugins/rldyour-lsps/scripts/install_lsps_brew.sh`: validates shell scripts.
- `plugins/rldyour-lsps/scripts/check_lsps.sh`: verifies local command availability and project prerequisites.
- `jq empty pyrightconfig.json`: validates the Python LSP project configuration file.
- `diff -qr plugins/rldyour-lsps ${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/rldyour-lsps/local`: verifies system cache matches the repository plugin.
