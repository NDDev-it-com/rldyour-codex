<!-- Memory Metadata
Last updated: 2026-05-29
Last commit: 818d3c1
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
- commit: `818d3c19388978564b29724488678cd803b99867`
- checked by: Codex system sync after nested legacy profile cleanup

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
- System config migration removes both exact legacy profile tables and nested
  legacy profile subtables such as `[profiles.rldyour-yolo.features]` before
  writing `$CODEX_HOME/config.toml`.
- `scripts/validate_instruction_docs.py` scans active instruction surfaces for
  stale Codex/OpenCode claims such as `[features].plugin_hooks = true`,
  `:danger-no-sandbox`, and current-pin wording drift.
- Current product/config version is `1.0.3`; the version bump is recorded in
  `VERSION`, `pyproject.toml`, and `CHANGELOG.md` without changing plugin,
  MCP, hook, or managed-agent runtime semantics.
- `uv.lock` records `1.0.3`; `pyproject.toml`, `VERSION`, and plugin
  manifests were updated together in the 1.0.3 release.
- Commit `b92c6a3290020771e57a9e415f8b131be573a770` refreshes Codex Semgrep
  and shadcn MCP pins to `semgrep==1.164.0` and `shadcn@4.8.2` across the MCP
  source manifest, managed TOML agents, runtime env pin file, and fixture
  tests.
- Commit `818d3c19388978564b29724488678cd803b99867` updates all shipped plugin
  manifests to `1.0.3`, aligns `README.md`, `VERSION`, and `pyproject.toml`, and
  refreshes `validate_plugin_versions.py` and `CONTRIBUTING.md` for the release
  release notes context.
- `scripts/validate_instruction_docs.py` also scans `.serena/research/*.md`
  for current-tense stale `plugin_hooks` claims unless the research file has a
  `SUPERSEDED` banner.

## Evidence
- `commit:d7909f83ae7ec947946f374ffae99af37db5335a`
- `path:config/rldyour-contract.json`
- `path:.agents/plugins/marketplace.json`
- `path:scripts/validate_instruction_docs.py`
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
