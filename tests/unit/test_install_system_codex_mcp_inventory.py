from __future__ import annotations

import subprocess
import tomllib
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TIMEOUT = 60


@pytest.mark.parametrize(
    ("name", "config_text"),
    [
        (
            "table",
            """
[mcp_servers.unapproved]
command = "custom-mcp"
args = ["--ok"]
""",
        ),
        (
            "dotted",
            """
mcp_servers.unapproved.command = "custom-mcp"
mcp_servers.unapproved.args = ["--ok"]
""",
        ),
        (
            "inline",
            """
mcp_servers = { unapproved = { command = "custom-mcp", args = ["--ok"] } }
""",
        ),
        (
            "parent-table",
            """
[mcp_servers]
unapproved = { command = "custom-mcp", args = ["--ok"] }
""",
        ),
    ],
)
def test_installer_replaces_unapproved_mcp_forms(tmp_path: Path, name: str, config_text: str) -> None:
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
        timeout=DEFAULT_TIMEOUT,
    )
    data = tomllib.loads(config.read_text(encoding="utf-8"))

    assert "unapproved" not in data.get("mcp_servers", {})
    assert "chrome-devtools" in data.get("mcp_servers", {})
    subprocess.run(
        ["bash", "scripts/doctor_system_codex.sh", "--quick", "--codex-home", str(codex_home)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
        timeout=DEFAULT_TIMEOUT,
    )


def test_installer_does_not_preserve_custom_inline_mcp_server(tmp_path: Path) -> None:
    codex_home = tmp_path / "custom-inline"
    codex_home.mkdir()
    config = codex_home / "config.toml"
    config.write_text(
        """
mcp_servers = { custom = { command = "custom-mcp", args = ["--ok"], env = { SAFE = "1" } } }
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
        timeout=DEFAULT_TIMEOUT,
    )
    data = tomllib.loads(config.read_text(encoding="utf-8"))

    assert "custom" not in data["mcp_servers"]
    assert sorted(data["mcp_servers"])
