# Claude Code Project Memory - rldyour-codex

Codex adapter project memory for `rldyour-codex`.

## Source of Truth

- `references/codex-baseline.json`
- `config/mcp-runtime-versions.env`
- `config/rldyour-contract.json`
- `.codex-plugin/*`
- `.agents/plugins/marketplace.json`
- `plugins/rldyour-*/.codex-plugin/plugin.json`
- `scripts/*.sh` and `scripts/*.py`

## Runtime Baseline

- Codex CLI runtime pin: `@openai/codex@0.144.1` (verified in baseline metadata).
- CloakBrowser wrapper policy pin: `cloakbrowser==0.4.10`; installation is
  owned by the `rldyour-new-mac-or-ubuntu` bootstrap.
- Sequential Thinking MCP `2026.7.4` and Context7 MCP `3.2.3` are mirrored
  between `config/mcp-runtime-versions.env` and the portable `.mcp.json` specs.

## Installer and Checks

```bash
bash scripts/install_system_codex.sh --dry-run
bash scripts/install_system_codex.sh --apply
bash scripts/doctor_system_codex.sh --quick --strict-runtime
bash scripts/validate_fast.sh
python3 scripts/validate_release.sh
python3 scripts/validate_runtime.sh --strict-runtime
python3 scripts/validate_instruction_docs.py
```

## Validation

Run before each merge and release boundary change:

```bash
bash scripts/validate_fast.sh
python3 scripts/validate_release.sh
python3 scripts/validate_runtime.sh --strict-runtime
python3 scripts/validate_instruction_docs.py
```

## Boundaries

Use Codex-native configuration only:

- `plugins/<...>/.codex-plugin/plugin.json`
- `.agents/` managed agent definitions
- `.rules/` managed rules and install targets
- `system/` rule sets
- `~/.codex` generated from installer output

Do not treat OpenCode or Gemini command formats as native Codex runtime.

## MCP and Security Notes

- MCP server definitions are portable in `plugins/rldyour-mcps/.mcp.json`.
- Browser work must use the bootstrap-owned `$HOME/.local/bin/webwright`,
  `$HOME/.local/bin/playwright-cli`, and
  `$HOME/.local/bin/chrome-devtools-mcp` wrappers backed by CloakBrowser; no
  stock Chromium, in-app browser, or raw-browser fallback is allowed.
- System install keeps `browser@openai-bundled`, `node_repl`, and
  `computer-use` explicitly disabled; doctor rejects reinjected active copies
  and requires reinstall plus Codex restart.
- Security checks (CodeQL, secret scanning, dependency checks) are required checks in
  this adapter.

## Git

- Keep `.serena/` durable context updated on `main` updates and avoid rewriting
  existing commit history.
- Commit adapter changes in this repo first, then update super-repo submodule pointer.
- Push a signed numeric release tag only after exact-SHA branch CI is stably
  green; release workflow dispatch may verify an existing tag but never create
  or push one.
