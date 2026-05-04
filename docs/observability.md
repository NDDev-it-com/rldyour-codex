# Observability

This repository uses lightweight operational observability: deterministic logs, failure artifacts, summaries, and local diagnostic bundles. It does not run a daemon or external telemetry service.

## What To Check First

- `git status -sb`: local repository state.
- `git log --oneline -20`: recent change history.
- `codex mcp list`: registered MCP server names and transports.
- `scripts/doctor_system_codex.sh`: installed system Codex state.
- `scripts/validate_marketplace.sh`: repository-level plugin, skill, MCP, hook, and policy validation.
- `scripts/smoke_clean_bootstrap.sh`: new-machine bootstrap behavior.
- `scripts/sync_fullrepo_branch.sh --status`: agent-only file and `fullrepo` branch state.
- `gh run list --repo rldyourmnd/rldyour-codex --limit 10`: latest CI state.

## Diagnostic Bundle

Run:

```bash
scripts/collect_diagnostics.sh
```

For deeper local validation:

```bash
scripts/collect_diagnostics.sh --include-doctor
```

The script writes a timestamped directory under `diagnostics/`. This directory is intentionally ignored by Git.

## CI Observability

GitHub Actions writes:

- job summaries through `GITHUB_STEP_SUMMARY`;
- failure diagnostic artifacts under `diagnostics/ci`;
- standard workflow logs for validation, doctor, bootstrap, and dependency checks.

The `validate` workflow runs on Ubuntu and macOS because this setup must remain portable across the owner's Linux and macOS machines plus clean CI runners.

## Failure Triage Order

1. Read the failing GitHub Actions job summary.
2. Download the diagnostics artifact if present.
3. Inspect `doctor.txt`, `validate.log`, `codex-mcp-list.txt`, `serena-memory-state.json`, `flow-post-task-state.json`, and `scripts/sync_fullrepo_branch.sh --status` output.
4. Reproduce locally with the exact script that failed.
5. If runtime config is corrupted, use `scripts/rollback_system_codex.sh --list` and dry-run restore before applying.

## Logging Rules

- Do not log environment dumps.
- Do not store secrets, tokens, cookies, OAuth data, or private keys.
- Prefer command outputs that already mask secrets, such as `codex mcp get` and `codex mcp list`.
- Store screenshots and browser artifacts under `browser/`; store diagnostic bundles under `diagnostics/`.
- Do not put diagnostics, screenshots, or secrets into `fullrepo`; it is only for durable agent-only workflow context.
