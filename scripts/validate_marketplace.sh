#!/usr/bin/env bash
set -euo pipefail

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$ROOT"

UV_BIN=${UV_BIN:-/opt/homebrew/bin/uv}
QUICK_VALIDATE=${QUICK_VALIDATE:-/Users/rldyourmnd/.codex/skills/.system/skill-creator/scripts/quick_validate.py}
CODEX_HOME_DIR=${CODEX_HOME:-/Users/rldyourmnd/.codex}
CACHE_ROOT=${CACHE_ROOT:-"$CODEX_HOME_DIR/plugins/cache/rldyour-codex"}

step() {
  printf '\n== %s ==\n' "$1"
}

step "JSON metadata"
jq empty .agents/plugins/marketplace.json plugins/*/.codex-plugin/plugin.json plugins/rldyour-mcps/.mcp.json plugins/rldyour-serena-mcp/hooks.json plugins/rldyour-flow/hooks.json

step "Skill frontmatter"
skill_count=0
while IFS= read -r skill_md; do
  skill_dir=$(dirname "$skill_md")
  "$UV_BIN" run --with pyyaml python "$QUICK_VALIDATE" "$skill_dir" >/dev/null
  printf 'valid %s\n' "$skill_dir"
  skill_count=$((skill_count + 1))
done < <(find plugins -path '*/skills/*/SKILL.md' -print | sort)
printf 'validated skills: %s\n' "$skill_count"

step "Skill routing descriptions"
python3 - <<'PY'
from pathlib import Path
import re
import sys

MAX_DESCRIPTION_CHARS = 240
errors = []
count = 0
seen_names = {}
seen_descriptions = {}
for path in sorted(Path("plugins").glob("rldyour-*/skills/*/SKILL.md")):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        errors.append(f"{path}: missing YAML frontmatter")
        continue
    frontmatter = match.group(1)
    name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.M)
    desc = re.search(r"^description:\s*(.+)$", frontmatter, re.M)
    if not name_match:
        errors.append(f"{path}: missing name")
        continue
    if not desc:
        errors.append(f"{path}: missing description")
        continue
    name = name_match.group(1).strip().strip("\"'")
    description = desc.group(1).strip().strip("\"'")
    count += 1
    if name in seen_names:
        errors.append(f"{path}: duplicate skill name {name} also used by {seen_names[name]}")
    seen_names[name] = path
    if description in seen_descriptions:
        errors.append(f"{path}: duplicate skill description also used by {seen_descriptions[description]}")
    seen_descriptions[description] = path
    if len(description) > MAX_DESCRIPTION_CHARS:
        errors.append(f"{path}: description length {len(description)} exceeds {MAX_DESCRIPTION_CHARS}")
    if not re.search(r"[А-Яа-яЁё]", description):
        errors.append(f"{path}: description must include Russian trigger phrases")
    if not re.search(r"[A-Za-z]", description):
        errors.append(f"{path}: description must include English trigger phrases")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)

print(f"validated compact bilingual routing descriptions: {count}")
PY

step "OpenAI skill metadata"
"$UV_BIN" run --with pyyaml python - <<'PY'
from pathlib import Path
import re
import sys
import yaml

MAX_DEFAULT_PROMPT_CHARS = 128
MIN_SHORT_DESCRIPTION_CHARS = 25
MAX_SHORT_DESCRIPTION_CHARS = 64
ORCHESTRATED_ONLY = {
    "flow-architecture-review",
    "flow-consistency-review",
    "flow-integration-review",
    "flow-quality-review",
    "flow-security-review",
    "flow-verification-review",
}
KNOWN_MCP_SERVERS = {
    "serena",
    "sequential-thinking",
    "playwright",
    "chrome-devtools",
    "context7",
    "deepwiki",
    "grep",
    "semgrep",
    "shadcn",
    "dart-flutter",
    "figma",
}


def skill_name_for(path: Path) -> str | None:
    skill_md = path.parent.parent / "SKILL.md"
    if not skill_md.is_file():
        return None
    match = re.match(r"^---\n(.*?)\n---\n", skill_md.read_text(encoding="utf-8"), re.S)
    if not match:
        return None
    name = re.search(r"^name:\s*(.+)$", match.group(1), re.M)
    if not name:
        return None
    return name.group(1).strip().strip("\"'")


errors = []
count = 0
for path in sorted(Path("plugins").glob("rldyour-*/skills/*/agents/openai.yaml")):
    count += 1
    skill_name = skill_name_for(path)
    if not skill_name:
        errors.append(f"{path}: cannot resolve sibling SKILL.md name")
        continue
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        errors.append(f"{path}: parse failed: {exc}")
        continue
    interface = data.get("interface") if isinstance(data, dict) else None
    if not isinstance(interface, dict):
        errors.append(f"{path}: missing interface object")
        continue
    short_description = str(interface.get("short_description") or "")
    default_prompt = str(interface.get("default_prompt") or "")
    if not (MIN_SHORT_DESCRIPTION_CHARS <= len(short_description) <= MAX_SHORT_DESCRIPTION_CHARS):
        errors.append(
            f"{path}: interface.short_description length {len(short_description)} must be "
            f"{MIN_SHORT_DESCRIPTION_CHARS}-{MAX_SHORT_DESCRIPTION_CHARS}"
        )
    if len(default_prompt) > MAX_DEFAULT_PROMPT_CHARS:
        errors.append(f"{path}: interface.default_prompt length {len(default_prompt)} exceeds {MAX_DEFAULT_PROMPT_CHARS}")
    if f"${skill_name}" not in default_prompt:
        errors.append(f"{path}: interface.default_prompt must mention ${skill_name}")
    policy = data.get("policy") if isinstance(data, dict) else None
    if not isinstance(policy, dict):
        errors.append(f"{path}: missing policy object")
        continue
    allow_implicit = policy.get("allow_implicit_invocation")
    if skill_name in ORCHESTRATED_ONLY:
        if allow_implicit is not False:
            errors.append(f"{path}: orchestrated reviewer skill must set policy.allow_implicit_invocation=false")
    elif allow_implicit is not True:
        errors.append(f"{path}: policy.allow_implicit_invocation must be true")

    dependencies = data.get("dependencies") if isinstance(data, dict) else None
    tools = dependencies.get("tools", []) if isinstance(dependencies, dict) else []
    if tools is None:
        tools = []
    if not isinstance(tools, list):
        errors.append(f"{path}: dependencies.tools must be a list")
        continue
    for tool in tools:
        if not isinstance(tool, dict):
            errors.append(f"{path}: dependency tool entries must be objects")
            continue
        if tool.get("type") != "mcp":
            errors.append(f"{path}: dependencies.tools only supports type=mcp")
            continue
        value = str(tool.get("value") or "")
        if value not in KNOWN_MCP_SERVERS:
            errors.append(f"{path}: unknown MCP dependency {value!r}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)

print(f"validated OpenAI metadata files: {count}")
PY

step "Shell scripts"
shellcheck plugins/rldyour-serena-mcp/hooks/*.sh plugins/rldyour-serena-mcp/scripts/*.sh plugins/rldyour-flow/hooks/*.sh plugins/rldyour-flow/scripts/*.sh plugins/rldyour-lsps/scripts/*.sh scripts/*.sh

step "Python scripts"
python3 - <<'PY'
from pathlib import Path
import ast

paths = [
    Path("plugins/rldyour-serena-mcp/scripts/serena_memory_state.py"),
    Path("plugins/rldyour-flow/scripts/flow_post_task_state.py"),
]

for path in paths:
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    print(f"syntax ok {path}")
PY

step "LSP health"
plugins/rldyour-lsps/scripts/check_lsps.sh

step "Serena memory state"
python3 plugins/rldyour-serena-mcp/scripts/serena_memory_state.py | python3 -m json.tool >/dev/null

step "Flow post-task state"
plugins/rldyour-flow/scripts/flow_post_task_state.py | python3 -m json.tool >/dev/null

step "MCP registration"
codex mcp list >/dev/null

step "Plugin cache sync"
if [ -d "$CACHE_ROOT" ]; then
  for plugin_dir in plugins/rldyour-*; do
    plugin_name=$(basename "$plugin_dir")
    cache_dir="$CACHE_ROOT/$plugin_name/local"
    if [ ! -d "$cache_dir" ]; then
      printf 'missing cache directory: %s\n' "$cache_dir" >&2
      exit 1
    fi
    diff -qr "$plugin_dir" "$cache_dir" >/dev/null
    printf 'cache in sync %s\n' "$plugin_name"
  done
else
  printf 'cache root missing: %s\n' "$CACHE_ROOT" >&2
  exit 1
fi

step "Secret pattern scan"
if rg -n 'ctx7sk-[A-Za-z0-9-]+|ghp_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+|sk-[A-Za-z0-9_-]{16,}|xox[baprs]-[A-Za-z0-9-]+|BEGIN (RSA|OPENSSH|PRIVATE) KEY|Bearer [A-Za-z0-9._-]+' .serena/memories plugins .agents AGENTS.md README.md scripts system; then
  printf 'Potential secret pattern detected\n' >&2
  exit 1
fi

step "Whitespace"
git diff --check

printf '\nMarketplace validation passed.\n'
