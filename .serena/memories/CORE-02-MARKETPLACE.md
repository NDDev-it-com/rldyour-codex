<!-- Memory Metadata
Last updated: 2026-05-17
Last commit: 9a1cdc2 fix(codex): harden hooks and validation gates
Scope: .agents/plugins/marketplace.json, plugins/*/.codex-plugin/plugin.json, plugins/*/README.md, README.md, CHANGELOG.md, scripts/validate_plugin_versions.py, scripts/release_manifest.py
Area: CORE
-->

# CORE-02-MARKETPLACE

## Purpose

This memory records marketplace catalog and plugin-manifest contracts for the owner's local Codex marketplace.

## Source Of Truth

- `.agents/plugins/marketplace.json`: active marketplace plugin list and local source paths.
- `plugins/<plugin>/.codex-plugin/plugin.json`: per-plugin manifest, version, interface metadata, and bundled capabilities.
- `README.md`: active catalog and architectural boundaries.
- `CHANGELOG.md`: human-readable release notes.
- `VERSION`: marketplace release version.
- `scripts/validate_plugin_versions.py`: manifest, marketplace, policy, and version validation.
- `scripts/release_manifest.py`: generated release/runtime inventory.

## Entry Points

- `python3 scripts/validate_plugin_versions.py`: plugin metadata validation.
- `python3 scripts/release_manifest.py`: current marketplace and runtime manifest.
- `scripts/validate_marketplace.sh`: full validation gate.

## Current Behavior

- Marketplace name is `rldyour-codex` and all active rldyour plugins are local sources under `./plugins/<plugin>`.
- Active plugin count is 9.
- `rldyour-serena-mcp` version is `0.2.3`; it declares `skills` and `hooks` and owns Serena code workflow and memory sync.
- `rldyour-flow` version is `0.2.6`; it declares `skills` and `hooks` and owns SDLC workflows, fullrepo, worktree bootstrap, instruction docs, and post-task sync.
- Only `rldyour-flow` and `rldyour-serena-mcp` may declare plugin hooks in this repository.
- `rldyour-mcps` owns MCP transport definitions only and must not contain behavior skills.
- Curated GitHub and Gmail plugins are enabled in system Codex but are not rldyour plugin directories in this repository.
- Repository marketplace version is `0.1.1` (from `VERSION`, committed in `6b6dfd3`).

## Contracts And Data

- Plugin manifests use `.codex-plugin/plugin.json`, not `.claude-plugin/plugin.json`.
- Manifest `interface.brandColor` must use valid hex format.
- Manifest bundled capability paths are relative to the plugin root.
- Marketplace plugin entries use policy `installation = AVAILABLE` and `authentication = ON_USE` for active local rldyour plugins.
- Release metadata is SemVer-shaped per plugin; repository `VERSION` remains the marketplace version.
- Current marketplace version remains `0.1.1`; commit `9a1cdc2` changes plugin behavior versions and `[Unreleased]` changelog entries without changing root `VERSION`.

## Invariants

- Do not add planned plugins to `.agents/plugins/marketplace.json` until they exist and pass validation.
- Do not duplicate MCP server registration outside `plugins/rldyour-mcps/.mcp.json`.
- Do not maintain hardcoded plugin allowlists in installer or doctor scripts; derive from marketplace catalog.
- README, plugin manifests, changelog, and release manifest must not describe behavior that code no longer implements.
- `plugin_hooks` is a managed canonical feature for this repo and should be treated as stable/required when plugin hook behavior is in scope.

## Change Rules

- When a plugin behavior changes, update its manifest version/description/capabilities if the user-facing contract changed.
- When plugin versions change, update `CHANGELOG.md` and rerun `scripts/release_manifest.py` as a sanity check.
- When adding/removing plugins, update `README.md`, marketplace catalog, manifest, routing policy if needed, and validation expectations.

## Verification

- `python3 scripts/validate_plugin_versions.py`: manifest and marketplace validation.
- `python3 scripts/release_manifest.py`: generated inventory includes plugin versions and runtime state.
- `scripts/validate_marketplace.sh`: repository-wide marketplace validation.
