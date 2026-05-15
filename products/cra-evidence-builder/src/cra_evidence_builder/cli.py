from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cra_evidence_builder.reporting import report_to_html, report_to_json
from cra_evidence_builder.scanner import (
    DEFAULT_HTML_REPORT,
    DEFAULT_JSON_REPORT,
    scan_repo,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cra-evidence-builder",
        description="Build a local Cyber Resilience Act evidence-readiness dossier.",
    )
    parser.add_argument("path", help="Project path to scan.")
    parser.add_argument(
        "--write-templates",
        action="store_true",
        help="Write safe .cra-template files for missing evidence artifacts.",
    )
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
    parser.add_argument("--no-html", action="store_true", help="Skip HTML output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        report = scan_repo(args.path, write_templates=args.write_templates)
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
        "cra-evidence-builder: "
        f"status={report.status} "
        f"findings={len(report.findings)} "
        f"blocking={len(report.blocking_findings)} "
        f"evidence={len(report.evidence_items)} "
        f"templates={len(report.template_files)}"
    )
    return 1 if report.blocking_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
