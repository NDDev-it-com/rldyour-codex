from __future__ import annotations

import json
import os
import subprocess
import sys
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

[mcp_servers.node_repl]
command = "app-node-repl"
args = ["--browser"]
enabled = true
""",
        ),
        (
            "dotted",
            """
mcp_servers.unapproved.command = "custom-mcp"
mcp_servers.unapproved.args = ["--ok"]
mcp_servers.node_repl.command = "app-node-repl"
mcp_servers.node_repl.args = ["--browser"]
mcp_servers.node_repl.enabled = true
plugins."browser@openai-bundled".enabled = true
""",
        ),
        (
            "inline",
            """
mcp_servers = { unapproved = { command = "custom-mcp", args = ["--ok"] }, node_repl = { command = "app-node-repl", args = ["--browser"], enabled = true } }
""",
        ),
        (
            "parent-table",
            """
[mcp_servers]
unapproved = { command = "custom-mcp", args = ["--ok"] }
node_repl = { command = "app-node-repl", args = ["--browser"], enabled = true }
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
    assert data["plugins"]["browser@openai-bundled"]["enabled"] is False
    assert data["mcp_servers"]["node_repl"] == {
        "command": "app-node-repl",
        "args": ["--browser"],
        "enabled": False,
    }
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
custom_root = "kept"
plugins = { "browser@openai-bundled" = { enabled = true }, custom = { enabled = true, channel = "local" } }
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
    assert data["custom_root"] == "kept"
    assert data["plugins"]["browser@openai-bundled"]["enabled"] is False
    assert data["plugins"]["custom"] == {"enabled": True, "channel": "local"}


def set_surface_enabled(config_text: str, header: str) -> str:
    lines = config_text.splitlines()
    current_header = ""
    changed = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            current_header = stripped[1:-1]
            continue
        if current_header == header and stripped == "enabled = false":
            lines[index] = "enabled = true"
            changed = True
            break
    assert changed, f"missing disabled surface table: {header}"
    return "\n".join(lines) + "\n"


def isolated_codex_env(codex_home: Path) -> dict[str, str]:
    fake_codex = codex_home / "fake-codex"
    fake_codex.write_text(
        """#!/usr/bin/env python3
import json
import sys

if sys.argv[1:2] != ["app-server"]:
    raise SystemExit(0)
for line in sys.stdin:
    request = json.loads(line)
    request_id = request.get("id")
    result = {"data": []} if request.get("method") == "hooks/list" else {}
    print(json.dumps({"id": request_id, "result": result}), flush=True)
""",
        encoding="utf-8",
    )
    fake_codex.chmod(0o755)
    env = os.environ.copy()
    env["CODEX_BIN"] = str(fake_codex)
    env["CODEX_HOME"] = str(codex_home)
    return env


def test_installer_disables_app_browser_surfaces_and_preserves_transport_metadata(tmp_path: Path) -> None:
    codex_home = tmp_path / "realistic-app-managed"
    codex_home.mkdir()
    config = codex_home / "config.toml"
    config.write_text(
        (ROOT / "tests/fixtures/codex_app_managed_browser_config.toml").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    install_command = ["bash", "scripts/install_system_codex.sh", "--apply", "--codex-home", str(codex_home)]
    doctor_command = ["bash", "scripts/doctor_system_codex.sh", "--quick", "--codex-home", str(codex_home)]
    env = isolated_codex_env(codex_home)
    subprocess.run(
        install_command,
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
        timeout=DEFAULT_TIMEOUT,
        env=env,
    )

    installed_text = config.read_text(encoding="utf-8")
    data = tomllib.loads(installed_text)
    assert data["plugins"]["browser@openai-bundled"]["enabled"] is False
    assert data["plugins"]["gmail@openai-curated"]["enabled"] is True
    assert data["plugins"]["github@openai-curated"]["enabled"] is True
    assert data["plugins"]["keep-me"] == {"enabled": True, "channel": "local"}
    marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    for entry in marketplace["plugins"]:
        plugin = entry["name"]
        if plugin == "rldyour-orchestrator" and sys.platform != "darwin":
            continue
        assert data["plugins"][f"{plugin}@rldyour-codex"]["enabled"] is True

    node_repl = data["mcp_servers"]["node_repl"]
    assert node_repl["enabled"] is False
    assert node_repl["command"] == "/Applications/Codex.app/Contents/Resources/node"
    assert node_repl["args"] == ["node_repl.js", "--stdio"]
    assert node_repl["startup_timeout_sec"] == 45
    assert node_repl["tool_timeout_sec"] == 180
    assert node_repl["instructions"] == "Use Chrome or the in-app browser when available."
    assert node_repl["env"] == {
        "BROWSER_USE_AVAILABLE_BACKENDS": "chrome,iab",
        "BROWSER_USE_CHROME_PATH": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "KEEP_APP_METADATA": "yes",
    }
    computer_use = data["mcp_servers"]["computer-use"]
    assert computer_use == {
        "command": "/Applications/Codex.app/Contents/Resources/computer-use",
        "args": ["--stdio"],
        "enabled": False,
        "required": False,
        "env": {"COMPUTER_USE_BACKEND": "iab"},
    }
    assert "unapproved" not in data["mcp_servers"]

    chrome_source = json.loads((ROOT / "plugins/rldyour-mcps/.mcp.json").read_text(encoding="utf-8"))["mcpServers"][
        "chrome-devtools"
    ]
    chrome_installed = data["mcp_servers"]["chrome-devtools"]
    assert chrome_installed["command"] == chrome_source["command"] == "/bin/sh"
    assert chrome_installed["args"] == chrome_source["args"]

    subprocess.run(
        doctor_command,
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
        timeout=DEFAULT_TIMEOUT,
        env=env,
    )
    subprocess.run(
        install_command,
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
        timeout=DEFAULT_TIMEOUT,
        env=env,
    )
    reinstalled_text = config.read_text(encoding="utf-8")
    assert tomllib.loads(reinstalled_text) == data

    reinjected = reinstalled_text
    for header in (
        'plugins."browser@openai-bundled"',
        "mcp_servers.node_repl",
        "mcp_servers.computer-use",
    ):
        reinjected = set_surface_enabled(reinjected, header)
    config.write_text(reinjected, encoding="utf-8")
    failed_doctor = subprocess.run(
        doctor_command,
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
        timeout=DEFAULT_TIMEOUT,
        env=env,
    )
    assert failed_doctor.returncode != 0
    assert "app-managed browser plugin explicitly disabled browser@openai-bundled" in failed_doctor.stderr
    assert "app-managed MCP disabled when present node_repl" in failed_doctor.stderr
    assert "app-managed MCP disabled when present computer-use" in failed_doctor.stderr
    assert "rerun" in failed_doctor.stderr
    assert "restart Codex" in failed_doctor.stderr

    subprocess.run(
        install_command,
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
        timeout=DEFAULT_TIMEOUT,
        env=env,
    )
    subprocess.run(
        doctor_command,
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
        timeout=DEFAULT_TIMEOUT,
        env=env,
    )
