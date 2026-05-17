from __future__ import annotations

from pathlib import Path
import sys

import pytest

from tests.conftest import import_script


mod = import_script("scripts/check_mcp_runtime_versions.py")


def test_parse_env_file_handles_comments_quotes_and_blanks(tmp_path: Path) -> None:
    env_file = tmp_path / "pins.env"
    env_file.write_text(
        """
# comment
CODEX_CLI_VERSION=0.130.0
SERENA_AGENT_VERSION='1.3.0'
EMPTY_LINE_IGNORED
SHADCN_VERSION="3.5.0"
""",
        encoding="utf-8",
    )
    assert mod.parse_env_file(env_file) == {
        "CODEX_CLI_VERSION": "0.130.0",
        "SERENA_AGENT_VERSION": "1.3.0",
        "SHADCN_VERSION": "3.5.0",
    }


def test_latest_for_rejects_unknown_ecosystem() -> None:
    with pytest.raises(RuntimeError, match="unsupported ecosystem"):
        mod.latest_for(mod.Pin("X", "unknown", "pkg"))


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
