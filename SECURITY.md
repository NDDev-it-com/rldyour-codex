# Security Policy

## Supported Surface

Security reporting covers this repository's Codex marketplace, plugin manifests, lifecycle hooks, MCP runtime definitions, CI/CD workflows, install/doctor/rollback scripts, release artifacts, and agent-only synchronization tooling.

## Supported Versions

Only the latest released minor line receives security fixes. Older releases are out of scope.

| Version | Supported |
| --- | --- |
| Latest minor (e.g. `0.4.x`) | Yes |
| Previous releases | No |

## Reporting A Vulnerability

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
- GitHub CodeQL runs on every push and pull request for Python and GitHub Actions languages with `security-and-quality` queries.
- No-paid static security gates use ShellCheck, Pyright, Semgrep CLI, action pin validation, repository text security scanning, and custom repository validators.
- Semgrep excludes only the `bash.lang.security.ifs-tampering.ifs-tampering` rule because the repository intentionally uses `IFS=$'\n\t'` as part of its strict shell prologue and validates shell scripts separately with ShellCheck.
- Release bundles use deterministic archives, release manifests, generated SPDX 2.3 SBOMs, GitHub artifact attestations, and (when available) GitHub dependency-graph SBOM export.
- `scripts/scan_text_security.py` scans tracked text and agent-only paths for credential patterns and hidden Unicode controls without printing matched values.

## Out Of Scope

- Findings against downstream environments running modified versions of this software.
- Issues stemming from running this repository's installer with non-default permission posture on shared or untrusted machines. The default `profile = "rldyour-yolo"` is documented as a maintainer-controlled trusted-machine mode.
- Findings against third-party MCP servers, runtimes, or actions referenced by this repository. Report those upstream.

## Coordinated Disclosure

The maintainer follows coordinated disclosure: a fix is prepared privately, a CVE or GitHub Security Advisory is requested when applicable, and public disclosure happens together with the release that contains the fix or a documented mitigation. Reporters who follow this policy will be credited in the release notes unless they request otherwise.
