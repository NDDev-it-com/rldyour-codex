<!-- Memory Metadata
Last updated: 2026-05-22
Last commit: 8e503c6c3674e9628e0ce4d537871e2d68a533b0 chore(mcp): bump GitHub MCP server pin to 1.5.0
Scope: MCP runtime transport and pin policy
Area: MCP
-->

# MCP Transport

## Scope
MCP runtime transport and pin policy

## Current source of truth
- `path:plugins/rldyour-mcps/.mcp.json`
- `path:README.md`

## Last verified
- date: 2026-05-22
- commit: `8e503c6c3674e9628e0ce4d537871e2d68a533b0`
- checked by: Codex ry-start memory taxonomy sync

## Facts
- MCP memories record server ownership, transports, versions, and toolset constraints.
- Current Codex MCP runtime pins include `GITHUB_MCP_SERVER_VERSION=1.5.0` in `config/mcp-runtime-versions.env`; this fixed the stale `1.4.0` GitHub MCP server pin detected by MCP runtime freshness validation.

## Evidence
- `commit:8e503c6c3674e9628e0ce4d537871e2d68a533b0`
- `path:plugins/rldyour-mcps/.mcp.json`
- `path:README.md`

## Known pitfalls
- Treat this memory as derived context. Current code, configuration, runtime output, and GitHub state override stale memory text.

## Update policy
Update after verified changes to the referenced source-of-truth files.

## Delete / merge policy
- Delete or merge only when the referenced source-of-truth files no longer support this memory and the replacement memory preserves the durable facts.
