from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from eslint_v10_radar.discovery import (
    ESLINTRC_NAMES,
    FLAT_CONFIG_NAMES,
    SOURCE_SUFFIXES,
    all_files,
    relative,
)
from eslint_v10_radar.models import Finding, Patch, RadarReport
from eslint_v10_radar.patching import (
    Replacement,
    apply_replacements,
    build_patches,
    script_replacements,
)
from eslint_v10_radar.rules import RULE_PACK_VERSION, rule

PRODUCT = "eslint-v10-radar"
VERSION = "0.1.0"
DEFAULT_JSON_REPORT = "eslint-v10-report.json"
DEFAULT_HTML_REPORT = "eslint-v10-report.html"


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
        path=relative(root, path),
        line=line,
        source_url=selected.source_url,
        source_label=selected.source_label,
        current=current,
        recommended=selected.recommendation,
        confidence=confidence,
        blocking=blocking,
    )


def _line_for(text: str, pattern: str) -> int | None:
    for index, line in enumerate(text.splitlines(), 1):
        if pattern in line:
            return index
    return None


def _scan_package_json(
    root: Path,
    path: Path,
) -> tuple[list[Finding], list[Replacement]]:
    findings: list[Finding] = []
    replacements: list[Replacement] = []
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return [
            _finding(
                "ESL000",
                root,
                path,
                f"Could not parse package.json: {exc}",
                line=exc.lineno,
                current=str(exc),
            )
        ], []

    if isinstance(data, dict) and "eslintConfig" in data:
        findings.append(
            _finding(
                "ESL002",
                root,
                path,
                "package.json contains eslintConfig.",
                line=_line_for(text, '"eslintConfig"'),
                current="eslintConfig",
                confidence=0.98,
            )
        )
    if "ESLINT_USE_FLAT_CONFIG=false" in text:
        findings.append(
            _finding(
                "ESL004",
                root,
                path,
                "package scripts include ESLINT_USE_FLAT_CONFIG=false.",
                line=_line_for(text, "ESLINT_USE_FLAT_CONFIG=false"),
                current="ESLINT_USE_FLAT_CONFIG=false",
                confidence=0.98,
            )
        )
    if "v10_config_lookup_from_file" in text:
        findings.append(
            _finding(
                "ESL005",
                root,
                path,
                (
                    "package scripts reference the removed "
                    "v10_config_lookup_from_file flag."
                ),
                line=_line_for(text, "v10_config_lookup_from_file"),
                current="v10_config_lookup_from_file",
                confidence=0.98,
            )
        )
    replacements.extend(script_replacements(path, text))
    return findings, replacements


def _scan_source(root: Path, path: Path) -> list[Finding]:
    findings: list[Finding] = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    patterns = [
        ("LegacyESLint", "LegacyESLint"),
        ("FlatESLint", "FlatESLint"),
        ('configType: "eslintrc"', 'configType: "eslintrc"'),
        ("configType: 'eslintrc'", "configType: 'eslintrc'"),
    ]
    for needle, current in patterns:
        if needle not in text:
            continue
        findings.append(
            _finding(
                "ESL006",
                root,
                path,
                "ESLint v10-incompatible API usage was found.",
                line=_line_for(text, needle),
                current=current,
                confidence=0.92,
            )
        )
    return findings


def _scan_env_files(root: Path, path: Path) -> list[Finding]:
    findings: list[Finding] = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    if "ESLINT_USE_FLAT_CONFIG=false" in text:
        findings.append(
            _finding(
                "ESL004",
                root,
                path,
                "Environment file disables flat config.",
                line=_line_for(text, "ESLINT_USE_FLAT_CONFIG=false"),
                current="ESLINT_USE_FLAT_CONFIG=false",
            )
        )
    if "v10_config_lookup_from_file" in text:
        findings.append(
            _finding(
                "ESL005",
                root,
                path,
                "Environment file includes a removed ESLint v10 flag.",
                line=_line_for(text, "v10_config_lookup_from_file"),
                current="v10_config_lookup_from_file",
            )
        )
    return findings


def _confidence(findings: list[Finding], patches: list[Patch]) -> float:
    if any(finding.classification == "blocked" for finding in findings):
        return 0.4
    if not findings:
        return 0.95
    manual = sum(1 for finding in findings if finding.classification == "manual_review")
    autofix = sum(1 for finding in findings if finding.classification == "autofix")
    score = 0.92 - manual * 0.05 - autofix * 0.02 + len(patches) * 0.02
    return max(0.5, min(0.92, round(score, 2)))


def scan_repo(root: Path | str, *, apply: bool = False) -> RadarReport:
    root_path = Path(root).resolve()
    if not root_path.exists() or not root_path.is_dir():
        raise FileNotFoundError(f"Repository path does not exist: {root_path}")

    files = all_files(root_path)
    scanned = [relative(root_path, path) for path in files]
    findings: list[Finding] = []
    replacements: list[Replacement] = []
    eslintrc_files = [path for path in files if path.name in ESLINTRC_NAMES]
    flat_configs = [path for path in files if path.name in FLAT_CONFIG_NAMES]

    for path in eslintrc_files:
        findings.append(
            _finding(
                "ESL001",
                root_path,
                path,
                "Legacy eslintrc config file exists.",
                current=path.name,
                confidence=0.99,
            )
        )
        if path.suffix in {".js", ".cjs", ".mjs"}:
            findings.append(
                _finding(
                    "ESL007",
                    root_path,
                    path,
                    "Dynamic JavaScript eslintrc file needs manual conversion.",
                    current=path.name,
                    confidence=0.9,
                )
            )

    if eslintrc_files and not flat_configs:
        findings.append(
            _finding(
                "ESL008",
                root_path,
                eslintrc_files[0],
                "Legacy ESLint config exists but no eslint.config.* file was found.",
                current=", ".join(path.name for path in eslintrc_files),
                confidence=0.96,
            )
        )

    for path in files:
        if path.name == "package.json":
            package_findings, package_replacements = _scan_package_json(root_path, path)
            findings.extend(package_findings)
            replacements.extend(package_replacements)
        elif path.name == ".eslintignore":
            findings.append(
                _finding(
                    "ESL003",
                    root_path,
                    path,
                    ".eslintignore exists and should move into flat config.",
                    current=".eslintignore",
                    confidence=0.95,
                )
            )
        elif path.suffix in SOURCE_SUFFIXES:
            findings.extend(_scan_source(root_path, path))
        elif path.name.startswith(".env"):
            findings.extend(_scan_env_files(root_path, path))

    patches = build_patches(root_path, replacements)
    files_changed: list[str] = []
    if apply and replacements:
        files_changed = apply_replacements(root_path, replacements)
        applied_paths = set(files_changed)
        patches = [
            Patch(
                path=patch.path,
                rule_id=patch.rule_id,
                title=patch.title,
                description=patch.description,
                diff=patch.diff,
                applied=patch.path in applied_paths,
            )
            for patch in patches
        ]

    notes = [
        "This radar finds v10 blockers; it is not a full flat-config converter.",
        "Patch mode only removes simple package-script compatibility flags.",
    ]
    return RadarReport(
        product=PRODUCT,
        version=VERSION,
        rule_pack_version=RULE_PACK_VERSION,
        root_path=str(root_path),
        mode="apply" if apply else "scan",
        created_at=_utc_now(),
        scanned_files=sorted(set(scanned)),
        findings=sorted(
            findings,
            key=lambda item: (item.path, item.line or 0, item.rule_id),
        ),
        patches=patches,
        files_changed=files_changed,
        confidence=_confidence(findings, patches),
        notes=notes,
    )


__all__ = [
    "DEFAULT_HTML_REPORT",
    "DEFAULT_JSON_REPORT",
    "PRODUCT",
    "VERSION",
    "scan_repo",
]
