from __future__ import annotations

import difflib
from dataclasses import dataclass
from pathlib import Path

from package_publisher_hardening.models import Patch


@dataclass(frozen=True)
class Replacement:
    path: Path
    rule_id: str
    title: str
    description: str
    before: str
    after: str


def permission_replacements(path: Path, text: str) -> list[Replacement]:
    if "id-token: write" in text:
        return []
    needle = "permissions:\n  contents: read\n"
    if needle not in text:
        return []
    if "npm publish" not in text and "pypa/gh-action-pypi-publish" not in text:
        return []
    return [
        Replacement(
            path=path,
            rule_id="PPH002,PPH005",
            title="Add OIDC permission to publish workflow",
            description="Add id-token: write to simple release workflow permissions.",
            before=needle,
            after="permissions:\n  contents: read\n  id-token: write\n",
        )
    ]


def build_patches(root: Path, replacements: list[Replacement]) -> list[Patch]:
    patches: list[Patch] = []
    for replacement in replacements:
        original = replacement.path.read_text(encoding="utf-8")
        updated = original.replace(replacement.before, replacement.after, 1)
        if updated == original:
            continue
        relative = str(replacement.path.relative_to(root)).replace("\\", "/")
        diff = "".join(
            difflib.unified_diff(
                original.splitlines(keepends=True),
                updated.splitlines(keepends=True),
                fromfile=f"a/{relative}",
                tofile=f"b/{relative}",
            )
        )
        patches.append(
            Patch(
                path=relative,
                rule_id=replacement.rule_id,
                title=replacement.title,
                description=replacement.description,
                diff=diff,
            )
        )
    return patches


def apply_replacements(root: Path, replacements: list[Replacement]) -> list[str]:
    changed: list[str] = []
    for replacement in replacements:
        original = replacement.path.read_text(encoding="utf-8")
        updated = original.replace(replacement.before, replacement.after, 1)
        if updated == original:
            continue
        replacement.path.write_text(updated, encoding="utf-8", newline="")
        changed.append(str(replacement.path.relative_to(root)).replace("\\", "/"))
    return sorted(set(changed))
