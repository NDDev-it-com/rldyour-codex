# ADR 0003: Release SBOM And Attestation Policy

## Status

Accepted.

## Date

2026-05-17.

## Context

The marketplace is installed into the owner's global Codex runtime, so release artifacts should be reproducible and inspectable. GitHub Enterprise Cloud supports artifact attestations for private/internal repositories, while GitHub dependency graph SBOM export may depend on repository feature availability.

## Decision

- Release `rldyour-codex` manually from GitHub Actions with `workflow_dispatch`.
- Validate `VERSION`, `CHANGELOG.md`, plugin manifests, routing policy, instruction docs, managed agent metadata, and pytest before publishing.
- Build a deterministic `tar.gz` bundle from tracked repository release paths.
- Generate `release-manifest.json` from repository code.
- Generate a lightweight SPDX 2.3 SBOM from plugin manifests and MCP runtime pins.
- Export the GitHub dependency graph SBOM when the repository endpoint is available, but do not fail the release when that optional export is unavailable.
- Generate GitHub artifact attestations for the release bundle and generated SBOM.

## Consequences

- Release evidence is useful even without paid GitHub security add-ons.
- Private/internal attestation availability depends on GitHub Enterprise Cloud, which the owner confirmed is the working organization context.
- The generated SBOM is intentionally repository-aware; it is not a substitute for a package-manager dependency graph when future package manifests add runtime dependencies.

## Verification

- `.github/workflows/release.yml`
- `python3 scripts/release_manifest.py`
- `python3 scripts/release_sbom.py`
