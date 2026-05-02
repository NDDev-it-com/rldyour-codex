# Dependency Update Checks

Pinned runtime versions keep MCP startup reproducible. Update checks are intentionally separate from normal validation so the main workflow does not mutate runtime state.

## Pinned Sources

- `config/mcp-runtime-versions.env`: named version variables.
- `plugins/rldyour-mcps/.mcp.json`: actual MCP launcher package specs consumed by the installer.
- `.github/dependabot.yml`: GitHub Actions dependency update configuration.

## Local Check

```bash
python3 scripts/check_mcp_runtime_versions.py
```

To fail when any known pin is stale:

```bash
python3 scripts/check_mcp_runtime_versions.py --fail-on-outdated
```

## Update Flow

1. Run the check and inspect upstream versions.
2. Read upstream release notes for every changed package.
3. Update both `config/mcp-runtime-versions.env` and `plugins/rldyour-mcps/.mcp.json`.
4. Reinstall into system Codex with `scripts/install_system_codex.sh --apply`.
5. Run `scripts/validate_marketplace.sh`, `scripts/doctor_system_codex.sh`, and `scripts/smoke_clean_bootstrap.sh`.
6. Commit the runtime pin update separately from unrelated workflow changes.

## CI

The `dependency-check` workflow runs weekly and through manual dispatch. It reports stale pinned MCP packages before they silently drift away from current upstream releases.
