from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import uuid
import zipfile
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_PRODUCTS = ROOT / "private_products"
DIST_DIR = PRIVATE_PRODUCTS / "dist"
UPLOAD_DIR = PRIVATE_PRODUCTS / "upload"
SMOKE_RUNS_DIR = PRIVATE_PRODUCTS / "smoke_runs"

EXCLUDED_DIR_NAMES = {
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".pytest_tmp",
    ".ruff_cache",
    "build",
    "build_tmp",
    "dist",
    "flatconfig_tmp",
    "mypy_cache",
    "pycache",
    "pydantic_v2_porter_tmp",
    "pytest_tmp",
    "ruff_cache",
    "sa20_tmp",
    "test_runs",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
TEMP_ENV_KEYS = ("TEMP", "TMP", "TMPDIR")


@dataclass(frozen=True)
class BundleSpec:
    key: str
    source_dir: Path
    archive_name: str
    upload_name: str
    smoke_commands: tuple[tuple[str, ...], ...]
    pythonpath_entry: str | None = None
    required_entries: tuple[str, ...] = ()


BUNDLE_SPECS = {
    "sa20-pack-edge-case-pack": BundleSpec(
        key="sa20-pack-edge-case-pack",
        source_dir=PRIVATE_PRODUCTS / "staging" / "sa20-pack-edge-case-pack-v0.1.0",
        archive_name="sa20-pack-edge-case-pack-v0.1.0-r3.zip",
        upload_name="sa20-pack-edge-case-pack.zip",
        smoke_commands=(
            ("python", "-m", "ruff", "check", ".", "--no-cache"),
            ("python", "-m", "mypy", "src", "tests"),
            ("python", "-m", "sa20_pack.build_runner"),
            ("python", "-m", "pytest", "-p", "no:cacheprovider"),
            (
                "python",
                "-m",
                "sa20_pack.cli",
                "fixtures/demo_repo",
                "--apply",
                "--report",
                "smoke-report.json",
            ),
        ),
        pythonpath_entry="src",
        required_entries=(
            "README.md",
            "pyproject.toml",
            "docs/commercial-case.md",
            "docs/public-proof.md",
            "packaging/INSTALL.md",
            "packaging/COVERAGE.md",
            "packaging/manager-summary.md",
            "packaging/rollout-checklist.md",
            "legal/license-terms.md",
            "legal/refund-policy.md",
            "legal/support-scope.md",
            "legal/terms-of-sale.md",
            "src/sa20_pack/cli.py",
        ),
    ),
    "pydantic-v2-porter-commercial-pack": BundleSpec(
        key="pydantic-v2-porter-commercial-pack",
        source_dir=PRIVATE_PRODUCTS
        / "staging"
        / "pydantic-v2-porter-commercial-pack-v0.1.0",
        archive_name="pydantic-v2-porter-commercial-pack-v0.1.0-r3.zip",
        upload_name="pydantic-v2-porter.zip",
        smoke_commands=(
            ("python", "-m", "ruff", "check", ".", "--no-cache"),
            ("python", "-m", "mypy", "src", "tests"),
            ("python", "-m", "pydantic_v2_porter.build_runner"),
            ("python", "-m", "pytest", "-p", "no:cacheprovider"),
            (
                "python",
                "-m",
                "pydantic_v2_porter.cli",
                "fixtures/simple_repo",
                "--apply",
                "--report",
                "smoke-report.json",
            ),
        ),
        pythonpath_entry="src",
        required_entries=(
            "README.md",
            "pyproject.toml",
            "docs/commercial-case.md",
            "docs/public-proof.md",
            "packaging/INSTALL.md",
            "packaging/COVERAGE.md",
            "packaging/manager-summary.md",
            "packaging/rollout-checklist.md",
            "legal/license-terms.md",
            "legal/refund-policy.md",
            "legal/support-scope.md",
            "legal/terms-of-sale.md",
            "src/pydantic_v2_porter/cli.py",
        ),
    ),
    "sa20-pack-preset-bundle": BundleSpec(
        key="sa20-pack-preset-bundle",
        source_dir=PRIVATE_PRODUCTS / "staging" / "sa20-pack-preset-bundle-v0.1.0",
        archive_name="sa20-pack-preset-bundle-v0.1.0-r3.zip",
        upload_name="sa20-pack-preset-bundle.zip",
        smoke_commands=(),
        required_entries=(
            "README.md",
            "PRESETS.md",
            "limitations.md",
            "legal/license-terms.md",
            "legal/refund-policy.md",
            "legal/support-scope.md",
            "legal/terms-of-sale.md",
            "manager-summary-template.md",
            "rollout-checklist.md",
            "report-templates/migration-report-template.md",
            "report-templates/weekly-status-template.md",
        ),
    ),
}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="release-bundles",
        description=(
            "Build clean private product ZIPs and smoke-test extracted bundles."
        ),
    )
    parser.add_argument(
        "--bundle",
        choices=sorted(BUNDLE_SPECS),
        action="append",
        help="Bundle key to process. Defaults to every configured bundle.",
    )
    parser.add_argument(
        "--skip-smoke",
        action="store_true",
        help="Build and inspect archives without extracting and smoke-testing them.",
    )
    return parser


def _should_exclude(path: Path) -> bool:
    if path.suffix in EXCLUDED_SUFFIXES:
        return True
    return any(part in EXCLUDED_DIR_NAMES for part in path.parts)


def _iter_clean_files(source_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in source_dir.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(source_dir)
        if _should_exclude(relative):
            continue
        files.append(path)
    return sorted(files)


def _scan_archive_for_leaks(archive_path: Path) -> None:
    banned_markers = [
        str(ROOT).encode("utf-8"),
        b"C:\\Users\\",
        b"/Users/",
        b"OneDrive - Oregon State University",
    ]
    with zipfile.ZipFile(archive_path) as bundle:
        for info in bundle.infolist():
            relative = Path(info.filename)
            if info.is_dir():
                continue
            if _should_exclude(relative):
                raise RuntimeError(
                    f"Excluded content leaked into archive: {info.filename}"
                )
            data = bundle.read(info.filename)
            for marker in banned_markers:
                if marker and marker in data:
                    raise RuntimeError(
                        f"Archive content leaks a local path marker in {info.filename}"
                    )


def _next_archive_path(archive_path: Path) -> Path:
    if not archive_path.exists():
        return archive_path

    stem = archive_path.stem
    suffix = archive_path.suffix
    counter = 1
    while True:
        candidate = archive_path.with_name(f"{stem}-rerun{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def _build_archive(spec: BundleSpec) -> Path:
    if not spec.source_dir.exists():
        raise FileNotFoundError(f"Missing source directory: {spec.source_dir}")

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    archive_path = _next_archive_path(DIST_DIR / spec.archive_name)

    clean_files = _iter_clean_files(spec.source_dir)
    if not clean_files:
        raise RuntimeError(f"No files found to package in {spec.source_dir}")

    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in clean_files:
            relative = path.relative_to(spec.source_dir)
            bundle.write(path, relative.as_posix())

    _scan_archive_for_leaks(archive_path)
    return archive_path


def _copy_upload_alias(spec: BundleSpec, archive_path: Path) -> None:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(archive_path, UPLOAD_DIR / spec.upload_name)


def _assert_required_entries(spec: BundleSpec, extracted_root: Path) -> None:
    missing = [
        entry
        for entry in spec.required_entries
        if not (extracted_root / entry).exists()
    ]
    if missing:
        raise RuntimeError(
            "Extracted bundle "
            f"{spec.key} is missing required entries: {', '.join(missing)}"
        )


def _command_env(extracted_root: Path, pythonpath_entry: str | None) -> dict[str, str]:
    env = os.environ.copy()
    temp_root = extracted_root / ".bundle_tmp"
    temp_root.mkdir(parents=True, exist_ok=True)
    for key in TEMP_ENV_KEYS:
        env[key] = str(temp_root)
    env["PYTHONPYCACHEPREFIX"] = str(temp_root / "pycache")
    env["MYPY_CACHE_DIR"] = str(temp_root / "mypy_cache")
    env["RUFF_CACHE_DIR"] = str(temp_root / "ruff_cache")
    if pythonpath_entry is not None:
        env["PYTHONPATH"] = str(extracted_root / pythonpath_entry)
    return env


def _run_smoke_commands(spec: BundleSpec, extracted_root: Path) -> None:
    _assert_required_entries(spec, extracted_root)
    env = _command_env(extracted_root, spec.pythonpath_entry)
    for command in spec.smoke_commands:
        completed = subprocess.run(
            list(command),
            cwd=extracted_root,
            capture_output=True,
            check=False,
            text=True,
            env=env,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"Smoke command failed for {spec.key}: {' '.join(command)}\n"
                f"stdout:\n{completed.stdout}\n"
                f"stderr:\n{completed.stderr}"
            )


def _extract_for_smoke(spec: BundleSpec, archive_path: Path) -> Path:
    SMOKE_RUNS_DIR.mkdir(parents=True, exist_ok=True)
    extracted_root = SMOKE_RUNS_DIR / f"{spec.key}-{uuid.uuid4().hex[:8]}"
    extracted_root.mkdir(parents=True, exist_ok=False)
    with zipfile.ZipFile(archive_path) as bundle:
        bundle.extractall(extracted_root)
    return extracted_root


def process_bundle(spec: BundleSpec, skip_smoke: bool) -> Path:
    archive_path = _build_archive(spec)
    _copy_upload_alias(spec, archive_path)
    if not skip_smoke:
        extracted_root = _extract_for_smoke(spec, archive_path)
        _run_smoke_commands(spec, extracted_root)
    return archive_path


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    bundle_keys = args.bundle or sorted(BUNDLE_SPECS)
    built_archives: list[Path] = []
    for bundle_key in bundle_keys:
        spec = BUNDLE_SPECS[bundle_key]
        built_archives.append(process_bundle(spec, skip_smoke=args.skip_smoke))

    for archive_path in built_archives:
        print(archive_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
