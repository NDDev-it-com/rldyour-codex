---
name: lsp-setup
description: "Установка/обновление LSP-серверов через brew + toolchain (rustup, dart, npm). Только по явному запросу. Используй для: установи LSP, обнови лсп, поставь язык-серверы, почини language server. EN triggers: install LSP, install language server, update LSP, fix LSP, brew LSP, set up language server, bootstrap LSPs."
---

# LSP Setup

## Purpose

Install or update LSP dependencies only after an explicit user request. Keep setup deterministic, brew-first, and safe for long-lived `stdio` language server use.

## Default Install Profile

Run from this repository when the user explicitly asks for setup:

```bash
plugins/rldyour-lsps/scripts/install_lsps_brew.sh
```

Then verify:

```bash
plugins/rldyour-lsps/scripts/check_lsps.sh
```

## Rules

- Prefer Homebrew for missing system tools.
- Use `rustup component add rust-src rust-analyzer` when `rustup` is installed.
- Do not reinstall already working non-brew commands just to standardize ownership.
- Do not put machine-local executable paths into committed project files.
- Do not auto-edit `.serena/project.yml`; propose or apply changes only on explicit setup request.
- After setup, run `lsp-health-check` and report exact remaining gaps.

## Install Profile Reference

Read `references/install-profiles.md` before changing the install script or adding new LSPs.
