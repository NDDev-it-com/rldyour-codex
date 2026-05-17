<!-- Memory Metadata
Last updated: 2026-05-18
Last commit: cdad168 fix(flow): make SessionStart offline and fast
Scope: scripts/validate_marketplace.sh, scripts/validate_fast.sh, scripts/validate_runtime.sh, scripts/validate_release.sh, scripts/validate_agent_tools.py, scripts/validate_execpolicy_rules.sh, scripts/smoke_serena_memory_taxonomy.sh, scripts/smoke_hooks.sh, scripts/doctor_system_codex.sh, scripts/release_manifest.py, scripts/release_sbom.py, scripts/check_mcp_runtime_versions.py, scripts/validate_runtime_prereqs.py, scripts/classify_ci_noise.py, system/agents/*.toml, system/rules/*.rules, pyproject.toml, tests/, CHANGELOG.md, VERSION, .github/workflows/*.yml, .github/actions/setup-codex-runtime/action.yml
Area: RELEASE
-->

# RELEASE-01-VALIDATION

## Purpose

This memory records the validation and release gates that keep the marketplace, plugins, hooks, MCP runtime, managed agents, and agent-only context coherent.

## Source Of Truth

- `scripts/validate_marketplace.sh`: top-level validation pipeline.
- `scripts/validate_fast.sh`: fast local/CI validation slice for static checks, routing, security text scan, and unit coverage.
- `scripts/validate_runtime.sh`: installer, hook, fullrepo, and runtime prerequisite validation slice.
- `scripts/validate_release.sh`: release manifest, SBOM, plugin version, and release artifact dry-run slice.
- `scripts/validate_agent_tools.py`: Codex-native agent/skill surface validation.
- `scripts/validate_plugin_versions.py`: plugin manifest and marketplace metadata validation.
- `scripts/validate_skill_routing.py`: deterministic prompt-to-skill routing checks.
- `scripts/validate_action_pins.py`: full-SHA pin validation for external GitHub Actions.
- `scripts/validate_execpolicy_rules.sh`: Codex execpolicy rule validation for managed YOLO rails.
- `scripts/scan_text_security.py`: tracked and agent-only text scan for secret-like values and hidden Unicode controls.
- `scripts/smoke_hooks.sh`: hook wiring, `PLUGIN_ROOT` command execution, and lifecycle smoke.
- `scripts/smoke_serena_memory_taxonomy.sh`: memory taxonomy/analyzer/hook smoke.
- `scripts/smoke_serena_memory_freshness.sh`: memory freshness regression smoke.
- `scripts/doctor_system_codex.sh`: installed runtime doctor.
- `scripts/release_manifest.py`: generated release manifest.
- `scripts/release_sbom.py`: generated SPDX 2.3 SBOM from plugin manifests and MCP runtime pins.
- `scripts/validate_runtime_prereqs.py`: strict launcher prerequisite validator for enabled MCP/Codex runtime surfaces.
- `scripts/classify_ci_noise.py`: strict targeted stderr/log classifier for CI noise.
- `pyproject.toml`: pytest, coverage, and Python 3.13 runtime contract.
- `.github/actions/setup-codex-runtime/action.yml`: shared GitHub Actions setup for Python, uv, Bun, Dart, system packages, and optional pinned Codex CLI.
- `.github/workflows/security-static.yml`: manual no-paid static security workflow.
- `.github/workflows/release.yml`: manual release bundle, SBOM, attestation, and GitHub Release workflow.
- `CHANGELOG.md` and `VERSION`: release notes and marketplace version.
- `.github/workflows/validate.yml`: manual validation workflow with Ubuntu default and explicit macOS opt-in.
- `.github/workflows/dependency-check.yml`: manual MCP pin freshness workflow.

## Entry Points

- `scripts/validate_marketplace.sh`: run before finalizing repository changes.
- `scripts/validate_fast.sh`: run the fast local CI slice.
- `scripts/validate_runtime.sh --strict-runtime`: run installer/runtime/hook/fullrepo gates with strict prerequisite checks.
- `scripts/validate_release.sh`: run release manifest/SBOM/version gates.
- `scripts/doctor_system_codex.sh`: run after installing changed global config/plugins/hooks/agents.
- `python3 scripts/release_manifest.py`: inspect release inventory.
- `python3 scripts/release_sbom.py`: inspect generated SBOM inventory.
- `python3 scripts/check_mcp_runtime_versions.py`: validate pinned runtime versions.
- `python3 scripts/validate_action_pins.py`: validate external GitHub Actions are pinned to 40-character commit SHAs.
- `scripts/validate_execpolicy_rules.sh`: validate managed Codex execpolicy rules when Codex CLI is available.
- `python3 scripts/scan_text_security.py`: scan repository text for secret-like patterns and hidden Unicode controls without printing matched values.
- `uv run --with pytest --with pytest-cov --with pyyaml python -m pytest`: run unit tests and coverage threshold.
- `python3 scripts/validate_instruction_docs.py --require-agent-docs`: validate restored agent-only instruction docs.

## Current Behavior

- Marketplace validation now runs `uv run --with pyyaml python scripts/validate_agent_tools.py` before shell/Python/smoke checks.
- `scripts/validate_agent_tools.py` verifies the temporary managed-subagent MCP isolation policy from the current `.mcp.json` registry. Every current non-core MCP server must be explicitly disabled in each managed agent TOML, each disabled MCP override must include registry-matching transport metadata, and the lightweight core inherited surface plus built-in `codex_apps` remain allowed without declaring `codex_apps` as an `mcp_servers` table.
- Marketplace validation now runs `python3 scripts/validate_action_pins.py` before skill checks.
- Marketplace validation now runs the Python unit/coverage harness and requires at least 75% coverage.
- Marketplace validation runs `scripts/validate_execpolicy_rules.sh` when Codex CLI is available, and runtime validation enforces it after temporary installation.
- Python syntax checks in `scripts/validate_marketplace.sh` include `plugins/rldyour-serena-mcp/scripts/analyze_sync_scope.py`, `scripts/validate_agent_tools.py`, `scripts/validate_action_pins.py`, `scripts/scan_text_security.py`, `scripts/classify_ci_noise.py`, and `scripts/release_sbom.py`.
- Marketplace validation runs `scripts/smoke_serena_memory_taxonomy.sh` after `scripts/smoke_serena_memory_freshness.sh`.
- `scripts/smoke_hooks.sh` supports multiple hooks under the same event/matcher, selects the expected hook by script path, rejects cwd/cache-search command wrappers, and runs configured hook commands from a temporary git repo with plugin runtime environment variables.
- `scripts/smoke_hooks.sh` includes a fake-network Flow SessionStart regression: a fake `git` sleeps/fails on `fetch` and `ls-remote`, and the smoke requires fast offline context without any network git calls.
- `scripts/smoke_hooks.sh` includes a bootstrap-only `.serena` regression scenario: an unborn git repository containing only auto-created `.serena/project.yml`, `.serena/.gitignore`, and flow runtime markers must not require Flow post-task sync.
- `scripts/smoke_hooks.sh` runs each hook smoke through a process-group timeout wrapper controlled by `RLDYOUR_HOOK_SMOKE_TIMEOUT` so a stuck hook reports a labeled timeout instead of hanging validation.
- `.github/workflows/validate.yml` is manual-only through `workflow_dispatch`. It defaults to Ubuntu and runs macOS only when `include_macos=true`, so expensive macOS minutes are spent only on explicit owner/agent requests.
- `.github/branch-protection/main.json` documents manual validation checks rather than enforcing required automatic checks, because this repository's GitHub Actions spend policy is explicit-run only.
- The manual `validate.yml` MCP safe-call job bootstraps `fullrepo` agent context before installing into temporary `CODEX_HOME`, then runs deterministic MCP capability calls and strict stderr classification against known first-run MCP/uv/Serena startup noise.
- `scripts/classify_ci_noise.py` recognizes known first-run Taplo/LSP configuration stderr such as `failed to fetch configuration` and `invalid configuration response`, while strict mode still fails on unknown MCP safe-call output.
- `scripts/smoke_codex_hooks_migration.sh` now expects installer output to contain `[features].hooks = true` and `[features].plugin_hooks = true`, while removing legacy `codex_hooks` aliases.
- `scripts/smoke_codex_hooks_migration.sh` and `scripts/doctor_system_codex.sh` keep deprecated key migration logic synchronized (including `codex_hooks`, legacy `web_search*`, unified exec/instructions/memories keys, and `use_legacy_landlock` cleanup).
- `scripts/doctor_system_codex.sh` keeps fullrepo current-state strict locally; a dirty normal branch or stale fullrepo is a real doctor failure outside the GitHub Actions advisory path.
- `scripts/doctor_system_codex.sh` verifies installed rldyour plugin hook count and requires every installed rldyour plugin hook to be enabled and trusted according to the app-server RPC method `hooks/list`.
- `scripts/doctor_system_codex.sh` also verifies that installed managed subagent TOML files match source, preserve the temporary specialist-MCP isolation policy, include complete disabled transport metadata, and do not declare built-in `codex_apps` under `mcp_servers`.
- GitHub Actions workflows pin external actions by full commit SHA, with the source tag kept as an inline comment for review.
- `.github/workflows/validate.yml` has a separate unit-test matrix job that uploads `pytest.xml`, `coverage.xml`, and strict stderr logs.
- `.github/workflows/security-static.yml` is manual-only and runs action pin validation, actionlint `1.7.12`, text security scan, ShellCheck, Pyright `1.1.409`, and Semgrep CLI without requiring paid GitHub Code Security.
- `.github/workflows/dependency-check.yml` is manual-only and keeps MCP/runtime freshness available without scheduled spend.
- `.github/workflows/release.yml` manually publishes exact SemVer tags without a `v` prefix, bootstraps `fullrepo` agent context before requiring agent docs, runs `validate_agent_tools.py` through `uv --with pyyaml`, extracts versioned release notes with a portable AWK expression, and produces deterministic `tar.gz` bundles, release manifests, generated SPDX SBOMs, GitHub dependency graph SBOM export via `/dependency-graph/sbom`, artifact attestations, and GitHub Releases.
- `scripts/classify_ci_noise.py` keeps known benign third-party stderr documented while failing targeted strict jobs on unknown lines.
- `config/skill-routing-policy.json` version 2 assigns routing classes to all 38 skills and requires cases for implicit, explicit-only, and finalization skills.
- Text security scan covers tracked text plus agent-only instruction/memory/research paths and rejects secret-like values, BIDI controls, and zero-width controls. When `.git` is absent, it falls back to a bounded text-extension tree walk so extracted release bundles and temporary audit copies are not under-scanned.
- `config/skill-routing-policy.json` supports `not_expected` assertions for conflict checks; broad review prompts must not route directly to orchestrated reviewer-only micro-skills.
- Full explicit GitHub CI/CD for commit `037397e685b6e347b56c061c7d2d03fc3e208da6` passed on 2026-05-17 UTC: `validate.yml` run `25998372448` with full scope and macOS parity, `security-static.yml` run `25998372535`, `dependency-check.yml` run `25998372436`, and `release.yml` run `25998372557`.
- Release `0.3.2` is published from commit `037397e` (`VERSION=0.3.2`) through manual release run `25998372557`. The GitHub Release tag is `0.3.2`, published at `2026-05-17T17:56:07Z`, with `release-manifest.json`, `release-notes.md`, `rldyour-codex-0.3.2.tar.gz`, `sbom.spdx.json`, and `SHA256SUMS` assets. The release keeps changelog coverage in `CHANGELOG.md`, deterministic release manifest/SBOM validation, manual-only CI workflows, strict runtime prerequisite gates, ordered lifecycle hook behavior, managed execpolicy rules, bounded hook smoke, CODEX_HOME-aware flow state, clean-runner MCP safe-call stderr classification, and temporary managed-subagent MCP startup isolation.
- Local validation for `66070a8` / version `0.3.3` passed on 2026-05-18: `scripts/validate_fast.sh` (68 tests, 75.83% coverage, 260-file text security scan), `scripts/validate_runtime.sh --strict-runtime`, `scripts/validate_release.sh`, `scripts/validate_marketplace.sh`, `scripts/install_system_codex.sh --apply --strict-runtime`, `scripts/doctor_system_codex.sh --quick --strict-runtime`, `python3 scripts/validate_instruction_docs.py --require-agent-docs`, and release manifest/SBOM generation.
- The `66070a8` runtime startup smoke launched `codex --no-alt-screen` after installing fixed agents and confirmed the previous `Ignoring malformed agent role definition ... invalid transport` warnings were absent.
- Local validation for `cdad168` / version `0.3.4` passed on 2026-05-18: `scripts/validate_fast.sh` (69 tests, 75.69% coverage, 260-file text security scan), `scripts/validate_runtime.sh --strict-runtime`, `scripts/validate_release.sh`, `scripts/validate_execpolicy_rules.sh`, `scripts/validate_marketplace.sh`, `scripts/install_system_codex.sh --apply --strict-runtime`, `scripts/doctor_system_codex.sh --quick --strict-runtime`, `python3 scripts/validate_instruction_docs.py --require-agent-docs`, `git diff --check`, release manifest/SBOM JSON generation, and direct `session_start_dispatcher.sh` timing at about `0.11s`.
- `tests/unit/test_fullrepo_sync.py` configures git identity for temporary repositories and clones before fixture commits, which keeps the unit-test matrix deterministic on GitHub-hosted runners.
- `tests/unit/test_fullrepo_sync.py` covers `git commit-tree` fallback author/committer identity, and `tests/unit/test_flow_post_task_state.py` covers CODEX_HOME installed helper lookup and bootstrap-only `.serena` no-sync behavior.
- `scripts/classify_ci_noise.py` allowlists `uv` package download progress lines such as `Downloading pygments (...)` and `Downloaded pygments` as deterministic setup noise.
- `scripts/validate_marketplace.sh` skips only the live Serena freshness state check in GitHub Actions when fullrepo-managed `.serena/memories/CORE-01-INDEX.md` is not tracked in the normal-branch checkout.
- `scripts/smoke_serena_memory_taxonomy.sh` keeps analyzer and fixture coverage when repository memories are absent or untracked in GitHub Actions, and runs index/taxonomy parity when `CORE-01-INDEX.md` is present as tracked fullrepo context.
- Validation contracts still include pinned runtime checks and smoke coverage defined in manual `dependency-check.yml` and `validate.yml`.

## Contracts And Data

- `scripts/validate_marketplace.sh` must include JSON validation, manifest validation, GitHub Action SHA pin validation, strict runtime prerequisite validation, managed-agent config parity, Codex agent surface validation, shellcheck, Python syntax, pytest/coverage, skill routing, hook feature migration smoke, hook smoke, memory freshness/taxonomy smoke, fullrepo smoke, local git guard smoke, branch cleanup smoke, text security scan, and release manifest checks.
- `scripts/validate_marketplace.sh` should include Codex execpolicy rule validation when Codex CLI is present; `scripts/validate_runtime.sh --strict-runtime` must validate installed rules.
- `scripts/validate_agent_tools.py` requires PyYAML and is normally run through `uv run --with pyyaml`; it is the source-tree gate for managed-agent model/reasoning settings, temporary subagent MCP isolation, and complete disabled MCP transport overrides.
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
- MCP runtime pin checks must stay synchronized across manual `validate.yml` and `dependency-check.yml`; neither should run on push/schedule unless the owner explicitly changes the spend policy.
- In docs, this contract must be described consistently in `docs/dependency-updates.md`, `docs/observability.md`, and `README.md` whenever validate/dependency-check behavior changes.

## Verification

- `scripts/validate_marketplace.sh`: full repository validation.
- `scripts/validate_fast.sh`: fast static/unit validation slice.
- `scripts/validate_runtime.sh --strict-runtime`: strict runtime/install/hook/fullrepo validation slice.
- `scripts/validate_release.sh`: release manifest/SBOM validation slice.
- `scripts/doctor_system_codex.sh`: installed runtime validation after cache/config install.
- App-server RPC method `hooks/list` over `codex app-server --listen stdio://`: live hook trust/hash verification used by installer and doctor.
- `python3 scripts/release_manifest.py`: generated manifest includes expected plugin versions.
- `python3 scripts/release_sbom.py`: generated SPDX 2.3 SBOM includes root package, plugins, and MCP runtime pins.
- `git diff --check`: whitespace sanity before commit.
