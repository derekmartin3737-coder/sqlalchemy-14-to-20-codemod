from __future__ import annotations

from pathlib import Path

from apple_privacy_manifest_composer.patterns import DEPENDENCY_FILE_NAMES

SOURCE_SUFFIXES = {
    ".swift",
    ".m",
    ".mm",
    ".c",
    ".cc",
    ".cpp",
    ".h",
    ".hpp",
}

IGNORED_PARTS = {
    ".build",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "build",
    "DerivedData",
    "dist",
    "Pods/Headers",
    "__pycache__",
}


def _is_ignored(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & IGNORED_PARTS)


def discover_source_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in SOURCE_SUFFIXES
        and not _is_ignored(path)
    )


def discover_manifest_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("PrivacyInfo.xcprivacy")
        if path.is_file() and not _is_ignored(path)
    )


def discover_dependency_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.name.lower() in DEPENDENCY_FILE_NAMES
        and not _is_ignored(path)
    )
