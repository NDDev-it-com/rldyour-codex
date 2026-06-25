#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def default_root() -> Path:
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0 and proc.stdout.strip():
        return Path(proc.stdout.strip())
    return Path(__file__).resolve().parents[1]


def load_state(root: Path, state_file: Path | None) -> dict[str, Any]:
    if state_file is not None:
        payload = state_file.read_text(encoding="utf-8")
    else:
        proc = subprocess.run(
            ["python3", "plugins/rldyour-serena-mcp/scripts/serena_memory_state.py"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "serena memory state failed")
        payload = proc.stdout

    parsed = json.loads(payload)
    if not isinstance(parsed, dict):
        raise RuntimeError("serena memory state payload must be a JSON object")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Serena memory freshness against the checked-out HEAD.")
    parser.add_argument("--root", type=Path, default=default_root(), help="Repository root.")
    parser.add_argument("--state-file", type=Path, help="Read a JSON state payload instead of running the state script.")
    args = parser.parse_args()

    root = args.root.resolve()
    # Serena memories are ordinary tracked files on the main branch; freshness is
    # always evaluated against the checked-out HEAD.
    try:
        payload = load_state(root, args.state_file)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if payload.get("is_current") is not True:
        print(f"Serena memories are stale for HEAD: {payload!r}", file=sys.stderr)
        return 1

    print(f"Serena memories current for {payload.get('head_sha', 'unknown')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
