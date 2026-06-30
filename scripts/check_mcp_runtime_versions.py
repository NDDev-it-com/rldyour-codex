#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Pin:
    key: str
    ecosystem: str
    package: str


PINS: tuple[Pin, ...] = (
    Pin("CODEX_CLI_VERSION", "npm", "@openai/codex"),
    Pin("GITHUB_MCP_SERVER_VERSION", "github-release", "github/github-mcp-server"),
    Pin("BUN_VERSION", "npm", "bun"),
    Pin("MCP_PYTHON_SDK_VERSION", "pypi", "mcp"),
    Pin("SERENA_AGENT_VERSION", "pypi", "serena-agent"),
    Pin("SEQUENTIAL_THINKING_MCP_VERSION", "npm", "@modelcontextprotocol/server-sequential-thinking"),
    Pin("CHROME_DEVTOOLS_MCP_VERSION", "npm", "chrome-devtools-mcp"),
    Pin("CONTEXT7_MCP_VERSION", "npm", "@upstash/context7-mcp"),
    Pin("SHADCN_VERSION", "npm", "shadcn"),
)


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip().strip("\"'")
    return values


def npm_latest(package: str) -> str:
    if not shutil.which("npm"):
        raise RuntimeError("npm command not found")
    output = subprocess.check_output(
        ["npm", "view", package, "version", "--json"],
        text=True,
        stderr=subprocess.STDOUT,
        timeout=45,
    ).strip()
    value = json.loads(output)
    if not isinstance(value, str) or not value:
        raise RuntimeError(f"unexpected npm response for {package}: {output!r}")
    return value


def pypi_latest(package: str) -> str:
    url = f"https://pypi.org/pypi/{package}/json"
    # PINS is a hardcoded repository allowlist, so package cannot be user-controlled.
    with urllib.request.urlopen(url, timeout=45) as response:
        data = json.load(response)
    version = data.get("info", {}).get("version")
    if not isinstance(version, str) or not version:
        raise RuntimeError(f"unexpected PyPI response for {package}")
    return version


def github_api_request(url: str) -> urllib.request.Request:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "rldyour-codex-mcp-runtime-version-check",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return urllib.request.Request(url, headers=headers)


def github_release_latest(repository: str) -> str:
    url = f"https://api.github.com/repos/{repository}/releases/latest"
    # PINS is a repository allowlist, so repository cannot be user-controlled.
    with urllib.request.urlopen(github_api_request(url), timeout=45) as response:
        data = json.load(response)
    tag = data.get("tag_name")
    if not isinstance(tag, str) or not tag:
        raise RuntimeError(f"unexpected GitHub releases response for {repository}")
    return tag.removeprefix("v")


def latest_for(pin: Pin) -> str:
    if pin.ecosystem == "npm":
        return npm_latest(pin.package)
    if pin.ecosystem == "pypi":
        return pypi_latest(pin.package)
    if pin.ecosystem == "github-release":
        return github_release_latest(pin.package)
    raise RuntimeError(f"unsupported ecosystem: {pin.ecosystem}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check pinned MCP runtime package versions against upstream latest versions.")
    parser.add_argument("--fail-on-outdated", action="store_true", help="Exit non-zero if any known pin is outdated.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of a human-readable table.")
    args = parser.parse_args()

    pinned = parse_env_file(ROOT / "config/mcp-runtime-versions.env")
    rows: list[dict[str, str]] = []
    failures: list[str] = []

    for pin in PINS:
        current = pinned.get(pin.key)
        if not current:
            rows.append(
                {
                    "key": pin.key,
                    "ecosystem": pin.ecosystem,
                    "package": pin.package,
                    "current": "",
                    "latest": "",
                    "status": "missing-pin",
                }
            )
            failures.append(f"{pin.key}: missing pin")
            continue
        try:
            latest = latest_for(pin)
        except Exception as exc:
            rows.append(
                {
                    "key": pin.key,
                    "ecosystem": pin.ecosystem,
                    "package": pin.package,
                    "current": current,
                    "latest": "",
                    "status": f"check-failed: {exc}",
                }
            )
            failures.append(f"{pin.key}: failed to check latest version: {exc}")
            continue
        status = "current" if current == latest else "outdated"
        if status == "outdated":
            failures.append(f"{pin.key}: pinned {current}, latest {latest}")
        rows.append(
            {
                "key": pin.key,
                "ecosystem": pin.ecosystem,
                "package": pin.package,
                "current": current,
                "latest": latest,
                "status": status,
            }
        )

    if args.json:
        print(json.dumps({"pins": rows}, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print("MCP runtime pin status:")
        for row in rows:
            print(
                f"- {row['key']}: {row['current'] or '<missing>'} "
                f"(latest {row['latest'] or '<unknown>'}, {row['status']})"
            )

    if failures and args.fail_on_outdated:
        print("\n".join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
