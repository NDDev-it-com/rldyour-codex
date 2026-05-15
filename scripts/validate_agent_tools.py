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


EXPECTED_AGENT_MODEL = "gpt-5.5"
EXPECTED_AGENT_REASONING = "medium"
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


def validate_openai_metadata(path: Path, valid_mcp_servers: set[str], failures: list[str]) -> None:
    try:
        data = load_yaml_mapping(path)
    except Exception as exc:
        failures.append(f"{path}: parse failed: {exc}")
        return

    dependencies = data.get("dependencies")
    tools = dependencies.get("tools", []) if isinstance(dependencies, dict) else []
    if tools is None:
        return
    if not isinstance(tools, list):
        failures.append(f"{path}: dependencies.tools must be a list")
        return
    for tool in tools:
        if not isinstance(tool, dict):
            failures.append(f"{path}: dependency tool entries must be objects")
            continue
        if tool.get("type") != "mcp":
            failures.append(f"{path}: dependencies.tools only supports type=mcp")
            continue
        value = str(tool.get("value") or "")
        if value not in valid_mcp_servers:
            failures.append(f"{path}: unknown MCP dependency {value!r}")


def validate_managed_agent(path: Path, failures: list[str]) -> None:
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


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    mcp_manifest = repo_root / "plugins" / "rldyour-mcps" / ".mcp.json"
    valid_mcp_servers = set(json.loads(mcp_manifest.read_text(encoding="utf-8"))["mcpServers"])

    failures: list[str] = []
    validate_no_claude_agent_files(repo_root, failures)
    validate_no_claude_plugin_manifests(repo_root, failures)

    skill_files = sorted((repo_root / "plugins").glob("rldyour-*/skills/*/SKILL.md"))
    metadata_files = sorted((repo_root / "plugins").glob("rldyour-*/skills/*/agents/openai.yaml"))
    managed_agents = sorted((repo_root / "system" / "agents").glob("*.toml"))

    for path in skill_files:
        validate_skill_frontmatter(path, failures)
    for path in metadata_files:
        validate_openai_metadata(path, valid_mcp_servers, failures)
    for path in managed_agents:
        validate_managed_agent(path, failures)

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
