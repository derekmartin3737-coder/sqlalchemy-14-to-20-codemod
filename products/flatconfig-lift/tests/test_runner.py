from __future__ import annotations

import json
import shutil
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from flatconfig_lift.cli import main
from flatconfig_lift.runner import DEFAULT_OUTPUT, run_migration

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
TEST_RUNS = Path(__file__).resolve().parents[1] / "test_runs"


@contextmanager
def _copied_fixture(name: str) -> Iterator[Path]:
    TEST_RUNS.mkdir(exist_ok=True)
    source = FIXTURES / name
    target = TEST_RUNS / f"{name}-{uuid4().hex}"
    shutil.copytree(source, target)
    try:
        yield target
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_json_repo_reports_supported_source_without_writing_files() -> None:
    with _copied_fixture("json_repo") as root:
        report = run_migration(root=root, apply=False, show_diff=True)

        assert report.status == "preview_only"
        assert report.output_path == DEFAULT_OUTPUT
        assert report.files_changed == []
        assert report.source_kind == ".eslintrc.json"
        assert any("commercial pack" in note for note in report.notes)


def test_package_json_source_is_supported() -> None:
    with _copied_fixture("package_json_repo") as root:
        report = run_migration(root=root, apply=False, show_diff=True)

        assert report.status == "preview_only"
        assert report.source_kind == "package.json"
        assert any("Supported source detected" in note for note in report.notes)


def test_yaml_ignore_negation_requires_manual_review() -> None:
    with _copied_fixture("yaml_repo") as root:
        report = run_migration(root=root, apply=False, show_diff=True)

        assert report.status == "manual_review_required"
        assert any(
            finding.code == "unsupported-eslintignore-pattern"
            for finding in report.findings
        )


def test_js_configs_are_blocked() -> None:
    with _copied_fixture("js_repo") as root:
        report = run_migration(root=root, apply=False, show_diff=False)

        assert report.status == "manual_review_required"
        assert any(
            finding.code == "unsupported-js-config" for finding in report.findings
        )


def test_multiple_sources_are_blocked() -> None:
    with _copied_fixture("multiple_repo") as root:
        report = run_migration(root=root, apply=False, show_diff=False)

        assert report.status == "manual_review_required"
        assert any(
            finding.code == "multiple-config-sources" for finding in report.findings
        )


def test_cli_exit_code_two_for_manual_review() -> None:
    with _copied_fixture("js_repo") as root:
        report_path = root / "report.json"

        exit_code = main([str(root), "--report", str(report_path)])

        assert exit_code == 2
        assert report_path.exists()


def test_apply_flag_is_rejected_for_public_repo() -> None:
    with _copied_fixture("json_repo") as root:
        report_path = root / "report.json"

        exit_code = main([str(root), "--apply", "--report", str(report_path)])

        report_data = json.loads(report_path.read_text(encoding="utf-8"))
        assert exit_code == 1
        assert report_data["status"] == "preview_only"
        assert report_data["files_changed"] == []


def test_package_json_with_bom_is_supported() -> None:
    TEST_RUNS.mkdir(exist_ok=True)
    root = TEST_RUNS / f"bom_repo-{uuid4().hex}"
    root.mkdir()
    try:
        (root / "package.json").write_text(
            "\ufeff"
            + json.dumps(
                {
                    "name": "bom-proof",
                    "private": True,
                    "eslintConfig": {"rules": {"semi": ["error", "always"]}},
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        report = run_migration(root=root, apply=False, show_diff=False)

        assert report.status == "preview_only"
        assert report.source_kind == "package.json"
        assert not (root / DEFAULT_OUTPUT).exists()
    finally:
        shutil.rmtree(root, ignore_errors=True)
