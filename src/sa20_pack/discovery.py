from __future__ import annotations

from pathlib import Path

IGNORED_DIRS = {
    "artifacts",
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "mypy_cache",
    "pycache",
    "ruff_cache",
    "sa20_tmp",
    "test_runs",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
}


def iter_python_files(root: Path) -> list[Path]:
    candidates: list[Path] = []
    for path in root.rglob("*.py"):
        relative_parts = path.relative_to(root).parts
        if any(part in IGNORED_DIRS for part in relative_parts):
            continue
        if path.is_file():
            candidates.append(path)
    return sorted(candidates)
