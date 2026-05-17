# ADR 0002: Testing And CI Quality Gates

## Status

Accepted.

## Date

2026-05-17.

## Context

The repository had a strong smoke/static validation gate but no conventional unit-test harness or coverage artifact. Audits identified this as a scalability risk because Python helpers such as routing validation, release evidence generation, fullrepo sync, MCP pin checks, and text/action scanners contain reusable state logic.

## Decision

- Add a Python `pytest` and `pytest-cov` harness governed by `pyproject.toml`.
- Keep a 70% repository coverage threshold for the first `0.2.0` hardening release.
- Keep `scripts/validate_marketplace.sh` as the complete local acceptance gate, and run pytest inside it.
- Split CI into a visible unit-test job with JUnit/coverage artifacts and a heavier marketplace/system smoke job.
- Add a no-paid static security workflow using ShellCheck, Pyright, Semgrep CLI, action SHA-pin validation, and text security scanning.
- Exclude Semgrep's global `IFS` tampering rule from the no-paid gate because the repository intentionally uses `IFS=$'\n\t'` as part of its strict shell prologue and relies on ShellCheck plus project validators for shell safety.

## Consequences

- Local failures should usually be diagnosable from targeted unit tests before reaching smoke checks.
- CI spends more minutes, which is acceptable for the owner's GitHub Enterprise Cloud quota.
- Coverage threshold can rise after the highest-risk shell/Python boundaries have dedicated tests.

## Verification

- `uv run --with pytest --with pytest-cov --with pyyaml python -m pytest`
- `scripts/validate_marketplace.sh`
- `.github/workflows/validate.yml`
- `.github/workflows/security-static.yml`
