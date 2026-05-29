#!/usr/bin/env python3
"""Validate Codex-native agent and skill tool surfaces.

This is the Codex counterpart to the Claude Code agent-tools validator. Codex
does not use plugin-root `agents/*.md` subagent files. The supported surfaces in
this repository are:

- managed subagents: `system/agents/*.toml`
- skill UI/dependency metadata: `plugins/*/skills/*/agents/openai.yaml`
- skill instructions: `plugins/*/skills/*/SKILL.md`

The validator rejects Claude-only agent artifacts and frontmatter fields so
memory-sync automation stays in the actual Codex format.
"""

from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path
from typing import Any

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from codex_openai_metadata_policy import validate_metadata_file


EXPECTED_AGENT_MODEL = "gpt-5.5"
EXPECTED_AGENT_REASONING = "medium"
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
CLAUDE_ONLY_SKILL_KEYS = {
    "allowed-tools",
    "allowed_tools",
    "disallowedTools",
    "disallowed-tools",
    "maxTurns",
    "model",
    "effort",
    "tools",
    "color",
}
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def load_yaml_mapping(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("YAML root must be a mapping")
    return data


def validate_no_claude_agent_files(repo_root: Path, failures: list[str]) -> None:
    for path in sorted((repo_root / "plugins").glob("rldyour-*/agents/*.md")):
        failures.append(
            f"{path}: plugin-root agents/*.md is Claude Code format; "
            "use system/agents/*.toml for Codex managed agents or "
            "skills/*/agents/openai.yaml for skill metadata"
        )


def validate_no_claude_plugin_manifests(repo_root: Path, failures: list[str]) -> None:
    for path in sorted(repo_root.glob("**/.claude-plugin/*")):
        failures.append(f"{path}: .claude-plugin is not a Codex plugin manifest path")


def validate_skill_frontmatter(path: Path, failures: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        failures.append(f"{path}: missing YAML frontmatter")
        return
    try:
        frontmatter = yaml.safe_load(match.group(1)) or {}
    except Exception as exc:
        failures.append(f"{path}: frontmatter parse failed: {exc}")
        return
    if not isinstance(frontmatter, dict):
        failures.append(f"{path}: frontmatter must be a mapping")
        return
    claude_keys = sorted(str(key) for key in frontmatter if str(key) in CLAUDE_ONLY_SKILL_KEYS)
    if claude_keys:
        failures.append(
            f"{path}: Claude-only frontmatter keys are not allowed in Codex skills: "
            + ", ".join(claude_keys)
        )


def validate_disabled_mcp_transport(
    path: Path,
    server: str,
    server_config: dict[str, Any],
    registry_spec: dict[str, Any],
    failures: list[str],
) -> None:
    if "command" not in server_config and "url" not in server_config:
        failures.append(
            f"{path}: temporary subagent MCP policy for {server} must include a valid disabled "
            "transport copied from plugins/rldyour-mcps/.mcp.json"
        )
        return

    for key in sorted(registry_spec):
        if key not in MCP_TRANSPORT_KEYS:
            continue
        if server_config.get(key) != registry_spec[key]:
            failures.append(
                f"{path}: temporary subagent MCP policy for {server} must copy {key} "
                "from plugins/rldyour-mcps/.mcp.json"
            )


def validate_managed_agent(path: Path, mcp_registry: dict[str, Any], failures: list[str]) -> None:
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"{path}: TOML parse failed: {exc}")
        return

    if data.get("name") != path.stem:
        failures.append(f"{path}: name must match filename stem")
    if data.get("model") != EXPECTED_AGENT_MODEL:
        failures.append(f"{path}: model must be {EXPECTED_AGENT_MODEL}")
    if data.get("model_reasoning_effort") != EXPECTED_AGENT_REASONING:
        failures.append(f"{path}: model_reasoning_effort must be {EXPECTED_AGENT_REASONING}")
    for unsupported in ("tools", "allowed_tools", "disallowed_tools", "allowed-tools", "disallowed-tools"):
        if unsupported in data:
            failures.append(
                f"{path}: {unsupported} is not a supported managed-agent TOML field in this repository"
            )
    mcp_servers = data.get("mcp_servers")
    if not isinstance(mcp_servers, dict):
        failures.append(f"{path}: managed agents must declare temporary mcp_servers isolation policy")
        return

    valid_mcp_servers = set(mcp_registry)
    known_servers = valid_mcp_servers | TEMPORARY_SUBAGENT_MCP_BUILTINS
    for server in sorted(mcp_servers):
        if server not in known_servers:
            failures.append(f"{path}: unknown managed-agent MCP server policy {server}")

    for server in sorted(valid_mcp_servers - TEMPORARY_SUBAGENT_MCP_ALLOWLIST):
        server_config = mcp_servers.get(server)
        if not isinstance(server_config, dict) or server_config.get("enabled") is not False:
            failures.append(
                f"{path}: temporary subagent MCP policy must set mcp_servers.{server}.enabled = false"
            )
            continue
        registry_spec = mcp_registry.get(server)
        if not isinstance(registry_spec, dict):
            failures.append(f"{path}: missing MCP registry spec for {server}")
            continue
        validate_disabled_mcp_transport(path, server, server_config, registry_spec, failures)

    for server in sorted(TEMPORARY_SUBAGENT_MCP_ALLOWLIST & valid_mcp_servers):
        server_config = mcp_servers.get(server)
        if isinstance(server_config, dict) and server_config.get("enabled") is False:
            failures.append(f"{path}: temporary subagent MCP allowlisted server {server} must not be disabled")

    for server in sorted(TEMPORARY_SUBAGENT_MCP_BUILTINS):
        server_config = mcp_servers.get(server)
        if isinstance(server_config, dict):
            failures.append(
                f"{path}: built-in subagent MCP surface {server} must not be declared under "
                "mcp_servers; leave it inherited from Codex Apps/connectors"
            )


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    mcp_manifest = repo_root / "plugins" / "rldyour-mcps" / ".mcp.json"
    mcp_registry = json.loads(mcp_manifest.read_text(encoding="utf-8"))["mcpServers"]
    valid_mcp_servers = set(mcp_registry)

    failures: list[str] = []
    validate_no_claude_agent_files(repo_root, failures)
    validate_no_claude_plugin_manifests(repo_root, failures)

    skill_files = sorted((repo_root / "plugins").glob("rldyour-*/skills/*/SKILL.md"))
    metadata_files = sorted((repo_root / "plugins").glob("rldyour-*/skills/*/agents/openai.yaml"))
    managed_agents = sorted((repo_root / "system" / "agents").glob("*.toml"))

    for path in skill_files:
        validate_skill_frontmatter(path, failures)
    for path in metadata_files:
        failures.extend(validate_metadata_file(path, repo_root, valid_mcp_servers))
    for path in managed_agents:
        validate_managed_agent(path, mcp_registry, failures)

    if failures:
        print("validate_agent_tools.py: validation FAILED", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1

    print(
        "OK Codex agent surfaces validated: "
        f"{len(managed_agents)} managed agents, "
        f"{len(metadata_files)} OpenAI metadata files, "
        f"{len(skill_files)} skills"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
