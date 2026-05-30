<!-- Memory Metadata
Last updated: 2026-05-30
Last verified: 2026-05-30
Last commit: fe7566ebc15149d57d9f1d65bf792e66d90daa26 chore(release): codex 1.1.7 (release_metadata)
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
- date: 2026-05-30
- commit: `fe7566ebc15149d57d9f1d65bf792e66d90daa26`
- checked by: Codex ry-start automated release and metadata sync

## Facts
- Release memories record numeric versioning, tags, CI gates, and clean artifact hygiene.
- Current product/config version is `1.1.7`; `VERSION`, `pyproject.toml`,
  `uv.lock`, plugin manifests, and `CHANGELOG.md` are the source of truth for
  the adapter-local SemVer state.
- Release `1.1.7` hardens Codex MCP runtime materialization: GitHub MCP now
  forwards `GITHUB_PERSONAL_ACCESS_TOKEN` through Codex `env_vars`, the
  installer normalizes legacy exact `${NAME}` env placeholders to forwarded
  env vars, and `scripts/validate_codex_mcp_env_forwarding.py` rejects literal
  secret placeholders in source, installed runtime config, and managed-agent
  MCP overrides.
- Release `1.1.7` keeps the Codex CLI runtime baseline at `0.135.0`, keeps the
  owner-standard legacy sandbox permission dialect, makes managed subagent
  descriptions Russian-first with compact `EN:` suffixes, and validates that
  policy through `scripts/validate_codex_managed_agents_bilingual.py`.
- Verified gates for this sync included `bash scripts/validate_marketplace.sh`
  with a temporary installed `CODEX_HOME`, `scripts/validate_fast.sh`,
  `scripts/validate_release.sh`, `scripts/validate_runtime.sh --mode static`,
  `validate_contract.py`, `validate_agent_tools.py`,
  `validate_plugin_versions.py`, `validate_codex_mcp_env_forwarding.py`,
  `validate_codex_managed_agents_bilingual.py`, and
  `validate_instruction_docs.py --require-agent-docs`.

## Evidence
- `commit:fe7566ebc15149d57d9f1d65bf792e66d90daa26`
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

## Historical evidence
- Release `1.1.7` made Codex skill `agents/openai.yaml` UI metadata
  Russian-first, made adapter `SKILL.md` descriptions Russian-first with
  English trigger suffixes, kept the Codex CLI runtime baseline at `0.135.0`,
  and preserved the owner-standard legacy sandbox permission dialect.
- Release `1.1.7` adopted Codex CLI `0.135.0`, refreshed
  `GITHUB_MCP_SERVER_VERSION=1.1.0`, kept the legacy sandbox permission
  dialect unchanged, and published GitHub Release `1.1.7`.
- Release `1.1.7` completed the Codex `0.135.0` surface-adoption notes for
  `/permissions`, patched zsh helper diagnostics, and Vim-mode refinements
  without changing the owner-standard legacy sandbox permission dialect.
- Commit `eefb9d4e48eb0d9e8562176ed08e0b1bdbed3222` kept product version
  `0.4.9`, updated Chrome DevTools MCP freshness to `1.1.1`, and added an
  instruction-doc guard against reintroducing removed Codex `plugin_hooks`
  feature-flag claims.
- Commit `8b746f31da1f1435d9ca5a9de5aa65cf7ccf7fa9` kept public fast
  validation compatible with normal source checkouts by requiring agent-only
  `AGENTS.md` / `.claude/CLAUDE.md` only when those files are present locally.
- Commit `18ff3847cd72d1f17c4db5509c70fe516cec1332` added explicit
  `auto`, `static`, `installed`, and `live` modes to `scripts/validate_runtime.sh`.
  Static mode materialized temp Codex config/profile TOML and verified hooks,
  multi-agent, MCP TOML, legacy sandbox policy, and absence of removed
  `plugin_hooks`, legacy profile selectors, and active `default_permissions`
  without requiring a Codex binary or network.
- Commit `062c2c1591265189665d8da2d05c7efb4b95ee21` bumped the product/config
  version to `0.5.0` in `VERSION`, `pyproject.toml`, and `CHANGELOG.md` without
  changing runtime semantics.
- Commit `98bcb04a2dc707ab820377056c0c7bff25a94cf5` kept product version
  `0.5.0`, restored `uv.lock` version parity, and classified retried MCP
  TaskGroup startup noise after the smoke reached a passing result.
- Commit `b92c6a3290020771e57a9e415f8b131be573a770` bumped product/config
  version to `1.0.0`, kept `pyproject.toml` and `uv.lock` in parity, refreshed
  Semgrep/shadcn MCP pins, grouped Codex Dependabot GitHub Actions updates, and
  added stale research-claim validation for superseded Codex `plugin_hooks`
  research notes.
- Commit `84ef50d1d0005e3977c3c644b4a680d5feb4b6e8` kept the `1.0.0`
  runtime/config tuple unchanged and extended `scripts/classify_ci_noise.py` so
  strict fast validation treats warnings about explicitly superseded Serena
  research claims as known benign CI noise while still failing on unknown
  stderr lines.
- Commit `33aae825830df3c262a1ccf9b31ad6b0efa12426` kept product/runtime
  semantics unchanged, refreshed all Codex `github/codeql-action` workflow
  pins to the `v4.36.0` dereferenced commit SHA, and grouped all Dependabot
  GitHub Actions version updates into one reviewable PR.
- Commit `2d4cee72988a99a934168c9649fec8307560c283` kept product/runtime
  semantics unchanged and aligned the Codex Dependabot `github-actions` update
  cadence to monthly grouped PRs.
- Commit `d7909f83ae7ec947946f374ffae99af37db5335a` kept product/runtime
  semantics unchanged and removed nested legacy profile tables from generated
  managed subagent TOML output; `scripts/smoke_codex_hooks_migration.sh`
  covered the regression.
- Commit `2172b16855bd550f580f4a631601953e3a956083` kept product/runtime
  semantics unchanged and recorded the Codex 0.134.0 surface adoption matrix in
  `references/codex-surface-adoption.md`.
- Commit `d35c3c90d7341d5ab9c94b868bfe47bb41858c74` kept product/runtime
  semantics unchanged and aligned public repository metadata surfaces in
  `README.md`, `CONTRIBUTING.md`, and `pyproject.toml` with the root
  control-plane GitHub description.
- Commit `2a852698661384a3ba4497c4ea2c98111d941965` bumped the product/config
  version to `1.0.2`, kept `pyproject.toml` and `uv.lock` in parity,
  synchronized all Codex plugin manifest versions to `1.0.2`, and published
  GitHub Release `1.1.7`.
- Commit `818d3c19388978564b29724488678cd803b99867` bumped the product/config
  version to `1.0.3`, aligned active repository descriptions with the root
  `config/repository-description-policy.json` template, preserved the existing
  `workflow_dispatch` release input as `version`, created or reused numeric
  tags during manual release runs, and published GitHub Release `1.1.7`.
- Commit `a13c0a18275af27a0148b9ccf01a893d77344503` bumped the product/config
  version to `1.1.0`, updated the Codex CLI runtime baseline to `0.135.0`,
  refreshed the GitHub MCP Server host-binary pin to `1.1.0`, kept
  `pyproject.toml`, `uv.lock`, and plugin manifest versions in parity, and
  published GitHub Release `1.1.7`.

## Update policy
Update after verified changes to the referenced source-of-truth files.

## Delete / merge policy
- Delete or merge only when the referenced source-of-truth files no longer support this memory and the replacement memory preserves the durable facts.

## Cross-References
- `CORE-01-INDEX.md`
- `CONTEXT-01-CORE.md`
- `PATTERNS-01-CANONICAL.md`

## Applies to
- The scope declared in this memory and the source-of-truth paths listed below.

## Invariants
- Code, configuration, tests, and git state override this memory when they disagree.

## Current State
- See `Facts` for current durable facts. Do not treat `Historical evidence` or old commit notes as current state.

## Do Not Infer
- Do not infer runtime versions, product versions, commits, permissions, release state, or tool behavior from this memory without checking the source of truth.

## Update Triggers
- Update after verified changes to the source-of-truth files, runtime baselines, release tuple, validation gates, or durable agent workflow contracts.

## Validation Commands
- `python3 scripts/validate_serena_memory_schema.py --scope all --strict-mode strict-all`
- `python3 scripts/validate_serena_memory_semantics.py --scope all --strict-current-facts`
- `python3 scripts/validate_memory_freshness.py --scope all`

## Repair Procedure
- Re-read source-of-truth files, update only verified current facts, move stale facts to historical evidence, then rerun the validation commands.
