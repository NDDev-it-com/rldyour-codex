---
name: project-instructions-policy
description: "Политика project-инструкций: AGENTS.md, .claude/CLAUDE.md, REVIEW.md, ADRs (MADR 4.0.0). Используй для: правила проекта, инструкции, документация, ADR, долгоживущая документация. EN triggers: project rules, project instructions, ADR, MADR, write durable docs, update AGENTS.md, update CLAUDE.md, instruction policy."
---

# Project Instructions Policy

## Purpose

Keep durable project instructions useful for future Codex sessions without turning them into chat history or generic advice.

## Rules

- Create or update `AGENTS.md` when durable Codex project rules, setup commands, quality gates, architecture constraints, deploy contracts, or workflow guidance change.
- Keep `AGENTS.md` concise because Codex loads it at session start and instruction size matters.
- Create or update `.claude/CLAUDE.md` for fullrepo-managed projects so Claude Code has first-class project memory.
- Keep `.claude/CLAUDE.md` optimized for Claude Code, not as a thin `@AGENTS.md` import.
- Do not create root `CLAUDE.md` by default; `.claude/CLAUDE.md` is the rldyour project memory path.
- Create or update `REVIEW.md` when review-specific rules are durable and materially help future review agents.
- Create ADRs for important architecture, technology, dependency, deployment, security, or irreversible design decisions.
- Repository docs, instructions, ADRs, memories, plans, comments, and commits are English. User-facing conversation with the owner is Russian.
- Do not store secrets, personal tokens, local-only credentials, private cookies, or chat transcripts in docs.

Read `references/project-instructions-and-adrs.md` before creating or updating durable instruction files.
