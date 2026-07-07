# RTK.md - rtk token economy (Codex)

rtk (Rust Token Killer, https://github.com/rtk-ai/rtk, Apache-2.0) is an external
single binary that compresses shell-command output 60-90% before it reaches
context. It is not an MCP server and is not vendored here. Install:
`brew install rtk`.

## Rule (always on)

For supported commands, prefix with `rtk`:

- git: `rtk git status`, `rtk git log -n 20`, `rtk git diff`
- tests: `rtk pytest`, `rtk cargo test`, `rtk go test`, `rtk jest`
- build/lint: `rtk cargo build`, `rtk tsc`, `rtk ruff check`, `rtk eslint`
- search/fs: `rtk ls`, `rtk find "<glob>" .`, `rtk grep "<pat>" .`
- large files: `rtk read <file>` or `rtk read <file> -l aggressive` (signatures only)
- containers/cloud: `rtk docker ...`, `rtk kubectl ...`, `rtk aws ...`

Do NOT prefix:

- interactive commands (editors, REPLs);
- an already-`rtk` command (never double-wrap);
- output that must be parsed byte-for-byte: control-plane validators
  (`python3 scripts/validate_*`), `git commit`/`merge`/`rebase` (watched by other
  hooks), `gh api`, `jq`. These are also listed in `~/.config/rtk/config.toml`
  `[hooks] exclude_commands`.

On a failed command, rtk saves full output to a tee log - read that log instead of
re-running. Check savings with `rtk gain`.

## Division of labour

- rtk = shell-output compression at the Bash boundary.
- Serena/LSP = symbol-level code reads/edits (`find_symbol`,
  `find_referencing_symbols`), not whole-file reads.

Do not duplicate the two.

## Optional deterministic hook

`plugins/rldyour-rtk` also ships an opt-in PreToolUse Bash hook (default OFF). Set
`RTK_CODEX_HOOK=1` to have Codex rewrite supported commands through rtk
automatically (Codex PreToolUse supports `updatedInput`). Without the flag the hook
is a no-op and this rules file is the mechanism.

Control-plane source of truth for the rtk pin and exclusion baseline:
`config/token-economy-policy.json` in `rldyour-ai-cli-tools`.
