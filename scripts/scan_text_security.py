#!/usr/bin/env python3
"""Scan repository text files for secret-like patterns and hidden Unicode controls."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("context7-api-key", re.compile(r"ctx7sk-[A-Za-z0-9-]+")),
    ("github-classic-token", re.compile(r"ghp_[A-Za-z0-9_]+")),
    ("github-fine-grained-token", re.compile(r"github_pat_[A-Za-z0-9_]+")),
    ("openai-api-key", re.compile(r"sk-[A-Za-z0-9_-]{16,}")),
    ("slack-token", re.compile(r"xox[baprs]-[A-Za-z0-9-]+")),
    (
        "private-key-header",
        re.compile(r"BEGIN (?:RSA|DSA|EC|OPENSSH|ENCRYPTED|PRIVATE) PRIVATE KEY|BEGIN (?:RSA|DSA|EC|OPENSSH|PRIVATE) KEY"),
    ),
    ("bearer-token", re.compile(r"Bearer\s+[A-Za-z0-9._-]{20,}")),
)

HIDDEN_UNICODE: tuple[tuple[str, str], ...] = (
    ("bidi-control", "[\u202a-\u202e\u2066-\u2069]"),
    ("zero-width-control", "[\u200b\u200c\u200d\ufeff]"),
)

EXTRA_TEXT_PATHS = (
    Path("AGENTS.md"),
    Path(".claude/CLAUDE.md"),
    Path("REVIEW.md"),
    Path(".serena/memories"),
    Path(".serena/plans"),
    Path(".serena/research"),
)

SKIP_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    "__pycache__",
    "browser",
    "diagnostics",
    "node_modules",
}


def tracked_files() -> set[Path]:
    proc = subprocess.run(
        ["git", "ls-files", "-z"],
        check=False,
        capture_output=True,
    )
    if proc.returncode != 0:
        return set()
    return {Path(raw.decode("utf-8")) for raw in proc.stdout.split(b"\0") if raw}


def extra_files() -> set[Path]:
    result: set[Path] = set()
    for path in EXTRA_TEXT_PATHS:
        if path.is_file():
            result.add(path)
        elif path.is_dir():
            result.update(child for child in path.rglob("*") if child.is_file())
    return result


def should_skip(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts)


def read_text(path: Path) -> str | None:
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if b"\0" in raw:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def scan_file(path: Path) -> list[str]:
    text = read_text(path)
    if text is None:
        return []
    findings: list[str] = []
    lines = text.splitlines()

    for name, pattern in SECRET_PATTERNS:
        for line_number, line in enumerate(lines, start=1):
            if pattern.search(line):
                findings.append(f"{path}:{line_number}: potential secret pattern: {name}")

    for name, char_class in HIDDEN_UNICODE:
        pattern = re.compile(char_class)
        for line_number, line in enumerate(lines, start=1):
            if pattern.search(line):
                findings.append(f"{path}:{line_number}: hidden unicode control: {name}")

    return findings


def main() -> int:
    files = sorted(path for path in tracked_files().union(extra_files()) if path.is_file() and not should_skip(path))
    findings: list[str] = []
    for path in files:
        findings.extend(scan_file(path))

    if findings:
        print("\n".join(findings), file=sys.stderr)
        return 1

    print(f"Text security scan passed: {len(files)} files checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
