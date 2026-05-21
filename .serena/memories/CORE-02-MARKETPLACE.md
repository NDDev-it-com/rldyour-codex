<!-- Memory Metadata
Last updated: 2026-05-21
Last commit: 89fabec chore(release): 0.4.3
Scope: .agents/plugins/marketplace.json, plugins/*/.codex-plugin/plugin.json, plugins/*/README.md, README.md, CHANGELOG.md, config/rldyour-contract.json, docs/contract-matrix.md, scripts/validate_plugin_versions.py, scripts/validate_contract.py, scripts/release_manifest.py
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
- `scripts/validate_contract.py`: adapter-surface validation that also enforces owned plugin license and canonical repository URLs.
- `config/rldyour-contract.json`: canonical plugin list, license, public repository URL, and adapter surface.
- `scripts/release_manifest.py`: generated release/runtime inventory.

## Entry Points

- `python3 scripts/validate_plugin_versions.py`: plugin metadata validation.
- `python3 scripts/validate_contract.py`: plugin set, manifest license/URL, skill, agent, hook, MCP, cache, and security contract validation.
- `python3 scripts/release_manifest.py`: current marketplace and runtime manifest.
- `scripts/validate_marketplace.sh`: full validation gate.

## Current Behavior

- Marketplace name is `rldyour-codex` and all active rldyour plugins are local sources under `./plugins/<plugin>`.
- Active plugin count is 9.
- `rldyour-serena-mcp` version is `0.2.4`; it declares `skills` and `hooks` and owns Serena code workflow and memory sync. Its Stop script is invoked by Flow's ordered Stop dispatcher rather than registered as an independent Stop command.
- `rldyour-flow` version is `0.3.3`; it declares `skills` and `hooks` and owns SDLC workflows, fullrepo, fast offline/local-only SessionStart bootstrap/context, cwd-safe PreToolUse guardrails, instruction docs, ordered local-only Stop lifecycle dispatch, and post-task sync.
- Only `rldyour-flow` and `rldyour-serena-mcp` may declare plugin hooks in this repository.
- `rldyour-mcps` owns MCP transport definitions only and must not contain behavior skills.
- Curated GitHub and Gmail plugins are enabled in system Codex but are not rldyour plugin directories in this repository.
- Repository marketplace version is `0.4.3` (from `VERSION`, committed in `89fabec`). The repository is licensed under GNU AGPL-3.0-or-later; the canonical FSF license text lives in `LICENSE` (SHA-256 `0d96a4ff68ad6d4b6f1f30f713b18d5184912ba8dd389f86aa7710db079abcb0`). `pyproject.toml` declares `license = "AGPL-3.0-or-later"`, `license-files = ["LICENSE"]`, public packaging metadata (authors, maintainers, classifiers, keywords), and project URLs pointing to `https://github.com/NDDev-it-com/rldyour-codex`.
- Owned plugin manifests declare `license = "AGPL-3.0-or-later"` and use `https://github.com/NDDev-it-com/rldyour-codex` for `homepage`, `repository`, `interface.websiteURL`, `interface.privacyPolicyURL`, and `interface.termsOfServiceURL`.

## Contracts And Data

- Plugin manifests use `.codex-plugin/plugin.json`, not `.claude-plugin/plugin.json`.
- Manifest `interface.brandColor` must use valid hex format.
- Manifest bundled capability paths are relative to the plugin root.
- Manifest owned license and repository URL values are enforced by both `scripts/validate_plugin_versions.py` and `scripts/validate_contract.py`.
- Marketplace plugin entries use policy `installation = AVAILABLE` and `authentication = ON_USE` for active local rldyour plugins.
- Release metadata is SemVer-shaped per plugin; repository `VERSION` remains the marketplace version.
- Current marketplace version is `0.4.3`; commit `89fabec` bumps the marketplace version, installs the pinned GitHub MCP server in CI runtime setup, tracks the GitHub MCP binary through pin freshness, and updates Context7 MCP to `2.3.0`. The `0.4.2` release merged the runtime-contract branch to `main`, added the adapter contract gate, and aligned Codex GitHub MCP parity. The `0.4.1` hardening release adds OpenSSF Scorecard, Dependency Review, and PR Labeler workflows, makes MCP pin freshness advisory on pull requests, and applies the public-repo GitHub settings.
- Previous release `0.3.5` was published by manual release workflow run `26006831237` after the full explicit CI/CD pipeline passed on `6ec3fb9`. Release `0.4.0` triggers via push of tag `0.4.0` to `origin/main` (release.yml `on: push: tags: [0-9]*.[0-9]*.[0-9]*`).

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
- `python3 scripts/validate_contract.py`: adapter contract and manifest license/URL validation.
- `python3 scripts/release_manifest.py`: generated inventory includes plugin versions and runtime state.
- `scripts/validate_marketplace.sh`: repository-wide marketplace validation.
