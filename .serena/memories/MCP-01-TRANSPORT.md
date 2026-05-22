<!-- Memory Metadata
Last updated: 2026-05-22
Last commit: c89b5380f272ac9553b254573383c71aa1e33e33 fix: align dart mcp smoke with dart 3.12
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
- date: 2026-05-22
- commit: `c89b5380f272ac9553b254573383c71aa1e33e33`
- checked by: Codex ry-start Dart 3.12 runtime sync

## Facts
- MCP memories record server ownership, transports, versions, and toolset constraints.
- Dart/Flutter MCP is provided by the local Dart SDK. On Dart SDK `3.12.0`,
  `dart mcp-server --force-roots-fallback` exposes `analyze_files` and
  `pub_dev_search` in this non-Dart checkout; `run_tests` is conditional and is
  not a global smoke requirement.

## Evidence
- `commit:c89b5380f272ac9553b254573383c71aa1e33e33`
- `path:plugins/rldyour-mcps/.mcp.json`
- `path:config/mcp-runtime-versions.env`
- `path:scripts/smoke_mcp_capabilities.py`
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
