# Contributing

This repository is an owner-controlled Codex marketplace. Changes should preserve the plugin boundaries, runtime pins, validation gates, and agent-only `fullrepo` workflow.

## Local Setup

Required tools: Git, Python 3.13, uv, Node/npm, Bun, Dart, jq, ripgrep, shellcheck, and Codex CLI.

```bash
uv run --with pytest --with pytest-cov --with pyyaml python -m pytest
python3 scripts/validate_action_pins.py
python3 scripts/scan_text_security.py
scripts/validate_marketplace.sh
```

Use the devcontainer when you need a clean, production-like local validation environment.

## Change Rules

- Keep repository artifacts in English.
- Do not commit secrets, tokens, cookies, private keys, browser artifacts, diagnostics, or runtime caches.
- Keep `rldyour-mcps` transport-only.
- Keep external GitHub Actions pinned to full commit SHAs.
- Add or update ADRs for non-trivial architecture, release, CI, hook, MCP, or governance decisions.
- Update `VERSION` and `CHANGELOG.md` for release behavior changes.
- Update Serena memories and instruction docs from verified code/config facts after durable workflow changes.

## Branches

Use feature or release branches for implementation. `main` remains the normal source branch. `fullrepo` carries portable agent-only context and is published with `--force-with-lease` by the repository tooling.
