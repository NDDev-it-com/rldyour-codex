#!/usr/bin/env python3
"""Validate that external GitHub Actions are pinned to full commit SHAs."""

from __future__ import annotations

import re
import sys
from pathlib import Path

USES_RE = re.compile(r"^(?P<indent>\s*)(?:-\s*)?uses:\s*(?P<value>[^#\s]+)")
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE)


def workflow_files() -> list[Path]:
    roots = [Path(".github/workflows"), Path(".github/actions")]
    files: list[Path] = []
    for root in roots:
        if root.is_dir():
            files.extend(sorted(root.rglob("*.yml")))
            files.extend(sorted(root.rglob("*.yaml")))
    return sorted(dict.fromkeys(files))


def is_external_action(value: str) -> bool:
    return not (
        value.startswith("./")
        or value.startswith("../")
        or value.startswith("docker://")
    )


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        match = USES_RE.match(line)
        if not match:
            continue
        value = match.group("value").strip("\"'")
        if not is_external_action(value):
            continue
        if "@" not in value:
            errors.append(f"{path}:{line_number}: external action must include @<full-sha>: {value}")
            continue
        _, ref = value.rsplit("@", 1)
        if not FULL_SHA_RE.fullmatch(ref):
            errors.append(f"{path}:{line_number}: external action must be pinned to a 40-char commit SHA: {value}")
    return errors


def main() -> int:
    files = workflow_files()
    if not files:
        print("No GitHub workflow/action files found")
        return 0

    errors: list[str] = []
    for path in files:
        errors.extend(validate_file(path))

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"GitHub Actions pinned by full SHA: {len(files)} files checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
