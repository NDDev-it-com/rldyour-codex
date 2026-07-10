from __future__ import annotations

from pathlib import Path

import pytest
from tests.support.importing import import_script

mod = import_script("scripts/validate_browser_provider_policy.py")
ROOT = Path(__file__).resolve().parents[2]


def write_browser_docs(root: Path) -> None:
    docs = {
        mod.MCP_README: """
bootstrap-owned managed wrapper
CloakBrowser-backed
/bin/sh
$HOME/.local/bin/chrome-devtools-mcp
Package-launched local MCP servers
explicit managed-wrapper exception
""",
        mod.BROWSER_README: """
CloakBrowser with no stock Chromium, in-app browser, or raw browser alternative; fail closed.
$HOME/.local/bin/webwright
$HOME/.local/bin/playwright-cli
$HOME/.local/bin/chrome-devtools-mcp
""",
        mod.BROWSER_ROUTING_SKILL: """
CloakBrowser with no stock Chromium, in-app browser, or raw browser alternative; fail closed.
$HOME/.local/bin/webwright
$HOME/.local/bin/playwright-cli
$HOME/.local/bin/chrome-devtools-mcp
""",
    }
    for relative_path, content in docs.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def test_current_browser_docs_contract() -> None:
    mod.validate_browser_docs(ROOT)


def test_rejects_stale_direct_bunx_table(tmp_path: Path) -> None:
    write_browser_docs(tmp_path)
    path = tmp_path / mod.MCP_README
    path.write_text(path.read_text(encoding="utf-8") + mod.STALE_CHROME_TABLE, encoding="utf-8")

    with pytest.raises(mod.Failure, match="stale direct-bunx Chrome table"):
        mod.validate_browser_docs(tmp_path)


def test_rejects_stale_blanket_runtime_rule(tmp_path: Path) -> None:
    write_browser_docs(tmp_path)
    path = tmp_path / mod.MCP_README
    path.write_text(
        path.read_text(encoding="utf-8") + "\n" + mod.STALE_LOCAL_RUNTIME_RULES[1] + "\n",
        encoding="utf-8",
    )

    with pytest.raises(mod.Failure, match="stale blanket local-runtime rule"):
        mod.validate_browser_docs(tmp_path)


def test_rejects_direct_bunx_chrome_package(tmp_path: Path) -> None:
    write_browser_docs(tmp_path)
    path = tmp_path / mod.MCP_README
    path.write_text(
        path.read_text(encoding="utf-8") + "\nbunx chrome-devtools-mcp@1.5.0\n",
        encoding="utf-8",
    )

    with pytest.raises(mod.Failure, match="direct Chrome DevTools package launch"):
        mod.validate_browser_docs(tmp_path)


def test_rejects_raw_browser_fallback(tmp_path: Path) -> None:
    write_browser_docs(tmp_path)
    path = tmp_path / mod.BROWSER_README
    path.write_text(path.read_text(encoding="utf-8") + "\nFallback to raw browser.\n", encoding="utf-8")

    with pytest.raises(mod.Failure, match="unmanaged browser fallback"):
        mod.validate_browser_docs(tmp_path)


def test_requires_every_managed_wrapper(tmp_path: Path) -> None:
    write_browser_docs(tmp_path)
    path = tmp_path / mod.BROWSER_ROUTING_SKILL
    path.write_text(
        path.read_text(encoding="utf-8").replace("$HOME/.local/bin/webwright", "webwright"),
        encoding="utf-8",
    )

    with pytest.raises(mod.Failure, match="missing managed browser contract terms"):
        mod.validate_browser_docs(tmp_path)
