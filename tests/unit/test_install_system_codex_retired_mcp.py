from __future__ import annotations

import subprocess
import tomllib
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(
    ("name", "config_text"),
    [
        (
            "table",
            """
[mcp_servers.semgrep]
command = "uvx"
args = ["--from", "semgrep==1.164.0", "semgrep", "mcp"]
""",
        ),
        (
            "dotted",
            """
mcp_servers.semgrep.command = "uvx"
mcp_servers.semgrep.args = ["--from", "semgrep==1.164.0", "semgrep", "mcp"]
""",
        ),
        (
            "inline",
            """
mcp_servers = { semgrep = { command = "uvx", args = ["--from", "semgrep==1.164.0", "semgrep", "mcp"] } }
""",
        ),
        (
            "parent-table",
            """
[mcp_servers]
semgrep = { command = "uvx", args = ["--from", "semgrep==1.164.0", "semgrep", "mcp"] }
""",
        ),
    ],
)
def test_installer_removes_retired_semgrep_mcp_forms(tmp_path: Path, name: str, config_text: str) -> None:
    codex_home = tmp_path / name
    codex_home.mkdir()
    config = codex_home / "config.toml"
    config.write_text(config_text.strip() + "\n", encoding="utf-8")

    subprocess.run(
        ["bash", "scripts/install_system_codex.sh", "--apply", "--codex-home", str(codex_home)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    text = config.read_text(encoding="utf-8")

    assert "mcp_servers.semgrep" not in text
    assert "semgrep mcp" not in text
    assert "semgrep==" not in text
    assert "semgrep_semgrep_scan" not in text
    data = tomllib.loads(text)
    assert "semgrep" not in data.get("mcp_servers", {})
    subprocess.run(
        ["bash", "scripts/doctor_system_codex.sh", "--quick", "--codex-home", str(codex_home)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )


def test_installer_preserves_custom_inline_mcp_server_while_removing_semgrep(tmp_path: Path) -> None:
    codex_home = tmp_path / "custom-inline"
    codex_home.mkdir()
    config = codex_home / "config.toml"
    config.write_text(
        """
mcp_servers = { custom = { command = "custom-mcp", args = ["--ok"], env = { SAFE = "1" } }, semgrep = { command = "uvx", args = ["--from", "semgrep==1.164.0", "semgrep", "mcp"] } }
""".strip()
        + "\n",
        encoding="utf-8",
    )

    subprocess.run(
        ["bash", "scripts/install_system_codex.sh", "--apply", "--codex-home", str(codex_home)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    data = tomllib.loads(config.read_text(encoding="utf-8"))

    assert data["mcp_servers"]["custom"]["command"] == "custom-mcp"
    assert data["mcp_servers"]["custom"]["env"]["SAFE"] == "1"
    assert "semgrep" not in data["mcp_servers"]
