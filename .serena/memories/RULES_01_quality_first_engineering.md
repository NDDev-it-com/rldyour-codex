<!-- Memory Metadata
Last updated: 2026-05-08
Last commit: 260345a docs: record runtime consistency fixes
Scope: plugins/rldyour-rules, plugins/rldyour-flow/skills/instruction-docs-sync, plugins/rldyour-flow/scripts/instruction_docs_state.py, scripts/validate_instruction_docs.py, README.md, AGENTS.md, .claude/CLAUDE.md, system/AGENTS.md
Area: RULES
-->

# RULES_01_quality_first_engineering

## Purpose

Keep the enforced rule layer for this marketplace: quality defaults, architecture boundaries, dependency/verification policy, and agent instruction governance.

## Source-of-Truth

- `plugins/rldyour-rules/.codex-plugin/plugin.json`
- `plugins/rldyour-rules/skills/*/SKILL.md`
- `plugins/rldyour-rules/references/rules-policy.md`
- `plugins/rldyour-rules/references/architecture-policy.md`
- `plugins/rldyour-rules/references/dependency-policy.md`
- `plugins/rldyour-rules/references/quality-gates.md`
- `plugins/rldyour-rules/references/project-instructions-and-adrs.md`
- `scripts/validate_instruction_docs.py`
- `plugins/rldyour-flow/scripts/instruction_docs_state.py`

## Scope and Responsibilities

- Quality-first behavior priority: safety, correctness, architecture, consistency, delivery speed.
- Hard bans are non-negotiable in scope:
  - no hacks,
  - no temporary workaround logic,
  - no fake green checks,
  - no swallowed errors,
  - no secrets/tokens in code/docs/artifacts.
- Architecture defaults:
  - frontend new work defaults to FSD,
  - backend to VSA,
  - existing coherent architecture is preserved unless owner approves a deliberate refactor.
- Verification-first mindset: run evidence-based checks matching touched stack and report outcomes explicitly.
- Instruction-doc governance:
  - `AGENTS.md` and `.claude/CLAUDE.md` are durable instruction surfaces and must be kept aligned with verified source-of-truth.
- No blocking hooks in `rldyour-rules`; policy is advisory-first unless hard bans are hit in current scope.

## Invariants

- Do not edit plugin or source files outside requested scope with speculative architecture rewrites.
- Do not store runtime markers, secrets, or browser evidence in durable docs.
- Keep the plugin as a policy layer; avoid duplicating behavior from `rldyour-flow`, `rldyour-serena-mcp`, `rldyour-lsps`, or `rldyour-explore`.
- Maintain compatibility with fullrepo workflows and instruction-doc synchronization gates.

## Verification

- `python3 scripts/validate_instruction_docs.py --require-agent-docs`
- `scripts/validate_marketplace.sh`
- `python3 scripts/validate_skill_routing.py`
- `python3 plugins/rldyour-serena-mcp/scripts/serena_memory_state.py` (durable memory checks)
- `python3 plugins/rldyour-flow/scripts/flow_post_task_state.py` (post-task state checks)
- `jq empty plugins/rldyour-rules/.codex-plugin/plugin.json`
- `python3 -m py_compile scripts/validate_instruction_docs.py` (or run equivalent static parse checks as needed)
- `python3 plugins/rldyour-flow/scripts/instruction_docs_state.py --json | python3 -m json.tool`
