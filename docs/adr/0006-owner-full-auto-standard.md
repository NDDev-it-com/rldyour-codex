# ADR-0006: Owner Full-Auto Standard

## Status

Accepted

## Date

2026-05-21

## Context

The owner has made an explicit product policy decision: YOLO mode, full-auto mode, and dangerously-skip-permissions mode must be available as the standard operating posture across the AI CLI toolchain. The Codex adapter is an owner-controlled configuration repository for the maintainer's trusted local environment, not a general-purpose safe-by-default distribution profile.

The repository still keeps deterministic hooks, execpolicy rules, validation, and doctor checks. Those controls document and verify the intended configuration, but they do not replace the owner's selected full-auto runtime posture.

## Decision

System Codex installs and validates the owner-standard full-auto profile by default:

- `approval_policy = "never"`
- `sandbox_mode = "danger-full-access"`
- `default_permissions = ":danger-full-access"`

Current Codex `--profile rldyour-yolo` startup loads
`$CODEX_HOME/rldyour-yolo.config.toml`; the installer must write that profile
file and must not write removed legacy `profile = "..."` selectors or
`[profiles.*]` tables.

The aliases `yolo`, `full-auto`, and `dangerously-skip-permissions` all refer to this owner-standard posture.

`scripts/install_system_codex.sh --apply --safe-mode` remains as an explicit conservative override for local experiments or constrained environments. Safe mode is not the default and must not be described as the canonical operating mode for this repository.

## Consequences

- The installer and doctor must default to the full-auto profile and validate it.
- `config/rldyour-contract.json` is the machine-readable policy source for this posture.
- `scripts/validate_contract.py` must fail if the repository drifts back to safe-default language or behavior.
- Running the default profile on shared, untrusted, or hostile machines is outside the repository's intended operating model.

## Verification

- `scripts/install_system_codex.sh`
- `scripts/doctor_system_codex.sh`
- `config/rldyour-contract.json`
- `scripts/validate_contract.py`
- `docs/contract-matrix.md`
