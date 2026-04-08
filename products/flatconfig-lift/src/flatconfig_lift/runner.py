from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from flatconfig_lift.discovery import (
    find_existing_flat_configs,
    find_supported_sources,
    find_unsupported_js_sources,
    load_legacy_config,
)
from flatconfig_lift.models import Finding, MigrationReport

DEFAULT_OUTPUT = "eslint.config.cjs"
DEFAULT_REPORT = "flatconfig-lift-report.json"


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _normalize_ignore_pattern(pattern: str) -> tuple[str | None, str | None]:
    normalized = pattern.strip().replace("\\", "/")
    if not normalized:
        return None, None
    if normalized.startswith("!"):
        return None, "Negated ignore patterns need manual review before migration."
    if normalized.startswith("./"):
        normalized = normalized[2:]
    if "/" not in normalized and not normalized.startswith("**/"):
        normalized = f"**/{normalized}"
    return normalized, None


def _extract_ignore_patterns(
    root: Path, legacy_config: dict[str, Any]
) -> tuple[list[str], list[Finding]]:
    findings: list[Finding] = []
    patterns: list[str] = []

    ignore_patterns = legacy_config.get("ignorePatterns")
    if isinstance(ignore_patterns, str):
        ignore_patterns = [ignore_patterns]

    if isinstance(ignore_patterns, list):
        for raw in ignore_patterns:
            if not isinstance(raw, str):
                findings.append(
                    Finding(
                        code="unsupported-ignore-pattern",
                        message="Non-string ignorePatterns entries need manual review.",
                        path="legacy-config",
                    )
                )
                continue
            normalized, error = _normalize_ignore_pattern(raw)
            if error:
                findings.append(
                    Finding(
                        code="unsupported-ignore-pattern",
                        message=error,
                        path="legacy-config",
                    )
                )
                continue
            if normalized is not None:
                patterns.append(normalized)

    ignore_file = root / ".eslintignore"
    if ignore_file.exists():
        for line_number, raw in enumerate(
            ignore_file.read_text(encoding="utf-8").splitlines(), start=1
        ):
            stripped = raw.strip()
            if not stripped or stripped.startswith("#"):
                continue
            normalized, error = _normalize_ignore_pattern(stripped)
            if error:
                findings.append(
                    Finding(
                        code="unsupported-eslintignore-pattern",
                        message=error,
                        path=".eslintignore",
                        line=line_number,
                    )
                )
                continue
            if normalized is not None:
                patterns.append(normalized)

    deduped: list[str] = []
    seen: set[str] = set()
    for pattern in patterns:
        if pattern not in seen:
            deduped.append(pattern)
            seen.add(pattern)
    return deduped, findings


def _build_blocked_report(
    root: Path,
    findings: list[Finding],
    notes: list[str],
) -> MigrationReport:
    return MigrationReport(
        root_path=str(root),
        mode="dry-run",
        created_at=_utc_now(),
        source_path=None,
        source_kind=None,
        output_path=DEFAULT_OUTPUT,
        findings=findings,
        confidence=0.0,
        notes=notes,
    )


def run_migration(root: Path, apply: bool, show_diff: bool) -> MigrationReport:
    del show_diff
    findings: list[Finding] = []
    notes: list[str] = []

    if apply:
        notes.append(
            "Community edition is scan-only. "
            "The commercial pack generates eslint.config.cjs and package updates."
        )

    for path in find_existing_flat_configs(root):
        findings.append(
            Finding(
                code="existing-flat-config",
                message=(
                    "A flat config already exists. Review manually before "
                    "generating another one."
                ),
                path=str(path.relative_to(root)),
            )
        )

    for path in find_unsupported_js_sources(root):
        findings.append(
            Finding(
                code="unsupported-js-config",
                message=(
                    "JS-based legacy ESLint configs are outside current "
                    "supported scope."
                ),
                path=str(path.relative_to(root)),
            )
        )

    sources = find_supported_sources(root)
    if len(sources) == 0:
        findings.append(
            Finding(
                code="no-supported-config",
                message="No supported static legacy ESLint config source was found.",
                path=str(root),
            )
        )
    elif len(sources) > 1:
        findings.append(
            Finding(
                code="multiple-config-sources",
                message=(
                    "Multiple legacy ESLint config sources were found. "
                    "Review manually before migrating."
                ),
                path=", ".join(str(item.path.relative_to(root)) for item in sources),
            )
        )

    if findings:
        return _build_blocked_report(root, findings, notes)

    source = sources[0]
    legacy_config = load_legacy_config(source)
    legacy_copy = deepcopy(legacy_config)
    ignore_patterns, ignore_findings = _extract_ignore_patterns(root, legacy_copy)

    for finding in ignore_findings:
        finding_path = finding.path
        if finding_path == "legacy-config":
            finding_path = str(source.path.relative_to(root))
        findings.append(replace(finding, path=finding_path))

    notes.extend(
        [
            (
                "Public repo reports whether the config is inside supported "
                "scope. The commercial pack generates eslint.config.cjs and "
                "dependency guidance."
            ),
            (f"Supported source detected: {source.path.name}."),
        ]
    )
    if ignore_patterns:
        notes.append(
            "Ignore patterns were detected and would be carried into the "
            "commercial migration pack."
        )

    confidence = 0.94
    if ignore_patterns:
        confidence -= 0.04
    if findings:
        confidence -= 0.2

    return MigrationReport(
        root_path=str(root),
        mode="dry-run",
        created_at=_utc_now(),
        source_path=str(source.path.relative_to(root)),
        source_kind=source.kind,
        output_path=DEFAULT_OUTPUT,
        artifact_changes=[],
        findings=findings,
        migrated_ignore_patterns=ignore_patterns,
        confidence=round(max(confidence, 0.0), 3),
        notes=notes,
    )
