from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from tests.support.importing import REPO_ROOT


def test_static_mode_parses_repo_config_without_installed_codex_home(
    tmp_path: Path,
) -> None:
    mcp_dir = tmp_path / "plugins" / "rldyour-mcps"
    mcp_dir.mkdir(parents=True)
    (mcp_dir / ".mcp.json").write_text(
        json.dumps(
            {
                "mcpServers": {
                    "serena": {
                        "command": "uvx",
                        "args": ["--from", "serena-agent==1.5.3", "serena"],
                    },
                    "openaiDeveloperDocs": {
                        "url": "https://developers.openai.com/mcp",
                    },
                }
            }
        ),
        encoding="utf-8",
    )
    missing_home = tmp_path / "missing-codex-home"
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "smoke_mcp_capabilities.py"),
            "--root",
            str(tmp_path),
            "--codex-home",
            str(missing_home),
            "--mode",
            "static",
            "--json",
        ],
        text=True,
        capture_output=True,
        check=False,
        timeout=10,
    )

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["mode"] == "static"
    assert payload["count"] == 2
    assert payload["errors"] == []
    assert {item["server"] for item in payload["results"]} == {"serena", "openaiDeveloperDocs"}
