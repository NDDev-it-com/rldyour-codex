# rldyour-rtk (Codex)

rtk token-economy core for the rldyour Codex adapter.

- **Rules-file (primary, always on)**: `RTK.md` + the token-economy section in
  `system/AGENTS.md` instruct the model to prefix supported shell commands with
  `rtk` so their output is compressed before it reaches context. This is the
  officially supported, guaranteed-compatible rtk-Codex mechanism.
- **Skill** (`skills/token-economy`): when to prefer rtk vs Serena/LSP symbol
  reads, and the scope limits.
- **Hook** (`hooks.json` -> `hooks/rtk_rewrite.sh`, opt-in, default OFF): with
  `RTK_CODEX_HOOK=1` a deterministic PreToolUse Bash hook rewrites supported
  commands through `rtk rewrite` and returns Codex `hookSpecificOutput.updatedInput`
  (Codex PreToolUse supports input mutation). Without the flag it is a no-op
  passthrough.

## rtk

rtk (Rust Token Killer, https://github.com/rtk-ai/rtk, Apache-2.0) is an external
single binary - install with `brew install rtk` (homebrew-core). It is **not** an
MCP server and is not vendored here. Machine-global config lives at
`~/.config/rtk/config.toml`, including `[hooks] exclude_commands` for
validator/JSON-verbatim safety. The control-plane source of truth for the rtk pin
and exclusion baseline is `config/token-economy-policy.json` in
`rldyour-ai-cli-tools`.

Owner: Danil Silantyev (github:rldyourmnd), CEO NDDev. License:
AGPL-3.0-or-later.
