<!-- Memory Metadata
Last updated: 2026-05-30
Last verified: 2026-05-30
Last commit: 6946af99905464a1ba4ef90052854eaaf9239d08 fix: classify MCP safe-call runtime noise
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
- date: 2026-05-30
- commit: `6946af99905464a1ba4ef90052854eaaf9239d08`
- checked by: Codex ry-start automated release and metadata sync

## Facts
- Core memories index repository identity, source-of-truth files, and the current validation map.
- Current product/config version is `1.1.10`; root control-plane must pin
  `6946af99905464a1ba4ef90052854eaaf9239d08` for this adapter after the
  Codex plugin-cache alias sync release.

## Evidence
- `commit:6946af99905464a1ba4ef90052854eaaf9239d08`
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

## Applies to
- The scope declared in this memory and the source-of-truth paths listed below.

## Invariants
- Code, configuration, tests, and git state override this memory when they disagree.

## Current State
- See `Facts` for current durable facts. Do not treat `Historical evidence` or old commit notes as current state.

## Do Not Infer
- Do not infer runtime versions, product versions, commits, permissions, release state, or tool behavior from this memory without checking the source of truth.

## Update Triggers
- Update after verified changes to the source-of-truth files, runtime baselines, release tuple, validation gates, or durable agent workflow contracts.

## Validation Commands
- `python3 scripts/validate_serena_memory_schema.py --scope all --strict-mode strict-all`
- `python3 scripts/validate_serena_memory_semantics.py --scope all --strict-current-facts`
- `python3 scripts/validate_memory_freshness.py --scope all`

## Repair Procedure
- Re-read source-of-truth files, update only verified current facts, move stale facts to historical evidence, then rerun the validation commands.
