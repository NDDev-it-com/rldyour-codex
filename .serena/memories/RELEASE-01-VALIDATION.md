<!-- Memory Metadata
Last updated: 2026-05-31
Last verified: 2026-05-31
Last commit: 6daebd91be6351fe76b0cb5b3d060917b5faec58 ci: align public free CI coverage
Scope: release readiness, versioning, and artifact hygiene
Area: RELEASE
-->

# RELEASE-01-VALIDATION

## Scope
release readiness, versioning, and artifact hygiene

## Current source of truth
- `path:VERSION`
- `path:CHANGELOG.md`
- `path:plugins/*/.codex-plugin/plugin.json`
- `path:.github/workflows/release.yml`

## Last verified
- date: 2026-05-31
- commit: `6daebd91be6351fe76b0cb5b3d060917b5faec58`
- checked by: Codex ry-start enterprise hardening

## Facts
- Current Codex product/config version is `1.1.12`; root control-plane pins
  must reference commit `6daebd91be6351fe76b0cb5b3d060917b5faec58` for this
  adapter.
- `VERSION`, `CHANGELOG.md`, `pyproject.toml`, `uv.lock`, and every
  `plugins/*/.codex-plugin/plugin.json` manifest must keep the same publishable
  adapter version. `scripts/validate_plugin_versions.py` enforces this release
  coordinate parity.
- The current release workflow is tag-driven, publishes GitHub Releases for
  numeric tags, and belongs to the public adapter release surface. Root
  `scripts/validate_release_supply_chain.py` and
  `scripts/validate_public_ci_policy.py` validate the supply-chain posture from
  the private control plane.
- Current Codex runtime baseline remains Codex CLI `0.135.0`. The release
  state keeps the Codex-native plugin marketplace, skills, managed agents,
  hooks, MCP materialization, and legacy owner-yolo sandbox dialect unchanged.
- Release validation should use `scripts/validate_fast.sh`,
  `scripts/validate_release.sh`, `bash scripts/validate_marketplace.sh`, and
  `scripts/validate_runtime.sh --strict-runtime` when installed runtime
  prerequisites are available.

## Evidence
- `commit:6daebd91be6351fe76b0cb5b3d060917b5faec58`
- `path:VERSION`
- `path:CHANGELOG.md`
- `path:plugins/*/.codex-plugin/plugin.json`
- `path:.github/workflows/release.yml`
- `path:scripts/validate_plugin_versions.py`

## Known pitfalls
- Treat this memory as derived context. Current code, configuration, runtime output, and GitHub state override stale memory text.

## Update policy
Update after verified changes to the referenced source-of-truth files.

## Delete / merge policy
- Delete or merge only when the referenced source-of-truth files no longer support this memory and the replacement memory preserves the durable facts.

## Applies to
- The scope declared in this memory and the source-of-truth paths listed below.

## Source of truth
- The `Current source of truth` section above, plus current code/config/tests/git state for the scoped repository.

## Invariants
- Code, configuration, tests, and git state override this memory when they disagree.
- Current product/config version claims must match `VERSION` and root `config/repositories.json`.
- Publishable plugin manifest versions must match the adapter `VERSION`.

## Current State
- See `Facts` for current durable facts. Do not treat `Historical evidence` or old commit notes as current state.

## Do Not Infer
- Do not infer runtime versions, product versions, commits, permissions, release state, or tool behavior from this memory without checking the source of truth.

## Update Triggers
- Update after verified changes to the source-of-truth files, runtime baselines, release tuple, validation gates, or durable agent workflow contracts.

## Validation Commands
- `python3 scripts/validate_plugin_versions.py`
- `python3 scripts/validate_contract.py`
- `python3 scripts/validate_instruction_docs.py --require-agent-docs`
- `python3 scripts/check_serena_memory_freshness.py`

## Repair Procedure
- Re-read source-of-truth files, update only verified current facts, move stale facts to historical evidence, then rerun the validation commands.
