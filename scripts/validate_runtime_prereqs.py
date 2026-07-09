#!/usr/bin/env python3
"""Validate launcher prerequisites for enabled local MCP servers."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAUNCHER_ENV = {
    "uvx": "UVX_BIN",
    "bunx": "BUNX_BIN",
    "dart": "DART_BIN",
    "github-mcp-server": "GITHUB_MCP_SERVER_BIN",
    "codex": "CODEX_BIN",
    "shellcheck": "SHELLCHECK_BIN",
}
REMEDIATION = {
    "uvx": "Install uv/uvx or set UVX_BIN to an executable uvx-compatible launcher.",
    "bunx": "Install Bun so bunx is available, or disable Bun-backed MCP servers for this profile.",
    "dart": "Install the Dart SDK or disable the dart-flutter MCP server for this profile.",
    "github-mcp-server": "Install GitHub's official MCP server binary or disable the github MCP server for this profile.",
    "codex": "Install the pinned @openai/codex CLI or set CODEX_BIN to its executable path.",
    "shellcheck": "Install ShellCheck with brew install shellcheck or apt-get install shellcheck.",
}
MANAGED_CHROME_WRAPPER = "~/.local/bin/chrome-devtools-mcp"


def load_mcp_servers(path: Path) -> dict[str, dict[str, object]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    servers = data.get("mcpServers")
    if not isinstance(servers, dict):
        raise ValueError(f"{path}: missing mcpServers object")
    result: dict[str, dict[str, object]] = {}
    for name, spec in servers.items():
        if isinstance(name, str) and isinstance(spec, dict):
            result[name] = spec
    return result


def launcher_path(command: str) -> str:
    override = os.environ.get(LAUNCHER_ENV.get(command, ""))
    if override:
        return override
    return command


def executable_exists(command: str) -> bool:
    value = launcher_path(command)
    if os.sep in value:
        return os.path.isfile(value) and os.access(value, os.X_OK)
    return shutil.which(value) is not None


def missing_launchers(
    servers: dict[str, dict[str, object]],
    *,
    require_codex: bool,
    require_shellcheck: bool = False,
) -> dict[str, list[str]]:
    affected: dict[str, list[str]] = {}
    for name, spec in sorted(servers.items()):
        if spec.get("enabled") is False:
            continue
        command = spec.get("command")
        if not isinstance(command, str) or not command:
            continue
        if name == "chrome-devtools":
            wrapper = os.path.expanduser(MANAGED_CHROME_WRAPPER)
            if not (os.path.isfile(wrapper) and os.access(wrapper, os.X_OK)):
                affected.setdefault(MANAGED_CHROME_WRAPPER, []).append(name)
            continue
        if not executable_exists(command):
            affected.setdefault(command, []).append(name)
    if require_codex and not executable_exists("codex"):
        affected.setdefault("codex", []).append("installer/doctor")
    if require_shellcheck and not executable_exists("shellcheck"):
        affected.setdefault("shellcheck", []).append("shell validation")
    return affected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mcp-config",
        type=Path,
        default=ROOT / "plugins/rldyour-mcps/.mcp.json",
        help="Path to the rldyour MCP registry.",
    )
    parser.add_argument("--require-codex", action="store_true", help="Require the codex CLI itself.")
    parser.add_argument("--require-shellcheck", action="store_true", help="Require ShellCheck for shell validators.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when prerequisites are missing.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument(
        "--mode",
        choices=("static", "local-launch", "live"),
        default="local-launch",
        help="static validates config shape only; local-launch checks command availability; live is reserved for runtime smoke lanes.",
    )
    args = parser.parse_args()

    servers = load_mcp_servers(args.mcp_config)
    missing = (
        missing_launchers({}, require_codex=False, require_shellcheck=args.require_shellcheck)
        if args.mode == "static"
        else missing_launchers(
            servers,
            require_codex=args.require_codex,
            require_shellcheck=args.require_shellcheck,
        )
    )

    payload = {
        "ok": not missing,
        "mode": args.mode,
        "mcp_config": str(args.mcp_config),
        "missing": [
            {
                "launcher": launcher,
                "affected": affected,
                "fix": REMEDIATION.get(
                    launcher,
                    "Run rldyour-new-mac-or-ubuntu bootstrap to install the managed CloakBrowser wrapper."
                    if launcher == MANAGED_CHROME_WRAPPER
                    else f"Install {launcher} or disable affected servers.",
                ),
            }
            for launcher, affected in sorted(missing.items())
        ],
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    elif missing:
        for item in payload["missing"]:
            print(f"missing launcher: {item['launcher']}", file=sys.stderr)
            print(f"affected MCP servers: {', '.join(item['affected'])}", file=sys.stderr)
            print(f"fix: {item['fix']}", file=sys.stderr)
    else:
        if args.mode == "static":
            print(f"Runtime prerequisite config is static-valid for {len(servers)} MCP server definitions")
        else:
            print(f"Runtime prerequisites available for {len(servers)} MCP server definitions")

    if missing and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
