<!-- Memory Metadata
Last updated: 2026-05-28
Last commit: 2a852698661384a3ba4497c4ea2c98111d941965 fix: sync plugin cache versions with adapter release
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
- date: 2026-05-28
- commit: `2a852698661384a3ba4497c4ea2c98111d941965`
- checked by: Codex ry-start internal adapter release version sync

## Facts
- Core memories index repository identity, source-of-truth files, and the current validation map.
- Current product/config version is `1.0.2`; root control-plane must pin
  `2a852698661384a3ba4497c4ea2c98111d941965` for this adapter after the
  plugin manifest/cache version sync.

## Evidence
- `commit:2a852698661384a3ba4497c4ea2c98111d941965`
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
