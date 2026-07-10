from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/release.yml"


def test_release_workflow_only_publishes_existing_numeric_tags_from_main() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "# manual dispatch only verifies an existing tag" in text
    assert "Existing numeric release tag X.Y.Z" in text
    assert "git ls-remote --refs origin" in text
    assert 'git fetch --no-tags origin "+refs/heads/main:refs/remotes/origin/main"' in text
    assert 'git merge-base --is-ancestor "$GITHUB_SHA" origin/main' in text
    assert 'git merge-base --is-ancestor "$tag_commit" origin/main' in text
    assert 'git rev-parse "${remote_tag_ref}^{commit}"' in text
    assert 'git checkout --detach "$tag_commit"' in text
    assert "grep -Eq '^[0-9]+\\.[0-9]+\\.[0-9]+$'" in text
    assert 'gh release create "$RELEASE_VERSION" --verify-tag' in text

    assert "Create release tag" not in text
    assert re.search(r"(?m)^\s*git\s+tag(?:\s|$)", text) is None
    assert re.search(r"(?m)^\s*git\s+push\b[^\n]*refs/tags", text) is None
