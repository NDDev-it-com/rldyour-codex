<!-- Memory Metadata
Last updated: 2026-05-29
Last commit: ea419bc0900cc934ca1b9434e8ff8f4e0304328b chore(release): codex 1.1.0
Scope: release readiness, versioning, and artifact hygiene
Area: RELEASE
-->

# RELEASE-01-VALIDATION

## Scope
release readiness, versioning, and artifact hygiene

## Current source of truth
- `path:VERSION`
- `path:CHANGELOG.md`
- `path:.github/workflows/release.yml`
- `path:scripts/smoke_codex_hook_listing.py`


## Source Of Truth
- `path:VERSION`
- `path:CHANGELOG.md`
- `path:.github/workflows/release.yml`
- `path:scripts/smoke_codex_hook_listing.py`

## Last verified
- date: 2026-05-29
- commit: `ea419bc0900cc934ca1b9434e8ff8f4e0304328b`
- checked by: Codex ry-start automated release and metadata sync

## Facts
- Release memories record numeric versioning, tags, CI gates, and clean artifact hygiene.
- Current product/config version is `1.1.0`; `VERSION`, `pyproject.toml`,
  `uv.lock`, plugin manifests, and `CHANGELOG.md` are the source of truth for
  the adapter-local SemVer state.
- Release `1.1.0` adopts Codex CLI `0.135.0`, refreshes
  `GITHUB_MCP_SERVER_VERSION=1.1.0`, keeps the legacy sandbox permission
  dialect unchanged, and publishes GitHub Release `1.1.0`.
- Commit `eefb9d4e48eb0d9e8562176ed08e0b1bdbed3222` keeps product version
  `0.4.9`, updates Chrome DevTools MCP freshness to `1.1.1`, and adds an
  instruction-doc guard against reintroducing removed Codex `plugin_hooks`
  feature-flag claims.
- Commit `8b746f31da1f1435d9ca5a9de5aa65cf7ccf7fa9` keeps public fast
  validation compatible with normal source checkouts by requiring agent-only
  `AGENTS.md` / `.claude/CLAUDE.md` only when those files are present locally.
- Commit `18ff3847cd72d1f17c4db5509c70fe516cec1332` adds explicit
  `auto`, `static`, `installed`, and `live` modes to `scripts/validate_runtime.sh`.
  Static mode materializes temp Codex config/profile TOML and verifies hooks,
  multi-agent, MCP TOML, legacy sandbox policy, and absence of removed
  `plugin_hooks`, legacy profile selectors, and active `default_permissions`
  without requiring a Codex binary or network.
- Commit `062c2c1591265189665d8da2d05c7efb4b95ee21` bumps the product/config
  version to `0.5.0` in `VERSION`, `pyproject.toml`, and `CHANGELOG.md` without
  changing runtime semantics.
- Commit `98bcb04a2dc707ab820377056c0c7bff25a94cf5` keeps product version
  `0.5.0`, restores `uv.lock` version parity, and classifies retried MCP
  TaskGroup startup noise after the smoke reaches a passing result.
- Commit `b92c6a3290020771e57a9e415f8b131be573a770` bumps product/config
  version to `1.0.0`, keeps `pyproject.toml` and `uv.lock` in parity, refreshes
  Semgrep/shadcn MCP pins, groups Codex Dependabot GitHub Actions updates, and
  adds stale research-claim validation for superseded Codex `plugin_hooks`
  research notes.
- Commit `84ef50d1d0005e3977c3c644b4a680d5feb4b6e8` keeps the `1.0.0`
  runtime/config tuple unchanged and extends `scripts/classify_ci_noise.py` so
  strict fast validation treats warnings about explicitly superseded Serena
  research claims as known benign CI noise while still failing on unknown
  stderr lines.
- Commit `33aae825830df3c262a1ccf9b31ad6b0efa12426` keeps product/runtime
  semantics unchanged, refreshes all Codex `github/codeql-action` workflow
  pins to the `v4.36.0` dereferenced commit SHA, and groups all Dependabot
  GitHub Actions version updates into one reviewable PR.
- Commit `2d4cee72988a99a934168c9649fec8307560c283` keeps product/runtime
  semantics unchanged and aligns the Codex Dependabot `github-actions` update
  cadence to monthly grouped PRs.
- Commit `d7909f83ae7ec947946f374ffae99af37db5335a` keeps product/runtime
  semantics unchanged and removes nested legacy profile tables from generated
  managed subagent TOML output; `scripts/smoke_codex_hooks_migration.sh`
  covers the regression.
- Commit `2172b16855bd550f580f4a631601953e3a956083` keeps product/runtime
  semantics unchanged and records the Codex 0.134.0 surface adoption matrix in
  `references/codex-surface-adoption.md`.
- Commit `d35c3c90d7341d5ab9c94b868bfe47bb41858c74` keeps product/runtime
  semantics unchanged and aligns public repository metadata surfaces in
  `README.md`, `CONTRIBUTING.md`, and `pyproject.toml` with the root
  control-plane GitHub description.
- Commit `2a852698661384a3ba4497c4ea2c98111d941965` bumps the product/config
  version to `1.0.2`, keeps `pyproject.toml` and `uv.lock` in parity,
  synchronizes all Codex plugin manifest versions to `1.0.2`, and publishes
  GitHub Release `1.0.2`.
- Commit `818d3c19388978564b29724488678cd803b99867` bumps the product/config
  version to `1.0.3`, aligns active repository descriptions with the root
  `config/repository-description-policy.json` template, preserves the existing
  `workflow_dispatch` release input as `version`, creates or reuses numeric
  tags during manual release runs, and publishes GitHub Release `1.0.3`.
- Commit `ea419bc0900cc934ca1b9434e8ff8f4e0304328b` bumps the product/config
  version to `1.1.0`, updates the Codex CLI runtime baseline to `0.135.0`,
  refreshes the GitHub MCP Server host-binary pin to `1.1.0`, keeps
  `pyproject.toml`, `uv.lock`, and plugin manifest versions in parity, and
  publishes GitHub Release `1.1.0`.
- Verified gates for this sync included `validate_instruction_docs.py
  --require-agent-docs`, `validate_contract.py`, `validate_agent_tools.py`,
  `scripts/validate_runtime.sh --mode static`, `scripts/validate_runtime.sh
  --mode installed`, `check_mcp_runtime_versions.py`, and root
  `scripts/validate_public_metadata_surfaces.py`.

## Evidence
- `commit:ea419bc0900cc934ca1b9434e8ff8f4e0304328b`
- `path:VERSION`
- `path:CHANGELOG.md`
- `path:references/codex-surface-adoption.md`
- `path:CONTRIBUTING.md`
- `path:config/mcp-runtime-versions.env`
- `path:.github/workflows/release.yml`
- `path:scripts/smoke_codex_hook_listing.py`
- `path:scripts/validate_instruction_docs.py`
- `path:scripts/validate_fast.sh`
- `path:scripts/validate_runtime.sh`
- `path:scripts/install_system_codex.sh`
- `path:scripts/smoke_codex_hooks_migration.sh`

## Known pitfalls
- Treat this memory as derived context. Current code, configuration, runtime output, and GitHub state override stale memory text.

## Update policy
Update after verified changes to the referenced source-of-truth files.

## Delete / merge policy
- Delete or merge only when the referenced source-of-truth files no longer support this memory and the replacement memory preserves the durable facts.

## Cross-References
- `CORE-01-INDEX.md`
- `CONTEXT-01-CORE.md`
- `PATTERNS-01-CANONICAL.md`
