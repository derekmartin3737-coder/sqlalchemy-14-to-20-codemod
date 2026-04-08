from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]

SUPPORTED_CONFIG_FILES = (
    ".eslintrc",
    ".eslintrc.json",
    ".eslintrc.yaml",
    ".eslintrc.yml",
)

UNSUPPORTED_JS_CONFIG_FILES = (
    ".eslintrc.js",
    ".eslintrc.cjs",
    ".eslintrc.mjs",
)

EXISTING_FLAT_CONFIG_FILES = (
    "eslint.config.js",
    "eslint.config.cjs",
    "eslint.config.mjs",
)


def _read_utf8_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


@dataclass(frozen=True)
class LegacyConfigSource:
    path: Path
    kind: str


def find_supported_sources(root: Path) -> list[LegacyConfigSource]:
    sources: list[LegacyConfigSource] = []
    for name in SUPPORTED_CONFIG_FILES:
        path = root / name
        if path.exists():
            sources.append(LegacyConfigSource(path=path, kind=name))

    package_json = root / "package.json"
    if package_json.exists():
        data = _read_utf8_json(package_json)
        if isinstance(data.get("eslintConfig"), dict):
            sources.append(LegacyConfigSource(path=package_json, kind="package.json"))

    return sources


def find_unsupported_js_sources(root: Path) -> list[Path]:
    return [
        root / name for name in UNSUPPORTED_JS_CONFIG_FILES if (root / name).exists()
    ]


def find_existing_flat_configs(root: Path) -> list[Path]:
    return [
        root / name for name in EXISTING_FLAT_CONFIG_FILES if (root / name).exists()
    ]


def load_legacy_config(source: LegacyConfigSource) -> dict[str, Any]:
    text = source.path.read_text(encoding="utf-8")
    if source.kind == "package.json":
        package_data = json.loads(source.path.read_text(encoding="utf-8-sig"))
        config = package_data.get("eslintConfig")
    elif source.kind == ".eslintrc.json":
        config = json.loads(text)
    else:
        config = yaml.safe_load(text)

    if not isinstance(config, dict):
        raise ValueError("Legacy ESLint config must parse to an object.")
    return config


def load_package_json(root: Path) -> dict[str, Any] | None:
    package_json = root / "package.json"
    if not package_json.exists():
        return None
    data = _read_utf8_json(package_json)
    if not isinstance(data, dict):
        raise ValueError("package.json root must be an object.")
    return data
