## Scope

Describe the repository, plugin, workflow, or documentation surface changed.

## Validation

- [ ] `uv run --with pytest --with pytest-cov --with pyyaml python -m pytest`
- [ ] `python3 scripts/validate_action_pins.py`
- [ ] `python3 scripts/scan_text_security.py`
- [ ] `scripts/validate_marketplace.sh`
- [ ] Targeted smoke/checks for the touched scope

## Release And Sync

- [ ] `VERSION` and `CHANGELOG.md` updated when release behavior changes
- [ ] ADR added or updated for durable architecture decisions
- [ ] Serena memories and instruction docs synchronized when behavior changed
- [ ] Agent context (`.serena/`, `AGENTS.md`, `.claude/`) committed on `main` when it changed

## Risk

- [ ] No secrets, tokens, cookies, private keys, or browser evidence committed
- [ ] No unpinned external GitHub Actions
- [ ] No deprecated Codex config aliases introduced
- [ ] No plugin boundary drift
