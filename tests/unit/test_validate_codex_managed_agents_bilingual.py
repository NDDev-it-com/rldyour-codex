from __future__ import annotations

import json
from pathlib import Path

from tests.support.importing import import_script

mod = import_script("scripts/validate_codex_managed_agents_bilingual.py")


def test_description_requires_russian_first_and_english_suffix() -> None:
    failures: list[str] = []

    mod.validate_description(Path("agent.toml"), "Read-only reviewer. RU: ревьюер.", failures)

    assert any("start with Russian" in failure for failure in failures)


def test_valid_description_passes() -> None:
    failures: list[str] = []

    mod.validate_description(Path("agent.toml"), "Ревьюер качества. EN: quality reviewer.", failures)

    assert failures == []


def test_disabled_mcp_transport_requires_registry_env_vars(tmp_path: Path) -> None:
    agent = tmp_path / "quality-reviewer.toml"
    agent.write_text(
        "\n".join(
            [
                'name = "quality-reviewer"',
                'description = "Ревьюер качества. EN: quality reviewer."',
                'model = "gpt-5.5"',
                'model_reasoning_effort = "medium"',
                "",
                "[mcp_servers.github]",
                "enabled = false",
                'command = "github-mcp-server"',
                'args = ["stdio"]',
                "",
            ]
        ),
        encoding="utf-8",
    )
    registry = {
        "github": {
            "command": "github-mcp-server",
            "args": ["stdio"],
            "env_vars": ["GITHUB_PERSONAL_ACCESS_TOKEN"],
        }
    }

    failures: list[str] = []
    mod.validate_agent(agent, registry, failures)

    assert any("must copy env_vars" in failure for failure in failures)


def test_real_agents_validate_against_real_registry() -> None:
    registry_path = mod.ROOT / "plugins/rldyour-mcps/.mcp.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))["mcpServers"]
    failures: list[str] = []
    for path in sorted((mod.ROOT / "system/agents").glob("*.toml")):
        mod.validate_agent(path, registry, failures)

    assert failures == []


def test_agent_rejects_bad_identity_model_and_builtin_mcp(tmp_path: Path) -> None:
    agent = tmp_path / "quality-reviewer.toml"
    agent.write_text(
        "\n".join(
            [
                'name = "wrong-name"',
                'description = "Read-only reviewer. RU: ревьюер."',
                'model = "gpt-4"',
                'model_reasoning_effort = "low"',
                "",
                "[mcp_servers.codex_apps]",
                "enabled = false",
                "",
            ]
        ),
        encoding="utf-8",
    )

    failures: list[str] = []
    mod.validate_agent(agent, {}, failures)

    assert any("name must match" in failure for failure in failures)
    assert any("model must be gpt-5.5" in failure for failure in failures)
    assert any("built-in MCP surface codex_apps" in failure for failure in failures)


def test_main_fails_for_empty_agents_dir(tmp_path: Path, monkeypatch, capsys) -> None:
    registry = tmp_path / ".mcp.json"
    registry.write_text(json.dumps({"mcpServers": {}}), encoding="utf-8")
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()
    monkeypatch.setattr(
        "sys.argv",
        ["validate", "--agents-dir", str(agents_dir), "--mcp-config", str(registry)],
    )

    assert mod.main() == 1
    assert "expected managed subagent TOML files" in capsys.readouterr().err
