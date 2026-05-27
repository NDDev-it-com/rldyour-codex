<!-- Memory Metadata
Last updated: 2026-05-27
Last commit: eefb9d4e48eb0d9e8562176ed08e0b1bdbed3222 test: guard codex active instruction drift
Scope: MCP runtime transport and pin policy
Area: MCP
-->

# MCP-01-TRANSPORT

## Scope
MCP runtime transport and pin policy

## Current source of truth
- `path:plugins/rldyour-mcps/.mcp.json`
- `path:README.md`


## Source Of Truth
- `path:plugins/rldyour-mcps/.mcp.json`
- `path:README.md`

## Last verified
- date: 2026-05-27
- commit: `eefb9d4e48eb0d9e8562176ed08e0b1bdbed3222`
- checked by: Codex ry-start current audit repair

## Facts
- MCP memories record server ownership, transports, versions, and toolset constraints.
- Codex MCP source remains `plugins/rldyour-mcps/.mcp.json`; installer and
  doctor materialize runtime MCP as native TOML `[mcp_servers.*]` blocks in
  `$CODEX_HOME/config.toml` / profile layers.
- Chrome DevTools MCP is pinned to `chrome-devtools-mcp@1.1.1` in
  `config/mcp-runtime-versions.env`, the MCP source manifest, and all managed
  agent disabled specialist-MCP transport metadata.
- Dart/Flutter MCP is provided by the local Dart SDK. On Dart SDK `3.12.0`,
  `dart mcp-server --force-roots-fallback` exposes `analyze_files` and
  `pub_dev_search` in this non-Dart checkout; `run_tests` is conditional and is
  not a global smoke requirement.

## Evidence
- `commit:eefb9d4e48eb0d9e8562176ed08e0b1bdbed3222`
- `path:plugins/rldyour-mcps/.mcp.json`
- `path:config/mcp-runtime-versions.env`
- `path:scripts/smoke_mcp_capabilities.py`
- `path:scripts/check_mcp_runtime_versions.py`
- `path:system/agents/*.toml`
- `path:README.md`

## Known pitfalls
- Treat this memory as derived context. Current code, configuration, runtime output, and GitHub state override stale memory text.

## Update policy
Update after verified changes to the referenced source-of-truth files.

## Delete / merge policy
- Delete or merge only when the referenced source-of-truth files no longer support this memory and the replacement memory preserves the durable facts.

## Cross-References
- `CORE-01-INDEX.md`
- `CONTEXT-01-CORE.md`
- `PATTERNS-01-CANONICAL.md`
