#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAX_SINGLE_BYTES = 10 * 1024
DEFAULT_MAX_COMBINED_BYTES = 24 * 1024
DEFAULT_WARN_COMBINED_BYTES = 20 * 1024

SYSTEM_DOC = "system/AGENTS.md"
PROJECT_DOC = "AGENTS.md"
REQUIRED_TERMS = {
    SYSTEM_DOC: (
        "rldyour-flow",
        "rldyour-serena-mcp",
        "sandbox_mode",
        "default_permissions",
    ),
    PROJECT_DOC: (
        "scripts/validate_marketplace.sh",
        "scripts/codex_openai_metadata_policy.py",
        "plugins/rldyour-mcps/.mcp.json",
        "AGPL-3.0-or-later",
    ),
}


def byte_len(path: Path) -> int:
    return len(path.read_bytes())


def validate_budget(
    root: Path,
    *,
    max_single_bytes: int = DEFAULT_MAX_SINGLE_BYTES,
    max_combined_bytes: int = DEFAULT_MAX_COMBINED_BYTES,
    warn_combined_bytes: int = DEFAULT_WARN_COMBINED_BYTES,
    require_project_agents: bool = False,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    present: list[tuple[str, Path, int]] = []

    for relative in (SYSTEM_DOC, PROJECT_DOC):
        path = root / relative
        if not path.is_file():
            if relative == SYSTEM_DOC or require_project_agents:
                errors.append(f"{relative}: required Codex instruction doc is missing")
            continue
        size = byte_len(path)
        present.append((relative, path, size))
        if size > max_single_bytes:
            errors.append(f"{relative}: {size} bytes exceeds {max_single_bytes} byte single-doc budget")
        text = path.read_text(encoding="utf-8", errors="replace")
        for term in REQUIRED_TERMS[relative]:
            if term not in text:
                errors.append(f"{relative}: missing required compact routing term {term!r}")

    combined = sum(size for _, _, size in present)
    if combined > max_combined_bytes:
        errors.append(f"combined AGENTS context: {combined} bytes exceeds {max_combined_bytes} byte budget")
    elif combined > warn_combined_bytes:
        warnings.append(f"combined AGENTS context: {combined} bytes is above {warn_combined_bytes} byte warning budget")

    return errors, warnings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Codex AGENTS.md context budget.")
    parser.add_argument("--root", default=ROOT)
    parser.add_argument("--max-single-bytes", type=int, default=DEFAULT_MAX_SINGLE_BYTES)
    parser.add_argument("--max-combined-bytes", type=int, default=DEFAULT_MAX_COMBINED_BYTES)
    parser.add_argument("--warn-combined-bytes", type=int, default=DEFAULT_WARN_COMBINED_BYTES)
    parser.add_argument("--require-project-agents", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors, warnings = validate_budget(
        Path(args.root).resolve(),
        max_single_bytes=args.max_single_bytes,
        max_combined_bytes=args.max_combined_bytes,
        warn_combined_bytes=args.warn_combined_bytes,
        require_project_agents=args.require_project_agents,
    )
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    if errors:
        print("validate_agents_context_budget.py: validation FAILED", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 1
    print("validated Codex AGENTS context budget")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
