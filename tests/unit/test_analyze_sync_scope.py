from __future__ import annotations

from tests.support.importing import import_script


mod = import_script("plugins/rldyour-serena-mcp/scripts/analyze_sync_scope.py")


def test_taxonomy_contains_indexed_areas() -> None:
    areas = {item["area"] for item in mod.MEMORY_TAXONOMY["areas"]}
    assert {"CORE", "CODEX", "MCP", "SERENA", "HOOKS", "FLOW", "DOCS", "RELEASE", "TECHDEBT", "DESIGN", "LSP", "RULES"} <= areas


def test_classify_core_paths() -> None:
    assert mod._classify("AGENTS.md") == "agent-instructions"
    assert mod._classify(".agents/plugins/marketplace.json") == "marketplace-manifest"
    assert mod._classify("config/mcp-runtime-versions.env") == "mcp-runtime-config"
    assert mod._classify("plugins/rldyour-flow/hooks/session_start_dispatcher.sh") == "rldyour-flow:hooks"
    assert mod._classify("plugins/rldyour-mcps/.mcp.json") == "rldyour-mcps:mcp-transport"
    assert mod._classify(".serena/.sync_marker") == "serena-runtime"


def test_analyze_produces_memory_targets_and_risk() -> None:
    result = mod.analyze(
        [
            "plugins/rldyour-flow/hooks/session_start_dispatcher.sh",
            "scripts/validate_marketplace.sh",
            "docs/release-process.md",
        ]
    )
    assert result["schema_version"] == 2
    assert result["file_count"] == 3
    assert result["risk_profile"]["requires_strong_verification"] is True
    targets = {entry["path"] for entry in result["memory_targets"]}
    assert {"FLOW-01-SDLC.md", "HOOKS-01-LIFECYCLE.md", "RELEASE-01-VALIDATION.md"} <= targets


def test_unique_preserves_order() -> None:
    assert mod._unique(["a", "b", "a", "c"]) == ["a", "b", "c"]
