from __future__ import annotations

from pathlib import Path

IGNORED_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "build",
    "dist",
    "node_modules",
    "__pycache__",
}


def _is_ignored(path: Path) -> bool:
    return bool(set(path.parts) & IGNORED_PARTS)


def all_files(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*") if path.is_file() and not _is_ignored(path)
    )


def workflow_files(root: Path) -> list[Path]:
    workflow_root = root / ".github" / "workflows"
    if not workflow_root.exists():
        return []
    return sorted(
        path
        for path in [*workflow_root.glob("*.yml"), *workflow_root.glob("*.yaml")]
        if path.is_file()
    )


def relative(root: Path, path: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/")
