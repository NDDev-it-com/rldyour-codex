from __future__ import annotations

from conftest import import_script


mod = import_script("scripts/release_sbom.py")


def test_spdx_id_sanitizes_names() -> None:
    assert mod.spdx_id("@openai/codex") == "SPDXRef-openai-codex"


def test_generate_sbom_contains_root_plugins_and_runtime_pins() -> None:
    sbom = mod.generate_sbom()
    package_names = {package["name"] for package in sbom["packages"]}

    assert sbom["spdxVersion"] == "SPDX-2.3"
    assert "rldyour-codex" in package_names
    assert "rldyour-flow" in package_names
    assert "codex-cli" in package_names
    assert sbom["relationships"]
