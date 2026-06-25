# Dependency Update Checks

Pinned runtime versions keep MCP startup reproducible. Update checks are intentionally separate from normal validation so the main workflow does not mutate runtime state.

## Pinned Sources

- `config/mcp-runtime-versions.env`: named version variables.
- `plugins/rldyour-mcps/.mcp.json`: actual MCP launcher package specs consumed by the installer.
- `.github/dependabot.yml`: GitHub Actions dependency update configuration.

`scripts/validate_marketplace.sh` enforces parity between `config/mcp-runtime-versions.env` and local MCP launcher package specs in `.mcp.json`.

`dart-flutter` is the explicit exception: it runs through the local Dart SDK and is declared as `DART_FLUTTER_MCP_RUNTIME=external-local-dart-sdk` instead of a package-version pin.

## Local Check

```bash
python3 scripts/check_mcp_runtime_versions.py
python3 scripts/validate_runtime_prereqs.py --strict --require-codex
```

To fail when any known pin is stale:

```bash
python3 scripts/check_mcp_runtime_versions.py --fail-on-outdated
```

## Update Flow

1. Run the check and inspect upstream versions.
2. Read upstream release notes for every changed package.
3. Update both `config/mcp-runtime-versions.env` and `plugins/rldyour-mcps/.mcp.json`.
4. For GitHub Actions, resolve the new tag to a full commit SHA, pin `uses:` to that SHA, and keep the tag as an inline comment for review.
5. Reinstall into system Codex with `scripts/install_system_codex.sh --apply --strict-runtime`.
6. Run `scripts/validate_fast.sh`, `scripts/validate_runtime.sh --strict-runtime`, and `scripts/validate_release.sh`.
7. Commit the runtime pin update separately from unrelated workflow changes.

## CI

The `dependency-check` workflow is manual-only. Run it when a task explicitly asks for CI/dependency validation or before a release that changes runtime pins.

`validate.yml` also runs `scripts/check_mcp_runtime_versions.py --fail-on-outdated --json` in the `dependency-pins` job for the manual `mcp` and `full` scopes. This keeps pin drift visible without spending GitHub Actions minutes on every push.
