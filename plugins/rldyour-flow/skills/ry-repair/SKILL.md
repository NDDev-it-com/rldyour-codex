---
name: ry-repair
description: "Чинит repository contracts и AI-tool context: source-of-truth scan, semantic entropy cleanup, stale docs/memory repair и validators. EN: ry-repair, repository repair."
---

# ry-repair

## Purpose

Normalize a repository so Codex, Claude Code, and OpenCode can work from the same verified facts with minimal semantic entropy. This is a technical repair workflow; it is not permission to change business logic, product semantics, deployment targets, data contracts, security posture, or ADR meaning silently.

For rldyour AI CLI configuration repositories, `/ry-repair` also owns deterministic install/update/sync convergence: local repository state, system Claude/Codex/OpenCode configs, Serena memories, and GitHub/fullrepo state must be checked through the root `config/ry-repair-sync-contract.json` and `scripts/ry_repair_sync.py` contract before being reported as synchronized.

## Workflow

1. Detect repository type, active branch/worktree, submodules, CI surface, and agent-only/fullrepo policy.
2. Read project instructions and native AI-tool config: `AGENTS.md`, `.claude/CLAUDE.md`, `.codex`, `.claude`, `.opencode`, plugin/skill/command/agent manifests, and repository contracts when present.
3. Inspect Serena memories, plans, and research archives for stale facts, unsupported claims, missing taxonomy, duplicated instructions, or contradictions with current code.
4. Inspect GitHub issues, pull requests, and recent history through the GitHub connector, GitHub MCP, or `gh` when available. Verify every issue against current code before treating it as a fact.
5. Inspect MCP/LSP/tooling config, hook lifecycles, CI gates, release manifests, dependency baselines, and docs source-of-truth declarations.
6. When the root control plane is present, run `python3 scripts/ry_repair_sync.py --plan --target "$PWD"` and use `--check` before claiming sync. Use `--apply --install-system` only for owner-approved system convergence.
7. Treat zero-active Semgrep policy as system-wide: source repo surfaces, installed `$CODEX_HOME/config.toml`, Claude marketplace cache, OpenCode project config, generated tool references, CI workflows, runtime pins, docs, and release gates must all be clean. Keep only negative validators/tests and historical changelog entries.
8. Detect semantic entropy: duplicated docs, stale pins, conflicting instructions, dead config, unclear source-of-truth, missing ADR/CONTEXT/FUTURE facts, broken validators, and adapter parity drift.
9. Produce a repair plan that separates technical repairs from owner-decision items.
10. Ask the owner in Russian before changing any business, functional, security-posture, deployment-target, data-model, or ADR decision. Use concise options with a recommended choice, reason, and impact.
11. Apply technical-only repairs using existing project patterns and native Codex surfaces.
12. Run matching validators, tests, schema checks, hook smoke, release/archive checks, installed-config checks, and instruction/memory freshness checks.
13. Synchronize durable docs and Serena memories from verified code/config state, then finish through `flow-post-task-sync` when durable artifacts changed.

## Non-Negotiables

- Current code, config, runtime checks, and verified GitHub state are the source of truth. Memories and docs are derived evidence.
- Hooks stay bounded and deterministic. They may mark state; `ry-repair` does the heavy repair work.
- Do not hide unresolved drift behind green summaries. Every blocked check names the blocker and next proof command.
- Do not report local repo, system config, Serena memory, or GitHub parity without evidence from `ry_repair_sync.py`, installed-config validators, current git state, and fullrepo/GitHub checks where applicable.

## Output

Report in Russian with scope, confirmed drift, repairs applied, owner-decision items, exact validation commands, and sync status.
