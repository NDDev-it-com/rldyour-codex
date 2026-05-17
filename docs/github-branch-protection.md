# GitHub Branch Protection Desired State

This repository keeps branch protection as documented desired state because the owner is the sole developer and must retain direct access to `main` and `fullrepo`.

## `main`

`main` should reject force pushes and deletions and prefer linear history. GitHub Actions stay manual-only by owner policy, so `.github/branch-protection/main.json` keeps `required_status_checks` empty and records the current manual validation job names under `manual_validation_checks`. Run those checks only when a task explicitly asks for CI, before a release, or before applying stricter branch rules.

## `fullrepo`

`fullrepo` is not a product branch. It stores portable agent-only context and is published by repository tooling with `--force-with-lease`. Do not require pull requests or status checks on this branch, and do not disable force pushes for the owner.

## Applying Settings

Apply these settings manually in GitHub repository rulesets or branch protection UI. Do not add an automatic workflow that mutates repository settings until a dedicated admin token or GitHub App policy has been reviewed and recorded in an ADR.
