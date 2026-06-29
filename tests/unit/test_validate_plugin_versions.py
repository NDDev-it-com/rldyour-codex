from __future__ import annotations

from pathlib import Path

from tests.support.importing import import_script

mod = import_script("scripts/validate_plugin_versions.py")


def test_basic_require_helpers() -> None:
    errors: list[str] = []
    mod.require_semver("1.2.3", "version", errors)
    mod.require_semver("1.2", "bad-version", errors)
    mod.require_non_empty_string("ok", "name", errors)
    mod.require_non_empty_string("", "empty", errors)
    assert "bad-version: expected SemVer string, got '1.2'" in errors
    assert "empty: expected non-empty string" in errors


def test_require_string_list() -> None:
    errors: list[str] = []
    assert mod.require_string_list(["a", "b"], "items", errors) == ["a", "b"]
    assert mod.require_string_list([], "empty-items", errors) == []
    assert mod.require_string_list(["ok", ""], "mixed", errors) == ["ok"]
    assert errors


def test_manifest_metadata_accepts_valid_plugin_shape(tmp_path: Path) -> None:
    plugin_dir = tmp_path / "plugins/rldyour-demo"
    manifest_dir = plugin_dir / ".codex-plugin"
    manifest_dir.mkdir(parents=True)
    (plugin_dir / "skills").mkdir()
    manifest_path = manifest_dir / "plugin.json"
    manifest_path.write_text("{}", encoding="utf-8")

    old_root = mod.ROOT
    mod.ROOT = tmp_path
    try:
        errors: list[str] = []
        manifest = {
            "author": {
                "name": mod.EXPECTED_AUTHOR,
                "email": "rldyourmnd@users.noreply.github.com",
                "url": "https://github.com/rldyourmnd",
            },
            "homepage": mod.EXPECTED_REPOSITORY_URL,
            "repository": mod.EXPECTED_REPOSITORY_URL,
            "license": mod.EXPECTED_PLUGIN_LICENSE,
            "keywords": ["codex"],
            "description": "Демо plugin. EN: demo plugin.",
            "skills": "./skills",
            "interface": {
                "displayName": "Demo",
                "shortDescription": "Демо plugin. EN: demo plugin",
                "longDescription": "Демо plugin для tests. EN: demo plugin for tests.",
                "developerName": mod.EXPECTED_AUTHOR,
                "category": "Development",
                "capabilities": ["skills"],
                "defaultPrompt": ["Используй $demo. EN: use demo."],
                "brandColor": "#123ABC",
                "websiteURL": mod.EXPECTED_REPOSITORY_URL,
                "privacyPolicyURL": mod.EXPECTED_REPOSITORY_URL,
                "termsOfServiceURL": mod.EXPECTED_REPOSITORY_URL,
            },
        }
        mod.require_manifest_metadata(manifest, "rldyour-demo", manifest_path, errors)
        assert errors == []
    finally:
        mod.ROOT = old_root


def test_manifest_metadata_rejects_parent_path(tmp_path: Path) -> None:
    plugin_dir = tmp_path / "plugins/rldyour-demo"
    manifest_dir = plugin_dir / ".codex-plugin"
    manifest_dir.mkdir(parents=True)
    manifest_path = manifest_dir / "plugin.json"
    manifest_path.write_text("{}", encoding="utf-8")
    old_root = mod.ROOT
    mod.ROOT = tmp_path
    try:
        errors: list[str] = []
        mod.require_manifest_metadata({"skills": "./../outside", "interface": {}}, "rldyour-demo", manifest_path, errors)
        assert any("parent-directory" in error for error in errors)
    finally:
        mod.ROOT = old_root


def test_manifest_metadata_rejects_license_and_url_drift(tmp_path: Path) -> None:
    plugin_dir = tmp_path / "plugins/rldyour-demo"
    manifest_dir = plugin_dir / ".codex-plugin"
    manifest_dir.mkdir(parents=True)
    (plugin_dir / "skills").mkdir()
    manifest_path = manifest_dir / "plugin.json"
    manifest_path.write_text("{}", encoding="utf-8")
    old_root = mod.ROOT
    mod.ROOT = tmp_path
    try:
        errors: list[str] = []
        manifest = {
            "author": {"name": "rldyour"},
            "homepage": "https://example.test",
            "repository": "https://example.test/repo",
            "license": "MIT",
            "keywords": ["codex"],
            "skills": "./skills",
            "interface": {
                "displayName": "Demo",
                "shortDescription": "Short",
                "longDescription": "Long enough",
                "developerName": "rldyour",
                "category": "Development",
                "capabilities": ["skills"],
                "defaultPrompt": ["$demo"],
                "brandColor": "#123ABC",
                "websiteURL": "https://example.test",
            },
        }
        mod.require_manifest_metadata(manifest, "rldyour-demo", manifest_path, errors)
        assert "rldyour-demo: license must be AGPL-3.0-or-later" in errors
        assert "rldyour-demo: homepage must be https://github.com/NDDev-it-com/rldyour-codex" in errors
        assert "rldyour-demo: repository must be https://github.com/NDDev-it-com/rldyour-codex" in errors
        assert "rldyour-demo: interface.websiteURL must be https://github.com/NDDev-it-com/rldyour-codex" in errors
    finally:
        mod.ROOT = old_root


def test_main_validates_current_repository() -> None:
    assert mod.main() == 0
