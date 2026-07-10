from __future__ import annotations

import json
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
$HOME/.local/bin/playwright-cli
$HOME/.local/bin/chrome-devtools-mcp
browser@openai-bundled node_repl computer-use enabled = false
""",
        mod.BROWSER_ROUTING_SKILL: """
CloakBrowser with no stock Chromium, in-app browser, or raw browser alternative; fail closed.
$HOME/.local/bin/playwright-cli
$HOME/.local/bin/chrome-devtools-mcp
browser@openai-bundled node_repl computer-use enabled = false
""",
    }
    for relative_path, content in docs.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def test_current_browser_docs_contract() -> None:
    mod.validate_browser_docs(ROOT)


def test_current_disabled_codex_surface_contract() -> None:
    mod.validate_disabled_codex_surfaces(ROOT)


def test_current_browser_skills_enforce_mandatory_cloak_boundary() -> None:
    mod.validate_skill_boundaries(ROOT)


def write_disabled_codex_surface_contract(
    root: Path, *, plugins: list[str], servers: list[str]
) -> None:
    contract = root / "config/rldyour-contract.json"
    contract.parent.mkdir(parents=True, exist_ok=True)
    contract.write_text(
        json.dumps(
            {
                "browser_providers": {
                    "disabled_codex_surfaces": {
                        "plugins": plugins,
                        "mcp_servers": servers,
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    scripts = root / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    (scripts / "install_system_codex.sh").write_text(
        "disabled_codex_plugins disabled_codex_mcp_servers preserved_disabled_mcp_servers "
        'spec["enabled"] = False "enabled = false"',
        encoding="utf-8",
    )
    (scripts / "doctor_system_codex.sh").write_text(
        "disabled_codex_plugins disabled_codex_mcp_servers "
        "forbidden raw/in-app/computer-use Codex surface rerun restart Codex",
        encoding="utf-8",
    )


@pytest.mark.parametrize(
    ("plugins", "servers", "message"),
    [
        ([], ["computer-use", "node_repl"], "disabled browser plugin contract drift"),
        (
            ["browser@openai-bundled"],
            ["node_repl"],
            "disabled app-managed MCP contract drift",
        ),
    ],
)
def test_rejects_disabled_codex_surface_contract_drift(
    tmp_path: Path,
    plugins: list[str],
    servers: list[str],
    message: str,
) -> None:
    write_disabled_codex_surface_contract(tmp_path, plugins=plugins, servers=servers)

    with pytest.raises(mod.Failure, match=message):
        mod.validate_disabled_codex_surfaces(tmp_path)


def test_rejects_stale_direct_bunx_table(tmp_path: Path) -> None:
    write_browser_docs(tmp_path)
    path = tmp_path / mod.MCP_README
    path.write_text(
        path.read_text(encoding="utf-8") + mod.STALE_CHROME_TABLE, encoding="utf-8"
    )

    with pytest.raises(mod.Failure, match="stale direct-bunx Chrome table"):
        mod.validate_browser_docs(tmp_path)


def test_rejects_stale_blanket_runtime_rule(tmp_path: Path) -> None:
    write_browser_docs(tmp_path)
    path = tmp_path / mod.MCP_README
    path.write_text(
        path.read_text(encoding="utf-8")
        + "\n"
        + mod.STALE_LOCAL_RUNTIME_RULES[1]
        + "\n",
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
    path.write_text(
        path.read_text(encoding="utf-8") + "\nFallback to raw browser.\n",
        encoding="utf-8",
    )

    with pytest.raises(mod.Failure, match="unmanaged browser fallback"):
        mod.validate_browser_docs(tmp_path)


def test_requires_every_managed_wrapper(tmp_path: Path) -> None:
    write_browser_docs(tmp_path)
    path = tmp_path / mod.BROWSER_ROUTING_SKILL
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "$HOME/.local/bin/playwright-cli", "playwright-cli"
        ),
        encoding="utf-8",
    )

    with pytest.raises(mod.Failure, match="missing managed browser contract terms"):
        mod.validate_browser_docs(tmp_path)


def write_skill_boundary_contract(root: Path) -> None:
    contract = {
        "browser_providers": {
            "required_common_providers": ["playwright-cli", "chrome-devtools-mcp"],
            "compatibility_skill_routes": {
                "webwright-task": ["playwright-cli", "chrome-devtools-mcp"],
            },
            "skill_boundary": {
                "required_skills": sorted(mod.REQUIRED_SKILLS),
                "preflight": {
                    "command": mod.HEALTH_PREFLIGHT,
                    "before_every_browser_action": True,
                    "failure_result": "NOT_PROVEN",
                },
                "playwright_cli": {
                    "executable": mod.PLAYWRIGHT_CLI,
                    "forbidden_arguments": ["run-code", "--filename"],
                },
                "chrome_devtools_mcp_transport": {
                    "command": mod.CHROME_COMMAND,
                    "args": mod.CHROME_ARGS,
                },
                "forbidden_surfaces": mod.FORBIDDEN_POLICY_SURFACES,
            },
        }
    }
    config = root / "config/rldyour-contract.json"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(json.dumps(contract), encoding="utf-8")
    for skill in sorted(mod.REQUIRED_SKILLS):
        path = root / "plugins/rldyour-browser/skills" / skill / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        content = "\n".join(mod.REQUIRED_SKILL_BOUNDARY_TERMS)
        if skill == "webwright-task":
            content += "\nretained only as a compatibility route\n"
        path.write_text(content, encoding="utf-8")


@pytest.mark.parametrize(
    "missing_term",
    [
        mod.HEALTH_PREFLIGHT,
        "Before every browser action",
        "missing or exits nonzero",
        mod.PLAYWRIGHT_CLI,
        "run-code",
        "--filename",
        mod.EXACT_CHROME_TRANSPORT,
        "Webwright runtime",
        "browser_agent",
        "Playwright MCP",
        "alternate CDP",
        "fallback",
    ],
)
def test_rejects_missing_boundary_term_in_each_browser_skill(
    tmp_path: Path, missing_term: str
) -> None:
    write_skill_boundary_contract(tmp_path)
    path = tmp_path / "plugins/rldyour-browser/skills/browser-debug/SKILL.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace(missing_term, "REMOVED", 1),
        encoding="utf-8",
    )

    with pytest.raises(mod.Failure, match="missing managed browser contract terms"):
        mod.validate_skill_boundaries(tmp_path)


def test_rejects_webwright_runtime_reintroduction(tmp_path: Path) -> None:
    write_skill_boundary_contract(tmp_path)
    path = tmp_path / "plugins/rldyour-browser/skills/webwright-task/SKILL.md"
    path.write_text(
        path.read_text(encoding="utf-8") + "\n$HOME/.local/bin/webwright\n",
        encoding="utf-8",
    )

    with pytest.raises(mod.Failure, match="enables Webwright runtime"):
        mod.validate_skill_boundaries(tmp_path)


@pytest.mark.parametrize(
    ("alternate", "message"),
    [
        ("/tmp/playwright-cli", "playwright-cli must use exact"),
        ("/tmp/chrome-devtools-mcp", "chrome-devtools-mcp must use exact"),
    ],
)
def test_rejects_alternate_provider_path_in_skill(
    tmp_path: Path,
    alternate: str,
    message: str,
) -> None:
    write_skill_boundary_contract(tmp_path)
    path = tmp_path / "plugins/rldyour-browser/skills/browser-debug/SKILL.md"
    path.write_text(
        path.read_text(encoding="utf-8") + f"\n{alternate}\n", encoding="utf-8"
    )

    with pytest.raises(mod.Failure, match=message):
        mod.validate_skill_boundaries(tmp_path)


def test_rejects_non_exact_playwright_policy(tmp_path: Path) -> None:
    write_skill_boundary_contract(tmp_path)
    path = tmp_path / "config/rldyour-contract.json"
    contract = json.loads(path.read_text(encoding="utf-8"))
    contract["browser_providers"]["skill_boundary"]["playwright_cli"]["executable"] = (
        "playwright-cli"
    )
    path.write_text(json.dumps(contract), encoding="utf-8")

    with pytest.raises(mod.Failure, match="managed Playwright CLI policy drift"):
        mod.validate_skill_boundaries(tmp_path)


def test_rejects_chrome_transport_drift_in_skill_policy(tmp_path: Path) -> None:
    write_skill_boundary_contract(tmp_path)
    path = tmp_path / "config/rldyour-contract.json"
    contract = json.loads(path.read_text(encoding="utf-8"))
    contract["browser_providers"]["skill_boundary"]["chrome_devtools_mcp_transport"][
        "args"
    ] = [
        "-c",
        "alternate",
    ]
    path.write_text(json.dumps(contract), encoding="utf-8")

    with pytest.raises(
        mod.Failure, match="managed Chrome DevTools MCP skill transport drift"
    ):
        mod.validate_skill_boundaries(tmp_path)
