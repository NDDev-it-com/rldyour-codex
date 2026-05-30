from __future__ import annotations

import json
from pathlib import Path

from tests.support.importing import import_script


mod = import_script("scripts/validate_codex_mcp_env_forwarding.py")


def test_source_rejects_literal_secret_placeholder() -> None:
    failures: list[str] = []
    mod.validate_server_map(
        "source",
        {
            "github": {
                "command": "github-mcp-server",
                "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"},
            }
        },
        failures,
    )

    assert any("env.GITHUB_PERSONAL_ACCESS_TOKEN uses placeholder" in failure for failure in failures)


def test_github_env_vars_pass() -> None:
    failures: list[str] = []
    mod.validate_server_map(
        "source",
        {
            "github": {
                "command": "github-mcp-server",
                "env_vars": ["GITHUB_PERSONAL_ACCESS_TOKEN"],
            }
        },
        failures,
    )

    assert failures == []


def test_installed_config_rejects_placeholder(tmp_path: Path) -> None:
    config = tmp_path / "config.toml"
    config.write_text(
        "\n".join(
            [
                "[mcp_servers.github]",
                'command = "github-mcp-server"',
                "",
                "[mcp_servers.github.env]",
                'GITHUB_PERSONAL_ACCESS_TOKEN = "${GITHUB_PERSONAL_ACCESS_TOKEN}"',
                "",
            ]
        ),
        encoding="utf-8",
    )

    failures: list[str] = []
    mod.validate_server_map(str(config), mod.load_installed_servers(config), failures)

    assert any("env.GITHUB_PERSONAL_ACCESS_TOKEN uses placeholder" in failure for failure in failures)


def test_source_loader_accepts_registry_shape(tmp_path: Path) -> None:
    source = tmp_path / ".mcp.json"
    source.write_text(
        json.dumps(
            {
                "mcpServers": {
                    "github": {
                        "command": "github-mcp-server",
                        "env_vars": ["GITHUB_PERSONAL_ACCESS_TOKEN"],
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    assert "github" in mod.load_source_servers(source)


def test_env_vars_shape_and_header_placeholders_are_rejected() -> None:
    failures: list[str] = []
    mod.validate_server_map(
        "source",
        {
            "bad": {
                "env_vars": ["", "${TOKEN}", {"name": "TOKEN", "source": "bad"}, 123],
                "http_headers": {"Authorization": "Bearer ${TOKEN}"},
                "env_http_headers": {"X-Token": "${TOKEN}"},
                "bearer_token_env_var": "${TOKEN}",
            }
        },
        failures,
    )

    assert any("env_vars[0] must not be empty" in failure for failure in failures)
    assert any("http_headers.Authorization uses placeholder" in failure for failure in failures)
    assert any("bearer_token_env_var must name an env var" in failure for failure in failures)


def test_main_validates_temp_source_agents_and_installed_config(tmp_path: Path, monkeypatch, capsys) -> None:
    source = tmp_path / ".mcp.json"
    source.write_text(
        json.dumps(
            {
                "mcpServers": {
                    "github": {
                        "command": "github-mcp-server",
                        "env_vars": ["GITHUB_PERSONAL_ACCESS_TOKEN"],
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()
    config = tmp_path / "config.toml"
    config.write_text(
        "\n".join(
            [
                "[mcp_servers.github]",
                'command = "github-mcp-server"',
                'env_vars = ["GITHUB_PERSONAL_ACCESS_TOKEN"]',
                "",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "validate",
            "--mcp-config",
            str(source),
            "--agents-dir",
            str(agents_dir),
            "--config",
            str(config),
        ],
    )

    assert mod.main() == 0
    assert "OK Codex MCP env forwarding" in capsys.readouterr().out
