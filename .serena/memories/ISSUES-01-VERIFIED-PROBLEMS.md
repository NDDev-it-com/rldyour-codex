<!-- Memory Metadata
Last updated: 2026-05-28
Last commit: 2a852698661384a3ba4497c4ea2c98111d941965 fix: sync plugin cache versions with adapter release
Scope: GitHub issue and PR evidence policy
Area: ISSUES
-->

# Verified Issues

## Scope
GitHub issue and PR evidence policy

## Current source of truth
- `path:README.md`
- `path:plugins/rldyour-flow/skills/ry-review`


## Source Of Truth
- `path:README.md`
- `path:plugins/rldyour-flow/skills/ry-review`

## Last verified
- date: 2026-05-28
- commit: `2a852698661384a3ba4497c4ea2c98111d941965`
- checked by: Codex ry-start memory-domain normalization

## Facts
- Issues memories record how GitHub issues and PRs become verified evidence after code/config checks.
- Status policy: issues and PRs are evidence only after verification against current code/config.

## Evidence
- `commit:86b2555935f4c2185658417a3aff82d225d25392`
- `path:README.md`
- `path:plugins/rldyour-flow/skills/ry-review`

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
