from __future__ import annotations

import difflib
from dataclasses import dataclass
from pathlib import Path

from eslint_v10_radar.models import Patch


@dataclass(frozen=True)
class Replacement:
    path: Path
    rule_id: str
    title: str
    description: str
    before: str
    after: str


def script_replacements(path: Path, text: str) -> list[Replacement]:
    replacements: list[Replacement] = []
    pairs = [
        (
            "ESL004",
            "ESLINT_USE_FLAT_CONFIG=false blocks v10 readiness",
            "Remove ESLINT_USE_FLAT_CONFIG=false from package scripts.",
            "ESLINT_USE_FLAT_CONFIG=false ",
            "",
        ),
        (
            "ESL005",
            "Removed v10_config_lookup_from_file flag is present",
            "Remove removed v10 config lookup flag from package scripts.",
            "ESLINT_FLAGS=v10_config_lookup_from_file ",
            "",
        ),
    ]
    for rule_id, title, description, before, after in pairs:
        if before in text:
            replacements.append(
                Replacement(
                    path=path,
                    rule_id=rule_id,
                    title=title,
                    description=description,
                    before=before,
                    after=after,
                )
            )
    return replacements


def build_patches(root: Path, replacements: list[Replacement]) -> list[Patch]:
    grouped: dict[Path, list[Replacement]] = {}
    for replacement in replacements:
        grouped.setdefault(replacement.path, []).append(replacement)

    patches: list[Patch] = []
    for path, items in grouped.items():
        original = path.read_text(encoding="utf-8")
        updated = original
        for item in items:
            updated = updated.replace(item.before, item.after)
        if updated == original:
            continue
        relative = str(path.relative_to(root)).replace("\\", "/")
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
                rule_id=",".join(sorted({item.rule_id for item in items})),
                title="; ".join(sorted({item.title for item in items})),
                description="; ".join(item.description for item in items),
                diff=diff,
            )
        )
    return patches


def apply_replacements(root: Path, replacements: list[Replacement]) -> list[str]:
    grouped: dict[Path, list[Replacement]] = {}
    for replacement in replacements:
        grouped.setdefault(replacement.path, []).append(replacement)

    changed: list[str] = []
    for path, items in grouped.items():
        original = path.read_text(encoding="utf-8")
        updated = original
        for item in items:
            updated = updated.replace(item.before, item.after)
        if updated == original:
            continue
        path.write_text(updated, encoding="utf-8", newline="")
        changed.append(str(path.relative_to(root)).replace("\\", "/"))
    return sorted(changed)
