<!-- Memory Metadata
Last updated: 2026-05-22
Last commit: 86b2555935f4c2185658417a3aff82d225d25392 feat(flow): enforce numeric releases and deploy routing
Scope: instruction docs and durable operator documentation
Area: DOCS
-->

# DOCS-01-INSTRUCTIONS

## Scope
instruction docs and durable operator documentation

## Current source of truth
- `path:AGENTS.md`
- `path:.claude/CLAUDE.md`
- `path:README.md`
- `path:system/AGENTS.md`

## Last verified
- date: 2026-05-22
- commit: `86b2555935f4c2185658417a3aff82d225d25392`
- checked by: Codex ry-start memory-domain normalization

## Facts
- Docs memories record which instruction and operator docs must change after durable behavior changes.

## Evidence
- `commit:86b2555935f4c2185658417a3aff82d225d25392`
- `path:AGENTS.md`
- `path:.claude/CLAUDE.md`
- `path:README.md`
- `path:system/AGENTS.md`

## Known pitfalls
- Treat this memory as derived context. Current code, configuration, runtime output, and GitHub state override stale memory text.

## Update policy
Update after verified changes to the referenced source-of-truth files.

## Delete / merge policy
- Delete or merge only when the referenced source-of-truth files no longer support this memory and the replacement memory preserves the durable facts.
