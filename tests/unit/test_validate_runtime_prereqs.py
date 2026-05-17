from __future__ import annotations

import json
from pathlib import Path
import sys

from tests.support.importing import import_script


mod = import_script("scripts/validate_runtime_prereqs.py")


def test_missing_launchers_groups_affected_servers(monkeypatch) -> None:
    servers = {
        "serena": {"command": "uvx"},
        "context7": {"command": "bunx"},
        "playwright": {"command": "bunx"},
        "deepwiki": {"url": "https://example.invalid/mcp"},
        "disabled": {"command": "dart", "enabled": False},
    }
    monkeypatch.setattr(mod, "executable_exists", lambda command: command == "uvx")

    assert mod.missing_launchers(servers, require_codex=True) == {
        "bunx": ["context7", "playwright"],
        "codex": ["installer/doctor"],
    }


def test_load_mcp_servers_accepts_registry_shape(tmp_path: Path) -> None:
    path = tmp_path / ".mcp.json"
    path.write_text(json.dumps({"mcpServers": {"serena": {"command": "uvx"}}}), encoding="utf-8")
    assert mod.load_mcp_servers(path) == {"serena": {"command": "uvx"}}


def test_launcher_path_honors_environment_override(monkeypatch) -> None:
    monkeypatch.setenv("BUNX_BIN", "/opt/bin/bunx")
    assert mod.launcher_path("bunx") == "/opt/bin/bunx"
    assert mod.launcher_path("uvx") == "uvx"


def test_executable_exists_checks_absolute_override(monkeypatch, tmp_path: Path) -> None:
    executable = tmp_path / "launcher"
    executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    executable.chmod(0o755)
    monkeypatch.setenv("UVX_BIN", str(executable))
    assert mod.executable_exists("uvx")

    missing = tmp_path / "missing"
    monkeypatch.setenv("UVX_BIN", str(missing))
    assert not mod.executable_exists("uvx")


def test_main_json_reports_missing_without_strict_failure(monkeypatch, tmp_path: Path, capsys) -> None:
    path = tmp_path / ".mcp.json"
    path.write_text(json.dumps({"mcpServers": {"context7": {"command": "bunx"}}}), encoding="utf-8")
    monkeypatch.setattr(mod, "executable_exists", lambda command: False)
    monkeypatch.setattr(sys, "argv", ["validate", "--mcp-config", str(path), "--json"])

    assert mod.main() == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is False
    assert payload["missing"][0]["launcher"] == "bunx"


def test_main_strict_fails_for_missing_launcher(monkeypatch, tmp_path: Path, capsys) -> None:
    path = tmp_path / ".mcp.json"
    path.write_text(json.dumps({"mcpServers": {"serena": {"command": "uvx"}}}), encoding="utf-8")
    monkeypatch.setattr(mod, "executable_exists", lambda command: False)
    monkeypatch.setattr(sys, "argv", ["validate", "--mcp-config", str(path), "--strict"])

    assert mod.main() == 1
    assert "missing launcher: uvx" in capsys.readouterr().err
