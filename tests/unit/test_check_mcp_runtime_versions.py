from __future__ import annotations

import io
import json
from pathlib import Path
import sys

import pytest

from tests.support.importing import import_script


mod = import_script("scripts/check_mcp_runtime_versions.py")


def test_parse_env_file_handles_comments_quotes_and_blanks(tmp_path: Path) -> None:
    env_file = tmp_path / "pins.env"
    env_file.write_text(
        """
# comment
CODEX_CLI_VERSION=0.136.0
SERENA_AGENT_VERSION='1.5.1'
EMPTY_LINE_IGNORED
SHADCN_VERSION="3.5.0"
GITHUB_MCP_SERVER_VERSION="1.1.0"
""",
        encoding="utf-8",
    )
    assert mod.parse_env_file(env_file) == {
        "CODEX_CLI_VERSION": "0.136.0",
        "SERENA_AGENT_VERSION": "1.5.1",
        "SHADCN_VERSION": "3.5.0",
        "GITHUB_MCP_SERVER_VERSION": "1.1.0",
    }


def test_latest_for_rejects_unknown_ecosystem() -> None:
    with pytest.raises(RuntimeError, match="unsupported ecosystem"):
        mod.latest_for(mod.Pin("X", "unknown", "pkg"))


def test_npm_latest_reads_json_string(monkeypatch) -> None:
    monkeypatch.setattr(mod.shutil, "which", lambda command: "/usr/bin/npm" if command == "npm" else None)
    monkeypatch.setattr(mod.subprocess, "check_output", lambda *args, **kwargs: '"1.2.3"')
    assert mod.npm_latest("example") == "1.2.3"


def test_npm_latest_requires_npm(monkeypatch) -> None:
    monkeypatch.setattr(mod.shutil, "which", lambda command: None)
    with pytest.raises(RuntimeError, match="npm command not found"):
        mod.npm_latest("example")


def test_pypi_latest_reads_response(monkeypatch) -> None:
    class Response(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            self.close()

    data = json.dumps({"info": {"version": "4.5.6"}}).encode()
    monkeypatch.setattr(mod.urllib.request, "urlopen", lambda *args, **kwargs: Response(data))
    assert mod.pypi_latest("example") == "4.5.6"


def test_github_release_latest_reads_tag(monkeypatch) -> None:
    class Response(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            self.close()

    data = json.dumps({"tag_name": "v1.1.0"}).encode()
    monkeypatch.setattr(mod.urllib.request, "urlopen", lambda *args, **kwargs: Response(data))
    assert mod.github_release_latest("github/github-mcp-server") == "1.1.0"


def test_pins_include_host_bun_runtime() -> None:
    assert any(pin.key == "BUN_VERSION" and pin.package == "bun" for pin in mod.PINS)


def test_pins_include_github_mcp_server_release() -> None:
    assert any(
        pin.key == "GITHUB_MCP_SERVER_VERSION"
        and pin.ecosystem == "github-release"
        and pin.package == "github/github-mcp-server"
        for pin in mod.PINS
    )


def test_main_json_success(monkeypatch, tmp_path: Path, capsys) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    env_file = config_dir / "mcp-runtime-versions.env"
    env_file.write_text("\n".join(f"{pin.key}=1.0.0" for pin in mod.PINS), encoding="utf-8")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "latest_for", lambda pin: "1.0.0")
    monkeypatch.setattr(sys, "argv", ["check", "--json", "--fail-on-outdated"])
    assert mod.main() == 0
    assert '"status": "current"' in capsys.readouterr().out


def test_main_fail_on_outdated(monkeypatch, tmp_path: Path, capsys) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    env_file = config_dir / "mcp-runtime-versions.env"
    env_file.write_text("\n".join(f"{pin.key}=1.0.0" for pin in mod.PINS), encoding="utf-8")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "latest_for", lambda pin: "2.0.0")
    monkeypatch.setattr(sys, "argv", ["check", "--fail-on-outdated"])
    assert mod.main() == 1
    assert "pinned 1.0.0, latest 2.0.0" in capsys.readouterr().err
