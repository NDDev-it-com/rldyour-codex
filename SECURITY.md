# Security Policy

## Supported Surface

Security reporting covers this repository's Codex marketplace, plugin manifests, lifecycle hooks, MCP runtime definitions, CI/CD workflows, install/doctor/rollback scripts, release artifacts, and agent-only synchronization tooling.

## Supported Versions

Only the current exact numeric product release tag receives security fixes.
The `1.1.x` line label tracks only the latest released patch, not every
historical patch in the line.

| Version | Supported |
|---|---|
| Current exact tag `1.1.48` | yes |
| Older `1.1.*` tags | no; upgrade to current exact tag |
| Older minor / major lines | no |

## Reporting a Vulnerability

Please report vulnerabilities privately. Do not open public issues or pull requests describing them.

Preferred channel: GitHub Security Advisories.

- https://github.com/NDDev-it-com/rldyour-codex/security/advisories/new

Alternative channel: contact the maintainer through their GitHub profile at https://github.com/rldyourmnd and request a private disclosure handle.

Include:

- affected path, plugin, workflow, or script,
- reproduction steps,
- expected impact and threat scenario,
- non-sensitive logs or command output,
- a suggested fix when known.

Do not paste credentials, tokens, cookies, private keys, browser cookies, OAuth grants, or sensitive logs into reports. If a report requires sharing sensitive material, request a secure channel before sending.

## Response Targets

The maintainer aims for:

- acknowledgement within 5 business days,
- triage and severity assessment within 10 business days,
- a fix or mitigation plan for accepted reports within 30 business days, depending on complexity.

These targets are best-effort and not contractual.

## Baseline Controls

- External GitHub Actions are pinned to full commit SHAs. `scripts/validate_action_pins.py` enforces this in CI.
- CI uses least-privilege `GITHUB_TOKEN` permissions by default. Release jobs request `contents: write`, `id-token: write`, and `attestations: write`. CodeQL jobs request `security-events: write`.
- **GitHub CodeQL** runs on every push and pull request for Python and GitHub Actions languages with the `security-and-quality` query suite.
- **OpenSSF Scorecard** runs weekly and on push to `main` in JSON artifact/check mode, with public results published to `scorecard.dev` for the public Scorecard badge.
- **Dependency Review** runs on pull requests through `actions/dependency-review-action` with `fail-on-severity: high` and a license allow-list compatible with AGPL-3.0-or-later.
- **Dependabot** is enabled for vulnerability alerts and automated security updates, plus a weekly GitHub Actions update schedule.
- **GitHub Secret Scanning** runs automatically for public repositories. Secret
  Scanning Push Protection and related live repository settings are required
  public-adapter controls and are verified from the private root control plane
  when an owner token is available.
- No-paid static security gates use ShellCheck, Pyright, action pin validation, repository text security scanning, CodeQL, Gitleaks, dependency review, and custom repository validators.
- Release bundles use deterministic archives, release manifests, generated SPDX 2.3 SBOMs, GitHub artifact attestations, and (when available) GitHub dependency-graph SBOM export.
- `scripts/scan_text_security.py` scans tracked text and agent-only paths for credential patterns and hidden Unicode controls without printing matched values.
- The full git history was scanned with `gitleaks` (8.30.1) before the public release; 190 commits, 0 leaks found.
- Branch protection on `main` requires all auto-running CI gates to pass before merge, blocks force pushes, blocks branch deletion, and requires linear history.
- SemVer release tags (`X.Y.Z` and `X.Y.Z-pre`) are protected by a repository ruleset against deletion, update, and non-fast-forward push. Only repository administrators can bypass.

## Out Of Scope

- Findings against downstream environments running modified versions of this software.
- Issues stemming from running this repository's owner-standard full-auto permission posture on shared or untrusted machines. The default install profile is `rldyour-yolo` with `approval_policy = "never"` and `sandbox_mode = "danger-full-access"` by maintainer policy; it intentionally does not write an active `default_permissions` permission-profile field while the legacy sandbox dialect is selected. Use `--safe-mode` only when a conservative local override is intentionally required.
- Findings against third-party MCP servers, runtimes, or actions referenced by this repository. Report those upstream.

## Coordinated Disclosure

The maintainer follows coordinated disclosure: a fix is prepared privately, a CVE or GitHub Security Advisory is requested when applicable, and public disclosure happens together with the release that contains the fix or a documented mitigation. Reporters who follow this policy will be credited in the release notes unless they request otherwise.
