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

SOURCE_SUFFIXES = {".js", ".cjs", ".mjs", ".ts", ".tsx"}
ESLINTRC_NAMES = {
    ".eslintrc",
    ".eslintrc.json",
    ".eslintrc.yaml",
    ".eslintrc.yml",
    ".eslintrc.js",
    ".eslintrc.cjs",
    ".eslintrc.mjs",
}
FLAT_CONFIG_NAMES = {
    "eslint.config.js",
    "eslint.config.mjs",
    "eslint.config.cjs",
    "eslint.config.ts",
    "eslint.config.mts",
    "eslint.config.cts",
}


def _is_ignored(path: Path) -> bool:
    return bool(set(path.parts) & IGNORED_PARTS)


def all_files(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*") if path.is_file() and not _is_ignored(path)
    )


def relative(root: Path, path: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/")
