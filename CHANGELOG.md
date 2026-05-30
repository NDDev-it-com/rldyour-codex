# Changelog

All notable changes to this project are documented in this file.

The format follows Keep a Changelog, and marketplace/plugin versions follow Semantic Versioning.

## [Unreleased]


## [1.1.10] - 2026-05-30

### Fixed

- Classify current MCP safe-call runtime noise.

## [1.1.9] - 2026-05-30

### Fixed

- Harden Russian-first routing metadata across Claude, Codex, and OpenCode.

## [1.1.7] - 2026-05-30

### Changed

- Make `ry-start` reviewer fanout explicit-opt-in while keeping `ry-review` reviewer orchestration available.

## [1.1.6] - 2026-05-30

### Fixed

- Fix Codex installer cleanup for managed MCP env forwarding.

## [1.1.5] - 2026-05-30

### Fixed

- Harden Codex MCP env forwarding, managed-agent routing metadata, and validation diagnostics.

## [1.1.4] - 2026-05-30

### Fixed

- Harden Codex skill metadata validation and marketplace routing.

## [1.1.3] - 2026-05-29

### Changed

- Make all Codex skill descriptions Russian-first while retaining English trigger suffixes.

## [1.1.2] - 2026-05-29

### Fixed

- Localize Codex OpenAI skill metadata and remove stale OpenCode inventory wording.

## [1.1.1] - 2026-05-29

### Changed

- Complete Codex 0.135.0 surface adoption notes.

## [1.1.0] - 2026-05-29

### Changed

- Adopt Codex CLI 0.135.0 runtime baseline.
- Refresh GitHub MCP Server host-binary pin to 1.1.0.

## [1.0.3] - 2026-05-29

### Changed

- Standardize release automation and repository descriptions.

## [1.0.2] - 2026-05-28

### Fixed

- Release nested legacy profile-table migration cleanup.
- System Codex migration now removes nested legacy profile tables such as
  `[profiles.rldyour-yolo.features]` from `config.toml` instead of leaving them
  behind for doctor/runtime validation to reject.

## [1.0.1] - 2026-05-28

### Changed

- Synchronize internal plugin and index versions with the adapter release.

## [1.0.0] - 2026-05-28

### Changed

- Shared MCP runtime pins now track `semgrep==1.164.0` and `shadcn@4.8.2`;
  managed Codex subagent TOML files and fixture tests were updated in lockstep.

## [0.5.0] - 2026-05-27

### Changed

- Codex CLI runtime baseline now targets `0.134.0`; system install and doctor
  checks use current profile files (`$CODEX_HOME/rldyour-yolo.config.toml` and
  `$CODEX_HOME/rldyour-safe.config.toml`) instead of removed legacy
  `profile = "..."` selectors and `[profiles.*]` tables.
- System install and doctor now remove the obsolete `features.plugin_hooks`
  flag because Codex 0.134 reports plugin hooks as default-enabled; hook
  correctness is verified through trusted `hooks/list` output.
- Context7 MCP now pins `@upstash/context7-mcp@3.0.0`, matching the current
  npm stable package in `.mcp.json` and `config/mcp-runtime-versions.env`.
- Shared MCP runtime pins now match current upstream stable packages:
  `serena-agent==1.5.3`, `chrome-devtools-mcp@1.1.1`, and `shadcn@4.8.1`.
- Runtime validation now exposes explicit `auto`, `static`, `installed`, and
  `live` lanes so source-only CI, installed local checks, and network freshness
  checks are classified instead of inferred from host state.

### Fixed

- System Codex migration now preserves manually repaired profile-file content
  while moving shared plugins, MCP, hooks, and agent configuration back into the
  base `config.toml`.
- Codex `hooks/list` smoke now accepts both versioned and `local` installed
  plugin cache hook source paths, matching the current local marketplace install
  layout used by system Codex.
- Dart/Flutter MCP capability smoke now requires the stable tools exposed by
  Dart SDK `3.12.0`; `run_tests` is no longer treated as globally available in
  non-Dart repository checkouts.
- Public fast validation now tolerates normal source checkouts without restored
  agent-only docs while preserving strict checks when fullrepo context is
  available.
- CI noise classification now treats retried MCP TaskGroup startup failures as
  benign only after the capability smoke itself reaches a passing result.

## [0.4.9] - 2026-05-22

### Changed

- Product release tags remain numeric-only (`X.Y.Z`) and the release workflow
  now rejects prerelease tag forms for this owner-standard configuration pack.
- `rldyour-flow` `ry-start` now routes explicit deploy/server rollout intent
  into `ry-deploy` after implementation validation and sync.
- `rldyour-flow` `ry-review` now defines time-window, PR, issue, branch, and
  last-deploy target parsing before reviewer dispatch.
- `rldyour-flow` `ry-newp` now explicitly seeds `CONTEXT-01-CORE.md` and
  `FUTURE-01-VISION.md` after approved scaffold commits.

## [0.4.8] - 2026-05-22

### Changed

- Flow and design skills now explicitly reference the root policy vocabulary for
  current-code research, deploy preflight/postflight verification, and
  accessibility validation, keeping Codex skill routing aligned with the
  control-plane policy validators.

## [0.4.7] - 2026-05-21

### Fixed

- Codex runtime baseline metadata and test fixtures now match the `0.133.0`
  runtime pin, keeping root `validate_runtime_baselines.py` aligned with the
  adapter release.

## [0.4.6] - 2026-05-21

### Changed

- Runtime Codex CLI pin updated from `0.132.0` to `0.133.0`, the current
  stable npm release observed by the CI dependency freshness gate on
  2026-05-21.

## [0.4.5] - 2026-05-21

### Changed

- `rldyour-mcps` now pins `shadcn@4.8.0`, the current stable shadcn MCP CLI
  package on 2026-05-21. The managed subagent specialist MCP overrides and
  `config/mcp-runtime-versions.env` were updated in the same release.

### Fixed

- `scripts/smoke_mcp_capabilities.py --mode static --json` is now a true
  parse-only path: it reads only the repository MCP manifest and no longer
  imports the Python MCP SDK or requires an installed `CODEX_HOME`.

## [0.4.4] - 2026-05-21

### Fixed

- Strict CI runtime-noise classification now treats the bounded official
  `github-mcp-server` `1.0.5` lifecycle stderr lines as known benign startup
  output after the deterministic MCP capability smoke already passed.

## [0.4.3] - 2026-05-21

### Changed

- GitHub Actions runtime setup now installs the pinned official GitHub MCP
  server `1.0.5` from the upstream release artifact with SHA-256 checksum
  verification before strict Codex runtime validation runs.
- Context7 MCP is updated from `2.2.5` to the current stable `2.3.0` in both
  `.mcp.json` and `config/mcp-runtime-versions.env`.
- MCP runtime freshness now tracks `GITHUB_MCP_SERVER_VERSION` through the
  GitHub releases API alongside npm and PyPI-backed runtime pins.

### Fixed

- `scripts/validate_contract.py` now narrows JSON-derived values before sorting
  or passing them to typed helpers, keeping Pyright strict checks green under
  the public `security-static` workflow.
- Public Codex CI no longer fails strict runtime prerequisite checks because the
  `github` MCP server launcher is absent on hosted Ubuntu/macOS runners.

## [0.4.2] - 2026-05-21

### Added

- `config/rldyour-contract.json`, `docs/contract-matrix.md`, and `scripts/validate_contract.py` now define and validate the Codex adapter surface: plugins, skills, absent slash commands, managed subagents, hook lifecycle mappings, MCP servers, versioned plugin cache, and the owner-standard full-auto profile.
- `scripts/plugin_cache_contract.py` centralizes installed plugin cache discovery and parity checks from plugin manifest versions.
- `scripts/smoke_codex_hook_listing.py` proves live Codex `app-server` `hooks/list` output includes all rldyour bundled plugin hooks as trusted, enabled, and sourced from versioned cache paths.

### Changed

- Repository release advanced to `0.4.2` after merging the runtime-contract
  branch to `main`. Local release evidence: `scripts/validate_fast.sh` passed
  with 80 tests and 76.65% coverage, then `scripts/validate_release.sh`
  passed on 2026-05-21.
- Runtime pins updated to current stable upstream versions: Codex CLI `0.132.0`, Serena Agent `1.5.1`, and Chrome DevTools MCP `1.0.1`.
- Plugin manifests now carry canonical authorship for Danil Silantyev
  (`github:rldyourmnd`), CEO NDDev, and validators enforce that
  author/developer attribution together with AGPL-3.0-or-later licensing.
- Generated `fullrepo` commits now default to Danil Silantyev
  (`rldyourmnd@users.noreply.github.com`) as author and committer when no Git
  identity is already provided by the environment.
- System Codex docs now clarify that the owner-selected `sandbox_mode = "danger-full-access"` remains the active runtime policy while `plugin_hooks` stays an explicit official Codex opt-in.
- Serena MCP capability smoke now uses the deterministic `list_memories` safe call for Serena Agent `1.5.1` to avoid classifying variable configuration output as CI noise.
- Installer, doctor, marketplace validation, hook smoke, local Git hook fallback, fullrepo fallback, and Flow post-task state now use the Codex versioned plugin cache layout `${CODEX_HOME}/plugins/cache/rldyour-codex/<plugin>/<version>` while retaining legacy `local` fallback where needed.
- Plugin manifests now align with the repository public license and canonical URL: `AGPL-3.0-or-later` and `https://github.com/NDDev-it-com/rldyour-codex`.
- Marketplace validation batches skill frontmatter parsing in one Python process and release validation now includes the Codex adapter contract gate.
- Runtime validation now includes live Codex `hooks/list` trust smoke after installing into a temporary `CODEX_HOME`.
- System installer and doctor now default to the owner-standard full-auto
  profile (`rldyour-yolo`, `danger-full-access`, `never`,
  `:danger-full-access`) and keep `--safe-mode` as an explicit conservative
  override.

### Security

- The Codex adapter contract records YOLO/full-auto/dangerously-skip-permissions
  as the standard owner posture and validates that safe mode is only an
  explicit override.

### Fixed

- `rldyour-flow` Stop state no longer loops on local-only `fullrepo` sync when
  the repository has no configured remote and the local `fullrepo` snapshot
  already matches the worktree agent context.

## [0.4.1] - 2026-05-19

### Added

- `.github/workflows/scorecard.yml`: OpenSSF Scorecard analysis on weekly schedule, on push to `main`, on branch protection rule changes, and on `workflow_dispatch`. Uploads SARIF to the GitHub Security tab and publishes results to `scorecard.dev`. Pinned `ossf/scorecard-action@4eaacf0543bb3f2c246792bd56e8cdeffafb205a # v2.4.3`.
- `.github/workflows/dependency-review.yml`: blocks pull requests that introduce dependencies with high-severity vulnerabilities or licenses outside the AGPL-3.0-or-later compatible allow-list. Pinned `actions/dependency-review-action@a1d282b36b6f3519aa1f3fc636f609c47dddb294 # v5.0.0`.
- `.github/workflows/labeler.yml` and `.github/labeler.yml`: PR auto-labeling by changed paths for ci-cd / scripts / plugin / docs / tests / serena-memories / release / security / system areas. Pinned `actions/labeler@f27b608878404679385c85cfa523b85ccb86e213 # v6.1.0`.
- README badge for OpenSSF Scorecard.
- Public-repo settings applied via GitHub API: repository visibility public, `admin:org`-level branch protection on `main` with 9 required status checks, repository tag ruleset blocking deletion/update/non-fast-forward push of SemVer release tags (admin bypass), repository description, homepage, topics, merge policy (squash + rebase, no merge commits, delete branch on merge, allow update branch), Dependabot vulnerability alerts, and Dependabot automated security updates.

### Changed

- `validate.yml` MCP runtime pin freshness job now runs without `--fail-on-outdated` so a stale pin produces an advisory step summary instead of blocking pull request merges. The `dependency-check.yml` workflow continues to fail on stale pins, providing a maintainer-visible signal without coupling it to the pull request gate.
- `README.md`, `CONTRIBUTING.md`, and `SECURITY.md` describe the OpenSSF Scorecard, Dependency Review, Labeler, gitleaks history scan, branch protection state, and tag ruleset.

### Security

- Full git history scanned with `gitleaks` 8.30.1 prior to the public visibility switch: 190 commits, 0 leaks found.
- GitHub branch protection on `main` enforces strict required status checks (9 jobs), linear history, no force pushes, no deletions, and requires conversation resolution. Maintainer keeps admin access (`enforce_admins: false`).
- GitHub tag ruleset protects `[0-9]*.[0-9]*.[0-9]*` and `[0-9]*.[0-9]*.[0-9]*-*` tags from deletion, update, and non-fast-forward push.

## [0.4.0] - 2026-05-19

### Added

- Public open-source release under the GNU Affero General Public License v3.0 or later. `LICENSE` now contains the canonical AGPL-3.0 text verbatim, sourced from the Free Software Foundation.
- `CODE_OF_CONDUCT.md` referencing Contributor Covenant 2.1 with a private reporting channel through GitHub Security Advisories.
- `.github/workflows/codeql.yml` running GitHub CodeQL with the `security-and-quality` query suite for Python and GitHub Actions on every push to `main`, every pull request, and on a weekly schedule.
- Maintainer attribution to Danil Silantyev (`github:rldyourmnd`), CEO NDDev, in `README.md`.
- `pyproject.toml` now declares SPDX license identifier `AGPL-3.0-or-later`, project authors, project URLs, classifiers, and keywords for public packaging metadata.

### Changed

- License switched from MIT to GNU AGPL-3.0-or-later. Downstream operators that run modified versions over a network must comply with AGPL-3.0 Section 13.
- `.github/workflows/validate.yml` now triggers automatically on push to `main` and on pull requests targeting `main` for fast, runtime, release, MCP, and dry-run jobs, with macOS parity included by default for push and pull-request events. `workflow_dispatch` remains available for narrower scopes and macOS opt-out.
- `.github/workflows/security-static.yml` now triggers automatically on push to `main`, on pull requests, and on a weekly schedule, in addition to the existing `workflow_dispatch` fallback.
- `.github/workflows/dependency-check.yml` now runs on a daily schedule, on push to MCP runtime pin sources (`config/mcp-runtime-versions.env`, `plugins/rldyour-mcps/.mcp.json`, `scripts/check_mcp_runtime_versions.py`, the workflow file itself), and through `workflow_dispatch`.
- `.github/workflows/release.yml` now triggers automatically on push of SemVer tags matching `X.Y.Z` or `X.Y.Z-pre`. The version validation step accepts both the tag ref and the manual `workflow_dispatch` input, enforces a SemVer pattern, and requires `VERSION` and `CHANGELOG.md` to match.
- `.github/branch-protection/main.json` now lists auto-running CI job names as desired required status checks for the public `main` branch, with strict_required_status_checks enabled and a maintainer-administrative note.
- `README.md`, `CONTRIBUTING.md`, and `SECURITY.md` rewritten for a public open-source audience with AGPL-3.0 messaging, badge row, automated CI description, private vulnerability disclosure flow, supported version policy, and explicit out-of-scope statements.
- Repository version updated to `0.4.0`. No plugin behavior versions changed; this release covers licensing, OSS posture, and CI automation only.

### Security

- GitHub CodeQL added as a continuous static analysis layer at no extra cost for the public repository, complementing existing Semgrep CLI, Pyright, ShellCheck, action pin validation, and `scripts/scan_text_security.py`.

## [0.3.5] - 2026-05-18

### Added

- Flow PreToolUse now includes a cwd guard that blocks Bash commands which would rename or remove the active Codex session directory or repository root.
- Hook smoke now includes large-stdin drain regressions for PreToolUse, PostToolUse, and Stop hooks, Stop offline/no-network regression coverage, and cwd-rename guard coverage.
- Unit tests now cover `fullrepo_sync.py --status-json --local-only` without fetch or remote inspection.

### Changed

- Stop lifecycle dispatcher now runs Serena and Flow children with internal process-group timeouts and actionable continuation messages instead of relying only on Codex's outer hook timeout.
- Flow Stop state now uses local-only fullrepo status in the hook hot path, avoiding `git fetch` and `git ls-remote` during Stop checks.
- Flow state script resolution now prefers sibling scripts next to the running plugin file before project-local or `${CODEX_HOME}` fallbacks, preventing stale installed-cache helpers from reintroducing old network behavior.
- Repository version updated to `0.3.5`.
- `rldyour-flow` plugin version updated to `0.3.3` for stdin-safe lifecycle hooks, local-only Stop state, and active-cwd rename protection.

### Fixed

- Flow and Serena lifecycle hooks now drain hook stdin before early exits, preventing Codex `Broken pipe` failures when `PostToolUse` or `PreToolUse` payloads include large tool responses.

## [0.3.4] - 2026-05-18

### Added

- Hook smoke now includes a fake-network regression case proving Flow `SessionStart` does not call `git fetch` or `git ls-remote` during startup.
- `fullrepo_sync.py` now provides `--restore-local`, a local-only restore mode for existing `origin/fullrepo` tracking refs.

### Changed

- Flow `SessionStart` is now fast and offline: worktree bootstrap uses local fullrepo refs only, and context generation no longer calls deep Serena/fullrepo/Flow state analyzers in the startup hook.
- `rldyour-flow` plugin version updated to `0.3.2` for offline SessionStart behavior and local-only bootstrap restore.

## [0.3.3] - 2026-05-18

### Changed

- Managed Codex subagent TOML files now include complete disabled MCP transport metadata for temporarily disabled specialist MCP servers, preventing Codex from ignoring custom agents with `invalid transport` warnings at CLI startup.
- `codex_apps` stays available as an inherited built-in Apps/connectors surface and is no longer allowed as a synthetic `[mcp_servers.codex_apps]` custom-agent transport table.
- `validate_agent_tools.py` and `doctor_system_codex.sh` now reject partial disabled MCP overrides and transport drift against `plugins/rldyour-mcps/.mcp.json`.

## [0.3.2] - 2026-05-18

### Changed

- Managed Codex subagents now carry a temporary per-agent MCP isolation policy: spawned subagents inherit only the lightweight core MCP surface (`sequential-thinking`, `serena`, `context7`, `grep`, `deepwiki`, `openaiDeveloperDocs`, and built-in `codex_apps`) while specialist MCP servers remain available to the parent session for explicit browser, design, security, Flutter, and shadcn work.
- `browser-tester` and `security-audit` instructions now account for the temporary policy by asking the parent session to run browser tooling or Semgrep when those specialist MCP tools are unavailable inside the subagent.
- `validate_agent_tools.py` and `doctor_system_codex.sh` now verify managed-agent temporary MCP policy from the current `.mcp.json` server registry so newly added non-core MCP servers must be explicitly disabled for subagents.

## [0.3.1] - 2026-05-17

### Added

- Managed Codex execpolicy rules under `system/rules/*.rules`, installer sync to `${CODEX_HOME:-$HOME/.codex}/rules`, doctor parity checks, and `scripts/validate_execpolicy_rules.sh`.

### Changed

- Flow SessionStart dispatcher now kills timed-out child process groups instead of only the direct child process.
- Hook smoke now runs each hook through a bounded process-group timeout runner and reports the exact hook label on timeout.
- `flow_post_task_state.py` resolves installed plugin helper scripts through `CODEX_HOME` before falling back to the default `~/.codex` location.
- `smoke_clean_bootstrap.sh` configures temporary git identity, and its live `codex mcp list` probe is optional unless `--require-codex` is passed.
- `fullrepo_sync.py` supplies deterministic git author/committer fallback identity for `git commit-tree` publish operations.
- Branch-protection desired state now matches the repository's manual-only CI policy and current workflow job names.
- `.serena/project.yml` is no longer ignored in this repository because it is a source-of-truth Serena project config.
- `rldyour-flow` plugin version updated to `0.3.1` for SessionStart timeout cleanup, `CODEX_HOME` helper resolution, and fullrepo identity fallback.

### Security

- Owner-controlled YOLO mode now has validated execpolicy rails for root deletion, direct forced pushes, private-key disclosure commands, and release/deploy side effects.

## [0.3.0] - 2026-05-17

### Added

- Ordered Flow Stop lifecycle dispatcher that runs Serena memory gating before Flow post-task synchronization, eliminating cross-plugin Stop hook races.
- Strict runtime prerequisite validation through `scripts/validate_runtime_prereqs.py`, `scripts/install_system_codex.sh --strict-runtime`, and `scripts/doctor_system_codex.sh --strict-runtime`.
- Modular local validation gates: `scripts/validate_fast.sh`, `scripts/validate_runtime.sh`, and `scripts/validate_release.sh`.
- No-git fallback scanning in `scripts/scan_text_security.py` so extracted release bundles and disposable source directories receive broad text security coverage.
- Explicit Node major, Bun, and Dart SDK runtime pins in `config/mcp-runtime-versions.env`, with CI/devcontainer setup reading the shared pin source.
- Dedicated test helper module under `tests/support/` so `pytest` and `python -m pytest` collect tests consistently.

### Changed

- GitHub validation, dependency-check, and no-paid security workflows are now manual-only through `workflow_dispatch`; macOS validation is opt-in to preserve quality coverage without spending macOS minutes by default.
- Flow SessionStart dispatch now has per-child timeouts and output caps so Codex receives bounded degraded context instead of a long-running hook failure.
- Release workflow now exports GitHub dependency graph SBOM data through the synchronous SBOM endpoint and validates that any exported artifact is SPDX JSON.
- Release bundles now retain governance artifacts such as `CONTRIBUTING.md`, `SECURITY.md`, and `.devcontainer/`.
- Fast validation now checks both pytest entrypoints and bootstraps fullrepo agent context in manual GitHub validation before requiring agent instruction docs.
- MCP safe-call validation now bootstraps fullrepo agent context and classifies known first-run MCP/uv/Serena stderr, keeping strict CI noise checks deterministic on clean GitHub runners.
- Marketplace validation now parses the strict runtime prerequisite validator and runs the non-strict runtime prerequisite policy check.
- Skill routing policy now supports `not_expected` entries and documents that reviewer micro-skills must not be selected directly for broad `ry-review` prompts.
- MCP runtime freshness checks now include the pinned Bun launcher version.
- Repository pytest coverage threshold increased from 70% to 75% after adding strict runtime and runtime-pin tests.
- Updated the no-paid security workflow actionlint pin to `1.7.12`, Pyright pin to `1.1.409`, and aligned `actions/attest` SHA comments with tag `v4.1.0`.
- `rldyour-flow` plugin version updated to `0.3.0` for bounded SessionStart dispatch, ordered Stop lifecycle dispatch, and modular validation integration.
- `rldyour-serena-mcp` plugin version updated to `0.2.4` because Stop memory gating is now invoked by the ordered Flow lifecycle dispatcher instead of a competing plugin Stop hook.
- `rldyour-mcps` plugin version updated to `0.1.6` for shared host runtime pinning and strict prerequisite validation.

### Security

- Strict runtime mode fails enabled MCP server configurations when required launchers such as `uvx`, `bunx`, `dart`, or `codex` are unavailable.
- Manual CI scopes separate fast, runtime, release, and MCP checks so expensive macOS validation is deliberate rather than automatic.

## [0.2.0] - 2026-05-17

### Added

- `docs/adr/0001-codex-marketplace-operating-model.md` records the core plugin, hook, fullrepo, CI, MCP, and ADR operating decisions.
- ADRs for testing/CI gates, release SBOM and attestations, governance/branch policy, and runtime-noise classification.
- `pytest`/`pytest-cov` harness with JUnit and coverage XML artifacts, enforced at a 70% initial threshold.
- GitHub Actions full-SHA pin validation through `scripts/validate_action_pins.py`.
- Repository text security scan for secret-like patterns and hidden Unicode controls through `scripts/scan_text_security.py`.
- Runtime-noise classifier through `scripts/classify_ci_noise.py` for strict stderr checks without hiding known benign third-party chatter.
- Generated SPDX 2.3 release SBOM support through `scripts/release_sbom.py`.
- GitHub Actions release workflow for deterministic bundles, release manifests, generated SBOMs, optional GitHub dependency graph SBOM export, GitHub artifact attestations, and GitHub Releases.
- No-paid `security-static` workflow with action pin validation, actionlint, text security scan, ShellCheck, Pyright, and Semgrep CLI.
- Shared `.github/actions/setup-codex-runtime` composite action for CI runtime setup.
- Devcontainer for reproducible marketplace validation with Python, uv, Node/npm, Bun, Dart, shellcheck, jq, ripgrep, and pinned Codex CLI.
- Contributor governance files: `CONTRIBUTING.md`, `SECURITY.md`, CODEOWNERS, PR template, and issue templates.
- Desired-state branch protection specs for owner-accessible `main` and `fullrepo` workflows.

### Changed

- Flow Stop hook state now ignores bootstrap-only untracked `.serena` files created by tool startup, preventing empty or unborn repositories from being forced into `flow-post-task-sync` loops.
- `flow-post-task-sync` guidance now resolves rldyour-flow helper scripts from the installed plugin cache when a product repository does not vendor this plugin.
- Flow `SessionStart` hook wiring now uses a single dispatcher so fullrepo bootstrap and session context run in deterministic order under Codex hook concurrency semantics.
- Serena memory analyzer taxonomy now includes `DESIGN`, `LSP`, and `RULES`, with smoke coverage against `CORE-01-INDEX.md`.
- Installer config handling now fails closed on malformed existing `config.toml` instead of silently regenerating from an empty config model.
- Rollback restore now writes backed-up files through temporary files before renaming them into place.
- GitHub Actions workflows now pin external actions to full commit SHAs.
- `dart-flutter` MCP runtime is documented and validated as an explicit external local Dart SDK exception.
- Marketplace validation now runs action SHA-pin validation and Python unit coverage tests.
- Skill routing policy now has explicit routing classes for all 38 skills and requires deterministic cases for callable implicit/explicit/finalization skills.
- GitHub validation now splits unit-test reports from marketplace/system smoke while preserving the full local acceptance gate.
- Dependency freshness workflows now share the CI runtime setup action and keep retention limits on generated reports.
- Release workflow now bootstraps `fullrepo` agent context before requiring agent instruction docs in release validation.
- Release workflow now runs Codex agent-surface validation through the same `uv --with pyyaml` dependency contract as marketplace validation.
- Release workflow now extracts versioned release notes with a portable AWK expression during deterministic bundle generation.
- Python project metadata now pins the validation runtime to Python 3.13.x for local/CI parity.
- `rldyour-flow` plugin version updated to `0.2.6` for deterministic SessionStart dispatch and hook prologue hardening.
- `rldyour-serena-mcp` plugin version updated to `0.2.3` for expanded memory taxonomy coverage.

### Security

- External GitHub Actions are required to use full 40-character commit SHA pins, including nested composite action steps.
- Release bundles and generated SBOMs are attested with GitHub artifact attestations on GitHub Enterprise Cloud.
- Private-repo CodeQL/code scanning remains optional unless GitHub Code Security is available without extra paid add-ons; baseline security uses no-paid CI checks.

## [0.1.1] - 2026-05-16

### Added

- Formal release, rollback, dependency-update, routing-policy, and observability workflows for the rldyour Codex marketplace.
- `rldyour-design` Figma delivery contract for implementation manifests, dynamic/static/admin content classification, centralized i18n, token/UI-kit gates, and browser/static validation before final delivery.
- `fullrepo` branch workflow for portable agent-only files: restore, migrate, publish, status, smoke validation, and Flow/Serena lifecycle integration.
- Safe `--force-with-lease` fullrepo publishing after normal branch synchronization.
- Instruction docs sync workflow for first-class Codex `AGENTS.md` and Claude Code `.claude/CLAUDE.md` maintenance.
- Branch-aware local Git pre-push guard for rldyour-managed repositories, with strict product-branch protection and fullrepo-aware AI context publishing.
- Flow branch-cleanup state and smoke coverage so merged workflow branches, remote branches, and merged worktree candidates keep post-task sync pending until cleanup is done or explicitly reported.
- `fullrepo` bootstrap init command and smoke coverage for first-run repository initialization, remote context restore, local AI-file publishing, and current-branch AI-file index cleanup.
- Serena memory freshness helper and smoke coverage for source-branch freshness, stale memory failures, and `fullrepo` snapshot skip behavior.
- Codex-native Serena sync impact analyzer, numbered memory taxonomy smoke coverage, managed `serena-sync` guidance, and agent surface validation for Codex TOML/OpenAI skill metadata.
- `scripts/worktree_add.sh` and Flow SessionStart worktree bootstrap so new Codex worktrees restore agent-only context from `origin/fullrepo` before deep work starts.

### Changed

- System Codex install now writes `[features].hooks = true`, `[features].plugin_hooks = true`, and `[features].multi_agent = true` so bundled rldyour plugin hooks load from enabled plugins across current Codex CLI releases where plugin hooks remain explicit opt-in.
- System Codex install now explicitly writes `suppress_unstable_features_warning = true` so under-development feature noise is stable and intentional.
- System Codex install migration now normalizes current Codex deprecated config aliases: `codex_hooks`, legacy `features.web_search*`, `experimental_instructions_file`, `background_terminal_timeout`, `experimental_use_unified_exec_tool`, `memories.no_memories_if_mcp_or_web_search`, and deprecated `use_legacy_landlock`, with dedicated smoke coverage in `scripts/smoke_codex_hooks_migration.sh`.
- Flow post-task state now treats stale Serena memories and stale fullrepo snapshots as pending sync instead of false green states.
- Doctor and validation now use stricter parsed-config/current-state checks for system config, Serena memory freshness, and fullrepo sync.
- System Codex install and doctor now derive rldyour plugin enablement from `.agents/plugins/marketplace.json` and MCP server checks from `plugins/rldyour-mcps/.mcp.json` instead of parallel hardcoded lists.
- Hook smoke validation now parses plugin `hooks.json` wiring and executes the configured command wrappers in addition to direct hook script lifecycle checks.
- GitHub validation now includes scheduled and manual MCP safe-call smoke coverage for deterministic unauthenticated MCP tool invocations.
- Fullrepo bootstrap-init smoke now covers `.claude/CLAUDE.md` restore, ignore, and current-branch index cleanup alongside `AGENTS.md` and Serena memories.
- Clean bootstrap smoke now restores agent-only context with `scripts/sync_fullrepo_branch.sh --bootstrap-init` before running strict system doctor checks.
- MCP runtime smoke now checks remote URL servers with a Streamable HTTP `initialize` POST preflight, parses JSON and SSE initialize responses, accepts auth-gated `401`/`403` endpoints, and keeps retry/timeout controls.
- MCP capability smoke now probes Grep with a fast code-pattern query that matches the current `searchGitHub` tool contract and gives transient remote calls five attempts by default.
- Marketplace validation now enforces parity between `config/mcp-runtime-versions.env` and local MCP launcher package specs in `plugins/rldyour-mcps/.mcp.json`.
- System doctor keeps the fullrepo current-state gate strict locally while treating it as advisory on GitHub Actions `main` runs, where the separate `fullrepo` workflow validates published agent-only snapshots.
- System Codex install now writes the official Codex config schema hint at the top of generated `config.toml`, and doctor/migration smoke verify it.
- System Codex install now reproduces the owner-selected `gpt-5.5`/`xhigh` model defaults and approved MCP tool overrides from a clean `CODEX_HOME`.
- Plugin release validation now enforces Codex marketplace policy fields, plugin interface metadata, relative bundled capability paths, default prompt limits, and brand color format.
- System Codex install now manages `~/.codex/agents/*.toml` subagent role configs from `system/agents/*.toml`, enables `features.multi_agent`, and verifies managed subagents use `gpt-5.5` with medium reasoning.
- Runtime Codex CLI pin updated from `0.128.0` to `0.130.0`.
- MCP Python SDK pin updated from `1.27.0` to `1.27.1` for the latest compatibility fixes.
- MCP runtime pins updated for Serena Agent `1.3.0`, Semgrep `1.163.0`, Playwright MCP `0.0.75`, Chrome DevTools MCP `0.26.0`, Context7 MCP `2.2.5`, and shadcn `4.7.0`.
- `rldyour-serena-mcp` plugin version updated to `0.2.2` for Codex-native memory taxonomy, impact analysis, and managed `serena-sync` routing.
- `rldyour-flow` plugin version updated to `0.2.5` for read-only `ry-init` memory discipline, fullrepo bootstrap init behavior, and SessionStart worktree bootstrap.
- `ry-init` is now explicitly read-only for Serena memories by default; it reports memory candidates instead of writing `.serena` unless the user requested memory sync or a stale-memory hook requires it.
- `serena-memory-sync` no longer auto-runs for read-only init, log audits, server snapshots, report-only reviews, or exploratory debugging without an explicit memory-sync request.
- Global and project instructions now state the explicit fullrepo-managed task sync order: Serena/docs, checks, normal branch push, fullrepo publish, and safe cleanup.
- `@upstash/context7-mcp` runtime pin updated from `2.2.3` to `2.2.5`.
- `rldyour-flow` now treats `fullrepo` as part of `ry-init` and `flow-post-task-sync`.
- `rldyour-flow` now detects missing or stale instruction docs and routes post-task sync through `$instruction-docs-sync`.
- `rldyour-serena-mcp` memory sync now supports fullrepo-managed `.serena` knowledge without committing AI files to normal branches.
- `rldyour-rules` now documents the agent-only file policy for `AGENTS.md`, `.claude/CLAUDE.md`, `.serena`, and related AI workflow paths.
- `validate.yml` now runs `scripts/check_mcp_runtime_versions.py --fail-on-outdated --json` in a dedicated `dependency-pins` job on `push`, `pull_request`, and manual dispatch; this catches MCP runtime pin drift in normal CI alongside the scheduled `dependency-check` workflow.

## [0.1.0] - 2026-05-03

### Added

- Initial controlled Codex marketplace with rldyour plugins, MCP runtime definitions, system install scripts, validation scripts, hooks, LSP policy, browser/design/security/research workflows, and Serena project knowledge.
