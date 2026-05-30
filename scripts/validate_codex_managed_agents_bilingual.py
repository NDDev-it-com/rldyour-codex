#!/usr/bin/env python3
"""Validate managed Codex subagent routing metadata and isolation policy."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_AGENT_MODEL = "gpt-5.5"
EXPECTED_AGENT_REASONING = "medium"
RUSSIAN_START_RE = re.compile(r"^\s*[А-Яа-яЁё]")
RUSSIAN_RE = re.compile(r"[А-Яа-яЁё]")
ENGLISH_SUFFIX_RE = re.compile(r"\bEN:\s*[A-Za-z]")
TEMPORARY_SUBAGENT_MCP_ALLOWLIST = {
    "context7",
    "deepwiki",
    "grep",
    "openaiDeveloperDocs",
    "sequential-thinking",
    "serena",
}
TEMPORARY_SUBAGENT_MCP_BUILTINS = {"codex_apps"}
MCP_TRANSPORT_KEYS = {
    "args",
    "bearer_token_env_var",
    "command",
    "cwd",
    "disabled_tools",
    "enabled_tools",
    "env",
    "env_http_headers",
    "env_vars",
    "experimental_environment",
    "http_headers",
    "oauth_resource",
    "required",
    "scopes",
    "startup_timeout_ms",
    "startup_timeout_sec",
    "tool_timeout_sec",
    "url",
}


def validate_description(path: Path, description: object, failures: list[str]) -> None:
    if not isinstance(description, str) or not description.strip():
        failures.append(f"{path}: description must be a non-empty string")
        return
    if not RUSSIAN_START_RE.search(description):
        failures.append(f"{path}: description must start with Russian trigger text")
    if not RUSSIAN_RE.search(description):
        failures.append(f"{path}: description must include Russian trigger text")
    if not ENGLISH_SUFFIX_RE.search(description):
        failures.append(f"{path}: description must include compact English suffix prefixed with EN:")


def validate_disabled_mcp_transport(
    path: Path,
    server: str,
    server_config: dict[str, Any],
    registry_spec: dict[str, Any],
    failures: list[str],
) -> None:
    if "command" not in server_config and "url" not in server_config:
        failures.append(f"{path}: disabled MCP {server} must copy command or url transport metadata")
        return
    for key in sorted(registry_spec):
        if key in MCP_TRANSPORT_KEYS and server_config.get(key) != registry_spec[key]:
            failures.append(f"{path}: disabled MCP {server} must copy {key} from plugins/rldyour-mcps/.mcp.json")


def validate_agent(path: Path, mcp_registry: dict[str, Any], failures: list[str]) -> None:
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"{path}: TOML parse failed: {exc}")
        return

    if data.get("name") != path.stem:
        failures.append(f"{path}: name must match filename stem")
    validate_description(path, data.get("description"), failures)
    if data.get("model") != EXPECTED_AGENT_MODEL:
        failures.append(f"{path}: model must be {EXPECTED_AGENT_MODEL}")
    if data.get("model_reasoning_effort") != EXPECTED_AGENT_REASONING:
        failures.append(f"{path}: model_reasoning_effort must be {EXPECTED_AGENT_REASONING}")

    mcp_servers = data.get("mcp_servers")
    if not isinstance(mcp_servers, dict):
        failures.append(f"{path}: managed agent must declare mcp_servers isolation policy")
        return
    valid_mcp_servers = set(mcp_registry)
    known_servers = valid_mcp_servers | TEMPORARY_SUBAGENT_MCP_BUILTINS
    for server in sorted(mcp_servers):
        if server not in known_servers:
            failures.append(f"{path}: unknown managed-agent MCP server policy {server}")

    for server in sorted(valid_mcp_servers - TEMPORARY_SUBAGENT_MCP_ALLOWLIST):
        server_config = mcp_servers.get(server)
        if not isinstance(server_config, dict) or server_config.get("enabled") is not False:
            failures.append(f"{path}: mcp_servers.{server}.enabled must be false for reviewer isolation")
            continue
        registry_spec = mcp_registry.get(server)
        if isinstance(registry_spec, dict):
            validate_disabled_mcp_transport(path, server, server_config, registry_spec, failures)

    for server in sorted(TEMPORARY_SUBAGENT_MCP_BUILTINS):
        if isinstance(mcp_servers.get(server), dict):
            failures.append(f"{path}: built-in MCP surface {server} must be inherited, not declared")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents-dir", type=Path, default=ROOT / "system/agents")
    parser.add_argument("--mcp-config", type=Path, default=ROOT / "plugins/rldyour-mcps/.mcp.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mcp_registry = json.loads(args.mcp_config.read_text(encoding="utf-8"))["mcpServers"]
    failures: list[str] = []
    agent_paths = sorted(args.agents_dir.glob("*.toml"))
    if not agent_paths:
        failures.append(f"{args.agents_dir}: expected managed subagent TOML files")
    for path in agent_paths:
        validate_agent(path, mcp_registry, failures)

    if failures:
        print("validate_codex_managed_agents_bilingual.py: validation FAILED", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1

    print(f"OK Codex managed agents are Russian-first and isolated: {len(agent_paths)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
