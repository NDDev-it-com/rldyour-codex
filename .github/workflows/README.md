# GitHub Actions Workflows

Ten workflows provide the public/free CI surface for the Codex adapter. The
repository is public, so standard GitHub-hosted runners do not consume the
owner's private-repository Actions minutes. Keep every workflow on standard
runner labels and keep third-party actions pinned to full commit SHAs.

## Required PR Gates

| Workflow | Purpose |
| --- | --- |
| `validate.yml` | Fast validation and optional runtime/release/MCP scopes on Ubuntu standard runners. |
| `cross-platform.yml` | Lightweight metadata/path smoke on standard Ubuntu, Windows, and macOS public runners. |
| `security-static.yml` | Action pin validation, actionlint, text security scan, ShellCheck, Pyright, Semgrep. |
| `secret-scan.yml` | Gitleaks history scan for accidental secrets. |
| `codeql.yml` | CodeQL code scanning for the adapter source surface. |
| `dependency-review.yml` | Pull-request dependency diff review. |

## Supply-Chain And Drift Gates

| Workflow | Trigger | Purpose |
| --- | --- | --- |
| `scorecard.yml` | push, weekly, manual, branch-protection changes | OpenSSF Scorecard SARIF and code-scanning upload. |
| `dependency-check.yml` | daily, config changes, manual | MCP/runtime pin freshness and dependency report. |
| `labeler.yml` | pull requests | Unprivileged PR labels, skipped for forks. |

## Release Gate

| Workflow | Trigger | Purpose |
| --- | --- | --- |
| `release.yml` | numeric product tag or manual dispatch | Release validation, deterministic bundle, SBOM, attestations, GitHub Release. |

## Cost Policy

- Public adapter CI must stay on standard GitHub-hosted runner labels only.
- No self-hosted, larger, runner-group, ARC, private organization, or paid-size
  runner labels.
- The public/free baseline includes one lightweight cross-platform workflow on
  standard Ubuntu, Windows, and macOS runners. Runtime-heavy and release jobs
  may stay Ubuntu-only when the local script is OS-independent or the required
  toolchain is Linux-only.
- Workflow artifacts must set explicit retention and stay at or below 30 days.
- Heavy or drift-oriented checks use schedules/manual dispatch where practical.
