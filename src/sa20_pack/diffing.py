from __future__ import annotations

from difflib import unified_diff


def build_unified_diff(path: str, before: str, after: str) -> str:
    diff = unified_diff(
        before.splitlines(keepends=True),
        after.splitlines(keepends=True),
        fromfile=f"a/{path}",
        tofile=f"b/{path}",
    )
    return "".join(diff)
