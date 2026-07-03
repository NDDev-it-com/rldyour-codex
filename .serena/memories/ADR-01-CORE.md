<!-- Memory Metadata
Last updated: 2026-05-22
Last commit: 698a800c48294a799de24f1f444044bb1bfbd6db chore(release): codex 1.6.1
Scope: architecture decisions and owner-approved policy changes
Area: ADR
-->

# ADR Core

## Scope
architecture decisions and owner-approved policy changes

## Current source of truth
- `path:docs/adr`

## Last verified
- date: 2026-05-22
- commit: `698a800c48294a799de24f1f444044bb1bfbd6db`
- checked by: Codex ry-start memory taxonomy sync

## Facts
- ADR memories record decisions and policy shape. Meaning changes require explicit owner approval.

## Evidence
- `commit:698a800c48294a799de24f1f444044bb1bfbd6db`
- `path:docs/adr`

## Known pitfalls
- Treat this memory as derived context. Current code, configuration, runtime output, and GitHub state override stale memory text.

## Update policy
ADR meaning changes require explicit owner approval; format-only normalization may be done without changing the decision.

## Delete / merge policy
- Delete or merge only when the referenced source-of-truth files no longer support this memory and the replacement memory preserves the durable facts.
