<!-- Memory Metadata
Last updated: 2026-05-30
Last verified: 2026-05-30
Last commit: 49803c423a7111b5fa4166334db59fb491dcf2c0 fix: skip GitHub MCP smoke without token
Scope: verified current technical debt
Area: TECHDEBT
-->

# TECHDEBT-01-NOW

## Scope
verified current technical debt

## Current source of truth
- `path:README.md`
- `path:CHANGELOG.md`


## Source Of Truth
- `path:README.md`
- `path:CHANGELOG.md`

## Last verified
- date: 2026-05-30
- commit: `49803c423a7111b5fa4166334db59fb491dcf2c0`
- checked by: Codex ry-start automated release and metadata sync

## Facts
- Current Codex product/config version is `1.1.11`; root control-plane pins must
  reference commit `49803c423a7111b5fa4166334db59fb491dcf2c0`, and plugin
  manifest versions must match the adapter `VERSION`.
- The audited marketplace metadata blocker is closed in current source:
  `scripts/codex_openai_metadata_policy.py` is the shared policy for direct
  and marketplace validation, all `agents/openai.yaml` routing metadata is
  compact/Russian-first/English-compatible, and
  `bash scripts/validate_marketplace.sh` passes.
- The audited Codex `plugin_hooks`, MCP freshness, public-CI instruction-doc,
  runtime-smoke, surface-adoption, public metadata, Dependabot cadence, and CI
  classifier debts are closed in current source-of-truth files.
- `scripts/validate_instruction_docs.py`, `check_mcp_runtime_versions.py`,
  `scripts/validate_fast.sh`, `scripts/validate_runtime.sh`, and
  `scripts/smoke_codex_hooks_migration.sh` are the active gates for the closed
  debt classes recorded by this memory.
- Remaining debt should be recorded here only when current code/config evidence
  proves it is still open.

## Evidence
- `commit:49803c423a7111b5fa4166334db59fb491dcf2c0`
- `path:README.md`
- `path:CHANGELOG.md`
- `path:references/codex-surface-adoption.md`
- `path:CONTRIBUTING.md`
- `path:scripts/validate_instruction_docs.py`
- `path:config/mcp-runtime-versions.env`
- `path:scripts/validate_fast.sh`
- `path:scripts/validate_runtime.sh`
- `path:scripts/install_system_codex.sh`
- `path:scripts/smoke_codex_hooks_migration.sh`

## Known pitfalls
- Treat this memory as derived context. Current code, configuration, runtime output, and GitHub state override stale memory text.

## Historical evidence
- Historical OpenAI skill metadata compactness drift was closed at adapter
  `1.1.5` and commit `b64239591f7e6af0c5d6a7682039a8b45683732a`.
- Historical `plugin_hooks` active-doc drift was closed by the
  `.claude/CLAUDE.md` fullrepo update and by tracked active-doc forbidden-claim
  validation in `scripts/validate_instruction_docs.py`.
- Historical Chrome DevTools MCP freshness drift was closed for Codex at
  `chrome-devtools-mcp@1.1.1`.
- Historical public-CI instruction-doc requirement mismatch was closed when
  `validate_fast.sh` began requiring agent-only instruction docs only when
  those files are restored locally/fullrepo.
- Historical runtime-smoke classification debt was closed when
  `scripts/validate_runtime.sh` gained explicit `auto`, `static`, `installed`,
  and `live` lanes.
- Historical version synchronization debt was closed at adapter `1.0.2` and
  commit `2a852698661384a3ba4497c4ea2c98111d941965`.
- Historical CodeQL action freshness debt was closed at `github/codeql-action`
  `v4.36.0`; Dependabot GitHub Actions version updates were grouped into one
  reviewable PR.
- Historical nested legacy profile table drift was closed by
  `d7909f83ae7ec947946f374ffae99af37db5335a`.
- Historical Codex surface-adoption matrix debt was closed by
  `references/codex-surface-adoption.md` at
  `2172b16855bd550f580f4a631601953e3a956083`.
- Historical public metadata wording drift was closed at
  `d35c3c90d7341d5ab9c94b868bfe47bb41858c74`.
- Historical Semgrep MCP freshness drift was closed for Codex at
  `semgrep==1.164.0`, and shadcn MCP freshness was closed at `shadcn@4.8.2`.

## Update policy
Update after verified changes to the referenced source-of-truth files.

## Delete / merge policy
- Delete or merge only when the referenced source-of-truth files no longer support this memory and the replacement memory preserves the durable facts.

## Cross-References
- `CORE-01-INDEX.md`
- `CONTEXT-01-CORE.md`
- `PATTERNS-01-CANONICAL.md`

## Applies to
- The scope declared in this memory and the source-of-truth paths listed below.

## Invariants
- Code, configuration, tests, and git state override this memory when they disagree.

## Current State
- See `Facts` for current durable facts. Do not treat `Historical evidence` or old commit notes as current state.

## Do Not Infer
- Do not infer runtime versions, product versions, commits, permissions, release state, or tool behavior from this memory without checking the source of truth.

## Update Triggers
- Update after verified changes to the source-of-truth files, runtime baselines, release tuple, validation gates, or durable agent workflow contracts.

## Validation Commands
- `python3 scripts/validate_serena_memory_schema.py --scope all --strict-mode strict-all`
- `python3 scripts/validate_serena_memory_semantics.py --scope all --strict-current-facts`
- `python3 scripts/validate_memory_freshness.py --scope all`

## Repair Procedure
- Re-read source-of-truth files, update only verified current facts, move stale facts to historical evidence, then rerun the validation commands.
