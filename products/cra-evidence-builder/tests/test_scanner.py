from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

from cra_evidence_builder.cli import main
from cra_evidence_builder.reporting import report_to_html, report_to_json
from cra_evidence_builder.scanner import scan_repo

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
WORK = Path(__file__).resolve().parents[1] / ".test-work"


def _copy_fixture(name: str) -> Path:
    destination = WORK / f"{name}-{uuid.uuid4().hex}"
    destination.parent.mkdir(exist_ok=True)
    shutil.copytree(FIXTURES / name, destination)
    return destination


def test_risky_product_reports_missing_evidence_and_templates() -> None:
    repo = _copy_fixture("risky_product")

    report = scan_repo(repo)
    rule_ids = {finding.rule_id for finding in report.findings}

    assert {"CRA002", "CRA003", "CRA004", "CRA005", "CRA006", "CRA007"} <= rule_ids
    assert report.status == "manual_review_required"
    assert len(report.template_files) == 3
    assert "CRA Evidence Report" in report_to_html(report)
    assert json.loads(report_to_json(report))["template_files"]


def test_write_templates_creates_safe_template_files() -> None:
    repo = _copy_fixture("risky_product")

    report = scan_repo(repo, write_templates=True)

    assert report.status == "manual_review_required"
    assert all(template.written for template in report.template_files)
    assert (repo / "SECURITY.md.cra-template").exists()
    assert (repo / "docs" / "incident-response.cra-template.md").exists()
    assert (repo / "docs" / "cra-release-evidence.cra-template.md").exists()


def test_clean_product_is_clean() -> None:
    repo = _copy_fixture("clean_product")

    report = scan_repo(repo)

    assert report.status == "clean"
    assert report.findings == []
    assert report.template_files == []


def test_broken_manifest_blocks_claim() -> None:
    repo = _copy_fixture("broken_manifest_product")

    report = scan_repo(repo)

    assert any(finding.rule_id == "CRA000" for finding in report.findings)
    assert report.status == "manual_review_required"


def test_cli_writes_reports() -> None:
    repo = _copy_fixture("risky_product")
    json_path = WORK / f"report-{uuid.uuid4().hex}.json"
    html_path = WORK / f"report-{uuid.uuid4().hex}.html"

    exit_code = main(
        [
            str(repo),
            "--write-templates",
            "--report",
            str(json_path),
            "--html-report",
            str(html_path),
        ]
    )

    assert exit_code == 1
    assert json_path.exists()
    assert html_path.exists()
    assert (repo / "SECURITY.md.cra-template").exists()


def test_cli_missing_path_returns_two() -> None:
    assert main([str(WORK / "missing"), "--no-html"]) == 2
