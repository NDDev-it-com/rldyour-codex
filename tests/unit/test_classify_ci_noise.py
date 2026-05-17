from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from tests.support.importing import import_script


mod = import_script("scripts/classify_ci_noise.py")


def test_known_noise_is_classified_as_benign() -> None:
    benign, unknown = mod.classify_lines(
        [
            'No entry for terminal type "wezterm";',
            "using dumb terminal settings.",
            "Using CPython 3.13.12",
            "Downloading pygments (1.2MiB)",
            " Downloaded pygments",
        ]
    )

    assert len(benign) == 5
    assert unknown == []


def test_unknown_noise_is_reported() -> None:
    benign, unknown = mod.classify_lines(["new unexpected stderr line"])

    assert benign == []
    assert unknown == ["new unexpected stderr line"]


def test_cli_strict_fails_on_unknown_noise(tmp_path: Path) -> None:
    log = tmp_path / "stderr.log"
    log.write_text("unexpected\n", encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, "scripts/classify_ci_noise.py", "--strict", str(log)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert proc.returncode == 1
    assert "Unknown noise lines" in proc.stderr
