---
name: project-instructions-policy
description: "Project instruction documentation rules for Codex. Use automatically when updating or creating AGENTS.md, CLAUDE.md, REVIEW.md, ADRs, project docs, conventions, quality gates, architecture decisions, deploy contracts, durable rules, инструкция проекта, правила проекта, agents.md, claude.md, review.md, ADR, документация."
---

# Project Instructions Policy

## Purpose

Keep durable project instructions useful for future Codex sessions without turning them into chat history or generic advice.

## Rules

- Create or update `AGENTS.md` when durable Codex project rules, setup commands, quality gates, architecture constraints, deploy contracts, or workflow guidance change.
- Keep `AGENTS.md` concise because Codex loads it at session start and instruction size matters.
- Update `CLAUDE.md` when it already exists, when the project explicitly uses Claude Code compatibility, or when the owner asks to create it.
- Do not create generic `CLAUDE.md` in every project by default.
- Create or update `REVIEW.md` when review-specific rules are durable and materially help future review agents.
- Create ADRs for important architecture, technology, dependency, deployment, security, or irreversible design decisions.
- Repository docs, instructions, ADRs, memories, plans, comments, and commits are English. User-facing conversation with the owner is Russian.
- Do not store secrets, personal tokens, local-only credentials, private cookies, or chat transcripts in docs.

Read `references/project-instructions-and-adrs.md` before creating or updating durable instruction files.

