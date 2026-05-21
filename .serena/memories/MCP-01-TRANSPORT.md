<!-- Memory Metadata
Last updated: 2026-05-22
Last commit: 86b2555935f4c2185658417a3aff82d225d25392 feat(flow): enforce numeric releases and deploy routing
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
- commit: `86b2555935f4c2185658417a3aff82d225d25392`
- checked by: Codex ry-start memory-domain normalization

## Facts
- MCP memories record server ownership, transports, versions, and toolset constraints.

## Evidence
- `commit:86b2555935f4c2185658417a3aff82d225d25392`
- `path:plugins/rldyour-mcps/.mcp.json`
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
