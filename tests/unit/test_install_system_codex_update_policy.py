from __future__ import annotations

import subprocess
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TIMEOUT = 60
MANAGED_CONFIGS = (
    "config.toml",
    "rldyour-yolo.config.toml",
    "rldyour-safe.config.toml",
)


def run_installer(codex_home: Path) -> None:
    subprocess.run(
        ["bash", "scripts/install_system_codex.sh", "--apply", "--codex-home", str(codex_home)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
        timeout=DEFAULT_TIMEOUT,
    )


def test_startup_update_check_is_disabled_and_existing_value_is_migrated(tmp_path: Path) -> None:
    codex_home = tmp_path / "managed"
    codex_home.mkdir()
    (codex_home / "config.toml").write_text(
        "check_for_update_on_startup = true\n",
        encoding="utf-8",
    )

    run_installer(codex_home)
    run_installer(codex_home)

    for name in MANAGED_CONFIGS:
        path = codex_home / name
        text = path.read_text(encoding="utf-8")
        data = tomllib.loads(text)
        assert data.get("check_for_update_on_startup") is False
        assert text.count("check_for_update_on_startup =") == 1
