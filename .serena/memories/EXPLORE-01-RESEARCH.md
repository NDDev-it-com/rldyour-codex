<!-- Memory Metadata
Last updated: 2026-05-30
Last verified: 2026-05-30
Last commit: b64239591f7e6af0c5d6a7682039a8b45683732a fix(codex): harden mcp env forwarding and agent routing
Scope: source-backed research workflow
Area: EXPLORE
-->

# Research Workflow

## Scope
source-backed research workflow

## Current source of truth
- `path:plugins/rldyour-explore`
- `path:README.md`


## Source Of Truth
- `path:plugins/rldyour-explore`
- `path:README.md`

## Last verified
- date: 2026-05-30
- commit: `b64239591f7e6af0c5d6a7682039a8b45683732a`
- checked by: Codex ry-start automated release and metadata sync

## Facts
- Explore memories record when current source-backed research is required before implementation.

## Evidence
- `commit:6814a398cf0026102cf15688e038f71744d9ac5b`
- `path:plugins/rldyour-explore`
- `path:README.md`

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
