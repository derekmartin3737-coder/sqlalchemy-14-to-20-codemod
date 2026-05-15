from __future__ import annotations

import json
import tomllib
from datetime import UTC, datetime
from pathlib import Path

from package_publisher_hardening.discovery import all_files, relative, workflow_files
from package_publisher_hardening.models import Finding, Patch, PublisherReport
from package_publisher_hardening.patching import (
    Replacement,
    apply_replacements,
    build_patches,
    permission_replacements,
)
from package_publisher_hardening.rules import RULE_PACK_VERSION, rule

PRODUCT = "package-publisher-hardening"
VERSION = "0.1.0"
DEFAULT_JSON_REPORT = "publisher-hardening-report.json"
DEFAULT_HTML_REPORT = "publisher-hardening-report.html"


def _utc_now() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat()


def _line_for(text: str, needle: str) -> int | None:
    for index, line in enumerate(text.splitlines(), 1):
        if needle in line:
            return index
    return None


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


def _scan_package_json(root: Path, path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return [
            _finding(
                "PPH000",
                root,
                path,
                f"Could not parse package.json: {exc}",
                line=exc.lineno,
                current=str(exc),
            )
        ]
    findings: list[Finding] = []
    if isinstance(data, dict):
        if "repository" not in data:
            findings.append(
                _finding(
                    "PPH007",
                    root,
                    path,
                    "package.json is missing repository metadata.",
                    line=1,
                    current="repository missing",
                    confidence=0.9,
                )
            )
        publish_config = data.get("publishConfig")
        if (
            isinstance(publish_config, dict)
            and publish_config.get("provenance") is False
        ):
            findings.append(
                _finding(
                    "PPH009",
                    root,
                    path,
                    "package.json publishConfig disables provenance.",
                    line=_line_for(text, '"provenance"'),
                    current="provenance=false",
                    confidence=0.95,
                )
            )
    return findings


def _scan_pyproject(root: Path, path: Path) -> list[Finding]:
    try:
        tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        return [
            _finding(
                "PPH000",
                root,
                path,
                f"Could not parse pyproject.toml: {exc}",
                current=str(exc),
            )
        ]
    return []


def _scan_workflow(root: Path, path: Path) -> tuple[list[Finding], list[Replacement]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    findings: list[Finding] = []
    uses_npm_publish = "npm publish" in text
    uses_pypi_action = "pypa/gh-action-pypi-publish" in text
    uses_twine = "twine upload" in text or "python -m twine upload" in text
    has_id_token = "id-token: write" in text
    uses_self_hosted = "self-hosted" in text

    if uses_npm_publish and ("NODE_AUTH_TOKEN" in text or "NPM_TOKEN" in text):
        findings.append(
            _finding(
                "PPH001",
                root,
                path,
                (
                    "npm publish appears to rely on long-lived token "
                    "environment variables."
                ),
                line=_line_for(text, "npm publish"),
                current="NODE_AUTH_TOKEN/NPM_TOKEN",
                confidence=0.92,
            )
        )
    if uses_npm_publish and not has_id_token:
        findings.append(
            _finding(
                "PPH002",
                root,
                path,
                "npm publish workflow lacks id-token: write permission.",
                line=_line_for(text, "npm publish"),
                current="id-token missing",
                confidence=0.9,
            )
        )
    if uses_npm_publish and not has_id_token and "--provenance" not in text:
        findings.append(
            _finding(
                "PPH003",
                root,
                path,
                "npm publish lacks visible provenance or trusted publishing posture.",
                line=_line_for(text, "npm publish"),
                current="npm publish",
                confidence=0.84,
            )
        )
    if uses_twine and ("TWINE_PASSWORD" in text or "PYPI_API_TOKEN" in text):
        findings.append(
            _finding(
                "PPH004",
                root,
                path,
                (
                    "PyPI upload appears to rely on long-lived token "
                    "environment variables."
                ),
                line=_line_for(text, "twine upload")
                or _line_for(text, "python -m twine upload"),
                current="TWINE_PASSWORD/PYPI_API_TOKEN",
                confidence=0.92,
            )
        )
    if (uses_pypi_action or uses_twine) and not has_id_token:
        findings.append(
            _finding(
                "PPH005",
                root,
                path,
                "PyPI publish workflow lacks id-token: write permission.",
                line=_line_for(text, "pypa/gh-action-pypi-publish")
                or _line_for(text, "twine upload"),
                current="id-token missing",
                confidence=0.88,
            )
        )
    if "contents: write" in text and (
        uses_npm_publish or uses_pypi_action or uses_twine
    ):
        findings.append(
            _finding(
                "PPH006",
                root,
                path,
                "Publish workflow grants contents: write.",
                line=_line_for(text, "contents: write"),
                current="contents: write",
                confidence=0.82,
            )
        )
    if uses_self_hosted and (uses_npm_publish or uses_pypi_action):
        findings.append(
            _finding(
                "PPH008",
                root,
                path,
                "Publish workflow uses a self-hosted runner.",
                line=_line_for(text, "self-hosted"),
                current="self-hosted",
                confidence=0.78,
            )
        )
    return findings, permission_replacements(path, text)


def _confidence(findings: list[Finding], patches: list[Patch]) -> float:
    if any(finding.classification == "blocked" for finding in findings):
        return 0.35
    if not findings:
        return 0.94
    manual = sum(1 for finding in findings if finding.classification == "manual_review")
    autofix = sum(1 for finding in findings if finding.classification == "autofix")
    score = 0.92 - manual * 0.05 - autofix * 0.02 + len(patches) * 0.02
    return max(0.45, min(0.92, round(score, 2)))


def scan_repo(root: Path | str, *, apply: bool = False) -> PublisherReport:
    root_path = Path(root).resolve()
    if not root_path.exists() or not root_path.is_dir():
        raise FileNotFoundError(f"Repository path does not exist: {root_path}")

    files = all_files(root_path)
    scanned = [relative(root_path, path) for path in files]
    findings: list[Finding] = []
    replacements: list[Replacement] = []
    for path in files:
        if path.name == "package.json":
            findings.extend(_scan_package_json(root_path, path))
        elif path.name == "pyproject.toml":
            findings.extend(_scan_pyproject(root_path, path))
    for path in workflow_files(root_path):
        if relative(root_path, path) not in scanned:
            scanned.append(relative(root_path, path))
        workflow_findings, workflow_replacements = _scan_workflow(root_path, path)
        findings.extend(workflow_findings)
        replacements.extend(workflow_replacements)

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
        "This scanner prepares repo-side publishing hardening work.",
        "Registry-side trusted publisher setup still happens in npm or PyPI.",
        "Patch mode only adds id-token: write to simple workflow permissions blocks.",
    ]
    return PublisherReport(
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
