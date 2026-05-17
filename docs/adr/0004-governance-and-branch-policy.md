# ADR 0004: Governance And Branch Policy

## Status

Accepted.

## Date

2026-05-17.

## Context

The owner is currently the only developer and must keep `main` and `fullrepo` available without extra approval friction. At the same time, audits recommended documenting branch protection, CODEOWNERS, issue templates, PR validation, and security reporting before the repository grows.

## Decision

- Add lightweight governance files: `CONTRIBUTING.md`, `SECURITY.md`, `CODEOWNERS`, PR template, and issue templates.
- Keep branch protection as desired-state documentation in `.github/branch-protection/*.json` and `docs/github-branch-protection.md`.
- Do not auto-apply repository settings from CI.
- `main` should reject force pushes and deletions when rulesets are applied, while still preserving owner admin access.
- `fullrepo` remains an agent-only context branch and must allow owner-controlled `--force-with-lease` publishing.

## Consequences

- The repository becomes contributor-ready without imposing process friction on the owner.
- Required status checks can be enabled manually once workflow names are stable in GitHub's UI.
- `fullrepo` remains intentionally different from product/source branches.

## Verification

- `.github/CODEOWNERS`
- `.github/pull_request_template.md`
- `.github/ISSUE_TEMPLATE/*.yml`
- `.github/branch-protection/*.json`
- `docs/github-branch-protection.md`
