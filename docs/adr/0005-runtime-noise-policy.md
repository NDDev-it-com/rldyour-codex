# ADR 0005: Runtime Noise Policy

## Status

Accepted.

## Date

2026-05-17.

## Context

Codex, MCP, browser, LSP, and security-tool runtimes can emit stderr lines that are either real regressions or benign third-party advisories. The owner wants a clean/ideal operating surface without fake green checks or brittle CI failures caused by known external chatter.

## Decision

- Treat new stderr/log chatter as a quality signal.
- Classify known benign third-party runtime messages through `scripts/classify_ci_noise.py`.
- Fail strict CI noise checks on unknown lines in targeted jobs, while keeping allowlist entries narrow and documented in code.
- Do not hide stderr by redirecting it to `/dev/null`.

## Consequences

- New warnings become visible and actionable.
- Known benign tool noise remains documented rather than normalized as unexplained CI spam.
- The allowlist requires maintenance when upstream tools change wording.

## Verification

- `python3 scripts/classify_ci_noise.py --strict <log-file>`
- `tests/unit/test_classify_ci_noise.py`
- `.github/workflows/validate.yml`
