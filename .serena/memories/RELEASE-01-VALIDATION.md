<!-- Memory Metadata
Last updated: 2026-05-22
Last commit: 86b2555935f4c2185658417a3aff82d225d25392 feat(flow): enforce numeric releases and deploy routing
Scope: release readiness, versioning, and artifact hygiene
Area: RELEASE
-->

# RELEASE-01-VALIDATION

## Scope
release readiness, versioning, and artifact hygiene

## Current source of truth
- `path:VERSION`
- `path:CHANGELOG.md`
- `path:.github/workflows/release.yml`

## Last verified
- date: 2026-05-22
- commit: `86b2555935f4c2185658417a3aff82d225d25392`
- checked by: Codex ry-start memory-domain normalization

## Facts
- Release memories record numeric versioning, tags, CI gates, and clean artifact hygiene.

## Evidence
- `commit:86b2555935f4c2185658417a3aff82d225d25392`
- `path:VERSION`
- `path:CHANGELOG.md`
- `path:.github/workflows/release.yml`

## Known pitfalls
- Treat this memory as derived context. Current code, configuration, runtime output, and GitHub state override stale memory text.

## Update policy
Update after verified changes to the referenced source-of-truth files.

## Delete / merge policy
- Delete or merge only when the referenced source-of-truth files no longer support this memory and the replacement memory preserves the durable facts.
