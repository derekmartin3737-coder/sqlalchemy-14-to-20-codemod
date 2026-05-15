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

DEPENDENCY_FILE_NAMES = {
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "pyproject.toml",
    "requirements.txt",
    "poetry.lock",
    "go.mod",
    "go.sum",
    "Cargo.toml",
    "Cargo.lock",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "Gemfile",
    "Gemfile.lock",
    "composer.json",
    "composer.lock",
}

SBOM_SUFFIXES = (".cdx.json", ".cdx.xml", ".spdx.json", ".spdx", ".spdx.yml")
RELEASE_FILE_NAMES = {
    "CHANGELOG.md",
    "RELEASES.md",
    "RELEASE_NOTES.md",
    "release-notes.md",
}
INCIDENT_FILE_NAMES = {
    "incident-response.md",
    "incident-response-plan.md",
    "vulnerability-handling.md",
    "vulnerability-disclosure.md",
}


def _is_ignored(path: Path) -> bool:
    return bool(set(path.parts) & IGNORED_PARTS)


def all_files(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*") if path.is_file() and not _is_ignored(path)
    )


def relative(root: Path, path: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/")
