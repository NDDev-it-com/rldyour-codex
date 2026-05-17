<!-- Memory Metadata
Last updated: 2026-05-17
Last commit: 18d9e80 fix(flow): prevent bootstrap stop hook loops
Scope: scripts/validate_marketplace.sh, scripts/validate_agent_tools.py, scripts/smoke_serena_memory_taxonomy.sh, scripts/smoke_hooks.sh, scripts/doctor_system_codex.sh, scripts/release_manifest.py, scripts/check_mcp_runtime_versions.py, CHANGELOG.md, VERSION, .github/workflows/validate.yml
Area: RELEASE
-->

# RELEASE-01-VALIDATION

## Purpose

This memory records the validation and release gates that keep the marketplace, plugins, hooks, MCP runtime, managed agents, and agent-only context coherent.

## Source Of Truth

- `scripts/validate_marketplace.sh`: top-level validation pipeline.
- `scripts/validate_agent_tools.py`: Codex-native agent/skill surface validation.
- `scripts/validate_plugin_versions.py`: plugin manifest and marketplace metadata validation.
- `scripts/validate_skill_routing.py`: deterministic prompt-to-skill routing checks.
- `scripts/smoke_hooks.sh`: hook wiring, `PLUGIN_ROOT` command execution, and lifecycle smoke.
- `scripts/smoke_serena_memory_taxonomy.sh`: memory taxonomy/analyzer/hook smoke.
- `scripts/smoke_serena_memory_freshness.sh`: memory freshness regression smoke.
- `scripts/doctor_system_codex.sh`: installed runtime doctor.
- `scripts/release_manifest.py`: generated release manifest.
- `CHANGELOG.md` and `VERSION`: release notes and marketplace version.
- `.github/workflows/validate.yml`: CI contract for MCP pin checks on evented CI runs.
- `.github/workflows/dependency-check.yml`: periodic MCP pin freshness workflow (scheduled/manual).

## Entry Points

- `scripts/validate_marketplace.sh`: run before finalizing repository changes.
- `scripts/doctor_system_codex.sh`: run after installing changed global config/plugins/hooks/agents.
- `python3 scripts/release_manifest.py`: inspect release inventory.
- `python3 scripts/check_mcp_runtime_versions.py`: validate pinned runtime versions.
- `python3 scripts/validate_instruction_docs.py --require-agent-docs`: validate restored agent-only instruction docs.

## Current Behavior

- Marketplace validation now runs `uv run --with pyyaml python scripts/validate_agent_tools.py` before shell/Python/smoke checks.
- Python syntax checks in `scripts/validate_marketplace.sh` include `plugins/rldyour-serena-mcp/scripts/analyze_sync_scope.py` and `scripts/validate_agent_tools.py`.
- Marketplace validation runs `scripts/smoke_serena_memory_taxonomy.sh` after `scripts/smoke_serena_memory_freshness.sh`.
- `scripts/smoke_hooks.sh` supports multiple hooks under the same event/matcher, selects the expected hook by script path, rejects cwd/cache-search command wrappers, and runs configured hook commands from a temporary git repo with plugin runtime environment variables.
- `scripts/smoke_hooks.sh` includes a bootstrap-only `.serena` regression scenario: an unborn git repository containing only auto-created `.serena/project.yml`, `.serena/.gitignore`, and flow runtime markers must not require Flow post-task sync.
- `.github/workflows/validate.yml` runs `dependency-pins` on `push`, `pull_request`, and `workflow_dispatch`; this job executes `python3 scripts/check_mcp_runtime_versions.py --fail-on-outdated --json`, writes a step-summary payload, and uploads `dependency-check.json`.
- `scripts/smoke_codex_hooks_migration.sh` now expects installer output to contain `[features].hooks = true` and `[features].plugin_hooks = true`, while removing legacy `codex_hooks` aliases.
- `scripts/smoke_codex_hooks_migration.sh` and `scripts/doctor_system_codex.sh` keep deprecated key migration logic synchronized (including `codex_hooks`, legacy `web_search*`, unified exec/instructions/memories keys, and `use_legacy_landlock` cleanup).
- `scripts/doctor_system_codex.sh` keeps fullrepo current-state strict locally; a dirty normal branch or stale fullrepo is a real doctor failure outside the GitHub Actions advisory path.
- `scripts/doctor_system_codex.sh` verifies installed rldyour plugin hook count and requires every installed rldyour plugin hook to be enabled and trusted according to `codex app-server hooks/list`.
- Release `v0.1.1` is now published from commit `6b6dfd3` (`VERSION=0.1.1`), with changelog coverage in `CHANGELOG.md`.
- Validation contracts still include pinned runtime checks and `smoke` coverage defined in `dependency-check.yml` and `validate.yml`.

## Contracts And Data

- `scripts/validate_marketplace.sh` must include JSON validation, manifest validation, managed-agent config parity, Codex agent surface validation, shellcheck, Python syntax, skill routing, hook feature migration smoke, hook smoke, memory freshness/taxonomy smoke, fullrepo smoke, local git guard smoke, branch cleanup smoke, and release manifest checks.
- `scripts/validate_agent_tools.py` requires PyYAML and is normally run through `uv run --with pyyaml`.
- `scripts/smoke_serena_memory_taxonomy.sh` creates temporary git repositories and must leave no repo changes behind.

## Invariants

- No fake green checks: if a validation command cannot run, final delivery must report the blocker.
- `scripts/doctor_system_codex.sh` should be rerun after `scripts/install_system_codex.sh --apply` when global AGENTS, managed agents, plugin cache, hooks, or MCP runtime definitions change.
- Doctor must fail when installed config lacks `features.plugin_hooks = true`, because rldyour hook behavior is distributed as bundled plugin hooks.
- Doctor must fail when installed rldyour plugin hooks are missing, disabled, untrusted, or modified relative to their stored trust hash.
- Full marketplace validation should pass before pushing normal branch changes.
- Changelog entries should describe durable behavior changes, not transient task notes.

## Change Rules

- When adding a new validator/smoke, wire it into `scripts/validate_marketplace.sh` if it is part of the release gate.
- When changing hook layout or Stop gate conditions, update `scripts/smoke_hooks.sh`.
- When changing installed hook commands, run installer apply before doctor so `hooks.state` trusted hashes match the new plugin cache.
- When changing memory taxonomy/freshness behavior, update `scripts/smoke_serena_memory_taxonomy.sh` and `scripts/smoke_serena_memory_freshness.sh` if needed.
- MCP runtime pin checks must stay synchronized across `validate.yml` and `dependency-check.yml`: one catches drift in evented CI and one preserves periodic/manual review cadence.
- In docs, this contract must be described consistently in `docs/dependency-updates.md`, `docs/observability.md`, and `README.md` whenever validate/dependency-check behavior changes.

## Verification

- `scripts/validate_marketplace.sh`: full repository validation.
- `scripts/doctor_system_codex.sh`: installed runtime validation after cache/config install.
- `codex app-server hooks/list`: live hook trust/hash verification used by installer and doctor.
- `python3 scripts/release_manifest.py`: generated manifest includes expected plugin versions.
- `git diff --check`: whitespace sanity before commit.
