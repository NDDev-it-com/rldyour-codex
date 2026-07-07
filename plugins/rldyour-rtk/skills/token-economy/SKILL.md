---
name: token-economy
description: "Экономия токенов: команды через rtk (сжатие вывода), код символами Serena, не целыми файлами. Запуск команд, вывод git/тестов/сборки/линта. EN: token economy, rtk, compress command output, reduce context."
---

# Token economy (rtk + Serena/LSP)

Keep context small. Two non-overlapping layers.

## rtk = shell-output compression

rtk (Rust Token Killer, github.com/rtk-ai/rtk, Apache-2.0) is an external single
binary that compresses command output 60-90% before it reaches context. It is not
an MCP server. Prefix supported commands with `rtk`:

- git: `rtk git status`, `rtk git log -n 20`, `rtk git diff`
- tests: `rtk pytest`, `rtk cargo test`, `rtk go test`, `rtk jest`
- build/lint: `rtk cargo build`, `rtk tsc`, `rtk ruff check`, `rtk eslint`
- search/fs: `rtk ls`, `rtk grep "<pat>" .`, `rtk find "<glob>" .`
- large files: `rtk read <file>` or `rtk read <file> -l aggressive` (signatures only)

The always-on mechanism is the `RTK.md` / `AGENTS.md` rule (prefix rtk yourself).
The plugin also ships an opt-in deterministic hook (set `RTK_CODEX_HOOK=1`) that
rewrites supported commands automatically; default off.

## Serena/LSP = symbol-level code reads

Navigate and edit code through `find_symbol` / `find_referencing_symbols` /
`insert_after_symbol`, not by reading whole files.

## Rules

1. Do not prefix interactive commands (editors, REPLs), already-`rtk` commands, or
   output that must be parsed byte-for-byte: control-plane validators
   (`python3 scripts/validate_*`), `git commit`/`merge`/`rebase` (watched by other
   hooks), `gh api`, `jq`. These are excluded in `~/.config/rtk/config.toml`
   `[hooks] exclude_commands`.
2. On a failed command rtk saves full output to a tee log - read that log instead
   of re-running.
3. Do not duplicate layers: rtk compresses command output; Serena/LSP handles
   symbol reads and edits.
4. Check savings with `rtk gain`.

## Requirement

`brew install rtk`. Without it, prefixing is a no-op and commands run raw - nothing
breaks.
