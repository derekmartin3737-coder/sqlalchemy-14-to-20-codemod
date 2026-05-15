from __future__ import annotations

import argparse
import sys
from pathlib import Path

from apple_privacy_manifest_composer.reporting import report_to_html, report_to_json
from apple_privacy_manifest_composer.scanner import (
    DEFAULT_HTML_REPORT,
    DEFAULT_JSON_REPORT,
    scan_repo,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="apple-privacy-manifest-composer",
        description="Scan an Apple app repo for privacy manifest readiness.",
    )
    parser.add_argument("path", help="Project path to scan.")
    parser.add_argument(
        "--report",
        default=DEFAULT_JSON_REPORT,
        help=f"Path for JSON report. Default: {DEFAULT_JSON_REPORT}",
    )
    parser.add_argument(
        "--html-report",
        default=DEFAULT_HTML_REPORT,
        help=f"Path for HTML report. Default: {DEFAULT_HTML_REPORT}",
    )
    parser.add_argument(
        "--candidate",
        help="Optional path to write PrivacyInfo.xcprivacy candidate output.",
    )
    parser.add_argument("--no-html", action="store_true", help="Skip HTML output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        report = scan_repo(args.path, candidate_path=args.candidate)
    except (FileNotFoundError, OSError, UnicodeDecodeError) as exc:
        print(f"scanner error: {exc}", file=sys.stderr)
        return 2

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_to_json(report), encoding="utf-8")

    if not args.no_html:
        html_path = Path(args.html_report)
        html_path.parent.mkdir(parents=True, exist_ok=True)
        html_path.write_text(report_to_html(report), encoding="utf-8")

    print(
        "apple-privacy-manifest-composer: "
        f"status={report.status} "
        f"findings={len(report.findings)} "
        f"blocking={len(report.blocking_findings)} "
        f"api_hits={len(report.api_hits)} "
        f"sdk_hits={len(report.sdk_hits)}"
    )
    return 1 if report.blocking_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
