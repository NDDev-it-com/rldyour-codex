# rldyour-lsps

`rldyour-lsps` defines the language-server workflow layer for Codex.

It does not start MCP servers and does not introduce a fake Codex `lspServers` manifest field. LSPs are local executables used by Serena MCP where Serena supports the language, by editors, or by explicit health/setup scripts.

## Scope

- Route coding tasks to the correct language server strategy.
- Keep Serena integration honest: use Serena LSP language keys where supported and fallback to text/project checks where not supported.
- Verify system LSP executables and project prerequisites before meaningful code work.
- Prefer stable local executables for long-lived `stdio` language server sessions.
- Prefer Homebrew for system installation, with toolchain-specific exceptions where they are more correct.

## Skills

- `lsp-routing`: choose the correct LSP workflow by language, task, and project evidence.
- `serena-lsp-integration`: align Serena MCP usage with supported language keys and project prerequisites.
- `lsp-health-check`: run `$ry-lsp-check` style verification for commands and project files.
- `lsp-setup`: install or update LSP dependencies only after an explicit user request.

## References

- `references/lsp-server-matrix.md`: supported languages, commands, and prerequisites.
- `references/serena-lsp-integration.md`: Serena language keys and limitations.
- `references/install-profiles.md`: brew-first setup profile and toolchain exceptions.

## Scripts

- `scripts/check_lsps.sh [project-root]`: checks local command availability and project prerequisites.
- `scripts/install_lsps_brew.sh`: installs missing brew-managed LSP dependencies and Rust analyzer components when `rustup` is available.

