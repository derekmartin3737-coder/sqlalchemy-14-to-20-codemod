from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from pathlib import Path

from actions_upgrade_guard.models import Patch


@dataclass(frozen=True)
class Replacement:
    rule_id: str
    title: str
    path: Path
    before: str
    after: str
    description: str


def replace_action_version(value: str) -> tuple[str, str] | None:
    replacements = {
        "actions/upload-artifact@v3": "actions/upload-artifact@v4",
        "actions/download-artifact@v3": "actions/download-artifact@v4",
        "actions/cache@v1": "actions/cache@v4",
        "actions/cache@v2": "actions/cache@v4",
    }
    return (value, replacements[value]) if value in replacements else None


def _replace_once_in_line(line: str, before: str, after: str) -> str:
    pattern = re.compile(
        rf"(?P<prefix>uses:\s*['\"]?){re.escape(before)}(?P<suffix>['\"]?)"
    )
    return pattern.sub(rf"\g<prefix>{after}\g<suffix>", line, count=1)


def patched_text(original: str, replacements: list[Replacement]) -> str:
    result = original
    for replacement in replacements:
        lines = result.splitlines(keepends=True)
        changed = False
        next_lines: list[str] = []
        for line in lines:
            if not changed and replacement.before in line and "uses:" in line:
                new_line = _replace_once_in_line(
                    line, replacement.before, replacement.after
                )
                changed = new_line != line
                next_lines.append(new_line)
            else:
                next_lines.append(line)
        result = "".join(next_lines)
    return result


def build_patches(root: Path, replacements: list[Replacement]) -> list[Patch]:
    grouped: dict[Path, list[Replacement]] = {}
    for replacement in replacements:
        grouped.setdefault(replacement.path, []).append(replacement)

    patches: list[Patch] = []
    for path, items in grouped.items():
        original = path.read_text(encoding="utf-8")
        updated = patched_text(original, items)
        if updated == original:
            continue
        relative = str(path.relative_to(root))
        diff = "".join(
            difflib.unified_diff(
                original.splitlines(keepends=True),
                updated.splitlines(keepends=True),
                fromfile=f"a/{relative}",
                tofile=f"b/{relative}",
            )
        )
        rule_ids = sorted({item.rule_id for item in items})
        patches.append(
            Patch(
                path=relative,
                rule_id=",".join(rule_ids),
                title="; ".join(sorted({item.title for item in items})),
                description="; ".join(item.description for item in items),
                replacements=[(item.before, item.after) for item in items],
                diff=diff,
            )
        )
    return patches


def apply_patches(root: Path, replacements: list[Replacement]) -> list[str]:
    grouped: dict[Path, list[Replacement]] = {}
    for replacement in replacements:
        grouped.setdefault(replacement.path, []).append(replacement)

    changed_files: list[str] = []
    for path, items in grouped.items():
        original = path.read_text(encoding="utf-8")
        updated = patched_text(original, items)
        if updated == original:
            continue
        path.write_text(updated, encoding="utf-8", newline="")
        changed_files.append(str(path.relative_to(root)).replace("\\", "/"))
    return sorted(changed_files)
