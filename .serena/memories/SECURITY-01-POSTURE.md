<!-- Memory Metadata
Last updated: 2026-07-10
Last verified: 2026-07-10
Last commit: 693a00640832d3af8355066c0fd2fda4e84ad78e chore(release): codex adapter 1.8.6
Scope: security posture and blocking/warning policy
Area: SECURITY
-->

# Security Posture

## Scope
security posture and blocking/warning policy

## Current source of truth
- `path:plugins/rldyour-security`
- `path:README.md`
- `path:config/rldyour-contract.json`
- `path:scripts/install_system_codex.sh`
- `path:scripts/doctor_system_codex.sh`

## Last verified
- date: 2026-07-10
- commit: `693a00640832d3af8355066c0fd2fda4e84ad78e`
- checked by: Codex app-managed browser trust-boundary hardening

## Facts
- Security memories record block/warn/review classes and defensive-only review policy.
- Browser routing fails closed at install and doctor boundaries: the bundled
  browser plugin is explicitly disabled, app-managed Node REPL/computer-use
  transports remain disabled, and active reinjection requires reinstall plus
  Codex restart rather than an unmanaged fallback.
- Release automation cannot mint tags: only exact pre-existing numeric tags
  whose peeled commits are contained in `origin/main` may reach publication.

## Evidence
- `commit:693a00640832d3af8355066c0fd2fda4e84ad78e`
- `path:plugins/rldyour-security`
- `path:README.md`
- `path:config/rldyour-contract.json`
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
