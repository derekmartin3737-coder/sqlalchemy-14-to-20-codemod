from __future__ import annotations

import json
import shutil
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from pydantic_v2_porter.cli import main
from pydantic_v2_porter.runner import run_migration

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


def test_simple_repo_reports_supported_candidates() -> None:
    with _copied_fixture("simple_repo") as root:
        report = run_migration(root=root, apply=False, show_diff=True)

        assert report.status == "preview_only"
        assert report.files_changed == []
        assert set(report.transforms_applied) == {
            "config_to_model_config",
            "validate_arguments_to_validate_call",
            "validator_to_field_validator",
        }


def test_pre_validator_reports_mode_before_candidate() -> None:
    with _copied_fixture("pre_validator_repo") as root:
        report = run_migration(root=root, apply=False, show_diff=False)

        assert report.status == "preview_only"
        assert "validator_to_field_validator" in report.transforms_applied


def test_settings_repo_detects_basesettings_move() -> None:
    with _copied_fixture("settings_repo") as root:
        report = run_migration(root=root, apply=False, show_diff=False)

        assert report.status == "preview_only"
        assert "basesettings_import_move" in report.transforms_applied
        assert any("pydantic-settings" in note for note in report.notes)


def test_root_validator_pre_reports_model_validator_candidate() -> None:
    with _copied_fixture("root_before_repo") as root:
        report = run_migration(root=root, apply=False, show_diff=False)

        assert report.status == "preview_only"
        assert "root_validator_to_model_validator" in report.transforms_applied


def test_pydantic_v1_imports_are_detected() -> None:
    with _copied_fixture("pydantic_v1_import_repo") as root:
        report = run_migration(root=root, apply=False, show_diff=False)

        assert report.status == "preview_only"
        assert "pydantic_v1_import_path" in report.transforms_applied


def test_validator_with_values_signature_is_blocked() -> None:
    with _copied_fixture("unsupported_values_repo") as root:
        report = run_migration(root=root, apply=False, show_diff=False)

        assert report.status == "manual_review_required"
        assert any(
            finding.code == "unsupported-validator-signature"
            for finding in report.findings
        )


def test_validator_with_each_item_is_blocked() -> None:
    with _copied_fixture("unsupported_each_item_repo") as root:
        report = run_migration(root=root, apply=False, show_diff=False)

        assert report.status == "manual_review_required"
        assert any(
            finding.code == "unsupported-validator-each-item"
            for finding in report.findings
        )


def test_post_root_validator_is_blocked() -> None:
    with _copied_fixture("unsupported_root_after_repo") as root:
        report = run_migration(root=root, apply=False, show_diff=False)

        assert report.status == "manual_review_required"
        assert any(
            finding.code == "unsupported-root-validator-post"
            for finding in report.findings
        )


def test_removed_config_key_is_blocked() -> None:
    with _copied_fixture("unsupported_config_repo") as root:
        report = run_migration(root=root, apply=False, show_diff=False)

        assert report.status == "manual_review_required"
        assert any(
            finding.code == "unsupported-removed-config-key"
            for finding in report.findings
        )


def test_alias_import_is_blocked() -> None:
    with _copied_fixture("alias_import_repo") as root:
        report = run_migration(root=root, apply=False, show_diff=False)

        assert report.status == "manual_review_required"
        assert any(
            finding.code == "unsupported-import-alias" for finding in report.findings
        )


def test_cli_writes_report_and_uses_exit_code_two_for_manual_review() -> None:
    with _copied_fixture("unsupported_values_repo") as root:
        report_path = root / "report.json"

        exit_code = main([str(root), "--report", str(report_path)])

        report_data = json.loads(report_path.read_text(encoding="utf-8"))
        assert exit_code == 2
        assert report_data["status"] == "manual_review_required"


def test_apply_flag_is_rejected_for_public_repo() -> None:
    with _copied_fixture("simple_repo") as root:
        report_path = root / "report.json"

        exit_code = main([str(root), "--apply", "--report", str(report_path)])

        report_data = json.loads(report_path.read_text(encoding="utf-8"))
        assert exit_code == 1
        assert report_data["status"] == "preview_only"
        assert report_data["files_changed"] == []
