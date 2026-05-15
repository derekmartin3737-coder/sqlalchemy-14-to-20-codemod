from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

from python314_readiness.cli import main
from python314_readiness.reporting import report_to_html, report_to_json
from python314_readiness.scanner import scan_repo

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
WORK = Path(__file__).resolve().parents[1] / ".test-work"


def _copy_fixture(name: str, label: str) -> Path:
    destination = WORK / f"{label}-{uuid.uuid4().hex}"
    destination.parent.mkdir(exist_ok=True)
    shutil.copytree(FIXTURES / name, destination)
    return destination


def test_risky_repo_reports_metadata_source_and_ci_patch_preview(
) -> None:
    repo = _copy_fixture("risky_repo", "risky-dry-run")
    workflow = repo / ".github" / "workflows" / "ci.yml"
    original_workflow = workflow.read_text(encoding="utf-8")

    report = scan_repo(repo)
    rule_ids = {finding.rule_id for finding in report.findings}

    assert {
        "PY314001",
        "PY314002",
        "PY314003",
        "PY314004",
        "PY314006",
        "PY314007",
    } <= rule_ids
    assert report.status == "manual_review_required"
    assert len(report.patches) == 1
    assert '"3.14"' in report.patches[0].diff
    assert workflow.read_text(encoding="utf-8") == original_workflow

    json_report = json.loads(report_to_json(report))
    html_report = report_to_html(report)
    assert json_report["status"] == "manual_review_required"
    assert "Python 3.14 Readiness Report" in html_report


def test_apply_writes_only_ci_matrix_patch() -> None:
    repo = _copy_fixture("risky_repo", "risky-apply")

    report = scan_repo(repo, apply=True)

    assert report.files_changed == [".github/workflows/ci.yml"]
    assert report.patches[0].applied is True
    assert '"3.14"' in (repo / ".github" / "workflows" / "ci.yml").read_text(
        encoding="utf-8"
    )
    assert '<3.14' in (repo / "pyproject.toml").read_text(encoding="utf-8")


def test_clean_repo_is_clean() -> None:
    repo = _copy_fixture("clean_repo", "clean")

    report = scan_repo(repo)

    assert report.status == "clean"
    assert report.findings == []
    assert report.patches == []


def test_old_pydantic_v2_pin_is_reported() -> None:
    repo = _copy_fixture("old_pydantic_v2_repo", "old-pydantic-v2")

    report = scan_repo(repo)
    rule_ids = {finding.rule_id for finding in report.findings}

    assert "PY314005" in rule_ids
    assert "PY314004" not in rule_ids


def test_parse_failure_blocks_readiness_claim() -> None:
    repo = _copy_fixture("broken_python_repo", "broken-python")

    report = scan_repo(repo)

    assert report.status == "manual_review_required"
    assert {finding.rule_id for finding in report.findings} == {"PY314000"}


def test_cli_writes_json_and_html_reports() -> None:
    repo = _copy_fixture("risky_repo", "cli")
    json_path = WORK / "cli-report.json"
    html_path = WORK / "cli-report.html"

    exit_code = main(
        [str(repo), "--report", str(json_path), "--html-report", str(html_path)]
    )

    assert exit_code == 1
    assert json_path.exists()
    assert html_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["findings"]


def test_cli_missing_path_returns_two() -> None:
    exit_code = main([str(WORK / "missing"), "--no-html"])

    assert exit_code == 2
