from __future__ import annotations

from pathlib import Path

from tests.support.importing import import_script


mod = import_script("scripts/scan_text_security.py")


def test_read_text_skips_binary_and_invalid_utf8(tmp_path: Path) -> None:
    binary = tmp_path / "binary.bin"
    binary.write_bytes(b"abc\x00def")
    assert mod.read_text(binary) is None

    invalid = tmp_path / "invalid.txt"
    invalid.write_bytes(b"\xff")
    assert mod.read_text(invalid) is None


def test_scan_file_reports_secret_without_value(tmp_path: Path) -> None:
    path = tmp_path / "workflow.yml"
    token = "ghp_" + "abcdefghijklmnopqrstuvwxyz"
    path.write_text(f"token: {token}\n", encoding="utf-8")
    findings = mod.scan_file(path)
    assert len(findings) == 1
    assert "github-classic-token" in findings[0]
    assert token not in findings[0]


def test_scan_file_reports_hidden_unicode(tmp_path: Path) -> None:
    path = tmp_path / "script.py"
    path.write_text("print('safe')\u200b\n", encoding="utf-8")
    assert "zero-width-control" in mod.scan_file(path)[0]


def test_should_skip_generated_paths() -> None:
    assert mod.should_skip(Path("browser/screenshot.png"))
    assert mod.should_skip(Path(".git/config"))
    assert mod.should_skip(Path(".venv/lib/python/site.py"))
    assert mod.should_skip(Path("dist/release.tar.gz"))
    assert not mod.should_skip(Path("scripts/validate_marketplace.sh"))


def test_fallback_text_files_scans_source_tree_without_git(tmp_path: Path) -> None:
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "tool.py").write_text("print('safe')\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "guide.md").write_text("# Safe\n", encoding="utf-8")
    (tmp_path / "dist").mkdir()
    (tmp_path / "dist" / "artifact.json").write_text("{}", encoding="utf-8")
    (tmp_path / "image.png").write_bytes(b"\x89PNG\r\n")

    files = mod.fallback_text_files(tmp_path)

    assert Path("scripts/tool.py") in files
    assert Path("docs/guide.md") in files
    assert Path("dist/artifact.json") not in files
    assert Path("image.png") not in files


def test_candidate_files_uses_fallback_when_git_is_unavailable(monkeypatch, tmp_path: Path) -> None:
    safe = tmp_path / "safe.md"
    safe.write_text("safe", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(mod, "tracked_files", lambda: set())
    monkeypatch.setattr(mod, "extra_files", lambda: set())
    assert mod.candidate_files() == {Path("safe.md")}


def test_main_scans_tracked_and_extra_files(monkeypatch, tmp_path: Path, capsys) -> None:
    safe = tmp_path / "safe.md"
    safe.write_text("safe", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(mod, "tracked_files", lambda: {Path("safe.md")})
    monkeypatch.setattr(mod, "extra_files", lambda: set())
    assert mod.main() == 0
    assert "1 files checked" in capsys.readouterr().out
