<!-- Memory Metadata
Last updated: 2026-05-29
Last commit: ea419bc0900cc934ca1b9434e8ff8f4e0304328b chore(release): codex 1.1.0
Scope: repository identity and source-of-truth map
Area: CORE
-->

# CORE-01-INDEX

## Scope
repository identity and source-of-truth map

## Current source of truth
- `path:README.md`
- `path:VERSION`
- `path:CHANGELOG.md`


## Source Of Truth
- `path:README.md`
- `path:VERSION`
- `path:CHANGELOG.md`

## Last verified
- date: 2026-05-29
- commit: `ea419bc0900cc934ca1b9434e8ff8f4e0304328b`
- checked by: Codex ry-start automated release and metadata sync

## Facts
- Core memories index repository identity, source-of-truth files, and the current validation map.
- Current product/config version is `1.1.0`; root control-plane must pin
  `ea419bc0900cc934ca1b9434e8ff8f4e0304328b` for this adapter after the
  automated release and metadata sync.

## Evidence
- `commit:ea419bc0900cc934ca1b9434e8ff8f4e0304328b`
- `path:README.md`
- `path:VERSION`
- `path:CHANGELOG.md`
- `path:references/codex-surface-adoption.md`

## Known pitfalls
- Treat this memory as derived context. Current code, configuration, runtime output, and GitHub state override stale memory text.

## Update policy
Update after verified changes to the referenced source-of-truth files.

## Delete / merge policy
- Delete or merge only when the referenced source-of-truth files no longer support this memory and the replacement memory preserves the durable facts.
## Cross-References
- `DOCS-01-INSTRUCTIONS.md`
- `TECHDEBT-01-NOW.md`
- `CODEX-01-PLUGIN-CANON.md`
