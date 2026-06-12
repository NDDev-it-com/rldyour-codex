---
name: dependency-compatibility-policy
description: "Зависимости: latest-compatible, package updates, SLSA, SBOM, lockfiles. Используй для: обнови зависимости. EN: dependency bump."
---

# Dependency Compatibility Policy

## Purpose

Use current, compatible, secure, and maintainable technology choices without blindly chasing `latest`.

## Rules

- Prefer latest compatible stable versions, not unverified latest versions.
- Check official docs, release notes, migration guides, compatibility matrices, and project constraints before changing technology or dependencies.
- Use `rldyour-explore` for technical research when compatibility or current best practice matters.
- Respect lockfiles and package manager conventions. Do not manually edit generated lockfile content unless that is the project-standard workflow.
- SemVer is a signal, not proof. Verify breaking changes against actual public API and runtime behavior.
- Major upgrades require an explicit migration plan, affected-scope analysis, and rollback or fix-forward strategy.
- New production dependencies must have a clear purpose, maintenance signal, license acceptability, security posture, and integration plan.
- Do not add dependencies to avoid writing small project-specific code unless the dependency materially reduces risk or complexity.

Read `references/dependency-policy.md` for detailed dependency selection and upgrade rules.
