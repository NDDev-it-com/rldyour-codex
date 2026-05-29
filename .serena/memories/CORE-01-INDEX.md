<!-- Memory Metadata
Last updated: 2026-05-29
Last commit: 818d3c1
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
- commit: `818d3c19388978564b29724488678cd803b99867`
- checked by: Codex system sync after nested legacy profile cleanup

## Facts
- Core memories index repository identity, source-of-truth files, and the current validation map.
- Current product/config version is `1.0.3`; root control-plane must pin
  `818d3c19388978564b29724488678cd803b99867` for this adapter after the
  nested legacy profile table migration fix.

## Evidence
- `commit:d7909f83ae7ec947946f374ffae99af37db5335a`
- `path:README.md`
- `path:VERSION`
- `path:CHANGELOG.md`

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
