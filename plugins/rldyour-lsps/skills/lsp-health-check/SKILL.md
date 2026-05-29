---
name: lsp-health-check
description: "Проверяет LSP и Serena prerequisites для Python, Rust, Dart/Flutter, TS/JS, Go, C/C++, Qt, YAML, Docker, HTML/CSS и Shell. EN: LSP health check, diagnostics."
---

# LSP Health Check

## Purpose

Verify that language servers and project prerequisites are available before relying on diagnostics, semantic navigation, or Serena symbol tools.

## Command

Run from a repository root:

```bash
plugins/rldyour-lsps/scripts/check_lsps.sh
```

For another project:

```bash
plugins/rldyour-lsps/scripts/check_lsps.sh /path/to/project
```

## Workflow

1. Run the health-check script when available.
2. If the script is not available in the current project, check commands manually using stable executable names from `references/lsp-server-matrix.md`.
3. Report missing commands separately from project prerequisite warnings.
4. Do not start raw `stdio` LSP sessions as a test.
5. For C, C++, and Qt C++, treat missing `compile_commands.json` as a serious warning because diagnostics may be wrong.
6. For TypeScript and JavaScript, verify `tsconfig.json` or `jsconfig.json`.
7. For Python, verify `pyproject.toml`, `pyrightconfig.json`, or virtual environment expectations.
8. For Dart and Flutter, verify `pubspec.yaml`, `analysis_options.yaml`, and dependency resolution.

## Output

In Russian, summarize:

- Installed and missing commands.
- Project prerequisite warnings.
- What must be installed or configured next.
- Whether Serena semantic work is safe for the detected languages.
