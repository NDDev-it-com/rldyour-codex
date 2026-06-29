#!/usr/bin/env python3
"""Validate Codex MCP secret forwarding semantics.

Codex treats ``env`` as static values and ``env_vars`` as variables forwarded
from the local or remote environment. Secret placeholders such as
``${GITHUB_PERSONAL_ACCESS_TOKEN}`` must therefore not be materialized into
``env`` where the MCP server can receive them literally.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER_RE = re.compile(r"\$\{[A-Z0-9_]+\}")
GITHUB_TOKEN_ENV = "GITHUB_PERSONAL_ACCESS_TOKEN"


def load_source_servers(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    servers = data.get("mcpServers")
    if not isinstance(servers, dict):
        raise ValueError(f"{path}: missing mcpServers object")
    return servers


def load_installed_servers(path: Path) -> dict[str, Any]:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    servers = data.get("mcp_servers")
    if not isinstance(servers, dict):
        raise ValueError(f"{path}: missing mcp_servers table")
    return servers


def env_var_names(value: object, label: str, failures: list[str]) -> set[str]:
    names: set[str] = set()
    if value is None:
        return names
    if not isinstance(value, list):
        failures.append(f"{label}: env_vars must be a list")
        return names
    for index, item in enumerate(value):
        if isinstance(item, str):
            if PLACEHOLDER_RE.search(item):
                failures.append(f"{label}: env_vars[{index}] must be an env var name, not {item!r}")
            elif item:
                names.add(item)
            else:
                failures.append(f"{label}: env_vars[{index}] must not be empty")
            continue
        if isinstance(item, dict):
            name = item.get("name")
            if not isinstance(name, str) or not name:
                failures.append(f"{label}: env_vars[{index}].name must be a non-empty string")
            elif PLACEHOLDER_RE.search(name):
                failures.append(f"{label}: env_vars[{index}].name must be an env var name, not {name!r}")
            else:
                names.add(name)
            source = item.get("source")
            if source is not None and source not in {"local", "remote"}:
                failures.append(f"{label}: env_vars[{index}].source must be local or remote")
            continue
        failures.append(f"{label}: env_vars[{index}] must be a string or object")
    return names


def validate_static_env(label: str, spec: dict[str, Any], failures: list[str]) -> None:
    env = spec.get("env")
    if isinstance(env, dict):
        for key, value in sorted(env.items()):
            if isinstance(value, str) and PLACEHOLDER_RE.search(value):
                failures.append(
                    f"{label}: env.{key} uses placeholder {value!r}; use env_vars for stdio "
                    "secret forwarding"
                )
    elif env is not None:
        failures.append(f"{label}: env must be an object when present")

    http_headers = spec.get("http_headers")
    if isinstance(http_headers, dict):
        for key, value in sorted(http_headers.items()):
            if isinstance(value, str) and PLACEHOLDER_RE.search(value):
                failures.append(
                    f"{label}: http_headers.{key} uses placeholder {value!r}; use env_http_headers"
                )
    elif http_headers is not None:
        failures.append(f"{label}: http_headers must be an object when present")

    env_http_headers = spec.get("env_http_headers")
    if isinstance(env_http_headers, dict):
        for key, value in sorted(env_http_headers.items()):
            if not isinstance(value, str) or not value:
                failures.append(f"{label}: env_http_headers.{key} must name an env var")
            elif PLACEHOLDER_RE.search(value):
                failures.append(
                    f"{label}: env_http_headers.{key} must name an env var, not placeholder {value!r}"
                )
    elif env_http_headers is not None:
        failures.append(f"{label}: env_http_headers must be an object when present")

    bearer = spec.get("bearer_token_env_var")
    if bearer is not None:
        if not isinstance(bearer, str) or not bearer:
            failures.append(f"{label}: bearer_token_env_var must be a non-empty env var name")
        elif PLACEHOLDER_RE.search(bearer):
            failures.append(
                f"{label}: bearer_token_env_var must name an env var, not placeholder {bearer!r}"
            )


def validate_server_map(label: str, servers: dict[str, Any], failures: list[str]) -> None:
    for name, raw_spec in sorted(servers.items()):
        server_label = f"{label}:{name}"
        if not isinstance(raw_spec, dict):
            failures.append(f"{server_label}: server spec must be an object")
            continue
        validate_static_env(server_label, raw_spec, failures)
        names = env_var_names(raw_spec.get("env_vars"), server_label, failures)
        if raw_spec.get("command") == "github-mcp-server" and GITHUB_TOKEN_ENV not in names:
            failures.append(f"{server_label}: github-mcp-server must forward {GITHUB_TOKEN_ENV} via env_vars")


def validate_managed_agents(path: Path, failures: list[str]) -> None:
    for agent_path in sorted(path.glob("*.toml")):
        data = tomllib.loads(agent_path.read_text(encoding="utf-8"))
        servers = data.get("mcp_servers")
        if isinstance(servers, dict):
            validate_server_map(str(agent_path), servers, failures)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mcp-config",
        type=Path,
        default=ROOT / "plugins/rldyour-mcps/.mcp.json",
        help="Source MCP registry to validate.",
    )
    parser.add_argument("--codex-home", type=Path, help="Validate CODEX_HOME/config.toml runtime MCP tables.")
    parser.add_argument("--config", type=Path, help="Validate a specific Codex config.toml path.")
    parser.add_argument(
        "--agents-dir",
        type=Path,
        default=ROOT / "system/agents",
        help="Managed Codex agent TOML directory to validate.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    failures: list[str] = []
    validate_server_map(str(args.mcp_config), load_source_servers(args.mcp_config), failures)
    validate_managed_agents(args.agents_dir, failures)

    installed_config = args.config
    if args.codex_home is not None:
        installed_config = args.codex_home / "config.toml"
    if installed_config is not None:
        validate_server_map(str(installed_config), load_installed_servers(installed_config), failures)

    if failures:
        print("validate_codex_mcp_env_forwarding.py: validation FAILED", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1

    print("OK Codex MCP env forwarding uses env_vars/header env names, not literal placeholders")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
