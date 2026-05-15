from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

from package_publisher_hardening.cli import main
from package_publisher_hardening.reporting import report_to_html, report_to_json
from package_publisher_hardening.scanner import scan_repo

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
WORK = Path(__file__).resolve().parents[1] / ".test-work"


def _copy_fixture(name: str) -> Path:
    destination = WORK / f"{name}-{uuid.uuid4().hex}"
    destination.parent.mkdir(exist_ok=True)
    shutil.copytree(FIXTURES / name, destination)
    return destination


def test_risky_repo_reports_tokens_permissions_and_patch_preview() -> None:
    repo = _copy_fixture("risky_repo")
    workflow = repo / ".github" / "workflows" / "release.yml"
    original = workflow.read_text(encoding="utf-8")

    report = scan_repo(repo)
    rule_ids = {finding.rule_id for finding in report.findings}

    assert {"PPH001", "PPH002", "PPH003", "PPH004", "PPH005", "PPH007"} <= rule_ids
    assert report.status == "manual_review_required"
    assert len(report.patches) == 1
    assert "id-token: write" in report.patches[0].diff
    assert workflow.read_text(encoding="utf-8") == original
    assert "Package Publisher Hardening Report" in report_to_html(report)
    assert json.loads(report_to_json(report))["findings"]


def test_apply_writes_only_release_workflow_patch() -> None:
    repo = _copy_fixture("risky_repo")

    report = scan_repo(repo, apply=True)

    assert report.files_changed == [".github/workflows/release.yml"]
    assert "id-token: write" in (
        repo / ".github" / "workflows" / "release.yml"
    ).read_text(encoding="utf-8")
    workflow_text = (repo / ".github" / "workflows" / "release.yml").read_text(
        encoding="utf-8"
    )
    assert "NODE_AUTH_TOKEN" in workflow_text


def test_clean_repo_is_clean() -> None:
    repo = _copy_fixture("clean_repo")

    report = scan_repo(repo)

    assert report.status == "clean"
    assert report.findings == []
    assert report.patches == []


def test_broken_package_blocks_claim() -> None:
    repo = _copy_fixture("broken_package_repo")

    report = scan_repo(repo)

    assert any(finding.rule_id == "PPH000" for finding in report.findings)
    assert report.status == "manual_review_required"


def test_cli_writes_reports() -> None:
    repo = _copy_fixture("risky_repo")
    json_path = WORK / f"report-{uuid.uuid4().hex}.json"
    html_path = WORK / f"report-{uuid.uuid4().hex}.html"

    exit_code = main(
        [str(repo), "--report", str(json_path), "--html-report", str(html_path)]
    )

    assert exit_code == 1
    assert json_path.exists()
    assert html_path.exists()


def test_cli_missing_path_returns_two() -> None:
    assert main([str(WORK / "missing"), "--no-html"]) == 2
