# ADR 0004: Governance And Branch Policy

## Status

Accepted.

Superseded in part (1.7.0): the `fullrepo` agent-only context branch is retired. Agent context is tracked normally on `main` as ordinary source, so `main` is the only governed branch and there is no separate agent-context branch to protect or force-publish.

## Date

2026-05-17.

## Context

The owner is currently the only developer and must keep `main` available without extra approval friction. At the same time, audits recommended documenting branch protection, CODEOWNERS, issue templates, PR validation, and security reporting before the repository grows. (At the time of this ADR a separate `fullrepo` agent-context branch also existed; it was retired in 1.7.0 — see the supersession note above.)

## Decision

- Add lightweight governance files: `CONTRIBUTING.md`, `SECURITY.md`, `CODEOWNERS`, PR template, and issue templates.
- Keep branch protection as desired-state documentation in `.github/branch-protection/*.json` and `docs/github-branch-protection.md`.
- Do not auto-apply repository settings from CI.
- `main` should reject force pushes and deletions when rulesets are applied, while still preserving owner admin access.
- Agent context is tracked on `main`; there is no separate agent-context branch. (Superseded the earlier rule that kept `fullrepo` as an owner-force-published agent-only branch.)

## Consequences

- The repository becomes contributor-ready without imposing process friction on the owner.
- Required status checks can be enabled manually once workflow names are stable in GitHub's UI.
- `main` carries both product source and agent context; a single branch-protection policy covers everything.

## Verification

- `.github/CODEOWNERS`
- `.github/pull_request_template.md`
- `.github/ISSUE_TEMPLATE/*.yml`
- `.github/branch-protection/*.json`
- `docs/github-branch-protection.md`
