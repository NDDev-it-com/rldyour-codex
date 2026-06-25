# ADR 0002: Testing And CI Quality Gates

## Status

Accepted.

Superseded in part (1.7.0): the `fullrepo` branch model and its sync helper are retired; agent context is tracked normally on `main`. CI no longer bootstraps, restores, or publishes agent context. The unit-test/coverage gate decision below still stands.

## Date

2026-05-17.

## Context

The repository had a strong smoke/static validation gate but no conventional unit-test harness or coverage artifact. Audits identified this as a scalability risk because Python helpers such as routing validation, release evidence generation, flow post-task state, MCP pin checks, and text/action scanners contain reusable state logic.

## Decision

- Add a Python `pytest` and `pytest-cov` harness governed by `pyproject.toml`.
- Keep a 75% repository coverage threshold for the `0.3.0` runtime-determinism release.
- Keep `scripts/validate_marketplace.sh` as the complete local acceptance gate, and run pytest inside it.
- Add modular gates for agent-driven manual CI: `scripts/validate_fast.sh`, `scripts/validate_runtime.sh`, and `scripts/validate_release.sh`.
- Split manual CI into fast, runtime, release, MCP, and full scopes with Ubuntu
  as the heavy runtime runner, and add lightweight standard public Ubuntu,
  Windows, and macOS smoke for path/archive/metadata portability.
- Keep the no-paid static security workflow manual-only, using ShellCheck, Pyright, action SHA-pin validation, and text security scanning.
- Keep shell safety covered through ShellCheck plus project validators; the repository intentionally uses `IFS=$'\n\t'` as part of its strict shell prologue.
- Keep the upstream repository public and standard-runner-only so normal push,
  PR, scheduled, CodeQL, Scorecard, and dependency-review workflows stay in the
  free public-repository GitHub Actions policy.
- Avoid `pull_request_target`; the labeler runs only on same-repository
  `pull_request` events and skips fork PRs rather than using a privileged
  write-scoped token for untrusted public contributions.

## Consequences

- Local failures should usually be diagnosable from targeted unit tests before reaching smoke checks.
- Public upstream CI does not consume paid private-repository Actions minutes
  while it uses standard public runners. Lightweight macOS and Windows smoke is
  part of the required public/free baseline; heavy runtime and release jobs stay
  Ubuntu-hosted when the local script is OS-independent or the toolchain is
  Linux-oriented.
- Private forks must review the workflow set before enabling Actions because
  private-repository usage is billed to the repository owner.
- Coverage threshold can rise again after the highest-risk shell/Python boundaries have dedicated tests.

## Verification

- `uv run --with pytest --with pytest-cov --with pyyaml python -m pytest`
- `scripts/validate_marketplace.sh`
- `scripts/validate_fast.sh`
- `scripts/validate_runtime.sh`
- `scripts/validate_release.sh`
- `.github/workflows/validate.yml`
- `.github/workflows/security-static.yml`
