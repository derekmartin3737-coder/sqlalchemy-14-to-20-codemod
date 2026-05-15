from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

from apple_privacy_manifest_composer.cli import main
from apple_privacy_manifest_composer.manifest import PLACEHOLDER_REASON
from apple_privacy_manifest_composer.reporting import report_to_html, report_to_json
from apple_privacy_manifest_composer.scanner import scan_repo

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
WORK = Path(__file__).resolve().parents[1] / ".test-work"


def _copy_fixture(name: str) -> Path:
    destination = WORK / f"{name}-{uuid.uuid4().hex}"
    destination.parent.mkdir(exist_ok=True)
    shutil.copytree(FIXTURES / name, destination)
    return destination


def test_risky_app_reports_api_sdk_and_candidate_manifest() -> None:
    repo = _copy_fixture("risky_app")

    report = scan_repo(repo)
    rule_ids = {finding.rule_id for finding in report.findings}
    categories = {hit.category for hit in report.api_hits}
    sdk_names = {hit.name for hit in report.sdk_hits}

    assert "APM001" in rule_ids
    assert "APM003" in rule_ids
    assert "APM004" in rule_ids
    assert "NSPrivacyAccessedAPICategoryUserDefaults" in categories
    assert "NSPrivacyAccessedAPICategoryFileTimestamp" in categories
    assert "firebasecore" in sdk_names
    assert report.candidate_manifest is not None
    assert PLACEHOLDER_REASON in report.candidate_manifest.xml
    assert report.status == "manual_review_required"
    assert "Apple Privacy Manifest Report" in report_to_html(report)
    assert json.loads(report_to_json(report))["candidate_manifest"]["categories"]


def test_candidate_write_creates_review_plist_only_when_requested() -> None:
    repo = _copy_fixture("risky_app")
    candidate = repo / "Generated" / "PrivacyInfo.xcprivacy"

    report = scan_repo(repo, candidate_path=candidate)

    assert candidate.exists()
    assert report.candidate_manifest is not None
    assert report.candidate_manifest.written is True
    assert "Generated/PrivacyInfo.xcprivacy" in report.candidate_manifest.path


def test_existing_manifest_reports_only_missing_categories() -> None:
    repo = _copy_fixture("partial_manifest_app")

    report = scan_repo(repo)

    assert report.candidate_manifest is not None
    assert report.candidate_manifest.categories == [
        "NSPrivacyAccessedAPICategoryFileTimestamp"
    ]
    assert any(finding.rule_id == "APM002" for finding in report.findings)


def test_clean_app_is_clean() -> None:
    repo = _copy_fixture("clean_app")

    report = scan_repo(repo)

    assert report.status == "clean"
    assert report.findings == []
    assert report.candidate_manifest is None


def test_invalid_manifest_blocks_claim() -> None:
    repo = _copy_fixture("broken_manifest_app")

    report = scan_repo(repo)

    assert report.status == "manual_review_required"
    assert any(finding.rule_id == "APM005" for finding in report.findings)


def test_cli_writes_reports_and_candidate() -> None:
    repo = _copy_fixture("risky_app")
    json_path = WORK / f"report-{uuid.uuid4().hex}.json"
    html_path = WORK / f"report-{uuid.uuid4().hex}.html"
    candidate = repo / "PrivacyInfo.xcprivacy.candidate"

    exit_code = main(
        [
            str(repo),
            "--report",
            str(json_path),
            "--html-report",
            str(html_path),
            "--candidate",
            str(candidate),
        ]
    )

    assert exit_code == 1
    assert json_path.exists()
    assert html_path.exists()
    assert candidate.exists()


def test_cli_missing_path_returns_two() -> None:
    assert main([str(WORK / "missing"), "--no-html"]) == 2
