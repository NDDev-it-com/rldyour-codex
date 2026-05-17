<!-- Memory Metadata
Last updated: 2026-05-17
Last commit: 08e3bc6 fix(release): bootstrap fullrepo context for release validation
Scope: plugins/rldyour-serena-mcp/scripts/analyze_sync_scope.py, plugins/rldyour-serena-mcp/hooks/stop_memory_sync.sh, plugins/rldyour-serena-mcp/hooks/mark_sync_required.sh, plugins/rldyour-serena-mcp/scripts/serena_memory_state.py, plugins/rldyour-serena-mcp/scripts/commit_serena_knowledge.sh, scripts/validate_agent_tools.py, scripts/worktree_add.sh, scripts/smoke_serena_memory_taxonomy.sh, plugins/rldyour-flow/hooks/session_start_worktree_bootstrap.sh, pyproject.toml, tests/, .github/workflows/*.yml, docs/adr/*.md
Area: TECHDEBT
-->

# TECHDEBT-01-NOW

## Purpose

This memory stores durable mistakes, edge cases, and anti-regression rules discovered while hardening the Codex memory-brain workflow. It is not a backlog; every item here is tied to current code behavior or a guardrail.

## Source Of Truth

- `scripts/validate_agent_tools.py`: rejects Claude-only surfaces in Codex plugins.
- `plugins/rldyour-serena-mcp/scripts/analyze_sync_scope.py`: Codex-specific memory target routing.
- `plugins/rldyour-serena-mcp/scripts/serena_memory_state.py`: distinction between Serena knowledge and other agent instructions.
- `plugins/rldyour-serena-mcp/hooks/stop_memory_sync.sh`: Stop advisory and loop guard.
- `plugins/rldyour-serena-mcp/scripts/commit_serena_knowledge.sh`: stale-memory refusal in fullrepo-managed repositories.
- `scripts/smoke_serena_memory_taxonomy.sh`: anti-regression coverage for the issues below.
- `scripts/worktree_add.sh` and `plugins/rldyour-flow/hooks/session_start_worktree_bootstrap.sh`: worktree/fullrepo bootstrap guardrails.

## Current Behavior

- Claude Code plugin-root agent files (`plugins/rldyour-*/agents/*.md`) are not valid Codex managed agents here. They are rejected by `scripts/validate_agent_tools.py`.
- Claude Code `SKILL.md` tool keys such as `allowed-tools` are not valid Codex skill metadata here. They are rejected by `scripts/validate_agent_tools.py`.
- Serena memory taxonomy is `AREA-01-SLUG.md`; old underscore names were migrated out to avoid analyzer/Stop-hook mismatch.
- The analyzer uses `CODEX-*` target memories for Codex-specific agent/plugin/runtime behavior. Do not reuse Claude-specific area names for Codex facts.
- Agent instruction files such as `AGENTS.md` and `.claude/CLAUDE.md` are not Serena knowledge paths for freshness comparison; they are durable agent context and can trigger memory/doc sync when behavior changes.
- `stop_memory_sync.sh` no longer points to Claude Code `Agent({ subagent_type: ... })` syntax. It points to managed Codex `serena-sync` when delegation is allowed and gives a fallback workflow.
- `commit_serena_knowledge.sh` refuses to acknowledge stale fullrepo-managed memories. A touched memory must directly mention current HEAD before markers are cleared.
- `scripts/worktree_add.sh` refuses to create a helper worktree without `origin/fullrepo`; it prints seed instructions instead of auto-publishing agent context from a helper script.
- `session_start_worktree_bootstrap.sh` only restores from existing `origin/fullrepo`; it never publishes.
- `plugin_hooks` was incorrectly treated as a deprecated/unstable key during the Codex adaptation. Official Codex docs make it the required opt-in for bundled plugin hooks, so installer/doctor/smoke now manage it as `true` and only remove `codex_hooks`.
- Codex alias migration is now split by risk: safe aliases (`experimental_instructions_file`, `background_terminal_timeout`, `experimental_use_unified_exec_tool`, `memories.no_memories_if_mcp_or_web_search`) are mapped deterministically; `use_legacy_landlock` is treated as explicit deprecated opt-in removal.
- Full migration smoke now includes a dedicated `suppress_warning_false` case to assert `suppress_unstable_features_warning = true` is respected as a unified config contract.
- MCP runtime pin freshness checks are now covered in both `.github/workflows/validate.yml` (`dependency-pins` on push/PR/dispatch) and `.github/workflows/dependency-check.yml` (scheduled/manual). Keep command flags, failure mode, and artifact contract in sync across both to avoid hidden drift by surface.
- `9a1cdc2` closed the stale SessionStart ordering debt by replacing separate Flow `SessionStart` hooks with one dispatcher, and `scripts/smoke_hooks.sh` now validates that dispatcher.
- `9a1cdc2` closed the malformed config fallback debt: `scripts/install_system_codex.sh` now fails closed on invalid existing TOML, and `scripts/smoke_codex_hooks_migration.sh` covers the failure.
- `9a1cdc2` closed the GitHub Actions tag-pin debt by pinning external actions to full SHAs and adding `scripts/validate_action_pins.py`.
- `9a1cdc2` closed the narrow secret-regex debt by adding `scripts/scan_text_security.py` for broader tracked/agent-only text scanning plus hidden Unicode controls.
- `9a1cdc2` introduced `docs/adr/0001-codex-marketplace-operating-model.md`; further irreversible decisions should add/update ADRs rather than living only in memories.
- `6b85464` closed the missing unit/coverage harness debt by adding `pyproject.toml`, 40 unit tests, `pytest.xml`, `coverage.xml`, and a 70% initial coverage threshold.
- `6b85464` closed the release evidence gap by adding `scripts/release_sbom.py` and a manual GitHub release workflow with deterministic bundle, release manifest, generated SPDX SBOM, optional GitHub dependency graph SBOM export, and artifact attestations.
- `6b85464` closed the governance-template gap with CODEOWNERS, issue templates, PR template, `CONTRIBUTING.md`, `SECURITY.md`, branch-protection desired-state files, and ADRs 0002-0005.
- `6b85464` closed the sparse routing-class debt by adding explicit routing classes for all 38 skills and coverage requirements for implicit, explicit-only, and finalization skills.
- `9da936d` closed the GitHub-hosted runner git-identity fixture gap by configuring local author settings for temp fullrepo repositories and clones before test commits.
- `af26c31` closed the strict-noise classifier false negative for clean-runner `uv` package download progress lines while preserving unknown-stderr failure behavior.
- `882030e` closed the normal-branch CI/fullrepo boundary gap: GitHub normal-branch validation no longer requires absent fullrepo-managed memories, while local/fullrepo-aware checkouts still validate live memory freshness.
- `eb39996` closed the follow-up untracked-memory CI gap: if GitHub Actions creates or restores `.serena/memories` as untracked fullrepo context during a normal-branch job, taxonomy and marketplace validation still skip live repository-memory freshness instead of treating that untracked context as normal-branch source.
- `08e3bc6` closed the release-workflow/fullrepo context gap: manual release validation bootstraps `fullrepo` before requiring agent instruction docs, so `main` can remain free of agent-only files while release validation stays strict.
- Semgrep's global `IFS` tampering rule is intentionally excluded in `security-static` because this repository uses `IFS=$'\n\t'` as a strict shell prologue and validates shell scripts with ShellCheck.

## Contracts And Data

- `scripts/smoke_serena_memory_taxonomy.sh` must keep tests for analyzer schema v2, `CORE-01-INDEX.md`, `AREA-01-SLUG.md`, agent-instruction sync routing, recursive memory scan, Stop advisory, loop guard, and fullrepo acknowledgement/refusal.
- `scripts/smoke_hooks.sh` must keep Flow `SessionStart` dispatcher coverage and hook strict prologue coverage.
- `scripts/validate_action_pins.py` and `scripts/scan_text_security.py` are now release-gate guardrails and should stay in `scripts/validate_marketplace.sh`.
- `scripts/classify_ci_noise.py` and the pytest/coverage harness are release-gate guardrails and should stay in `scripts/validate_marketplace.sh` or visible CI jobs.
- `RLDYOUR_DRY_RUN=1 scripts/worktree_add.sh <branch>` must show one git command and one fullrepo restore command without side effects.
- Fullrepo-managed memory acknowledgement is allowed only after `serena_memory_state.py` reports current or a memory directly mentions HEAD.

## Invariants

- Do not port Claude Code implementation files verbatim into Codex without mapping them to Codex surfaces.
- Do not treat runtime markers or one-off audit observations as memories.
- Do not let Stop hooks edit memory content directly; they should route the workflow.
- Do not allow a hook loop to block Stop forever for the same HEAD/state.
- Do not let fullrepo helper scripts publish from a newly created worktree implicitly.
- Do not port old hook-feature assumptions forward without re-checking official Codex docs; `plugin_hooks` must remain enabled while rldyour hooks are bundled in plugins.

## Change Rules

- If a new cross-tool mismatch is discovered, add a validator or smoke assertion first, then encode the correction in the relevant memory.
- If official Codex docs change hook/plugin/skill config shape, update `CODEX-01-PLUGIN-CANON.md`, validators, and smoke tests together.
- If a memory target is renamed, update analyzer targets, smoke expectations, the index memory, and any Stop advisory copy.

## Verification

- `uv run --with pyyaml python scripts/validate_agent_tools.py`: catches Claude/Codex surface drift.
- `scripts/smoke_serena_memory_taxonomy.sh`: catches memory taxonomy and hook regressions.
- `RLDYOUR_DRY_RUN=1 scripts/worktree_add.sh test/codex-memory-brain`: proves safe worktree command construction.
- `plugins/rldyour-serena-mcp/scripts/commit_serena_knowledge.sh`: refuses stale fullrepo-managed memories and clears markers only when current.
