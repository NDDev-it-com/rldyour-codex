<!-- Memory Metadata
Last updated: 2026-06-28
Last verified: 2026-06-28
Last commit: 9adbc0788922b9555a1ca7d5a5ddc57a2e5c1453 chore(release): rldyour-codex 1.7.12
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
- `path:scripts/smoke_mcp_capabilities.py` (two-layer external-MCP smoke resilience: per-server handler graceful skip + `--skip-server` CI policy)

## Last verified
- date: 2026-06-28
- commit: `9adbc0788922b9555a1ca7d5a5ddc57a2e5c1453`
- checked by: Codex 1.7.12 release sync after CodeQL regex-anchor remediation
- checked by: Codex 1.7.12 release sync after CodeQL regex-anchor remediation

## Facts
- Current rldyour-codex adapter VERSION is `1.7.12`; the release workflow publishes the matching numeric GitHub Release tag at the released commit. Root `config/repositories.json` and the superproject gitlink own the current adapter HEAD.
- Release memories record numeric versioning, tags, CI gates, and clean artifact hygiene without copying current control-plane pins.

## Evidence
- `commit:9adbc0788922b9555a1ca7d5a5ddc57a2e5c1453`
- `path:VERSION`
- `path:CHANGELOG.md`
- `path:.github/workflows/release.yml`

## Known pitfalls
- Treat this memory as derived context. Current code, configuration, runtime output, and GitHub state override stale memory text.

## Update policy
Update after verified changes to the referenced source-of-truth files.

## Delete / merge policy
- Delete or merge only when the referenced source-of-truth files no longer support this memory and the replacement memory preserves the durable facts.

## Applies to
- The scope declared in this memory and the source-of-truth paths listed below.

## Source of truth
- The `Current source of truth` section above, plus current code, configuration, tests, git state, and live GitHub state where the memory explicitly references live release or repository surfaces.

## Invariants
- Code, configuration, tests, validators, git state, and live GitHub state override this memory when they disagree.

## Current State
- See `Facts` for current durable facts. Do not treat `Historical evidence`, old commit notes, or previous release entries as current state.

## Do Not Infer
- Do not infer runtime versions, product versions, commits, permissions, release state, security posture, or tool behavior from this memory without checking the source of truth.

## Update Triggers
- Update after verified changes to the source-of-truth files, runtime baselines, release tuple, validation gates, live release state, or durable agent workflow contracts.

## Validation Commands
- `python3 scripts/validate_serena_memory_schema.py --scope all --strict-mode strict-all`
- `python3 scripts/validate_serena_memory_semantics.py --scope all --strict-current-facts`

## Repair Procedure
- Re-read source-of-truth files, update only verified current facts, move stale facts to historical evidence, then rerun the validation commands.
