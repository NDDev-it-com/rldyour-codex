<!-- Memory Metadata
Last updated: 2026-05-30
Last verified: 2026-05-30
Last commit: 7df63a3ba7302bad4af6c7a6d2e26703cec76a03 chore(release): codex 1.1.6 (source)
Scope: GitHub Actions and local CI policy
Area: CI
-->

# CI Actions

## Scope
GitHub Actions and local CI policy

## Current source of truth
- `path:.github/workflows`
- `path:README.md`


## Source Of Truth
- `path:.github/workflows`
- `path:README.md`

## Last verified
- date: 2026-05-30
- commit: `7df63a3ba7302bad4af6c7a6d2e26703cec76a03`
- checked by: Codex ry-start automated release and metadata sync

## Facts
- CI memories record which checks prove repository integrity and which checks are intentionally lightweight.
- GitHub Actions workflows pin third-party actions to full commit SHAs. Dependabot
  monitors `github-actions` monthly and groups all action version updates into a
  single PR through `.github/dependabot.yml`.

## Evidence
- `commit:7df63a3ba7302bad4af6c7a6d2e26703cec76a03`
- `path:.github/workflows`
- `path:.github/dependabot.yml`
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
