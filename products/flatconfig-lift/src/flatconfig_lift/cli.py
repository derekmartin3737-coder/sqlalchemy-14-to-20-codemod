from __future__ import annotations

import argparse
from pathlib import Path

from flatconfig_lift.models import MigrationReport
from flatconfig_lift.reporting import report_to_json
from flatconfig_lift.runner import DEFAULT_REPORT, run_migration


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="flatconfig-lift",
        description=(
            "Scan an ESLint repo for flat-config migration fit in the public "
            "community edition."
        ),
    )
    parser.add_argument("path", help="Repository path to scan.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Reserved for the commercial pack. The public repo is scan-only.",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="Accepted for compatibility. Community scans do not emit file diffs.",
    )
    parser.add_argument(
        "--report",
        default=DEFAULT_REPORT,
        help="Where to write the machine-generated JSON report.",
    )
    return parser


def _print_summary(report: MigrationReport) -> None:
    print(f"Status: {report.status}")
    print(f"Source: {report.source_path or 'none'}")
    print(f"Output: {report.output_path}")
    print(f"Files changed: {len(report.files_changed)}")
    print(f"Unsupported findings: {len(report.findings)}")
    print(f"Confidence: {report.confidence:.3f}")
    if report.notes:
        print("Notes:")
        for note in report.notes:
            print(f"- {note}")


def _write_report(report: MigrationReport, report_path: Path) -> None:
    report_path.write_text(report_to_json(report), encoding="utf-8")


def _exit_code(report: MigrationReport, apply_requested: bool) -> int:
    if apply_requested:
        return 1
    if report.status in {"preview_only", "applied"}:
        return 0
    if report.status == "manual_review_required":
        return 2
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    root = Path(args.path).resolve()
    report = run_migration(root=root, apply=args.apply, show_diff=args.diff)
    _write_report(report, Path(args.report).resolve())
    if args.apply:
        print(
            "Community edition is scan-only. "
            "Apply mode is only available in the commercial pack."
        )
    _print_summary(report)
    return _exit_code(report, args.apply)


if __name__ == "__main__":
    raise SystemExit(main())
