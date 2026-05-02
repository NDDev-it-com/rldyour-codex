---
name: web-research
description: "Research current web sources and cite them. Use for посмотри в интернете, изучи интернет, latest/current, найди источники, сравни, подтверди факт ссылками."
---

# Web Research

## Purpose

Give Codex a reliable workflow for internet research: avoid chaotic searching, first define what must be proved or discovered, then choose high-quality sources, read them, and synthesize conclusions.

User-facing conversation stays in Russian unless requested otherwise. Company names, products, APIs, laws, standards, and document titles stay exact.

## Auto Invocation

Use this skill without waiting for an explicit `$web-research` call when the request asks to:

- Research on the internet, search the web, verify current information, or check the latest state.
- Find source-backed facts, citations, authoritative links, or comparisons.
- Research non-technical topics, products, companies, people, market information, legal/security updates, standards, or recommendations.
- Validate a claim where the answer may have changed recently.
- Supplement technical MCP research with changelogs, issue threads, vendor announcements, advisories, pricing, or release notes.

If the request is primarily technical and concerns docs, APIs, frameworks, repository architecture, or GitHub usage patterns, use `tech-research` first and add this skill only when broader web sources are needed.

## When To Use

Use this skill automatically when the user asks to research the internet, verify current information, find sources, compare current data, confirm a fact with links, or gather research before a decision.

If the request is technical and concerns a library, API, framework, open-source repository architecture, or GitHub usage patterns, use `tech-research` first. Add `web-research` when the task needs news, changelogs, issues/discussions, pricing, legal/security docs, recent releases, or sources beyond MCP research.

## Workflow

1. Define scope: what the user wants to solve, what result is needed, and which questions actually block the answer or implementation.
2. Form search hypotheses: which sources should exist, which domains are likely authoritative, and which dates or versions matter.
3. Search in multiple passes: broad query, refined query, and domain-specific query across official sites, repositories, docs, standards, papers, changelogs, or issue trackers.
4. Open and read sources instead of answering from snippets. For unstable topics, compare publication dates, event dates, and the current date.
5. Reject weak sources: SEO aggregators, AI rewrites, unverified posts, and outdated articles when a more primary source exists.
6. Compare sources. If sources conflict, identify the conflict and choose the more reliable source.
7. Synthesize the answer: what was found, how it changes the decision, which constraints remain, and what should happen next.

## Source Priority

For technical and product questions: official documentation, source code, release notes, changelogs, RFCs/specifications, issue/PR/discussion threads in the primary repository, and vendor docs.

For security, legal, financial, and medical topics: use only primary or highly authoritative sources. State that the answer is not a replacement for professional advice when stakes are high.

For recommendations: account for freshness, independent reviews, user constraints, total cost of ownership, and risks.

## Quality Rules

Do not rely on memory when the user explicitly asks for internet research or the topic may have changed. Use web search/browser and cite source links.

Do not copy long source fragments. Summarize concisely and quote only short necessary excerpts.

Separate found facts from your own conclusions. If you infer something from sources, label it as an inference.

If research leads to a code task, proceed to implementation and verification. Research should improve the solution, not replace the work.

## Output

For a standalone research answer, respond in Russian with:

- `Questions`: what was checked.
- `Sources`: which sources were primary and why they are trustworthy.
- `Conclusions`: direct answers without filler.
- `Next steps`: practical actions if needed.

For a code task, keep the final shorter: key findings, code change, verification, and remaining risks.
