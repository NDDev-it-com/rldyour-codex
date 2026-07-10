<!-- Memory Metadata
Last updated: 2026-07-10
Last verified: 2026-07-10
Last commit: 7f39e8f3704126d9808604168a5c9061da228684 chore(release): codex adapter 1.8.4
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
- commit: `7f39e8f3704126d9808604168a5c9061da228684`
- checked by: Codex runtime and MCP pin refresh

## Facts
- The stable Codex CLI baseline is `@openai/codex@0.144.1`, pinned identically in `references/codex-baseline.json` and `config/mcp-runtime-versions.env`.
- Upstream `rust-v0.144.1` is a non-prerelease patch for standalone installer and code-mode host reliability; no adapter schema migration is required.
- The bootstrap-owned browser wrapper policy pin is `CLOAKBROWSER_VERSION=0.4.10`; its wrapper-only fixes do not change managed Chromium binary pins.
- Sequential Thinking MCP `2026.7.4` and Context7 MCP `3.2.3` are the current
  exact runtime pins; both preserve the existing `bunx` stdio launch contract.
- Runtime memories record pinned CLI/package baselines and freshness checks.

## Evidence
- `commit:7f39e8f3704126d9808604168a5c9061da228684`
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
