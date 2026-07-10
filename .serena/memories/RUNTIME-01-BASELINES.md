<!-- Memory Metadata
Last updated: 2026-07-10
Last verified: 2026-07-10
Last commit: b15ae75129911a81c6c8e562cee31a1473ab25e9 ci(deps): repin reusable workflows to 0.5.1
Scope: CLI runtime and package baselines
Area: RUNTIME
-->

# Runtime Baselines

## Scope
CLI runtime and package baselines

## Current source of truth
- `path:references/codex-baseline.json`
- `path:config/mcp-runtime-versions.env`
- `path:references/codex-surface-adoption.md`

## Last verified
- date: 2026-07-10
- commit: `b15ae75129911a81c6c8e562cee31a1473ab25e9`
- checked by: Codex CLI stable-baseline refresh

## Facts
- The stable Codex CLI baseline is `@openai/codex@0.144.1`, pinned identically in `references/codex-baseline.json` and `config/mcp-runtime-versions.env`.
- Upstream `rust-v0.144.1` is a non-prerelease patch for standalone installer and code-mode host reliability; no adapter schema migration is required.
- The bootstrap-owned browser wrapper policy pin is `CLOAKBROWSER_VERSION=0.4.10`; its wrapper-only fixes do not change managed Chromium binary pins.
- Runtime memories record pinned CLI/package baselines and freshness checks.

## Evidence
- `commit:b15ae75129911a81c6c8e562cee31a1473ab25e9`
- `path:references/codex-baseline.json`
- `path:config/mcp-runtime-versions.env`
- `https://github.com/openai/codex/releases/tag/rust-v0.144.1`

## Known pitfalls
- Treat this memory as derived context. Current code, configuration, runtime output, and GitHub state override stale memory text.

## Update policy
Update after verified changes to the referenced source-of-truth files.

## Delete / merge policy
- Delete or merge only when the referenced source-of-truth files no longer support this memory and the replacement memory preserves the durable facts.

## Applies to

- The scope and source-of-truth paths declared in this memory.

## Source of truth

- The `Current source of truth` entries above, plus current code, configuration, tests, git state, and live GitHub state where this memory references live release or repository surfaces.

## Invariants

- Current code, configuration, tests, validators, git state, and live GitHub state override this memory whenever they disagree.

## Current State

- Treat the `Facts` section as the current durable state. Do not treat historical evidence, superseded notes, or previous release entries as current.

## Do Not Infer

- Do not infer runtime versions, product versions, commits, permissions, release state, security posture, or tool behavior from this memory without checking the source of truth.

## Update Triggers

- Update after verified changes to the source-of-truth files, runtime baselines, release tuple, validation gates, live release state, or durable agent-workflow contracts.

## Validation Commands

- Run the rldyour control-plane Serena memory validators in strict mode: `validate_serena_memory_schema` (`--strict-mode strict-all`) and `validate_serena_memory_semantics` (`--strict-current-facts --strict-metadata-dates --strict-evidence-commits`).

## Repair Procedure

1. Re-read the source-of-truth files listed above.
2. Update only verified current facts; move stale facts into historical evidence.
3. Rerun the validation commands until green.
