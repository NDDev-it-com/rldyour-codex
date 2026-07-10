<!-- Memory Metadata
Last updated: 2026-07-10
Last verified: 2026-07-10
Last commit: b8f326c53ba27dfda4173fb59b7de03191a7b5f6 chore(release): codex 1.8.9 (release_metadata)
Scope: Codex adapter implementation surface
Area: CODEX
-->

# Codex Adapter Surface

## Scope
Codex adapter implementation surface

## Current source of truth
- `path:config/rldyour-contract.json`
- `path:.agents/plugins/marketplace.json`
- `path:scripts/install_system_codex.sh`
- `path:scripts/doctor_system_codex.sh`

## Last verified
- date: 2026-07-10
- commit: `b8f326c53ba27dfda4173fb59b7de03191a7b5f6`
- checked by: Codex 1.8.10 managed update-policy preparation

## Facts
- Codex memories describe the Codex plugin marketplace, system install, hooks, MCP, apps, and managed agents.
- Installer owns the explicit disabled state for `browser@openai-bundled` and
  any present app-managed `node_repl` / `computer-use` MCP tables. Doctor is the
  enforcement boundary for active or reinjected copies and requires reinstall
  plus process restart before browser work resumes.
- Installer owns `check_for_update_on_startup = false` in the base, owner, and
  safe configs. Exact Codex runtime upgrades remain bootstrap-owned
  transactions and never target an unrelated global npm prefix.

## Evidence
- `commit:693a00640832d3af8355066c0fd2fda4e84ad78e`
- `commit:b8f326c53ba27dfda4173fb59b7de03191a7b5f6`
- `path:config/rldyour-contract.json`
- `path:.agents/plugins/marketplace.json`
- `path:scripts/install_system_codex.sh`
- `path:scripts/doctor_system_codex.sh`

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
