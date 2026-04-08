from __future__ import annotations

from pathlib import Path

EXCLUDED_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".pytest_tmp",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "pydantic_v2_porter_tmp",
    "pytest_tmp",
    "test_runs",
    "venv",
}

RELEVANCE_MARKERS = (
    "pydantic",
    "@validator",
    "@root_validator",
    "validate_arguments",
    "BaseSettings",
)


def _is_excluded(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return any(part in EXCLUDED_DIRS for part in relative.parts[:-1])


def discover_python_targets(root: Path) -> list[Path]:
    return [
        path
        for path in sorted(root.rglob("*.py"))
        if not _is_excluded(path, root)
        and any(
            marker in path.read_text(encoding="utf-8", errors="ignore")
            for marker in RELEVANCE_MARKERS
        )
    ]
