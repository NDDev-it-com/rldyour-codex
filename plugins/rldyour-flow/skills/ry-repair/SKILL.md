---
name: ry-repair
description: "Чинит repository contracts и AI-tool context: source-of-truth scan, semantic entropy cleanup, stale docs/memory repair и validators. EN: ry-repair, repository repair."
---

# ry-repair

## Purpose

Normalize a repository so Codex, Claude Code, and OpenCode can work from the same verified facts with minimal semantic entropy. This is a technical repair workflow; it is not permission to change business logic, product semantics, deployment targets, data contracts, security posture, or ADR meaning silently.

## Workflow

1. Detect repository type, active branch/worktree, submodules, CI surface, and agent-only/fullrepo policy.
2. Read project instructions and native AI-tool config: `AGENTS.md`, `.claude/CLAUDE.md`, `.codex`, `.claude`, `.opencode`, plugin/skill/command/agent manifests, and repository contracts when present.
3. Inspect Serena memories, plans, and research archives for stale facts, unsupported claims, missing taxonomy, duplicated instructions, or contradictions with current code.
4. Inspect GitHub issues, pull requests, and recent history through the GitHub connector, GitHub MCP, or `gh` when available. Verify every issue against current code before treating it as a fact.
5. Inspect MCP/LSP/tooling config, hook lifecycles, CI gates, release manifests, dependency baselines, and docs source-of-truth declarations.
6. Detect semantic entropy: duplicated docs, stale pins, conflicting instructions, dead config, unclear source-of-truth, missing ADR/CONTEXT/FUTURE facts, broken validators, and adapter parity drift.
7. Produce a repair plan that separates technical repairs from owner-decision items.
8. Ask the owner in Russian before changing any business, functional, security-posture, deployment-target, data-model, or ADR decision. Use concise options with a recommended choice, reason, and impact.
9. Apply technical-only repairs using existing project patterns and native Codex surfaces.
10. Run matching validators, tests, schema checks, hook smoke, release/archive checks, and instruction/memory freshness checks.
11. Synchronize durable docs and Serena memories from verified code/config state, then finish through `flow-post-task-sync` when durable artifacts changed.

## Non-Negotiables

- Current code, config, runtime checks, and verified GitHub state are the source of truth. Memories and docs are derived evidence.
- Hooks stay bounded and deterministic. They may mark state; `ry-repair` does the heavy repair work.
- Do not hide unresolved drift behind green summaries. Every blocked check names the blocker and next proof command.

## Output

Report in Russian with scope, confirmed drift, repairs applied, owner-decision items, exact validation commands, and sync status.
