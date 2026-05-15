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
class ApiHit:
    category: str
    path: str
    line: int
    symbol: str
    confidence: float


@dataclass(frozen=True)
class SdkHit:
    name: str
    path: str
    line: int | None = None
    confidence: float = 0.9


@dataclass(frozen=True)
class ManifestSummary:
    path: str
    declared_categories: list[str] = field(default_factory=list)
    valid: bool = True


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
class CandidateManifest:
    path: str
    categories: list[str] = field(default_factory=list)
    xml: str = ""
    written: bool = False


@dataclass(frozen=True)
class PrivacyReport:
    product: str
    version: str
    rule_pack_version: str
    root_path: str
    mode: str
    created_at: str
    scanned_files: list[str] = field(default_factory=list)
    api_hits: list[ApiHit] = field(default_factory=list)
    sdk_hits: list[SdkHit] = field(default_factory=list)
    manifests: list[ManifestSummary] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    candidate_manifest: CandidateManifest | None = None
    confidence: float = 0.0
    notes: list[str] = field(default_factory=list)

    @property
    def blocking_findings(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.blocking]

    @property
    def status(self) -> str:
        if self.blocking_findings:
            return "manual_review_required"
        if self.candidate_manifest and self.candidate_manifest.written:
            return "candidate_written"
        if self.candidate_manifest:
            return "candidate_available"
        if self.findings:
            return "informational_findings"
        return "clean"
