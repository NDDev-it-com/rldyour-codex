<!-- Memory Metadata
Last updated: 2026-05-31
Last verified: 2026-05-31
Last commit: 1252b518c85b3d3ea359109062c6d804696ef7f7 chore(release): codex 1.1.14 (other)
Scope: instruction docs and durable operator documentation
Area: DOCS
-->

# DOCS-01-INSTRUCTIONS

## Scope
instruction docs and durable operator documentation

## Current source of truth
- `path:AGENTS.md`
- `path:.claude/CLAUDE.md`
- `path:README.md`
- `path:system/AGENTS.md`


## Source Of Truth
- `path:AGENTS.md`
- `path:.claude/CLAUDE.md`
- `path:README.md`
- `path:system/AGENTS.md`

## Last verified
- date: 2026-05-31
- commit: `1252b518c85b3d3ea359109062c6d804696ef7f7`
- checked by: Codex ry-start automated release and metadata sync

## Facts
- Docs memories record which instruction and operator docs must change after durable behavior changes.
- `system/AGENTS.md` is the compact global Codex owner/runtime contract and
  fullrepo `AGENTS.md` is the compact project-specific contract. The
  `1.1.6` hardening keeps each file below 10 KiB and validates the combined
  pair with `scripts/validate_agents_context_budget.py`; deep operational
  detail belongs in skills, references, and Serena memories rather than
  bloating AGENTS context.

## Evidence
- `commit:1252b518c85b3d3ea359109062c6d804696ef7f7`
- `path:AGENTS.md`
- `path:.claude/CLAUDE.md`
- `path:README.md`
- `path:system/AGENTS.md`

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
