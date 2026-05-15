from __future__ import annotations

from pathlib import Path


def discover_python_files(root: Path) -> list[Path]:
    ignored = {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "__pycache__",
        "build",
        "dist",
        "test_runs",
    }
    files: list[Path] = []
    for path in root.rglob("*.py"):
        if any(part in ignored for part in path.parts):
            continue
        files.append(path)
    return sorted(path for path in files if path.is_file())


def discover_workflow_files(root: Path) -> list[Path]:
    workflow_root = root / ".github" / "workflows"
    if not workflow_root.exists():
        return []
    return sorted(
        path
        for path in [*workflow_root.glob("*.yml"), *workflow_root.glob("*.yaml")]
        if path.is_file()
    )
