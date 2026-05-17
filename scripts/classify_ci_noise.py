#!/usr/bin/env python3
"""Classify stderr/log noise so CI can fail on new unexpected runtime chatter."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class NoiseRule:
    name: str
    pattern: re.Pattern[str]
    reason: str


BENIGN_RULES: tuple[NoiseRule, ...] = (
    NoiseRule(
        "terminalinfo-wezterm-fallback",
        re.compile(r"No entry for terminal type \"wezterm\";|using dumb terminal settings\."),
        "Python terminal metadata warning in local noninteractive runners.",
    ),
    NoiseRule(
        "uv-environment-setup",
        re.compile(r"Using CPython \d+\.\d+\.\d+|Removed virtual environment at:|Creating virtual environment at:|Installed \d+ packages? in"),
        "uv may report environment setup to stderr while preparing an isolated test runtime.",
    ),
    NoiseRule(
        "chrome-devtools-localstorage",
        re.compile(r"chrome-devtools.*localstorage|localstorage-file", re.IGNORECASE),
        "Chrome DevTools MCP warns about optional local storage in ephemeral CI.",
    ),
    NoiseRule(
        "semgrep-pro-engine-advisory",
        re.compile(r"Pro Engine|Semgrep Pro", re.IGNORECASE),
        "Semgrep community runtime can print a non-blocking Pro Engine advisory.",
    ),
    NoiseRule(
        "serena-lsp-configuration",
        re.compile(r"workspace/configuration|taplo.*catalog|language server.*configuration", re.IGNORECASE),
        "Known LSP capability warning from third-party language servers.",
    ),
)


def read_log(paths: list[Path]) -> list[str]:
    if not paths:
        return sys.stdin.read().splitlines()

    lines: list[str] = []
    for path in paths:
        try:
            lines.extend(path.read_text(encoding="utf-8", errors="replace").splitlines())
        except OSError as exc:
            raise SystemExit(f"failed to read {path}: {exc}") from exc
    return lines


def classify_line(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped:
        return ("empty", "blank log line")
    for rule in BENIGN_RULES:
        if rule.pattern.search(stripped):
            return (rule.name, rule.reason)
    return None


def classify_lines(lines: list[str]) -> tuple[list[str], list[str]]:
    benign: list[str] = []
    unknown: list[str] = []
    for line in lines:
        classification = classify_line(line)
        if classification is None:
            unknown.append(line)
        elif classification[0] != "empty":
            benign.append(f"{classification[0]}: {line}")
    return benign, unknown


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="Log files to classify. Reads stdin when omitted.")
    parser.add_argument("--strict", action="store_true", help="Fail when unknown non-empty log lines are present.")
    args = parser.parse_args()

    lines = read_log(args.paths)
    benign, unknown = classify_lines(lines)

    if benign:
        print(f"Known benign noise lines: {len(benign)}")
        for line in benign:
            print(line)

    if unknown:
        print(f"Unknown noise lines: {len(unknown)}", file=sys.stderr)
        for line in unknown:
            print(line, file=sys.stderr)
        return 1 if args.strict else 0

    print("CI noise classification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
