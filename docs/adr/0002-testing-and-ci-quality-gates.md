# ADR 0002: Testing And CI Quality Gates

## Status

Accepted.

## Date

2026-05-17.

## Context

The repository had a strong smoke/static validation gate but no conventional unit-test harness or coverage artifact. Audits identified this as a scalability risk because Python helpers such as routing validation, release evidence generation, fullrepo sync, MCP pin checks, and text/action scanners contain reusable state logic.

## Decision

- Add a Python `pytest` and `pytest-cov` harness governed by `pyproject.toml`.
- Keep a 75% repository coverage threshold for the `0.3.0` runtime-determinism release.
- Keep `scripts/validate_marketplace.sh` as the complete local acceptance gate, and run pytest inside it.
- Add modular gates for agent-driven manual CI: `scripts/validate_fast.sh`, `scripts/validate_runtime.sh`, and `scripts/validate_release.sh`.
- Split manual CI into fast, runtime, release, MCP, and full scopes with Ubuntu as the default runner and opt-in macOS parity.
- Keep the no-paid static security workflow manual-only, using ShellCheck, Pyright, Semgrep CLI, action SHA-pin validation, and text security scanning.
- Exclude Semgrep's global `IFS` tampering rule from the no-paid gate because the repository intentionally uses `IFS=$'\n\t'` as part of its strict shell prologue and relies on ShellCheck plus project validators for shell safety.

## Consequences

- Local failures should usually be diagnosable from targeted unit tests before reaching smoke checks.
- CI spends minutes only when the owner or agent explicitly requests a workflow run. macOS coverage remains available but opt-in because it is much more expensive than Ubuntu.
- Coverage threshold can rise again after the highest-risk shell/Python boundaries have dedicated tests.

## Verification

- `uv run --with pytest --with pytest-cov --with pyyaml python -m pytest`
- `scripts/validate_marketplace.sh`
- `scripts/validate_fast.sh`
- `scripts/validate_runtime.sh`
- `scripts/validate_release.sh`
- `.github/workflows/validate.yml`
- `.github/workflows/security-static.yml`
