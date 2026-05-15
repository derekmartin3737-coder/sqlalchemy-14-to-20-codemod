from __future__ import annotations

import plistlib
import re
from datetime import UTC, datetime
from pathlib import Path

from apple_privacy_manifest_composer.discovery import (
    discover_dependency_files,
    discover_manifest_files,
    discover_source_files,
)
from apple_privacy_manifest_composer.manifest import build_candidate_manifest
from apple_privacy_manifest_composer.models import (
    ApiHit,
    CandidateManifest,
    Finding,
    ManifestSummary,
    PrivacyReport,
    SdkHit,
)
from apple_privacy_manifest_composer.patterns import (
    LISTED_THIRD_PARTY_SDKS,
    REQUIRED_REASON_PATTERNS,
)
from apple_privacy_manifest_composer.rules import RULE_PACK_VERSION, rule

PRODUCT = "apple-privacy-manifest-composer"
VERSION = "0.1.0"
DEFAULT_JSON_REPORT = "apple-privacy-report.json"
DEFAULT_HTML_REPORT = "apple-privacy-report.html"


def _relative(root: Path, path: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/")


def _utc_now() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat()


def _finding(
    rule_id: str,
    root: Path,
    path: Path,
    message: str,
    *,
    line: int | None = None,
    current: str | None = None,
    recommended: str | None = None,
    confidence: float = 1.0,
    blocking: bool | None = None,
) -> Finding:
    selected = rule(rule_id)
    if blocking is None:
        blocking = selected.classification in {"autofix", "manual_review", "blocked"}
    return Finding(
        rule_id=selected.id,
        title=selected.title,
        severity=selected.severity,
        classification=selected.classification,
        message=message,
        path=_relative(root, path),
        line=line,
        source_url=selected.source_url,
        source_label=selected.source_label,
        current=current,
        recommended=recommended or selected.recommendation,
        confidence=confidence,
        blocking=blocking,
    )


def _scan_sources(root: Path) -> tuple[list[str], list[ApiHit], list[Finding]]:
    scanned: list[str] = []
    hits: list[ApiHit] = []
    findings: list[Finding] = []
    for path in discover_source_files(root):
        relative = _relative(root, path)
        scanned.append(relative)
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError as exc:
            findings.append(
                _finding(
                    "APM000",
                    root,
                    path,
                    f"Could not read source file: {exc}",
                    current=str(exc),
                )
            )
            continue
        for line_number, line in enumerate(lines, 1):
            for pattern in REQUIRED_REASON_PATTERNS:
                if not pattern.pattern.search(line):
                    continue
                hit = ApiHit(
                    category=pattern.category,
                    path=relative,
                    line=line_number,
                    symbol=pattern.symbol,
                    confidence=pattern.confidence,
                )
                hits.append(hit)
                findings.append(
                    _finding(
                        "APM003",
                        root,
                        path,
                        "Required-reason API usage needs a human-selected "
                        "Apple reason code.",
                        line=line_number,
                        current=pattern.symbol,
                        confidence=pattern.confidence,
                    )
                )
    return scanned, hits, findings


def _scan_manifests(
    root: Path,
) -> tuple[list[str], list[ManifestSummary], list[Finding]]:
    scanned: list[str] = []
    summaries: list[ManifestSummary] = []
    findings: list[Finding] = []
    for path in discover_manifest_files(root):
        scanned.append(_relative(root, path))
        try:
            data = plistlib.loads(path.read_bytes())
        except (plistlib.InvalidFileException, ValueError, OSError) as exc:
            findings.append(
                _finding(
                    "APM005",
                    root,
                    path,
                    f"PrivacyInfo.xcprivacy could not be parsed: {exc}",
                    current=str(exc),
                    confidence=1.0,
                )
            )
            summaries.append(
                ManifestSummary(path=_relative(root, path), valid=False)
            )
            continue
        categories = _declared_categories(data)
        summaries.append(
            ManifestSummary(
                path=_relative(root, path),
                declared_categories=categories,
                valid=True,
            )
        )
    return scanned, summaries, findings


def _declared_categories(data: object) -> list[str]:
    if not isinstance(data, dict):
        return []
    raw_entries = data.get("NSPrivacyAccessedAPITypes", [])
    if not isinstance(raw_entries, list):
        return []
    categories: list[str] = []
    for entry in raw_entries:
        if not isinstance(entry, dict):
            continue
        category = entry.get("NSPrivacyAccessedAPIType")
        if isinstance(category, str):
            categories.append(category)
    return sorted(set(categories))


def _scan_dependencies(root: Path) -> tuple[list[str], list[SdkHit], list[Finding]]:
    scanned: list[str] = []
    sdk_hits: list[SdkHit] = []
    findings: list[Finding] = []
    sdk_patterns = {
        sdk: re.compile(rf"(?<![A-Za-z0-9_]){re.escape(sdk)}(?![A-Za-z0-9_])", re.I)
        for sdk in LISTED_THIRD_PARTY_SDKS
    }
    for path in discover_dependency_files(root):
        relative = _relative(root, path)
        scanned.append(relative)
        text = path.read_text(encoding="utf-8", errors="ignore")
        lines = text.splitlines()
        for sdk, pattern in sdk_patterns.items():
            match_line: int | None = None
            for line_number, line in enumerate(lines, 1):
                if pattern.search(line):
                    match_line = line_number
                    break
            if match_line is None:
                continue
            hit = SdkHit(
                name=sdk,
                path=relative,
                line=match_line,
                confidence=0.88,
            )
            sdk_hits.append(hit)
            findings.append(
                _finding(
                    "APM004",
                    root,
                    path,
                    "Dependency matches Apple's listed third-party SDK set.",
                    line=match_line,
                    current=sdk,
                    confidence=0.88,
                )
            )
    return scanned, sdk_hits, findings


def _missing_categories(
    api_hits: list[ApiHit],
    manifests: list[ManifestSummary],
) -> list[str]:
    required = {hit.category for hit in api_hits}
    declared: set[str] = set()
    for manifest in manifests:
        declared.update(manifest.declared_categories)
    return sorted(required - declared)


def _manifest_findings(
    root: Path,
    api_hits: list[ApiHit],
    manifests: list[ManifestSummary],
) -> list[Finding]:
    if not api_hits:
        return []
    first_hit_path = root / api_hits[0].path
    required = sorted({hit.category for hit in api_hits})
    if not manifests:
        return [
            _finding(
                "APM001",
                root,
                first_hit_path,
                "Required-reason API usage was found, but no privacy manifest "
                "was found in the scanned tree.",
                line=api_hits[0].line,
                current=", ".join(required),
                confidence=0.96,
            )
        ]
    missing = _missing_categories(api_hits, manifests)
    return [
        _finding(
            "APM002",
            root,
            first_hit_path,
            "Privacy manifest is missing detected accessed API categories.",
            line=api_hits[0].line,
            current=", ".join(missing),
            confidence=0.95,
        )
    ] if missing else []


def _confidence(findings: list[Finding]) -> float:
    if any(finding.classification == "blocked" for finding in findings):
        return 0.35
    if not findings:
        return 0.94
    manual = sum(1 for finding in findings if finding.classification == "manual_review")
    return max(0.5, min(0.9, round(0.9 - manual * 0.03, 2)))


def scan_repo(
    root: Path | str,
    *,
    candidate_path: Path | str | None = None,
) -> PrivacyReport:
    root_path = Path(root).resolve()
    if not root_path.exists() or not root_path.is_dir():
        raise FileNotFoundError(f"Project path does not exist: {root_path}")

    scanned_files: list[str] = []
    notes = [
        "This tool detects API categories; it does not choose Apple reason codes.",
        "Candidate manifests include REVIEW_REQUIRED placeholders by design.",
        "Binary SDK signature verification is outside the v0.1 scope.",
    ]

    source_files, api_hits, source_findings = _scan_sources(root_path)
    manifest_files, manifests, manifest_parse_findings = _scan_manifests(root_path)
    dependency_files, sdk_hits, sdk_findings = _scan_dependencies(root_path)
    scanned_files.extend(source_files)
    scanned_files.extend(manifest_files)
    scanned_files.extend(dependency_files)

    findings = [
        *source_findings,
        *manifest_parse_findings,
        *sdk_findings,
        *_manifest_findings(root_path, api_hits, manifests),
    ]

    missing_categories = _missing_categories(api_hits, manifests)
    candidate: CandidateManifest | None = None
    if missing_categories:
        output_path = Path(candidate_path or "PrivacyInfo.xcprivacy.candidate")
        if not output_path.is_absolute():
            output_path = root_path / output_path
        xml = build_candidate_manifest(missing_categories)
        written = False
        if candidate_path is not None:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(xml, encoding="utf-8", newline="")
            written = True
            scanned_files.append(_relative(root_path, output_path))
            findings.append(
                _finding(
                    "APM006",
                    root_path,
                    output_path,
                    "Candidate privacy manifest was written for review.",
                    current=", ".join(missing_categories),
                    confidence=1.0,
                    blocking=False,
                )
            )
        candidate = CandidateManifest(
            path=_relative(root_path, output_path),
            categories=missing_categories,
            xml=xml,
            written=written,
        )

    return PrivacyReport(
        product=PRODUCT,
        version=VERSION,
        rule_pack_version=RULE_PACK_VERSION,
        root_path=str(root_path),
        mode="candidate" if candidate_path else "scan",
        created_at=_utc_now(),
        scanned_files=sorted(set(scanned_files)),
        api_hits=sorted(
            api_hits,
            key=lambda item: (item.path, item.line, item.category),
        ),
        sdk_hits=sorted(sdk_hits, key=lambda item: (item.path, item.name)),
        manifests=manifests,
        findings=sorted(
            findings,
            key=lambda item: (item.path, item.line or 0, item.rule_id),
        ),
        candidate_manifest=candidate,
        confidence=_confidence(findings),
        notes=notes,
    )


__all__ = [
    "DEFAULT_HTML_REPORT",
    "DEFAULT_JSON_REPORT",
    "PRODUCT",
    "VERSION",
    "scan_repo",
]
