<!-- Memory Metadata
Last updated: 2026-05-22
Last commit: d6aaeea3d3ff5a732bc5bc18434247f86de75183 chore(release): codex 1.7.19 (other)
Scope: release readiness, versioning, and artifact hygiene
Area: RELEASE
-->

# Release Validation

## Scope
release readiness, versioning, and artifact hygiene

## Current source of truth
- `path:VERSION`
- `path:CHANGELOG.md`
- `path:.github/workflows/release.yml`

## Last verified
- date: 2026-05-22
- commit: `d6aaeea3d3ff5a732bc5bc18434247f86de75183`
- checked by: Codex ry-start memory taxonomy sync

## Facts
- Current rldyour-codex adapter VERSION is `1.7.20`; the release workflow publishes the matching numeric GitHub Release tag at the released commit. Root `config/repositories.json` and the superproject gitlink own the current adapter HEAD.
- Release memories record numeric versioning, tags, CI gates, and clean artifact hygiene without copying current control-plane pins.

## Evidence
- `commit:d6aaeea3d3ff5a732bc5bc18434247f86de75183`
- `path:VERSION`
- `path:CHANGELOG.md`
- `path:.github/workflows/release.yml`

## Known pitfalls
- Treat this memory as derived context. Current code, configuration, runtime output, and GitHub state override stale memory text.

## Update policy
Update after verified changes to the referenced source-of-truth files.

## Delete / merge policy
- Delete or merge only when the referenced source-of-truth files no longer support this memory and the replacement memory preserves the durable facts.
