<!-- Memory Metadata
Last updated: 2026-05-22
Last commit: 86b2555935f4c2185658417a3aff82d225d25392 feat(flow): enforce numeric releases and deploy routing
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
- date: 2026-05-22
- commit: `86b2555935f4c2185658417a3aff82d225d25392`
- checked by: Codex ry-start memory-domain normalization

## Facts
- Core memories index repository identity, source-of-truth files, and the current validation map.

## Evidence
- `commit:86b2555935f4c2185658417a3aff82d225d25392`
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
