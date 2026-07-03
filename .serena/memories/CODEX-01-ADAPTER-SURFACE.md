<!-- Memory Metadata
Last updated: 2026-05-22
Last commit: 698a800c48294a799de24f1f444044bb1bfbd6db chore(release): codex 1.6.1
Scope: Codex adapter implementation surface
Area: CODEX
-->

# Codex Adapter Surface

## Scope
Codex adapter implementation surface

## Current source of truth
- `path:config/rldyour-contract.json`
- `path:.agents/plugins/marketplace.json`

## Last verified
- date: 2026-05-22
- commit: `698a800c48294a799de24f1f444044bb1bfbd6db`
- checked by: Codex ry-start memory taxonomy sync

## Facts
- Codex memories describe the Codex plugin marketplace, system install, hooks, MCP, apps, and managed agents.

## Evidence
- `commit:698a800c48294a799de24f1f444044bb1bfbd6db`
- `path:config/rldyour-contract.json`
- `path:.agents/plugins/marketplace.json`

## Known pitfalls
- Treat this memory as derived context. Current code, configuration, runtime output, and GitHub state override stale memory text.

## Update policy
Update after verified changes to the referenced source-of-truth files.

## Delete / merge policy
- Delete or merge only when the referenced source-of-truth files no longer support this memory and the replacement memory preserves the durable facts.
