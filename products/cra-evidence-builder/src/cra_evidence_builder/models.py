from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Classification = Literal["autofix", "manual_review", "blocked", "informational"]
Severity = Literal["critical", "high", "medium", "low", "info"]


@dataclass(frozen=True)
class Rule:
    id: str
    title: str
    category: str
    severity: Severity
    classification: Classification
    source_url: str
    source_label: str
    description: str
    recommendation: str


@dataclass(frozen=True)
class EvidenceItem:
    kind: str
    path: str
    detail: str = ""


@dataclass(frozen=True)
class Finding:
    rule_id: str
    title: str
    severity: Severity
    classification: Classification
    message: str
    path: str
    line: int | None = None
    source_url: str = ""
    source_label: str = ""
    current: str | None = None
    recommended: str | None = None
    confidence: float = 1.0
    blocking: bool = False


@dataclass(frozen=True)
class TemplateFile:
    path: str
    title: str
    content: str
    written: bool = False


@dataclass(frozen=True)
class EvidenceReport:
    product: str
    version: str
    rule_pack_version: str
    root_path: str
    mode: str
    created_at: str
    scanned_files: list[str] = field(default_factory=list)
    evidence_items: list[EvidenceItem] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    template_files: list[TemplateFile] = field(default_factory=list)
    confidence: float = 0.0
    notes: list[str] = field(default_factory=list)

    @property
    def blocking_findings(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.blocking]

    @property
    def status(self) -> str:
        if self.blocking_findings:
            return "manual_review_required"
        if any(template.written for template in self.template_files):
            return "templates_written"
        if self.template_files:
            return "templates_available"
        if self.findings:
            return "informational_findings"
        return "clean"
