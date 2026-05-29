<!-- Memory Metadata
Last updated: 2026-05-29
Last commit: ea419bc0900cc934ca1b9434e8ff8f4e0304328b chore(release): codex 1.1.0
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


## Source Of Truth
- `path:AGENTS.md`
- `path:.claude/CLAUDE.md`
- `path:README.md`
- `path:system/AGENTS.md`

## Last verified
- date: 2026-05-29
- commit: `ea419bc0900cc934ca1b9434e8ff8f4e0304328b`
- checked by: Codex ry-start automated release and metadata sync

## Facts
- Docs memories record which instruction and operator docs must change after durable behavior changes.

## Evidence
- `commit:ea419bc0900cc934ca1b9434e8ff8f4e0304328b`
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

## Cross-References
- `CORE-01-INDEX.md`
- `CONTEXT-01-CORE.md`
- `PATTERNS-01-CANONICAL.md`
