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
    deadline: str | None
    autofix: bool
    description: str
    recommendation: str


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
    deadline: str | None = None
    current: str | None = None
    recommended: str | None = None
    confidence: float = 1.0
    blocking: bool = False


@dataclass(frozen=True)
class Patch:
    path: str
    rule_id: str
    title: str
    description: str
    replacements: list[tuple[str, str]] = field(default_factory=list)
    diff: str = ""
    applied: bool = False


@dataclass(frozen=True)
class WorkflowSummary:
    path: str
    jobs: int
    steps: int
    actions: int
    local_actions: int


@dataclass(frozen=True)
class ScanReport:
    product: str
    version: str
    rule_pack_version: str
    root_path: str
    mode: str
    created_at: str
    scanned_files: list[str] = field(default_factory=list)
    workflow_summaries: list[WorkflowSummary] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    patches: list[Patch] = field(default_factory=list)
    files_changed: list[str] = field(default_factory=list)
    confidence: float = 0.0
    notes: list[str] = field(default_factory=list)

    @property
    def blocking_findings(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.blocking]

    @property
    def autofix_findings(self) -> list[Finding]:
        return [
            finding for finding in self.findings if finding.classification == "autofix"
        ]

    @property
    def manual_review_findings(self) -> list[Finding]:
        return [
            finding
            for finding in self.findings
            if finding.classification in {"manual_review", "blocked"}
        ]

    @property
    def status(self) -> str:
        if self.blocking_findings:
            return "manual_review_required"
        if self.files_changed:
            return "applied"
        if self.patches:
            return "patches_available"
        if self.findings:
            return "informational_findings"
        return "clean"
