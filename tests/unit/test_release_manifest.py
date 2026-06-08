from __future__ import annotations

from pathlib import Path

from tests.support.importing import import_script


mod = import_script("scripts/release_manifest.py")


def test_parse_env_file(tmp_path: Path) -> None:
    env_file = tmp_path / "versions.env"
    env_file.write_text("A=1\n# comment\nB='two'\nC=\"three\"\n", encoding="utf-8")
    assert mod.parse_env_file(env_file) == {"A": "1", "B": "two", "C": "three"}


def test_plugin_manifests_include_known_plugins() -> None:
    manifests = mod.plugin_manifests()
    names = {manifest["name"] for manifest in manifests}
    assert {"rldyour-flow", "rldyour-mcps", "rldyour-serena-mcp"} <= names
    assert manifests == sorted(manifests, key=lambda item: item["name"])


def test_mcp_servers_include_known_servers() -> None:
    servers = mod.mcp_servers()
    assert {"serena", "chrome-devtools", "openaiDeveloperDocs"} <= set(servers)
    assert "playwright" not in servers
