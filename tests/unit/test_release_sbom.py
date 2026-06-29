from __future__ import annotations

from tests.support.importing import import_script

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


def test_generate_sbom_declares_agpl_license_for_owned_packages() -> None:
    sbom = mod.generate_sbom()
    packages_by_name = {package["name"]: package for package in sbom["packages"]}

    root = packages_by_name["rldyour-codex"]
    assert root["licenseDeclared"] == "AGPL-3.0-or-later"
    assert root["licenseConcluded"] == "AGPL-3.0-or-later"

    plugin = packages_by_name["rldyour-flow"]
    assert plugin["licenseDeclared"] == "AGPL-3.0-or-later"

    runtime = packages_by_name["codex-cli"]
    assert runtime["licenseDeclared"] == "NOASSERTION"


def test_generate_sbom_namespace_uses_canonical_org() -> None:
    sbom = mod.generate_sbom()
    namespace = sbom["documentNamespace"]
    assert isinstance(namespace, str)
    assert namespace.startswith("https://github.com/NDDev-it-com/rldyour-codex/")
