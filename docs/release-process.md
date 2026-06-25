# Release Process

This repository has two versioning layers:

- Marketplace release version: stored in `VERSION` and used for repository-level releases, CI gates, rollback records, and Git tags.
- Plugin versions: stored in `plugins/<plugin>/.codex-plugin/plugin.json` and incremented only when that plugin's public behavior changes.

## Versioning Rules

- Use Semantic Versioning for `VERSION` and every plugin manifest version.
- Increment `MAJOR` for incompatible behavior, manifest, hook, config, or install changes.
- Increment `MINOR` for backward-compatible plugin capabilities, skills, scripts, checks, or documentation that add behavior.
- Increment `PATCH` for backward-compatible fixes, validation hardening, typo fixes, and non-behavioral maintenance.
- Do not modify an already released Git tag. Cut a new version instead.
- Keep `CHANGELOG.md` human-readable and grouped by version.

## Release Checklist

1. Decide the release scope: marketplace-only, one plugin, multiple plugins, or MCP runtime pins.
2. Update `VERSION` when the repository release changes.
3. Update affected plugin manifest versions when plugin behavior changes.
4. Update `CHANGELOG.md` with owner-relevant changes.
5. Run local validation:

```bash
scripts/validate_fast.sh
scripts/validate_runtime.sh --strict-runtime
scripts/validate_release.sh
scripts/validate_execpolicy_rules.sh
scripts/validate_marketplace.sh
scripts/doctor_system_codex.sh
scripts/smoke_local_git_guard.sh
scripts/smoke_flow_branch_cleanup.sh
python3 scripts/release_manifest.py > diagnostics/release-manifest.json
python3 scripts/release_sbom.py > diagnostics/sbom.spdx.json
```

6. Commit with a Conventional Commit message.
7. Push to `main` (agent context is tracked normally on `main`, so there is no separate publish step), then manually run the `validate` workflow with `scope=full` on the Ubuntu standard runner.
8. Create the release from `.github/workflows/release.yml` after the requested manual CI scope is green. The workflow validates `VERSION` and `CHANGELOG.md`, builds a deterministic `tar.gz`, writes `release-manifest.json`, writes generated SPDX SBOM evidence, exports the GitHub dependency graph SPDX SBOM from the dependency graph SBOM endpoint when available, creates artifact attestations, and publishes the GitHub Release.

Release tags use the exact SemVer value from `VERSION` without a `v` prefix, for example `0.2.0`.

## Release Manifest

`scripts/release_manifest.py` prints a machine-readable snapshot with:

- repository version and Git SHA;
- marketplace plugin list;
- plugin manifest versions;
- pinned MCP runtime versions;
- local MCP server package specs.

Use this manifest as the release evidence and rollback reference. Generated manifests belong in `diagnostics/` or GitHub artifacts, not in normal commits unless explicitly needed for an audit.

## SBOM And Attestation

`scripts/release_sbom.py` generates a lightweight SPDX 2.3 SBOM from plugin manifests and MCP runtime pins. The release workflow also attempts to export GitHub's dependency graph SBOM through the repository API when available. GitHub artifact attestations are generated for the release bundle and generated SBOM on GitHub Enterprise Cloud.

## Dependency Pin Updates

Pinned MCP runtime versions live in `config/mcp-runtime-versions.env` and `plugins/rldyour-mcps/.mcp.json`. Update them intentionally:

```bash
python3 scripts/check_mcp_runtime_versions.py
# edit config/mcp-runtime-versions.env and plugins/rldyour-mcps/.mcp.json
scripts/install_system_codex.sh --apply
scripts/validate_marketplace.sh
scripts/doctor_system_codex.sh
```

Manual CI runs `scripts/check_mcp_runtime_versions.py --fail-on-outdated` through the `dependency-check` workflow or the `validate` workflow's `mcp`/`full` scopes when the owner or agent explicitly requests pin freshness validation.
