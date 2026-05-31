<!-- Memory Metadata
Last updated: 2026-05-31
Last verified: 2026-05-31
Last commit: 1252b518c85b3d3ea359109062c6d804696ef7f7 chore(release): codex 1.1.14 (other)
Scope: Codex adapter implementation surface
Area: CODEX
-->

# Codex Adapter Surface

## Scope
Codex adapter implementation surface

## Current source of truth
- `path:config/rldyour-contract.json`
- `path:.agents/plugins/marketplace.json`


## Source Of Truth
- `path:config/rldyour-contract.json`
- `path:.agents/plugins/marketplace.json`

## Last verified
- date: 2026-05-31
- commit: `1252b518c85b3d3ea359109062c6d804696ef7f7`
- checked by: Codex ry-start automated release and metadata sync

## Facts
- Codex adapter surface currently validates as 9 plugins, 39 skills with
  `agents/openai.yaml`, 8 managed TOML agents, and 13 MCP servers.
- Current owner install policy is the legacy sandbox dialect:
  `approval_policy = "never"` and `sandbox_mode = "danger-full-access"` for
  `rldyour-yolo`; active `default_permissions`, `profile =`, and
  `[profiles.*]` are forbidden while this dialect is selected.
- Current Codex 0.135 treats `plugin_hooks` as a removed feature flag. Hook
  discovery is modeled as explicit contract fields:
  `hooks_feature_default_enabled`, `plugin_bundled_hooks_discoverable`,
  `plugin_hook_trust_required`, and
  `trusted_hook_hashes_refreshed_by_installer`; runtime hook availability is
  verified through trusted `hooks/list` output, not through
  `[features].plugin_hooks = true`.
- `scripts/validate_instruction_docs.py` scans active instruction surfaces for
  stale Codex/OpenCode claims such as `[features].plugin_hooks = true`,
  `:danger-no-sandbox`, and current-pin wording drift.
- Current product/config version is `1.1.14`; the version bump is recorded in
  `VERSION`, `pyproject.toml`, `uv.lock`, and `CHANGELOG.md` without changing
  MCP, hook, or managed-agent runtime semantics.
- All `plugins/*/.codex-plugin/plugin.json` manifests record the same `1.1.14`
  version as `VERSION`; `scripts/validate_plugin_versions.py` enforces this
  release-coordinate parity and requires user-facing plugin manifest metadata
  to stay Russian-first and English-compatible.
- Commit `1252b518c85b3d3ea359109062c6d804696ef7f7` moves the adapter to
  `1.1.14`, keeps plugin manifest versions in parity with `VERSION`, adds
  standard public Ubuntu/Windows/macOS cross-platform smoke coverage, and
  preserves Codex-native plugin, MCP, hook, managed-agent, and owner-yolo
  runtime semantics.
- `scripts/validate_instruction_docs.py` also scans `.serena/research/*.md`
  for current-tense stale `plugin_hooks` claims unless the research file has a
  `SUPERSEDED` banner.
## Evidence
- `commit:1252b518c85b3d3ea359109062c6d804696ef7f7`
- `path:config/rldyour-contract.json`
- `path:.agents/plugins/marketplace.json`
- `path:references/codex-surface-adoption.md`
- `path:scripts/validate_instruction_docs.py`
- `path:scripts/install_system_codex.sh`
- `path:scripts/smoke_codex_hooks_migration.sh`
- `path:system/agents/*.toml`

## Known pitfalls
- Treat this memory as derived context. Current code, configuration, runtime output, and GitHub state override stale memory text.

## Historical evidence
- Commit `6814a398cf0026102cf15688e038f71744d9ac5b` moved the adapter to
  `1.1.3`, kept plugin manifest versions in parity with `VERSION`, and
  recorded the Russian-first `agents/openai.yaml` metadata release.
- Commit `a13c0a18275af27a0148b9ccf01a893d77344503` moved the adapter to
  `1.1.1`, completed Codex `0.135.0` surface-adoption notes, kept plugin
  manifest versions in parity with `VERSION`, and kept the legacy sandbox
  permission dialect unchanged.
- Commit `b92c6a3290020771e57a9e415f8b131be573a770` refreshed Codex Semgrep
  and shadcn MCP pins to `semgrep==1.164.0` and `shadcn@4.8.2` across the MCP
  source manifest, managed TOML agents, runtime env pin file, and fixture
  tests.
- Commit `d7909f83ae7ec947946f374ffae99af37db5335a` hardened
  `scripts/install_system_codex.sh` so managed subagent TOML output stays
  flat and does not emit nested legacy profile tables. The migration smoke
  covers this regression class.
- Commit `2172b16855bd550f580f4a631601953e3a956083` added
  `references/codex-surface-adoption.md` as the Codex 0.134.0 adoption matrix:
  `--profile` is adopted, legacy profile selectors remain forbidden, MCP
  runtime materialization stays native TOML, and plugin hooks remain
  default-enabled/trusted rather than a `[features].plugin_hooks` flag.
- Commit `2a852698661384a3ba4497c4ea2c98111d941965` moved the adapter to
  `1.0.2`, synchronized plugin manifest versions with the adapter product
  version, and hardened plugin-version validation.
- Commit `818d3c19388978564b29724488678cd803b99867` moved the adapter to
  `1.0.3`, aligned active descriptions with the root
  `config/repository-description-policy.json` template, kept plugin manifest
  versions in parity with `VERSION`, and published GitHub Release `1.1.3`.

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
