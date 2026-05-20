from __future__ import annotations

from pathlib import Path

from tests.support.importing import import_script


mod = import_script("scripts/plugin_cache_contract.py")


def write_manifest(plugin_dir: Path, name: str, version: str) -> None:
    manifest_dir = plugin_dir / ".codex-plugin"
    manifest_dir.mkdir(parents=True)
    (manifest_dir / "plugin.json").write_text(
        f'{{"name":"{name}","version":"{version}"}}',
        encoding="utf-8",
    )


def test_discover_entries_uses_manifest_versioned_cache_path(tmp_path: Path) -> None:
    plugin_dir = tmp_path / "plugins/rldyour-demo"
    write_manifest(plugin_dir, "rldyour-demo", "1.2.3")

    entries = mod.discover_entries(tmp_path, tmp_path / "cache")

    assert entries == [
        mod.PluginCacheEntry(
            name="rldyour-demo",
            version="1.2.3",
            source_dir=plugin_dir,
            cache_dir=tmp_path / "cache/rldyour-demo/1.2.3",
        )
    ]


def test_verify_reports_missing_cache(tmp_path: Path, capsys) -> None:
    entry = mod.PluginCacheEntry(
        name="rldyour-demo",
        version="1.2.3",
        source_dir=tmp_path / "plugins/rldyour-demo",
        cache_dir=tmp_path / "cache/rldyour-demo/1.2.3",
    )

    assert mod.verify([entry]) == 1
    assert "missing cache directory" in capsys.readouterr().err


def test_verify_accepts_matching_source_and_cache(tmp_path: Path) -> None:
    source = tmp_path / "plugins/rldyour-demo"
    cache = tmp_path / "cache/rldyour-demo/1.2.3"
    write_manifest(source, "rldyour-demo", "1.2.3")
    write_manifest(cache, "rldyour-demo", "1.2.3")
    (source / "skills").mkdir()
    (cache / "skills").mkdir()

    entry = mod.PluginCacheEntry("rldyour-demo", "1.2.3", source, cache)

    assert mod.verify([entry]) == 0
