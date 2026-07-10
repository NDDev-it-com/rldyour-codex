<!-- Memory Metadata
Last updated: 2026-07-10
Last verified: 2026-07-10
Last commit: 693a00640832d3af8355066c0fd2fda4e84ad78e chore(release): codex adapter 1.8.6
Scope: instruction docs and durable operator documentation
Area: DOCS
-->

# Instruction Docs

## Scope
instruction docs and durable operator documentation

## Current source of truth
- `path:AGENTS.md`
- `path:.claude/CLAUDE.md`
- `path:README.md`
- `path:system/AGENTS.md`
- `path:CONTRIBUTING.md`
- `path:docs/release-process.md`

## Last verified
- date: 2026-07-10
- commit: `693a00640832d3af8355066c0fd2fda4e84ad78e`
- checked by: Codex browser trust-boundary instruction sync

## Facts
- Docs memories record which instruction and operator docs must change after durable behavior changes.
- `AGENTS.md`, `.claude/CLAUDE.md`, README, browser skill docs, and MCP docs
  consistently require the managed CloakBrowser wrappers and the explicit
  disabled state for app-managed browser, Node REPL, and computer-use surfaces.
- Release operator docs consistently require stable-green branch CI before a
  manually created signed numeric tag and describe workflow dispatch as an
  existing-tag-only verification/retry path.

## Evidence
- `commit:693a00640832d3af8355066c0fd2fda4e84ad78e`
- `path:AGENTS.md`
- `path:.claude/CLAUDE.md`
- `path:README.md`
- `path:system/AGENTS.md`
- `path:CONTRIBUTING.md`
- `path:docs/release-process.md`

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
