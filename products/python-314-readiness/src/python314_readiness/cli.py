from __future__ import annotations

import argparse
import sys
from pathlib import Path

from python314_readiness.reporting import report_to_html, report_to_json
from python314_readiness.scanner import (
    DEFAULT_HTML_REPORT,
    DEFAULT_JSON_REPORT,
    scan_repo,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python-314-readiness",
        description="Scan a repository for Python 3.14 readiness risks.",
    )
    parser.add_argument("path", help="Repository path to scan.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply only deterministic CI matrix patches.",
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
    parser.add_argument(
        "--no-html",
        action="store_true",
        help="Skip writing the HTML report.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        report = scan_repo(args.path, apply=args.apply)
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
        "python-314-readiness: "
        f"status={report.status} "
        f"findings={len(report.findings)} "
        f"blocking={len(report.blocking_findings)} "
        f"patches={len(report.patches)}"
    )
    return 1 if report.blocking_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
