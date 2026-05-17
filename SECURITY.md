# Security Policy

## Supported Surface

Security reporting covers this repository's Codex marketplace, plugin manifests, hooks, MCP runtime definitions, CI/CD workflows, install/doctor/rollback scripts, release artifacts, and agent-only synchronization tooling.

## Reporting

Open a private issue or contact the owner directly. Do not paste secrets, tokens, cookies, private keys, or sensitive logs into public issues or pull requests.

Include:

- affected path or workflow,
- reproduction steps,
- expected impact,
- non-sensitive logs or command output,
- suggested fix when known.

## Baseline Controls

- External GitHub Actions must be pinned to full commit SHAs.
- CI uses least-privilege `GITHUB_TOKEN` permissions by default.
- Private-repo CodeQL/code scanning is not required unless GitHub Code Security is available without extra paid add-ons.
- No-paid security gates use ShellCheck, Pyright, Semgrep CLI, action pin validation, text security scanning, and custom repository validators.
- Semgrep excludes only the `bash.lang.security.ifs-tampering.ifs-tampering` rule because the repository intentionally uses `IFS=$'\n\t'` as part of its strict shell prologue and validates shell scripts separately with ShellCheck.
- Release bundles use deterministic archives, release manifests, generated SPDX SBOMs, and GitHub artifact attestations when run on GitHub Enterprise Cloud.
