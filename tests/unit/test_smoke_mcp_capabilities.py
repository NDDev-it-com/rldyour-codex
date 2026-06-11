from __future__ import annotations

import asyncio
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

from tests.support.importing import REPO_ROOT


def _load_smoke_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "smoke_mcp_capabilities",
        REPO_ROOT / "scripts" / "smoke_mcp_capabilities.py",
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def test_allow_missing_env_skips_startup_required_github(tmp_path: Path) -> None:
    mcp_dir = tmp_path / "plugins" / "rldyour-mcps"
    mcp_dir.mkdir(parents=True)
    github_spec = {
        "command": "/bin/false",
        "env_vars": ["GITHUB_PERSONAL_ACCESS_TOKEN"],
    }
    (mcp_dir / ".mcp.json").write_text(
        json.dumps({"mcpServers": {"github": github_spec}}),
        encoding="utf-8",
    )
    codex_home = tmp_path / "codex-home"
    codex_home.mkdir()
    (codex_home / "config.toml").write_text(
        """
[mcp_servers.github]
command = "/bin/false"
env_vars = ["GITHUB_PERSONAL_ACCESS_TOKEN"]
""".lstrip(),
        encoding="utf-8",
    )
    env = os.environ.copy()
    env.pop("GITHUB_PERSONAL_ACCESS_TOKEN", None)

    proc = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "smoke_mcp_capabilities.py"),
            "--root",
            str(tmp_path),
            "--codex-home",
            str(codex_home),
            "--allow-missing-env",
            "--server",
            "github",
        ],
        text=True,
        capture_output=True,
        check=False,
        timeout=10,
        env=env,
    )

    assert proc.returncode == 0, proc.stderr
    assert "skip    github: startup skipped; missing env: GITHUB_PERSONAL_ACCESS_TOKEN" in proc.stdout


@pytest.mark.no_cover
def test_transient_grep_cancelled_error_is_skip_and_clears_cancellation(monkeypatch) -> None:
    # Direct import verifies the retry helper without enrolling the whole CLI
    # runner in aggregate coverage; the CLI surface is covered by subprocess tests.
    module = _load_smoke_module()

    async def fail_probe(*args, **kwargs) -> tuple[str, str]:
        task = asyncio.current_task()
        assert task is not None
        task.cancel()
        await asyncio.sleep(0)

    async def run_probe() -> tuple[str, str, int]:
        status, message = await module._probe_with_retries(
            "grep",
            {"url": "https://mcp.grep.app"},
            list_only=False,
            allow_missing_env=True,
            include_auth=False,
            timeout=1.0,
            retries=1,
        )
        task = asyncio.current_task()
        assert task is not None
        return status, message, task.cancelling()

    monkeypatch.setattr(module, "_probe_server", fail_probe)

    status, message, cancelling = asyncio.run(run_probe())

    assert status == "skip"
    assert "grep: transient external MCP unavailable" in message
    assert cancelling == 0


@pytest.mark.no_cover
def test_transient_grep_base_exception_group_is_skip(monkeypatch) -> None:
    module = _load_smoke_module()

    async def fail_probe(*args, **kwargs) -> tuple[str, str]:
        raise BaseExceptionGroup(
            "unhandled errors in a TaskGroup",
            [asyncio.CancelledError("Cancelled via cancel scope 123")],
        )

    monkeypatch.setattr(module, "_probe_server", fail_probe)

    status, message = asyncio.run(
        module._probe_with_retries(
            "grep",
            {"url": "https://mcp.grep.app"},
            list_only=False,
            allow_missing_env=True,
            include_auth=False,
            timeout=1.0,
            retries=1,
        )
    )

    assert status == "skip"
    assert "grep: transient external MCP unavailable" in message
