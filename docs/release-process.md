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
scripts/validate_marketplace.sh
scripts/doctor_system_codex.sh
scripts/smoke_local_git_guard.sh
scripts/smoke_clean_bootstrap.sh
scripts/smoke_fullrepo_sync.sh
scripts/sync_fullrepo_branch.sh --status
python3 scripts/release_manifest.py > diagnostics/release-manifest.json
```

6. Commit with a Conventional Commit message.
7. Push to `main`, publish `fullrepo` when agent-only files changed, and wait for CI on Ubuntu and macOS.
8. Tag only after CI is green:

```bash
version=$(cat VERSION)
git tag -a "v${version}" -m "Release ${version}"
git push origin "v${version}"
```

## Release Manifest

`scripts/release_manifest.py` prints a machine-readable snapshot with:

- repository version and Git SHA;
- marketplace plugin list;
- plugin manifest versions;
- pinned MCP runtime versions;
- local MCP server package specs.

Use this manifest as the release evidence and rollback reference. Generated manifests belong in `diagnostics/` or GitHub artifacts, not in normal commits unless explicitly needed for an audit.

## Dependency Pin Updates

Pinned MCP runtime versions live in `config/mcp-runtime-versions.env` and `plugins/rldyour-mcps/.mcp.json`. Update them intentionally:

```bash
python3 scripts/check_mcp_runtime_versions.py
# edit config/mcp-runtime-versions.env and plugins/rldyour-mcps/.mcp.json
scripts/install_system_codex.sh --apply
scripts/validate_marketplace.sh
scripts/doctor_system_codex.sh
scripts/smoke_clean_bootstrap.sh
```

Scheduled CI runs `scripts/check_mcp_runtime_versions.py --fail-on-outdated` to surface stale pins.
