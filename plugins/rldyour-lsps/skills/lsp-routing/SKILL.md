---
name: lsp-routing
description: Automatic language-server routing for Codex. Use automatically for Russian or English requests that mention LSP, language servers, diagnostics, type checking, code intelligence, symbol navigation, semantic refactors, project setup, or implementation work involving Python, Rust, Dart, Flutter, TypeScript, JavaScript, Go, C, C++, Qt, QML, YAML, Docker, HTML, CSS, Shell, JSON, TOML, or Markdown.
---

# LSP Routing

## Purpose

Choose the correct language-server workflow before coding. The goal is accurate diagnostics, semantic navigation, and low-entropy implementation without pretending every file type is Serena-native.

User-facing conversation stays Russian unless requested otherwise. Repository docs and plugin files stay English.

## Auto Invocation

Use this skill when a task involves:

- LSPs, language servers, diagnostics, type checking, symbol navigation, code intelligence, or semantic refactoring.
- Project setup for Python, Rust, Dart, Flutter, TypeScript, JavaScript, Go, C, C++, Qt, QML, YAML, Docker, HTML, CSS, Shell, JSON, TOML, or Markdown.
- Choosing whether Serena MCP can provide semantic tools for a file type.
- Preparing a high-quality implementation where language-server feedback matters.

## Routing Rules

1. Detect the language from files, manifests, lockfiles, and build files, not from file extensions alone when project structure matters.
2. Read `references/lsp-server-matrix.md` when exact command names, Serena keys, or prerequisites matter.
3. Use `serena-lsp-integration` when the question affects Serena project languages, `.serena/project.yml`, `ls_specific_settings`, or `serena project index`.
4. Use `lsp-health-check` when the user asks whether LSPs work, when a project has missing diagnostics, or before non-trivial code work in a newly seen stack.
5. Use `lsp-setup` only after an explicit user request to install or update tools.

## Default Decisions

- Python: Pyright for semantic analysis, Ruff as companion lint/format tooling.
- TypeScript and JavaScript: `typescript-language-server` by default. Use `typescript_vts` or `vtsls` only when explicitly requested or project evidence requires it.
- Rust: `rust-analyzer` and `rust-src`.
- Dart and Flutter: Dart SDK analyzer, with Flutter SDK awareness for Flutter projects.
- Go: `gopls` only inside a real module or workspace.
- C, C++, Qt C++: `clangd` and `compile_commands.json`.
- Qt QML: `qmlls` externally; do not claim Serena-native QML support.
- YAML: `yaml-language-server` plus schemas.
- Docker: Docker Language Server externally.
- HTML/CSS/JSON: `vscode-langservers-extracted`.
- Shell: `bash-language-server` plus `shellcheck`.
- TOML: Taplo.
- Markdown: Marksman.

## Runtime Safety

Do not start a `stdio` language server manually unless a real LSP client controls the session. For checks, verify command availability, versions, and project prerequisites.

Do not use first-run `bunx` or `uvx` as a long-lived LSP runtime. Use stable local executables. Package managers are allowed for explicit setup and health checks.

