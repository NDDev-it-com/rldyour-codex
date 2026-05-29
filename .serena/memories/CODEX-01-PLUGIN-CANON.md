<!-- Memory Metadata
Last updated: 2026-05-29
Last commit: ea419bc0900cc934ca1b9434e8ff8f4e0304328b chore(release): codex 1.1.0
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
- date: 2026-05-29
- commit: `ea419bc0900cc934ca1b9434e8ff8f4e0304328b`
- checked by: Codex ry-start automated release and metadata sync

## Facts
- Codex adapter surface currently validates as 9 plugins, 39 skills with
  `agents/openai.yaml`, 8 managed TOML agents, and 13 MCP servers.
- Current owner install policy is the legacy sandbox dialect:
  `approval_policy = "never"` and `sandbox_mode = "danger-full-access"` for
  `rldyour-yolo`; active `default_permissions`, `profile =`, and
  `[profiles.*]` are forbidden while this dialect is selected.
- Current Codex 0.134 treats `plugin_hooks` as a removed feature flag. Plugin
  hook availability is default-enabled and verified through trusted
  `hooks/list` output, not through `[features].plugin_hooks = true`.
- `scripts/validate_instruction_docs.py` scans active instruction surfaces for
  stale Codex/OpenCode claims such as `[features].plugin_hooks = true`,
  `:danger-no-sandbox`, and current-pin wording drift.
- Current product/config version is `1.0.3`; the version bump is recorded in
  `VERSION`, `pyproject.toml`, `uv.lock`, and `CHANGELOG.md` without changing
  MCP, hook, or managed-agent runtime semantics.
- All `plugins/*/.codex-plugin/plugin.json` manifests record the same `1.0.3`
  version as `VERSION`; `scripts/validate_plugin_versions.py` enforces this
  release-coordinate parity.
- Commit `b92c6a3290020771e57a9e415f8b131be573a770` refreshes Codex Semgrep
  and shadcn MCP pins to `semgrep==1.164.0` and `shadcn@4.8.2` across the MCP
  source manifest, managed TOML agents, runtime env pin file, and fixture
  tests.
- `scripts/validate_instruction_docs.py` also scans `.serena/research/*.md`
  for current-tense stale `plugin_hooks` claims unless the research file has a
  `SUPERSEDED` banner.
- Commit `d7909f83ae7ec947946f374ffae99af37db5335a` hardens
  `scripts/install_system_codex.sh` so managed subagent TOML output stays
  flat and does not emit nested legacy profile tables. The migration smoke
  covers this regression class.
- Commit `2172b16855bd550f580f4a631601953e3a956083` adds
  `references/codex-surface-adoption.md` as the Codex 0.134.0 adoption matrix:
  `--profile` is adopted, legacy profile selectors remain forbidden, MCP
  runtime materialization stays native TOML, and plugin hooks remain
  default-enabled/trusted rather than a `[features].plugin_hooks` flag.
- Commit `2a852698661384a3ba4497c4ea2c98111d941965` moves the adapter to
  `1.0.2`, synchronizes plugin manifest versions with the adapter product
  version, and hardens plugin-version validation.
- Commit `818d3c19388978564b29724488678cd803b99867` moves the adapter to
  `1.0.3`, aligns active descriptions with the root
  `config/repository-description-policy.json` template, keeps plugin manifest
  versions in parity with `VERSION`, and publishes GitHub Release `1.0.3`.

## Evidence
- `commit:ea419bc0900cc934ca1b9434e8ff8f4e0304328b`
- `path:config/rldyour-contract.json`
- `path:.agents/plugins/marketplace.json`
- `path:references/codex-surface-adoption.md`
- `path:scripts/validate_instruction_docs.py`
- `path:scripts/install_system_codex.sh`
- `path:scripts/smoke_codex_hooks_migration.sh`
- `path:system/agents/*.toml`

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
