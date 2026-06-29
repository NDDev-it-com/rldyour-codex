#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SECRET_RE = re.compile(
    r"ctx7sk-[A-Za-z0-9-]+|"
    r"ghp_[A-Za-z0-9_]+|"
    r"github_pat_[A-Za-z0-9_]+|"
    r"sk-[A-Za-z0-9_-]{16,}|"
    r"xox[baprs]-[A-Za-z0-9-]+|"
    r"BEGIN (?:RSA|OPENSSH|PRIVATE) KEY|"
    r"Bearer\s+[A-Za-z0-9._-]{20,}"
)

CODEX_DOC = "AGENTS.md"
CLAUDE_DOC = ".claude/CLAUDE.md"
LEGACY_CLAUDE_DOC = "CLAUDE.md"
ACTIVE_DOCS = (
    CODEX_DOC,
    CLAUDE_DOC,
    "README.md",
    "docs/contract-matrix.md",
    "system/AGENTS.md",
)
RESEARCH_DIR = ".serena/research"
FORBIDDEN_ACTIVE_CLAIMS = {
    "[features].plugin_hooks = true": "Codex 0.134 treats plugin_hooks as a removed feature flag",
    "features.plugin_hooks = true": "Codex 0.134 treats plugin_hooks as a removed feature flag",
    "requires `[features].plugin_hooks = true`": "plugin_hooks is removed in current Codex",
    "forces `plugin_hooks = true`": "plugin_hooks is removed in current Codex",
    "active `hooks`, `plugin_hooks`, and `multi_agent`": "plugin hooks are verified through hooks/list, not an active feature flag",
    "active hooks, plugin_hooks, and multi_agent": "plugin hooks are verified through hooks/list, not an active feature flag",
    ":danger-no-sandbox": "current Codex built-ins use :danger-full-access for the danger profile",
    "currently pinned at v1.15.4": "active current-pin wording must match the current OpenCode baseline",
}


def run_state(root: Path) -> dict[str, object]:
    script = root / "plugins/rldyour-flow/scripts/instruction_docs_state.py"
    if not script.is_file():
        script = Path(__file__).resolve().parents[1] / "plugins/rldyour-flow/scripts/instruction_docs_state.py"
    if not script.is_file():
        raise RuntimeError(f"missing {script}")
    proc = subprocess.run(
        ["python3", str(script), "--root", str(root), "--json"],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "instruction docs state failed")
    return json.loads(proc.stdout)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def validate_file_content(root: Path, relative: str, errors: list[str], warnings: list[str]) -> None:
    path = root / relative
    if not path.is_file():
        return
    text = read_text(path)
    lines = text.splitlines()
    if SECRET_RE.search(text):
        errors.append(f"{relative}: contains secret-looking content")
    for needle, reason in FORBIDDEN_ACTIVE_CLAIMS.items():
        if needle in text:
            errors.append(f"{relative}: forbidden active claim {needle!r}: {reason}")
    if relative == CODEX_DOC:
        if len(lines) > 260:
            warnings.append(f"{relative}: {len(lines)} lines; keep Codex instructions compact")
        for term in ("Codex", "Validation", "Git"):
            if term not in text:
                warnings.append(f"{relative}: expected high-signal section or term {term!r}")
        if "Claude Code" in text and ".claude/CLAUDE.md" not in text:
            warnings.append(f"{relative}: mentions Claude Code without pointing to .claude/CLAUDE.md")
    elif relative == CLAUDE_DOC:
        if len(lines) > 220:
            warnings.append(f"{relative}: {len(lines)} lines; Claude recommends targeting about 200 lines")
        for term in ("Claude Code", "Validation", "Git"):
            if term not in text:
                warnings.append(f"{relative}: expected Claude-specific section or term {term!r}")
        non_empty = [line.strip() for line in lines if line.strip()]
        if non_empty and non_empty[0] == "@AGENTS.md" and len(non_empty) < 8:
            errors.append(f"{relative}: must be first-class Claude Code memory, not only @AGENTS.md")


def validate_research_content(root: Path, errors: list[str], warnings: list[str]) -> None:
    research_root = root / RESEARCH_DIR
    if not research_root.is_dir():
        return
    for path in sorted(research_root.glob("*.md")):
        relative = path.relative_to(root).as_posix()
        text = read_text(path)
        header = "\n".join(text.splitlines()[:16])
        superseded = "SUPERSEDED ON" in header
        for needle, reason in FORBIDDEN_ACTIVE_CLAIMS.items():
            if needle not in text:
                continue
            if superseded:
                warnings.append(f"{relative}: contains superseded historical claim {needle!r}: {reason}")
            else:
                errors.append(
                    f"{relative}: stale research claim {needle!r} requires a SUPERSEDED banner or rewrite: {reason}"
                )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate rldyour AGENTS.md and .claude/CLAUDE.md policy.")
    parser.add_argument("--root", default=".", help="Repository root to inspect.")
    parser.add_argument("--require-agent-docs", action="store_true", help="Require AGENTS.md and .claude/CLAUDE.md.")
    parser.add_argument("--json", action="store_true", help="Emit JSON report.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    try:
        state = run_state(root)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    missing_docs = state.get("missing_docs", [])
    if args.require_agent_docs:
        if isinstance(missing_docs, list):
            errors.extend(f"{path}: required agent instruction doc is missing" for path in missing_docs)
        for relative in (CODEX_DOC, CLAUDE_DOC):
            if not (root / relative).is_file():
                errors.append(f"{relative}: required agent instruction doc is missing")

    if (root / LEGACY_CLAUDE_DOC).is_file():
        errors.append(f"{LEGACY_CLAUDE_DOC}: use .claude/CLAUDE.md for Claude Code project memory")

    for relative in ACTIVE_DOCS:
        validate_file_content(root, relative, errors, warnings)
    validate_research_content(root, errors, warnings)

    payload = {
        "state": state,
        "errors": errors,
        "warnings": warnings,
        "ok": not errors,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for warning in warnings:
            print(f"warning: {warning}", file=sys.stderr)
        if errors:
            print("\n".join(errors), file=sys.stderr)
        else:
            print("instruction docs validation passed")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
