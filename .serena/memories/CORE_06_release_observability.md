<!-- Memory Metadata
Last updated: 2026-05-04
Last commit: 6e0e1b9 docs(system): clarify fullrepo sync order
Scope: VERSION, CHANGELOG.md, docs/release-process.md, docs/rollback-restore.md, docs/dependency-updates.md, docs/observability.md, config/skill-routing-policy.json, scripts/validate_plugin_versions.py, scripts/validate_skill_routing.py, scripts/release_manifest.py, scripts/check_mcp_runtime_versions.py, scripts/collect_diagnostics.sh, scripts/rollback_system_codex.sh, scripts/smoke_fullrepo_sync.sh, scripts/sync_fullrepo_branch.sh, plugins/rldyour-flow/scripts/fullrepo_sync.py, .github/workflows/validate.yml, .github/workflows/dependency-check.yml, .github/dependabot.yml, .gitignore, AGENTS.md, README.md, system/AGENTS.md, plugins/rldyour-serena-mcp/scripts/serena_memory_state.py
Area: CORE
-->

# CORE_06_release_observability

## Purpose

This area owns formal operational wrappers around the rldyour Codex runtime. It does not change the active MCP server set or YOLO permission model. It covers versioning, release evidence, rollback/restore, dependency freshness checks, routing policy tests, CI matrix coverage, diagnostics, and the generated `fullrepo` branch used for complete agent-only context.

## Source Of Truth

- `VERSION`: marketplace release version. Current value is `0.1.0`.
- `CHANGELOG.md`: human-readable release history with `[Unreleased]` and `[0.1.0] - 2026-05-03` sections.
- `docs/release-process.md`: release/versioning process, checklist, tag flow, release manifest usage, and MCP pin update flow.
- `docs/rollback-restore.md`: backup listing, dry-run restore, apply restore, released-state restore, and pre-rollback diagnostics.
- `docs/dependency-updates.md`: pinned MCP runtime update policy and local/CI check commands.
- `docs/observability.md`: diagnostics, GitHub Actions summaries/artifacts, failure triage order, fullrepo status checks, and logging rules.
- `config/skill-routing-policy.json`: deterministic Russian/English prompt-to-skill routing policy fixture.
- `scripts/validate_plugin_versions.py`: validates SemVer release metadata, release documents, marketplace entries, plugin manifest versions, and meaningful descriptions.
- `scripts/validate_skill_routing.py`: validates prompt terms, expected skill names, and expected skill description trigger terms.
- `scripts/release_manifest.py`: prints a JSON release snapshot with repository version/SHA/branch/dirty state, marketplace entries, plugin manifest versions, MCP runtime pins, and MCP server specs.
- `scripts/check_mcp_runtime_versions.py`: checks pinned runtime versions against npm and PyPI latest versions.
- `scripts/collect_diagnostics.sh`: writes sanitized diagnostics under ignored `diagnostics/`.
- `scripts/rollback_system_codex.sh`: lists and restores installer-created backups for `AGENTS.md` and `config.toml`.
- `scripts/smoke_fullrepo_sync.sh`: validates fullrepo branch publish, migration, restore, and exclude rules.
- `scripts/sync_fullrepo_branch.sh`: operational wrapper for fullrepo status, restore, publish, and migration.
- `plugins/rldyour-flow/scripts/fullrepo_sync.py`: fullrepo state and sync implementation.
- `.github/workflows/validate.yml`: Ubuntu/macOS validation matrix with success summary and failure diagnostic artifacts.
- `.github/workflows/dependency-check.yml`: weekly/manual MCP runtime pin freshness workflow.
- `.github/dependabot.yml`: weekly GitHub Actions update checks.

## Entry Points

- `python3 scripts/validate_plugin_versions.py`: validate release metadata, plugin manifest versions, and release document presence.
- `python3 scripts/validate_skill_routing.py`: validate deterministic Russian and English routing policy cases.
- `python3 scripts/release_manifest.py`: print a machine-readable release snapshot.
- `python3 scripts/check_mcp_runtime_versions.py --fail-on-outdated`: fail when pinned Codex/MCP runtime packages are stale.
- `scripts/collect_diagnostics.sh [--include-doctor]`: collect sanitized local diagnostics under ignored `diagnostics/`.
- `scripts/rollback_system_codex.sh --list`: list installer backups.
- `scripts/rollback_system_codex.sh --restore <backup> --dry-run`: preview restore of backed up system Codex files.
- `scripts/smoke_fullrepo_sync.sh`: validate fullrepo branch behavior in an isolated temporary repository.
- `scripts/sync_fullrepo_branch.sh --status`: inspect local and remote fullrepo state.
- `scripts/sync_fullrepo_branch.sh --restore`: restore agent-only context from `origin/fullrepo`.
- `scripts/sync_fullrepo_branch.sh --publish`: publish the complete agent-only context snapshot to `fullrepo`.
- `gh workflow run dependency-check.yml --repo rldyourmnd/rldyour-codex --ref main`: manually run runtime pin freshness checks on GitHub Actions.

## Current Behavior

`scripts/validate_marketplace.sh` now includes:

- `Release metadata`: runs `python3 scripts/validate_plugin_versions.py` and generates a release manifest.
- `Skill routing policy`: runs `python3 scripts/validate_skill_routing.py`.
- Python syntax checks for `validate_plugin_versions.py`, `validate_skill_routing.py`, `release_manifest.py`, `check_mcp_runtime_versions.py`, and `plugins/rldyour-flow/scripts/fullrepo_sync.py`.
- Fullrepo sync smoke through `scripts/smoke_fullrepo_sync.sh`.

`python3 scripts/check_mcp_runtime_versions.py --fail-on-outdated` passed after commit `5d0a389`; every pin in `config/mcp-runtime-versions.env` matched upstream latest at check time:

- `@openai/codex`: `0.128.0`.
- `mcp`: `1.27.0`.
- `serena-agent`: `1.2.0`.
- `semgrep`: `1.161.0`.
- `@modelcontextprotocol/server-sequential-thinking`: `2025.12.18`.
- `@playwright/mcp`: `0.0.73`.
- `chrome-devtools-mcp`: `0.23.0`.
- `@upstash/context7-mcp`: `2.2.3`.
- `shadcn`: `4.6.0`.

`scripts/collect_diagnostics.sh --output diagnostics/local-test` completed and wrote a local diagnostics bundle. `diagnostics/` is ignored by Git.

`scripts/rollback_system_codex.sh --list` lists installer backup timestamps under `/Users/rldyourmnd/.codex/backups/rldyour-codex`. `scripts/rollback_system_codex.sh --restore <backup> --dry-run` prints the exact `AGENTS.md` and `config.toml` restore paths without writing.

`scripts/install_system_codex.sh --apply` was run after adding the new system AGENTS commands. It backed up the previous `/Users/rldyourmnd/.codex/AGENTS.md` and `/Users/rldyourmnd/.codex/config.toml`, installed the updated global instructions, patched config, and synced plugin cache.

`scripts/doctor_system_codex.sh` passed after install with zero warnings and zero failures.

`scripts/smoke_clean_bootstrap.sh` passed after commit `5d0a389`. The clean-bootstrap run installed into a temporary `CODEX_HOME`, used a temporary `SERENA_HOME`, passed doctor, validated plugin cache and hooks, and verified all twelve MCP registrations.

Commit `d12a51f fix(serena): clarify knowledge-only memory sync state` made diagnostics more internally consistent by adding explicit Serena memory state fields: `memory_directly_mentions_head`, semantic `memory_matches_head`, and `memory_match_reason`. Knowledge-only commits now report `memory_matches_head: true` with reason `knowledge-only-commits-since-sync`, instead of looking stale while still being current.

Commit `614b71e chore(serena): document memory state semantics` documented the new Serena memory-state semantics in `.serena/memories/CORE_06_release_observability.md` and `.serena/memories/MCP_02_serena_workflow_hooks.md`. After that commit, local verification confirmed `scripts/doctor_system_codex.sh`, `scripts/smoke_clean_bootstrap.sh`, LSP health, and runtime pin freshness checks. GitHub Actions `validate` passed on Ubuntu and macOS, and the manual `dependency-check` workflow passed on `main`.

Commit `018cc6e feat(flow): add fullrepo agent context sync` added `plugins/rldyour-flow/scripts/fullrepo_sync.py`, `scripts/sync_fullrepo_branch.sh`, and `scripts/smoke_fullrepo_sync.sh`. It also updated `scripts/release_manifest.py` to include `fullrepo_sha`, `scripts/collect_diagnostics.sh` to collect `fullrepo-state.json`, `scripts/doctor_system_codex.sh` to report fullrepo state, `scripts/validate_marketplace.sh` to run fullrepo smoke, and docs to include fullrepo release, rollback, and observability procedures.

Commit `6abd7b8 fix(serena): classify agent files as knowledge paths` updated `serena_memory_state.py` so fullrepo migration commits that remove agent-only files from `main` do not falsely count as product-code drift.

Commit `6e0e1b9 docs(system): clarify fullrepo sync order` updated `system/AGENTS.md` and `CHANGELOG.md` so the global instruction layer states the fullrepo-managed initialization and finish sequence directly. Root `AGENTS.md` mirrors the finish-order statement as agent-only project context for the `fullrepo` snapshot.

## CI Model

`.github/workflows/validate.yml` now uses a matrix with:

- `ubuntu-latest`.
- `macos-latest`.

The workflow keeps `CODEX_HOME=/tmp/rldyour-codex-home`, list-only MCP capability probes, missing-env tolerance for auth-dependent MCPs, and skipped LSP health for CI portability.

The validate workflow runs on pushes to `main` and `fullrepo`, pull requests to `main`, and manual dispatch. This makes both the normal branch and the complete agent-context branch visible to CI.

On success, the validate workflow writes OS/ref/SHA/check summary to `GITHUB_STEP_SUMMARY`. On failure, it runs `scripts/collect_diagnostics.sh --output diagnostics/ci` and uploads `diagnostics/ci` with `actions/upload-artifact@v7.0.1`.

`.github/workflows/dependency-check.yml` runs every Monday at `06:17` UTC and through `workflow_dispatch`. It runs the dependency freshness check with `--fail-on-outdated` so stale runtime pins become visible in CI.

`.github/dependabot.yml` monitors GitHub Actions weekly with `package-ecosystem: "github-actions"`, `directory: "/"`, and `open-pull-requests-limit: 5`.

## Contracts And Data

`VERSION` is the marketplace release version and is independent from individual plugin manifest versions. Plugin behavior versions live in each `plugins/<plugin>/.codex-plugin/plugin.json`.

`config/mcp-runtime-versions.env` is the pinned runtime version source used by local scripts, the installer, and CI. The repository should not use unpinned local MCP package specs or `@latest`.

Diagnostics output belongs under ignored `diagnostics/`. Release bundles or generated manifests belong under ignored `dist/` unless the owner explicitly wants to publish them.

GitHub Actions validation is the remote proof layer for committed state. Local `doctor` and `smoke_clean_bootstrap` prove the owner machine and clean-clone installation path; CI proves the same committed source on Ubuntu and macOS using temporary runtime state.

`fullrepo` is a generated branch for complete agent-only context. `main` remains the normal product branch. `scripts/sync_fullrepo_branch.sh --publish` is the supported update path because it refuses non-agent dirty files, scans agent-only files for secret-looking content, and pushes with `--force-with-lease`.

`scripts/release_manifest.py` includes `fullrepo_sha` in the repository section. `scripts/collect_diagnostics.sh` writes `fullrepo-state.json` so failures can be triaged without relying on chat history.

## Invariants

- Release and observability scripts must not mutate MCP runtime config unless an explicit install or restore command is run.
- `scripts/rollback_system_codex.sh` must remain read-only unless `--restore <backup>` is explicitly provided without `--dry-run`.
- `scripts/collect_diagnostics.sh` must not dump environment variables or secrets.
- Diagnostics, browser evidence, Serena runtime markers, caches, local env files, and credentials must not be included in `fullrepo`.
- `fullrepo` updates must use `--force-with-lease`, not blind `git push --force`.
- `diagnostics/` and `dist/` remain ignored.
- `VERSION` and plugin manifest versions must stay valid SemVer.
- `CHANGELOG.md` must keep `[Unreleased]` and human-readable release entries.
- Routing policy cases must target real skills and real description trigger terms.

## Change Rules

- Update `VERSION`, `CHANGELOG.md`, and affected plugin manifest versions before cutting a release.
- Run `python3 scripts/release_manifest.py` to capture release evidence.
- Run `scripts/validate_marketplace.sh`, `scripts/doctor_system_codex.sh`, `scripts/smoke_clean_bootstrap.sh`, and `scripts/sync_fullrepo_branch.sh --status` before release tagging.
- Run `scripts/sync_fullrepo_branch.sh --publish` after the normal branch is pushed when agent-only files changed and the complete setup snapshot should be portable.
- Run `python3 scripts/check_mcp_runtime_versions.py` before updating MCP runtime pins.
- Use `scripts/rollback_system_codex.sh --restore <backup> --dry-run` before any real restore.
- Use `scripts/sync_fullrepo_branch.sh --restore` to restore agent-only context from `origin/fullrepo` during rollback or new-machine initialization.
- Use `scripts/collect_diagnostics.sh --include-doctor` before rollback when the failed state needs evidence.

## Verification

- `python3 scripts/validate_plugin_versions.py`: validates release/versioning metadata.
- `python3 scripts/validate_skill_routing.py`: validates prompt routing policy.
- `python3 scripts/release_manifest.py | python3 -m json.tool`: validates release manifest JSON.
- `python3 scripts/check_mcp_runtime_versions.py --fail-on-outdated`: validates pinned package freshness.
- `scripts/collect_diagnostics.sh --output diagnostics/local-test`: validates diagnostics bundle creation.
- `scripts/rollback_system_codex.sh --list`: validates backup discovery.
- `scripts/rollback_system_codex.sh --restore <backup> --dry-run`: validates restore preview.
- `scripts/smoke_fullrepo_sync.sh`: validates fullrepo publish, migration, restore, and exclude behavior.
- `scripts/sync_fullrepo_branch.sh --status`: validates fullrepo status reporting.
- `scripts/validate_marketplace.sh`: validates the integrated release/routing checks with the rest of the repository.
- `scripts/doctor_system_codex.sh`: validates installed system state after `system/AGENTS.md` changes.
- `scripts/smoke_clean_bootstrap.sh`: validates committed clean-clone bootstrap behavior.
