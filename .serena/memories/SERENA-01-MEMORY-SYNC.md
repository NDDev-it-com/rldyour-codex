<!-- Memory Metadata
Last updated: 2026-05-31
Last verified: 2026-05-31
Last commit: 67e05455d3e35449d070874257acdfa13520f886 ci: enforce ubuntu-only public runners
Scope: Serena memory, fullrepo, and knowledge sync policy
Area: SERENA
-->

# SERENA-01-MEMORY-SYNC

## Scope
Serena memory, fullrepo, and knowledge sync policy

## Current source of truth
- `path:plugins/rldyour-serena-mcp`
- `path:.serena/project.yml`
- `path:README.md`


## Source Of Truth
- `path:plugins/rldyour-serena-mcp`
- `path:.serena/project.yml`
- `path:README.md`

## Last verified
- date: 2026-05-31
- commit: `67e05455d3e35449d070874257acdfa13520f886`
- checked by: Codex ry-start automated release and metadata sync

## Facts
- Serena memories record memory format, evidence, freshness, fullrepo, and runtime marker policy.
- `scripts/check_serena_memory_freshness.py` compares the newest `Last commit`
  evidence in `.serena/memories/*.md` with the adapter source branch HEAD and
  fails when high-impact non-knowledge changes are not reflected.
- Root `scripts/validate_adapter_health.py` now delegates the Codex freshness
  check when adapter Serena memories are present, so root local/fullrepo health
  can catch stale adapter knowledge.
- The 2026-05-28 Codex release-hardening sync records `b92c6a3` as the current
  memory evidence head after Semgrep/shadcn MCP pin updates, product version
  `1.0.0`, and stale research-claim validation changes.
- The 2026-05-28 internal adapter release sync records `2a85269` as the current
  memory evidence head after the `1.0.2` product bump and plugin manifest
  version parity hardening.

## Evidence
- `commit:67e05455d3e35449d070874257acdfa13520f886`
- `path:plugins/rldyour-serena-mcp`
- `path:.serena/project.yml`
- `path:README.md`
- `path:scripts/check_serena_memory_freshness.py`

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
