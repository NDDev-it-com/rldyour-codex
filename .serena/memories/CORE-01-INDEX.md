<!-- Memory Metadata
Last updated: 2026-05-28
Last commit: 2d4cee72988a99a934168c9649fec8307560c283 ci: align Dependabot action cadence
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
- commit: `2d4cee72988a99a934168c9649fec8307560c283`
- checked by: Codex ry-start Dependabot hardening

## Facts
- Core memories index repository identity, source-of-truth files, and the current validation map.
- Current product/config version is `1.0.0`; root control-plane must pin
  `2d4cee72988a99a934168c9649fec8307560c283` for this adapter after the
  Dependabot GitHub Actions cadence alignment.

## Evidence
- `commit:2d4cee72988a99a934168c9649fec8307560c283`
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
