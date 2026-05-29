#!/usr/bin/env python3
"""Shared policy for Codex skill `agents/openai.yaml` metadata."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


MAX_DEFAULT_PROMPT_CHARS = 128
MIN_SHORT_DESCRIPTION_CHARS = 25
MAX_SHORT_DESCRIPTION_CHARS = 64
MAX_DEPENDENCY_DESCRIPTION_CHARS = 128

ORCHESTRATED_ONLY = {
    "flow-architecture-review",
    "flow-consistency-review",
    "flow-integration-review",
    "flow-quality-review",
    "flow-security-review",
    "flow-verification-review",
}

CYRILLIC_FIRST_RE = re.compile(r"^\s*[А-Яа-яЁё]")
CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
ASCII_ALPHA_RE = re.compile(r"[A-Za-z]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def display_path(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def load_yaml_mapping(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("YAML root must be a mapping")
    return data


def load_mcp_servers(repo_root: Path) -> set[str]:
    manifest_path = repo_root / "plugins" / "rldyour-mcps" / ".mcp.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    servers = data.get("mcpServers")
    if not isinstance(servers, dict):
        raise ValueError(f"{manifest_path}: mcpServers must be a mapping")
    return set(servers)


def skill_name_for(path: Path) -> str | None:
    skill_md = path.parent.parent / "SKILL.md"
    if not skill_md.is_file():
        return None
    match = FRONTMATTER_RE.match(skill_md.read_text(encoding="utf-8"))
    if not match:
        return None
    frontmatter = yaml.safe_load(match.group(1)) or {}
    if not isinstance(frontmatter, dict):
        return None
    name = frontmatter.get("name")
    return name.strip() if isinstance(name, str) and name.strip() else None


def is_russian_first_bilingual(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    return bool(CYRILLIC_FIRST_RE.search(value) and ASCII_ALPHA_RE.search(value))


def require_ru_first_bilingual(
    failures: list[str],
    path: Path,
    repo_root: Path,
    field: str,
    value: Any,
) -> None:
    if not is_russian_first_bilingual(value):
        failures.append(f"{display_path(path, repo_root)}: {field} must be Russian-first and English-compatible")


def validate_metadata_file(path: Path, repo_root: Path, valid_mcp_servers: set[str]) -> list[str]:
    failures: list[str] = []
    skill_name = skill_name_for(path)
    if not skill_name:
        return [f"{display_path(path, repo_root)}: cannot resolve sibling SKILL.md name"]

    try:
        data = load_yaml_mapping(path)
    except Exception as exc:
        return [f"{display_path(path, repo_root)}: parse failed: {exc}"]

    interface = data.get("interface")
    if not isinstance(interface, dict):
        failures.append(f"{display_path(path, repo_root)}: missing interface object")
        return failures

    short_description = interface.get("short_description")
    default_prompt = interface.get("default_prompt")
    require_ru_first_bilingual(failures, path, repo_root, "interface.short_description", short_description)
    require_ru_first_bilingual(failures, path, repo_root, "interface.default_prompt", default_prompt)

    short_len = len(short_description) if isinstance(short_description, str) else 0
    if not (MIN_SHORT_DESCRIPTION_CHARS <= short_len <= MAX_SHORT_DESCRIPTION_CHARS):
        failures.append(
            f"{display_path(path, repo_root)}: interface.short_description length {short_len} must be "
            f"{MIN_SHORT_DESCRIPTION_CHARS}-{MAX_SHORT_DESCRIPTION_CHARS}"
        )

    prompt_len = len(default_prompt) if isinstance(default_prompt, str) else 0
    if prompt_len > MAX_DEFAULT_PROMPT_CHARS:
        failures.append(
            f"{display_path(path, repo_root)}: interface.default_prompt length {prompt_len} "
            f"exceeds {MAX_DEFAULT_PROMPT_CHARS}"
        )
    if isinstance(default_prompt, str) and f"${skill_name}" not in default_prompt:
        failures.append(f"{display_path(path, repo_root)}: interface.default_prompt must mention ${skill_name}")

    policy = data.get("policy")
    if not isinstance(policy, dict):
        failures.append(f"{display_path(path, repo_root)}: missing policy object")
    else:
        allow_implicit = policy.get("allow_implicit_invocation")
        if skill_name in ORCHESTRATED_ONLY:
            if allow_implicit is not False:
                failures.append(
                    f"{display_path(path, repo_root)}: orchestrated reviewer skill must set "
                    "policy.allow_implicit_invocation=false"
                )
        elif allow_implicit is not True:
            failures.append(f"{display_path(path, repo_root)}: policy.allow_implicit_invocation must be true")

    dependencies = data.get("dependencies")
    tools = dependencies.get("tools", []) if isinstance(dependencies, dict) else []
    if tools is None:
        tools = []
    if not isinstance(tools, list):
        failures.append(f"{display_path(path, repo_root)}: dependencies.tools must be a list")
        return failures

    for index, tool in enumerate(tools):
        if not isinstance(tool, dict):
            failures.append(f"{display_path(path, repo_root)}: dependencies.tools[{index}] must be a mapping")
            continue
        if tool.get("type") != "mcp":
            failures.append(f"{display_path(path, repo_root)}: dependencies.tools only supports type=mcp")
            continue
        value = str(tool.get("value") or "")
        if value not in valid_mcp_servers:
            failures.append(f"{display_path(path, repo_root)}: unknown MCP dependency {value!r}")
        description = tool.get("description")
        label = value or str(index)
        require_ru_first_bilingual(failures, path, repo_root, f"dependencies.tools[{label}].description", description)
        description_len = len(description) if isinstance(description, str) else 0
        if description_len > MAX_DEPENDENCY_DESCRIPTION_CHARS:
            failures.append(
                f"{display_path(path, repo_root)}: dependencies.tools[{label}].description length "
                f"{description_len} exceeds {MAX_DEPENDENCY_DESCRIPTION_CHARS}"
            )

    return failures


def validate_repository(repo_root: Path) -> list[str]:
    valid_mcp_servers = load_mcp_servers(repo_root)
    metadata_files = sorted(repo_root.glob("plugins/rldyour-*/skills/*/agents/openai.yaml"))
    failures: list[str] = []
    if not metadata_files:
        failures.append("no Codex agents/openai.yaml metadata files found")
    for path in metadata_files:
        failures.extend(validate_metadata_file(path, repo_root, valid_mcp_servers))
    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Codex OpenAI skill metadata.")
    parser.add_argument("--repo-root", default=Path(__file__).resolve().parent.parent)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    failures = validate_repository(repo_root)
    if failures:
        print("codex_openai_metadata_policy.py: validation FAILED", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1

    print("validated Codex OpenAI skill metadata")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
