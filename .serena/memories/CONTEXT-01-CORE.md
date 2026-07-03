<!-- Memory Metadata
Last updated: 2026-05-22
Last commit: 698a800c48294a799de24f1f444044bb1bfbd6db chore(release): codex 1.6.1
Scope: always-needed repository context
Area: CONTEXT
-->

# Core Context

## Scope
always-needed repository context

## Current source of truth
- `path:README.md`
- `path:config/rldyour-contract.json`

## Last verified
- date: 2026-05-22
- commit: `698a800c48294a799de24f1f444044bb1bfbd6db`
- checked by: Codex ry-start memory taxonomy sync

## Facts
- Context memories hold stable facts that agents need before planning or editing.

## Evidence
- `commit:698a800c48294a799de24f1f444044bb1bfbd6db`
- `path:README.md`
- `path:config/rldyour-contract.json`

## Known pitfalls
- Treat this memory as derived context. Current code, configuration, runtime output, and GitHub state override stale memory text.

## Update policy
Update after verified changes to the referenced source-of-truth files.

## Delete / merge policy
- Delete or merge only when the referenced source-of-truth files no longer support this memory and the replacement memory preserves the durable facts.
