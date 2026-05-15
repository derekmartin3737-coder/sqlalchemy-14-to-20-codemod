from __future__ import annotations

import json
import tomllib
from datetime import UTC, datetime
from pathlib import Path

from cra_evidence_builder.discovery import (
    DEPENDENCY_FILE_NAMES,
    INCIDENT_FILE_NAMES,
    RELEASE_FILE_NAMES,
    SBOM_SUFFIXES,
    all_files,
    relative,
)
from cra_evidence_builder.models import (
    EvidenceItem,
    EvidenceReport,
    Finding,
    TemplateFile,
)
from cra_evidence_builder.rules import RULE_PACK_VERSION, rule
from cra_evidence_builder.templates import build_templates

PRODUCT = "cra-evidence-builder"
VERSION = "0.1.0"
DEFAULT_JSON_REPORT = "cra-evidence-report.json"
DEFAULT_HTML_REPORT = "cra-evidence-report.html"


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
        path=relative(root, path) if path.exists() else ".",
        line=line,
        source_url=selected.source_url,
        source_label=selected.source_label,
        current=current,
        recommended=recommended or selected.recommendation,
        confidence=confidence,
        blocking=blocking,
    )


def _scan_parse_failures(root: Path, files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in files:
        try:
            if path.name == "package.json":
                json.loads(path.read_text(encoding="utf-8"))
            elif path.name == "pyproject.toml":
                tomllib.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, tomllib.TOMLDecodeError) as exc:
            findings.append(
                _finding(
                    "CRA000",
                    root,
                    path,
                    f"Could not parse {path.name}: {exc}",
                    current=str(exc),
                    confidence=1.0,
                )
            )
    return findings


def _kind_for_dependency_file(path: Path) -> str:
    lowered = path.name.lower()
    if lowered in {"package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock"}:
        return "node-dependency-manifest"
    if lowered in {"pyproject.toml", "requirements.txt", "poetry.lock"}:
        return "python-dependency-manifest"
    if lowered in {"go.mod", "go.sum"}:
        return "go-dependency-manifest"
    if lowered in {"cargo.toml", "cargo.lock"}:
        return "rust-dependency-manifest"
    if lowered in {"pom.xml", "build.gradle", "build.gradle.kts"}:
        return "java-dependency-manifest"
    return "dependency-manifest"


def _is_sbom(path: Path) -> bool:
    lowered = path.name.lower()
    return lowered in {"bom.json", "bom.xml", "sbom.json"} or lowered.endswith(
        SBOM_SUFFIXES
    )


def _is_security_file(path: Path) -> bool:
    rel = str(path).replace("\\", "/").lower()
    return path.name.lower() == "security.md" or rel.endswith(
        "/.well-known/security.txt"
    )


def _has_security_update_policy(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    return "supported version" in text or "security update" in text


def _scan_dockerfiles(
    root: Path,
    files: list[Path],
) -> tuple[list[EvidenceItem], list[Finding]]:
    evidence: list[EvidenceItem] = []
    findings: list[Finding] = []
    for path in files:
        if path.name != "Dockerfile" and not path.name.startswith("Dockerfile."):
            continue
        evidence.append(EvidenceItem("containerfile", relative(root, path)))
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        for line_number, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped.upper().startswith("FROM "):
                continue
            image = stripped.split()[1]
            if "@sha256:" in image or image.lower() == "scratch":
                continue
            findings.append(
                _finding(
                    "CRA007",
                    root,
                    path,
                    "Dockerfile base image is not pinned by digest.",
                    line=line_number,
                    current=image,
                    confidence=0.9,
                )
            )
    return evidence, findings


def _scan_evidence(root: Path) -> tuple[list[str], list[EvidenceItem], list[Finding]]:
    files = all_files(root)
    scanned = [relative(root, path) for path in files]
    findings = _scan_parse_failures(root, files)
    evidence: list[EvidenceItem] = []

    dependency_files = [path for path in files if path.name in DEPENDENCY_FILE_NAMES]
    if dependency_files:
        evidence.extend(
            EvidenceItem(_kind_for_dependency_file(path), relative(root, path))
            for path in dependency_files
        )
    else:
        findings.append(
            _finding(
                "CRA001",
                root,
                root,
                "No dependency manifest or lockfile was found.",
                confidence=0.9,
            )
        )

    sbom_files = [path for path in files if _is_sbom(path)]
    if sbom_files:
        evidence.extend(
            EvidenceItem("sbom", relative(root, path)) for path in sbom_files
        )
    elif dependency_files:
        findings.append(
            _finding(
                "CRA002",
                root,
                dependency_files[0],
                "Dependency manifests were found, but no SBOM artifact was found.",
                confidence=0.9,
            )
        )

    security_files = [path for path in files if _is_security_file(path)]
    if security_files:
        evidence.extend(
            EvidenceItem("vulnerability-contact", relative(root, path))
            for path in security_files
        )
    else:
        findings.append(
            _finding(
                "CRA003",
                root,
                root,
                "No SECURITY.md or .well-known/security.txt file was found.",
                confidence=0.9,
            )
        )

    incident_files = [
        path for path in files if path.name.lower() in INCIDENT_FILE_NAMES
    ]
    if incident_files:
        evidence.extend(
            EvidenceItem("incident-playbook", relative(root, path))
            for path in incident_files
        )
    else:
        findings.append(
            _finding(
                "CRA004",
                root,
                root,
                "No incident or vulnerability handling playbook was found.",
                confidence=0.88,
            )
        )

    release_files = [path for path in files if path.name in RELEASE_FILE_NAMES]
    if release_files:
        evidence.extend(
            EvidenceItem("release-traceability", relative(root, path))
            for path in release_files
        )
    else:
        findings.append(
            _finding(
                "CRA005",
                root,
                root,
                "No changelog, release notes, or release evidence file was found.",
                confidence=0.84,
            )
        )

    policy_hits = [path for path in security_files if _has_security_update_policy(path)]
    if policy_hits:
        evidence.extend(
            EvidenceItem("security-update-policy", relative(root, path))
            for path in policy_hits
        )
    else:
        findings.append(
            _finding(
                "CRA006",
                root,
                root,
                "No supported-version or security-update policy language was found.",
                confidence=0.78,
            )
        )

    container_evidence, container_findings = _scan_dockerfiles(root, files)
    evidence.extend(container_evidence)
    findings.extend(container_findings)
    return scanned, sorted(evidence, key=lambda item: (item.kind, item.path)), findings


def _needed_templates(findings: list[Finding]) -> list[TemplateFile]:
    ids = {finding.rule_id for finding in findings}
    templates = build_templates()
    needed: list[TemplateFile] = []
    for template in templates:
        if template.path.startswith("SECURITY") and {"CRA003", "CRA006"} & ids:
            needed.append(template)
        elif "incident-response" in template.path and "CRA004" in ids:
            needed.append(template)
        elif "release-evidence" in template.path and "CRA005" in ids:
            needed.append(template)
    return needed


def _write_templates(root: Path, templates: list[TemplateFile]) -> list[TemplateFile]:
    written: list[TemplateFile] = []
    for template in templates:
        target = root / template.path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(template.content, encoding="utf-8", newline="")
        written.append(
            TemplateFile(
                path=template.path,
                title=template.title,
                content=template.content,
                written=True,
            )
        )
    return written


def _confidence(findings: list[Finding]) -> float:
    if any(finding.classification == "blocked" for finding in findings):
        return 0.35
    if not findings:
        return 0.93
    manual = sum(1 for finding in findings if finding.classification == "manual_review")
    return max(0.45, min(0.9, round(0.9 - manual * 0.05, 2)))


def scan_repo(root: Path | str, *, write_templates: bool = False) -> EvidenceReport:
    root_path = Path(root).resolve()
    if not root_path.exists() or not root_path.is_dir():
        raise FileNotFoundError(f"Project path does not exist: {root_path}")

    scanned, evidence_items, findings = _scan_evidence(root_path)
    templates = _needed_templates(findings)
    if write_templates and templates:
        templates = _write_templates(root_path, templates)
        for template in templates:
            selected = rule("CRA008")
            findings.append(
                Finding(
                    rule_id=selected.id,
                    title=selected.title,
                    severity=selected.severity,
                    classification=selected.classification,
                    message=f"Template generated: {template.path}",
                    path=template.path,
                    source_url=selected.source_url,
                    source_label=selected.source_label,
                    recommended=selected.recommendation,
                    confidence=1.0,
                    blocking=False,
                )
            )

    notes = [
        "This is evidence-readiness support, not legal advice.",
        (
            "CRA reporting obligations apply from 2026-09-11; full application "
            "is 2027-12-11."
        ),
        (
            "Run vulnerability scanners and SBOM generators separately, then "
            "attach the outputs."
        ),
    ]
    return EvidenceReport(
        product=PRODUCT,
        version=VERSION,
        rule_pack_version=RULE_PACK_VERSION,
        root_path=str(root_path),
        mode="write-templates" if write_templates else "scan",
        created_at=_utc_now(),
        scanned_files=sorted(set(scanned)),
        evidence_items=evidence_items,
        findings=sorted(
            findings,
            key=lambda item: (item.path, item.line or 0, item.rule_id),
        ),
        template_files=templates,
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
