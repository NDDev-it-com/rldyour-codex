from __future__ import annotations

from pathlib import Path

from tests.support.importing import import_script


mod = import_script("scripts/validate_agent_tools.py")


MCP_REGISTRY = {
    "serena": {"command": "uvx", "args": ["serena", "start-mcp-server"]},
    "figma": {"url": "https://mcp.figma.com/mcp"},
}


def write_agent(path: Path, body: str) -> Path:
    path.write_text(body, encoding="utf-8")
    return path


def write_openai_metadata(tmp_path: Path, *, short: str, prompt: str, dependency: str) -> Path:
    skill_dir = tmp_path / "plugins" / "rldyour-demo" / "skills" / "demo"
    metadata_dir = skill_dir / "agents"
    metadata_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        """---
name: demo-skill
description: "Демо skill. EN: demo skill."
---

# Demo
""",
        encoding="utf-8",
    )
    path = metadata_dir / "openai.yaml"
    path.write_text(
        f"""interface:
  display_name: Demo
  short_description: "{short}"
  default_prompt: "{prompt}"
dependencies:
  tools:
    - type: mcp
      value: serena
      description: "{dependency}"
policy:
  allow_implicit_invocation: true
""",
        encoding="utf-8",
    )
    return path


def valid_agent_text(name: str, mcp_policy: str) -> str:
    return f'''name = "{name}"
description = "Managed test agent for validator coverage."
model = "gpt-5.5"
model_reasoning_effort = "medium"
developer_instructions = """
Validate the managed agent policy.
"""
{mcp_policy}
'''


def test_managed_agent_accepts_temporary_mcp_policy_with_disabled_transport(tmp_path: Path) -> None:
    path = write_agent(
        tmp_path / "demo.toml",
        valid_agent_text(
            "demo",
            """
mcp_servers.figma.enabled = false
mcp_servers.figma.url = "https://mcp.figma.com/mcp"
""",
        ),
    )

    failures: list[str] = []
    mod.validate_managed_agent(path, MCP_REGISTRY, failures)
    assert failures == []


def test_managed_agent_does_not_require_explicit_codex_apps_policy(tmp_path: Path) -> None:
    path = write_agent(
        tmp_path / "demo.toml",
        valid_agent_text(
            "demo",
            """
mcp_servers.figma.enabled = false
mcp_servers.figma.url = "https://mcp.figma.com/mcp"
""",
        ),
    )

    failures: list[str] = []
    mod.validate_managed_agent(path, MCP_REGISTRY, failures)
    assert failures == []


def test_managed_agent_requires_temporary_mcp_policy(tmp_path: Path) -> None:
    path = write_agent(tmp_path / "demo.toml", valid_agent_text("demo", ""))

    failures: list[str] = []
    mod.validate_managed_agent(path, MCP_REGISTRY, failures)
    assert any("temporary mcp_servers isolation policy" in failure for failure in failures)


def test_managed_agent_rejects_non_allowlisted_enabled_mcp(tmp_path: Path) -> None:
    path = write_agent(
        tmp_path / "demo.toml",
        valid_agent_text(
            "demo",
            """
mcp_servers.figma.enabled = true
""",
        ),
    )

    failures: list[str] = []
    mod.validate_managed_agent(path, MCP_REGISTRY, failures)
    assert any("mcp_servers.figma.enabled = false" in failure for failure in failures)


def test_managed_agent_rejects_disabled_mcp_without_transport(tmp_path: Path) -> None:
    path = write_agent(
        tmp_path / "demo.toml",
        valid_agent_text(
            "demo",
            """
mcp_servers.figma.enabled = false
""",
        ),
    )

    failures: list[str] = []
    mod.validate_managed_agent(path, MCP_REGISTRY, failures)
    assert any("figma must include a valid disabled transport" in failure for failure in failures)


def test_managed_agent_rejects_disabled_mcp_transport_drift(tmp_path: Path) -> None:
    path = write_agent(
        tmp_path / "demo.toml",
        valid_agent_text(
            "demo",
            """
mcp_servers.figma.enabled = false
mcp_servers.figma.url = "https://wrong.example.com/mcp"
""",
        ),
    )

    failures: list[str] = []
    mod.validate_managed_agent(path, MCP_REGISTRY, failures)
    assert any("figma must copy url" in failure for failure in failures)


def test_managed_agent_rejects_disabled_allowlisted_mcp(tmp_path: Path) -> None:
    path = write_agent(
        tmp_path / "demo.toml",
        valid_agent_text(
            "demo",
            """
mcp_servers.serena.enabled = false
mcp_servers.figma.enabled = false
mcp_servers.figma.url = "https://mcp.figma.com/mcp"
""",
        ),
    )

    failures: list[str] = []
    mod.validate_managed_agent(path, MCP_REGISTRY, failures)
    assert any("allowlisted server serena must not be disabled" in failure for failure in failures)


def test_managed_agent_rejects_explicit_codex_apps_mcp_table(tmp_path: Path) -> None:
    path = write_agent(
        tmp_path / "demo.toml",
        valid_agent_text(
            "demo",
            """
mcp_servers.figma.enabled = false
mcp_servers.figma.url = "https://mcp.figma.com/mcp"
mcp_servers.codex_apps.enabled = true
""",
        ),
    )

    failures: list[str] = []
    mod.validate_managed_agent(path, MCP_REGISTRY, failures)
    assert any("built-in subagent MCP surface codex_apps must not be declared" in failure for failure in failures)


def test_managed_agent_rejects_unknown_mcp_policy(tmp_path: Path) -> None:
    path = write_agent(
        tmp_path / "demo.toml",
        valid_agent_text(
            "demo",
            """
mcp_servers.figma.enabled = false
mcp_servers.figma.url = "https://mcp.figma.com/mcp"
mcp_servers.unknown-server.enabled = false
""",
        ),
    )

    failures: list[str] = []
    mod.validate_managed_agent(path, MCP_REGISTRY, failures)
    assert any("unknown managed-agent MCP server policy unknown-server" in failure for failure in failures)


def test_openai_metadata_accepts_compact_russian_first_fields(tmp_path: Path) -> None:
    path = write_openai_metadata(
        tmp_path,
        short="Демо metadata. EN: compact metadata",
        prompt="Используй $demo-skill: проверь metadata. EN: compact routing.",
        dependency="Семантика Serena. EN: code symbols and memory.",
    )

    failures = mod.validate_metadata_file(path, tmp_path, {"serena"})

    assert failures == []


def test_openai_metadata_rejects_marketplace_length_drift(tmp_path: Path) -> None:
    path = write_openai_metadata(
        tmp_path,
        short="Очень длинное описание metadata для проверки лимитов Codex marketplace validator. EN: too long",
        prompt="Используй $demo-skill: "
        + "очень длинный prompt " * 8
        + "EN: too long.",
        dependency="Семантика Serena. EN: code symbols and memory.",
    )

    failures = mod.validate_metadata_file(path, tmp_path, {"serena"})

    assert any("short_description length" in failure for failure in failures)
    assert any("default_prompt length" in failure for failure in failures)


def test_openai_metadata_rejects_non_russian_first_dependency(tmp_path: Path) -> None:
    path = write_openai_metadata(
        tmp_path,
        short="Демо metadata. EN: compact metadata",
        prompt="Используй $demo-skill: проверь metadata. EN: compact routing.",
        dependency="Serena: semantic code workflow.",
    )

    failures = mod.validate_metadata_file(path, tmp_path, {"serena"})

    assert any("dependencies.tools[serena].description" in failure for failure in failures)


def test_main_validates_current_repository() -> None:
    assert mod.main() == 0
