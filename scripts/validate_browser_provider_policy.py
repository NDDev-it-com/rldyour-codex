#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = (
    "@playwright/" + "mcp",
    "Playwright " + "MCP",
    "mcp__plugin_rldyour-mcps_" + "playwright",
    "mcp_servers." + "playwright",
    "PLAYWRIGHT_" + "MCP_VERSION",
    "playwright_" + "*",
)
REQUIRED_SKILLS = {
    "browser-tool-routing",
    "browser-validation",
    "browser-debug",
    "playwright-cli-validation",
    "webwright-task",
    "visual-diff-review",
}
CHROME_COMMAND = "/bin/sh"
CHROME_ARGS = [
    "-c",
    'exec "$HOME/.local/bin/chrome-devtools-mcp" --headless --isolated '
    "--no-usage-statistics --no-performance-crux",
]
MCP_README = Path("plugins/rldyour-mcps/README.md")
BROWSER_README = Path("plugins/rldyour-browser/README.md")
BROWSER_ROUTING_SKILL = Path("plugins/rldyour-browser/skills/browser-tool-routing/SKILL.md")
MANAGED_BROWSER_WRAPPERS = (
    "$HOME/.local/bin/webwright",
    "$HOME/.local/bin/playwright-cli",
    "$HOME/.local/bin/chrome-devtools-mcp",
)
DISABLED_CODEX_PLUGINS = {"browser@openai-bundled"}
DISABLED_CODEX_MCP_SERVERS = {"computer-use", "node_repl"}
DISABLED_CODEX_SURFACE_TERMS = (
    "browser@openai-bundled",
    "node_repl",
    "computer-use",
    "enabled = false",
)
STALE_CHROME_TABLE = (
    "| `chrome-devtools` | Page diagnostics through Chrome DevTools | "
    "`bunx`, headless, isolated |"
)
STALE_LOCAL_RUNTIME_RULES = (
    "All local MCP servers must run only through owner-approved runtimes:",
    "Local MCP servers run only through `uv`, `uvx`, `bun`, `bunx`, or `dart`.",
)
DIRECT_CHROME_PACKAGE = re.compile(
    r"\b(?:bunx|npx|npm\s+exec|node)\b[^\n]{0,120}\bchrome-devtools-mcp(?:@[^\s`]*)?\b",
    re.IGNORECASE,
)
UNSAFE_BROWSER_FALLBACK = re.compile(
    r"\b(?:fallback|fall\s+back)\s+(?:to\s+)?(?:the\s+|an?\s+)?"
    r"(?:stock\s+chromium|in-app\s+browser|raw\s+browser)\b",
    re.IGNORECASE,
)


class Failure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Failure(message)


def require_terms(text: str, terms: tuple[str, ...], label: str) -> None:
    missing = [term for term in terms if term not in text]
    require(not missing, f"{label} missing managed browser contract terms: {', '.join(missing)}")


def validate_browser_docs(root: Path = ROOT) -> None:
    docs = {
        MCP_README: (root / MCP_README).read_text(encoding="utf-8"),
        BROWSER_README: (root / BROWSER_README).read_text(encoding="utf-8"),
        BROWSER_ROUTING_SKILL: (root / BROWSER_ROUTING_SKILL).read_text(encoding="utf-8"),
    }
    mcp_readme = docs[MCP_README]
    require(STALE_CHROME_TABLE not in mcp_readme, "MCP README contains the stale direct-bunx Chrome table row")
    for stale_rule in STALE_LOCAL_RUNTIME_RULES:
        require(stale_rule not in mcp_readme, "MCP README contains a stale blanket local-runtime rule")
    require_terms(
        mcp_readme,
        (
            "Package-launched local MCP servers",
            "explicit managed-wrapper exception",
            "bootstrap-owned managed wrapper",
            "CloakBrowser-backed",
            "/bin/sh",
            "$HOME/.local/bin/chrome-devtools-mcp",
        ),
        str(MCP_README),
    )

    for path in (BROWSER_README, BROWSER_ROUTING_SKILL):
        require_terms(
            docs[path],
            MANAGED_BROWSER_WRAPPERS
            + DISABLED_CODEX_SURFACE_TERMS
            + ("CloakBrowser", "stock Chromium", "in-app browser", "raw browser", "fail closed"),
            str(path),
        )

    combined = "\n".join(docs.values())
    direct_match = DIRECT_CHROME_PACKAGE.search(combined)
    require(
        direct_match is None,
        f"browser docs contain a direct Chrome DevTools package launch: {direct_match.group(0) if direct_match else ''}",
    )
    fallback_match = UNSAFE_BROWSER_FALLBACK.search(combined)
    require(
        fallback_match is None,
        f"browser docs allow an unmanaged browser fallback: {fallback_match.group(0) if fallback_match else ''}",
    )


def validate_disabled_codex_surfaces(root: Path = ROOT) -> None:
    contract = json.loads((root / "config/rldyour-contract.json").read_text(encoding="utf-8"))
    surfaces = ((contract.get("browser_providers") or {}).get("disabled_codex_surfaces") or {})
    require(
        surfaces.get("plugins") == sorted(DISABLED_CODEX_PLUGINS),
        "Codex disabled browser plugin contract drift",
    )
    require(
        surfaces.get("mcp_servers") == sorted(DISABLED_CODEX_MCP_SERVERS),
        "Codex disabled app-managed MCP contract drift",
    )

    installer = (root / "scripts/install_system_codex.sh").read_text(encoding="utf-8")
    doctor = (root / "scripts/doctor_system_codex.sh").read_text(encoding="utf-8")
    require_terms(
        installer,
        (
            "disabled_codex_plugins",
            "disabled_codex_mcp_servers",
            "preserved_disabled_mcp_servers",
            'spec["enabled"] = False',
            '"enabled = false"',
        ),
        "scripts/install_system_codex.sh",
    )
    require_terms(
        doctor,
        (
            "disabled_codex_plugins",
            "disabled_codex_mcp_servers",
            "forbidden raw/in-app/computer-use Codex surface",
            "rerun",
            "restart Codex",
        ),
        "scripts/doctor_system_codex.sh",
    )


def text_files() -> list[Path]:
    paths: list[Path] = []
    ignored_report_names = {"coverage.xml", "pytest.xml", "junit.xml"}
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".git", ".venv", "node_modules", "__pycache__", ".pytest_cache"} for part in path.parts):
            continue
        if path.name in ignored_report_names or "htmlcov" in path.parts:
            continue
        if ".serena" in path.parts and "cache" in path.parts:
            continue
        if path.name == "CHANGELOG.md" or "decisions" in path.parts:
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".zip", ".pyc"}:
            continue
        paths.append(path)
    return paths


def validate() -> None:
    validate_browser_docs()
    validate_disabled_codex_surfaces()
    hits: list[str] = []
    allowed_negative_surfaces = (
        "scripts/validate_browser_provider_policy.py",
        "tests/",
    )
    for path in text_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line_no, line in enumerate(text.splitlines(), start=1):
            for pattern in FORBIDDEN:
                if pattern in line:
                    hit = f"{path.relative_to(ROOT)}:{line_no}: {line.strip()}"
                    if not any(surface in hit for surface in allowed_negative_surfaces):
                        hits.append(hit)
    require(not hits, "retired browser MCP references remain:\n" + "\n".join(hits[:40]))

    mcp = json.loads((ROOT / "plugins/rldyour-mcps/.mcp.json").read_text(encoding="utf-8"))["mcpServers"]
    require("playwright" not in mcp, "playwright must not be an active MCP server")
    chrome = mcp.get("chrome-devtools") or {}
    require(bool(chrome), "chrome-devtools MCP server is required")
    require(chrome.get("command") == CHROME_COMMAND, "chrome-devtools must use the managed wrapper shell transport")
    require(chrome.get("args") == CHROME_ARGS, "chrome-devtools must use the exact managed wrapper invocation")
    for agent_path in sorted((ROOT / "system/agents").glob("*.toml")):
        agent = tomllib.loads(agent_path.read_text(encoding="utf-8"))
        agent_chrome = ((agent.get("mcp_servers") or {}).get("chrome-devtools") or {})
        require(
            agent_chrome.get("command") == CHROME_COMMAND and agent_chrome.get("args") == CHROME_ARGS,
            f"{agent_path.relative_to(ROOT)} must copy the exact managed Chrome DevTools transport",
        )

    skills_root = ROOT / "plugins/rldyour-browser/skills"
    for skill in REQUIRED_SKILLS:
        path = skills_root / skill / "SKILL.md"
        require(path.is_file(), f"missing browser skill: {skill}")
    env = (ROOT / "config/mcp-runtime-versions.env").read_text(encoding="utf-8")
    require("CLOAKBROWSER_VERSION=0.4.10" in env, "CloakBrowser wrapper version pin missing")
    require("PLAYWRIGHT_CLI_VERSION=0.1.17" in env, "Playwright CLI version pin missing")
    require("WEBWRIGHT_PIN=4a46f282ec37f27d6003cc498a977939d62d9015" in env, "Webwright pin missing")

    contract = json.loads((ROOT / "config/rldyour-contract.json").read_text(encoding="utf-8"))
    engine = ((contract.get("browser_providers") or {}).get("required_engine") or {})
    require(engine.get("name") == "cloakbrowser", "CloakBrowser must be the required browser engine")
    require(engine.get("version_pin") == "CLOAKBROWSER_VERSION", "CloakBrowser contract version pin drift")
    require(
        engine.get("installer_owner") == "rldyour-new-mac-or-ubuntu",
        "CloakBrowser installer ownership must remain with bootstrap",
    )
    require(
        engine.get("managed_wrapper") == "~/.local/bin/chrome-devtools-mcp",
        "CloakBrowser managed wrapper contract drift",
    )
    require(engine.get("stock_chromium_fallback") is False, "stock Chromium fallback must remain disabled")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Codex browser provider policy.")
    parser.add_argument("--strict", action="store_true")
    parser.parse_args()
    try:
        validate()
    except Failure as exc:
        print(f"ERROR: {exc}", flush=True)
        return 1
    print("ok: Codex browser provider policy validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
