# GitHub Branch Protection Desired State

This repository keeps branch protection as documented desired state because the owner is the sole developer and must retain direct access to `main` and `fullrepo`.

## `main`

`main` should reject force pushes and deletions, prefer linear history, and use the CI checks in `.github/branch-protection/main.json` as the normal quality gate. The owner can keep admin bypass enabled to avoid blocking urgent controlled maintenance.

## `fullrepo`

`fullrepo` is not a product branch. It stores portable agent-only context and is published by repository tooling with `--force-with-lease`. Do not require pull requests or status checks on this branch, and do not disable force pushes for the owner.

## Applying Settings

Apply these settings manually in GitHub repository rulesets or branch protection UI. Do not add an automatic workflow that mutates repository settings until a dedicated admin token or GitHub App policy has been reviewed and recorded in an ADR.
