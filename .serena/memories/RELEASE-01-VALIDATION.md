<!-- Memory Metadata
Last updated: 2026-07-10
Last verified: 2026-07-10
Last commit: b8f326c53ba27dfda4173fb59b7de03191a7b5f6 chore(release): codex 1.8.9 (release_metadata)
Scope: release readiness, versioning, and artifact hygiene
Area: RELEASE
-->

# Release Validation

## Scope
release readiness, versioning, and artifact hygiene

## Current source of truth
- `path:VERSION`
- `path:CHANGELOG.md`
- `path:.github/workflows/release.yml`

## Last verified
- date: 2026-07-10
- commit: `b8f326c53ba27dfda4173fb59b7de03191a7b5f6`
- checked by: Codex adapter 1.8.10 managed update-policy preparation

## Facts
- Current rldyour-codex adapter VERSION is `1.8.10`; the release workflow publishes the matching numeric GitHub Release tag at the released commit. Root `config/repositories.json` and the superproject gitlink own the current adapter HEAD.
- Release `1.8.10` disables Codex startup update checks in every managed config
  so exact, transactional bootstrap upgrades cannot drift into an unrelated
  global npm prefix. It preserves Codex CLI `0.144.1`, CloakBrowser `0.4.10`,
  the mandatory managed browser boundary, approved MCP pins/transports,
  curated GitHub/Gmail plugins, and reusable CI `0.5.1`.
- Non-strict static runtime materialization is portable to macOS Bash 3.2 and
  covered by the 151-test fast gate; strict installed-runtime proof remains a
  separate target-machine check.
- Release automation consumes only a pre-existing signed numeric tag created
  after stable-green branch CI. Tag-push and manual retry paths verify exact
  remote tag peel/ancestry from `origin/main`; workflow dispatch cannot create
  or push tags.
- Release memories record numeric versioning, tags, CI gates, and clean artifact hygiene without copying current control-plane pins.

## Evidence
- `commit:13e997a1f839a753404ac161f69a749276dee18b`
- `commit:4bd04d1837100ecc64530665cdd0fd8c3118697b`
- `commit:b8f326c53ba27dfda4173fb59b7de03191a7b5f6`
- `path:VERSION`
- `path:CHANGELOG.md`
- `path:.github/workflows/release.yml`

## Known pitfalls
- Treat this memory as derived context. Current code, configuration, runtime output, and GitHub state override stale memory text.

## Update policy
Update after verified changes to the referenced source-of-truth files.

## Delete / merge policy
- Delete or merge only when the referenced source-of-truth files no longer support this memory and the replacement memory preserves the durable facts.

## Applies to

- The scope and source-of-truth paths declared in this memory.

## Source of truth

- The `Current source of truth` entries above, plus current code, configuration, tests, git state, and live GitHub state where this memory references live release or repository surfaces.

## Invariants

- Current code, configuration, tests, validators, git state, and live GitHub state override this memory whenever they disagree.

## Current State

- Treat the `Facts` section as the current durable state. Do not treat historical evidence, superseded notes, or previous release entries as current.

## Do Not Infer

- Do not infer runtime versions, product versions, commits, permissions, release state, security posture, or tool behavior from this memory without checking the source of truth.

## Update Triggers

- Update after verified changes to the source-of-truth files, runtime baselines, release tuple, validation gates, live release state, or durable agent-workflow contracts.

## Validation Commands

- Run the rldyour control-plane Serena memory validators in strict mode: `validate_serena_memory_schema` (`--strict-mode strict-all`) and `validate_serena_memory_semantics` (`--strict-current-facts --strict-metadata-dates --strict-evidence-commits`).

## Repair Procedure

1. Re-read the source-of-truth files listed above.
2. Update only verified current facts; move stale facts into historical evidence.
3. Rerun the validation commands until green.
