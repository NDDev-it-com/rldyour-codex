from __future__ import annotations

from pathlib import Path

from tests.support.importing import import_script


mod = import_script("scripts/validate_agent_tools.py")


MCP_REGISTRY = {
    "serena": {"command": "uvx", "args": ["serena", "start-mcp-server"]},
    "semgrep": {"command": "uvx", "args": ["--from", "semgrep==1.164.0", "semgrep", "mcp"]},
    "figma": {"url": "https://mcp.figma.com/mcp"},
}


def write_agent(path: Path, body: str) -> Path:
    path.write_text(body, encoding="utf-8")
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
mcp_servers.semgrep.enabled = false
mcp_servers.semgrep.command = "uvx"
mcp_servers.semgrep.args = ["--from", "semgrep==1.164.0", "semgrep", "mcp"]
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
mcp_servers.semgrep.enabled = false
mcp_servers.semgrep.command = "uvx"
mcp_servers.semgrep.args = ["--from", "semgrep==1.164.0", "semgrep", "mcp"]
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
mcp_servers.semgrep.enabled = true
""",
        ),
    )

    failures: list[str] = []
    mod.validate_managed_agent(path, MCP_REGISTRY, failures)
    assert any("mcp_servers.semgrep.enabled = false" in failure for failure in failures)


def test_managed_agent_rejects_disabled_mcp_without_transport(tmp_path: Path) -> None:
    path = write_agent(
        tmp_path / "demo.toml",
        valid_agent_text(
            "demo",
            """
mcp_servers.semgrep.enabled = false
mcp_servers.figma.enabled = false
mcp_servers.figma.url = "https://mcp.figma.com/mcp"
""",
        ),
    )

    failures: list[str] = []
    mod.validate_managed_agent(path, MCP_REGISTRY, failures)
    assert any("semgrep must include a valid disabled transport" in failure for failure in failures)


def test_managed_agent_rejects_disabled_mcp_transport_drift(tmp_path: Path) -> None:
    path = write_agent(
        tmp_path / "demo.toml",
        valid_agent_text(
            "demo",
            """
mcp_servers.semgrep.enabled = false
mcp_servers.semgrep.command = "uvx"
mcp_servers.semgrep.args = ["semgrep", "mcp"]
mcp_servers.figma.enabled = false
mcp_servers.figma.url = "https://mcp.figma.com/mcp"
""",
        ),
    )

    failures: list[str] = []
    mod.validate_managed_agent(path, MCP_REGISTRY, failures)
    assert any("semgrep must copy args" in failure for failure in failures)


def test_managed_agent_rejects_disabled_allowlisted_mcp(tmp_path: Path) -> None:
    path = write_agent(
        tmp_path / "demo.toml",
        valid_agent_text(
            "demo",
            """
mcp_servers.serena.enabled = false
mcp_servers.semgrep.enabled = false
mcp_servers.semgrep.command = "uvx"
mcp_servers.semgrep.args = ["--from", "semgrep==1.164.0", "semgrep", "mcp"]
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
mcp_servers.semgrep.enabled = false
mcp_servers.semgrep.command = "uvx"
mcp_servers.semgrep.args = ["--from", "semgrep==1.164.0", "semgrep", "mcp"]
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
mcp_servers.semgrep.enabled = false
mcp_servers.semgrep.command = "uvx"
mcp_servers.semgrep.args = ["--from", "semgrep==1.164.0", "semgrep", "mcp"]
mcp_servers.figma.enabled = false
mcp_servers.figma.url = "https://mcp.figma.com/mcp"
mcp_servers.unknown-server.enabled = false
""",
        ),
    )

    failures: list[str] = []
    mod.validate_managed_agent(path, MCP_REGISTRY, failures)
    assert any("unknown managed-agent MCP server policy unknown-server" in failure for failure in failures)


def test_main_validates_current_repository() -> None:
    assert mod.main() == 0
