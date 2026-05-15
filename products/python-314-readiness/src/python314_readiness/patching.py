from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from pathlib import Path

from python314_readiness.models import Patch


@dataclass(frozen=True)
class Replacement:
    rule_id: str
    title: str
    path: Path
    before: str
    after: str
    description: str


def add_314_to_inline_matrix(text: str) -> tuple[str, str] | None:
    pattern = re.compile(
        r"(?P<line>python-version\s*:\s*\[(?P<body>[^\]]+)\])",
        flags=re.IGNORECASE,
    )
    match = pattern.search(text)
    if not match:
        return None
    line = match.group("line")
    body = match.group("body")
    versions = re.findall(r"['\"]?(\d+\.\d+)['\"]?", body)
    if "3.14" in versions or not versions:
        return None
    quote = '"' if '"' in body else "'"
    separator = ", "
    replacement_body = body.rstrip() + f"{separator}{quote}3.14{quote}"
    replacement_line = line.replace(body, replacement_body)
    return line, replacement_line


def build_patches(root: Path, replacements: list[Replacement]) -> list[Patch]:
    grouped: dict[Path, list[Replacement]] = {}
    for replacement in replacements:
        grouped.setdefault(replacement.path, []).append(replacement)

    patches: list[Patch] = []
    for path, items in grouped.items():
        original = path.read_text(encoding="utf-8")
        updated = original
        used: list[Replacement] = []
        for item in items:
            if item.before not in updated:
                continue
            updated = updated.replace(item.before, item.after, 1)
            used.append(item)
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
                rule_id=",".join(sorted({item.rule_id for item in used})),
                title="; ".join(sorted({item.title for item in used})),
                description="; ".join(item.description for item in used),
                replacements=[(item.before, item.after) for item in used],
                diff=diff,
            )
        )
    return patches


def apply_patches(root: Path, replacements: list[Replacement]) -> list[str]:
    grouped: dict[Path, list[Replacement]] = {}
    for replacement in replacements:
        grouped.setdefault(replacement.path, []).append(replacement)

    changed: list[str] = []
    for path, items in grouped.items():
        original = path.read_text(encoding="utf-8")
        updated = original
        for item in items:
            updated = updated.replace(item.before, item.after, 1)
        if updated == original:
            continue
        path.write_text(updated, encoding="utf-8", newline="")
        changed.append(str(path.relative_to(root)).replace("\\", "/"))
    return sorted(changed)
