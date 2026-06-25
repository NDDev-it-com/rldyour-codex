# GitHub Branch Protection Desired State

This repository keeps branch protection as documented desired state because the owner is the sole developer and must retain direct access to `main`.

## `main`

`main` should reject force pushes and deletions and prefer linear history. Agent context (`.serena/`, `AGENTS.md`, `.claude/`) is tracked normally on `main` as ordinary source, so there is no separate agent-context branch to protect. GitHub Actions stay manual-only by owner policy, so `.github/branch-protection/main.json` keeps `required_status_checks` empty and records the current manual validation job names under `manual_validation_checks`. Run those checks only when a task explicitly asks for CI, before a release, or before applying stricter branch rules.

## Applying Settings

Apply these settings manually in GitHub repository rulesets or branch protection UI. Do not add an automatic workflow that mutates repository settings until a dedicated admin token or GitHub App policy has been reviewed and recorded in an ADR.
