---
name: quality-first-engineering
description: "Quality-first engineering: clean, scalable, consistent, no hacks/debt. Используй для: качество, техдолг. EN: clean code, scalable code."
---

# Quality-First Engineering

## Purpose

Apply the owner's default engineering standard: correctness, clean architecture, long-term scalability, low semantic entropy, and consistency over speed.

## Core Rules

- Code is the source of truth. Verify rules, memories, docs, and plans against actual code, diffs, tests, and runtime evidence.
- Quality has priority over delivery speed. Do not choose a shortcut just because it is faster.
- Use Sequential Thinking MCP for non-trivial decisions when available, with at least 3 thoughts before committing to an approach.
- Prefer consistency with existing project patterns. If existing patterns are harmful, explain the risk and ask before widening scope.
- Keep semantic entropy low: one concept should have one clear home, one naming style, one contract, and one implementation pattern unless there is a documented reason.
- Reuse stable code where it already exists. Extract reusable code only after real repeated need is clear.
- Optimize for future change without speculative over-engineering.

## Hard Bans

- No hacks, temporary workarounds, fake implementations, or knowingly deferred debt in the touched scope.
- No swallowed errors. Handle errors at boundaries with meaningful typed or structured messages.
- No secrets, tokens, cookies, private keys, or credentials in code, docs, memories, logs, prompts, screenshots, or commits.
- No fake checks. Never claim tests, lint, type checks, browser checks, security checks, or deploy checks passed unless they were actually run or evidence was collected.
- No unrelated destructive git or filesystem operations.

## Scope Policy

Fix quality issues inside the touched scope and affected integration path. If serious technical debt is found outside scope, stop expanding and ask the user in Russian with 2-3 concrete options.

## Clean Git History

Use Conventional Commits. Keep history logical and inspectable: split unrelated
implementation, tests, validators, docs/instructions, license/metadata,
generated artifacts, and Serena/fullrepo sync into separate commits when they
are independently reviewable. Do not rewrite already-pushed history without
explicit owner approval; use a follow-up commit for published branches.

Read `references/rules-policy.md` when a task requires the full policy.
