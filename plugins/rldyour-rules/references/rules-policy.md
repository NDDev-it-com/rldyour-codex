# rldyour Rules Policy

This reference is the source of truth for the owner's general engineering rules.

## Priority Order

1. Safety and repository integrity.
2. Correctness and verified behavior.
3. Clean architecture and long-term scalability.
4. Project consistency and low semantic entropy.
5. Delivery speed.

## Advisory-First Behavior

Rules guide the agent and should be applied automatically inside the current scope. They should not block normal progress through hooks by default.

Hard bans are non-negotiable inside the touched scope:

- No hacks.
- No temporary workarounds.
- No fake implementations.
- No swallowed errors.
- No secrets in code, docs, logs, prompts, screenshots, memories, or commits.
- No fake green checks.

## Technical Debt Outside Scope

When serious technical debt is found outside the task scope:

1. Explain the issue in Russian.
2. Give 2-3 concrete options.
3. Do not expand scope until the owner chooses.

## Sequential Thinking

Use Sequential Thinking MCP for non-trivial decisions when available. Minimum 3 thoughts:

1. Understand the task and constraints.
2. Evaluate options and risks.
3. Decide and define verification.

Use more thoughts for architecture, migrations, security, deployment, and high-risk refactors.

## Semantic Entropy

Low semantic entropy means:

- One concept has one clear location.
- Similar behavior uses similar patterns.
- Names match domain language.
- Public contracts are explicit.
- Integration paths are synchronized.
- Generated artifacts, tests, docs, and memories match code.

## Source-Backed Decisions

Use current official docs and source-backed research for:

- New technologies and dependencies.
- Migrations and major upgrades.
- Framework behavior and compatibility.
- Security-sensitive implementation.
- Architecture decisions with long-term consequences.

## Clean Git History

Use Conventional Commits and one logical concern per commit. Split unrelated
implementation, tests, validators, docs/instructions, license/metadata,
generated artifacts, and Serena knowledge sync when they are independently
reviewable. Adapter implementation changes live in the adapter repository; the
control plane should only advance submodule gitlinks after those commits are
pushed. Do not rewrite already-pushed history without explicit owner approval;
use a follow-up commit for published branches.
