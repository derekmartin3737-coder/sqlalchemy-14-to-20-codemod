from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Finding:
    code: str
    message: str
    path: str
    line: int | None = None
    blocking: bool = True


@dataclass(frozen=True)
class ArtifactChange:
    path: str
    kind: str
    changed: bool
    diff: str | None = None


@dataclass(frozen=True)
class MigrationReport:
    root_path: str
    mode: str
    created_at: str
    source_path: str | None
    source_kind: str | None
    output_path: str
    artifact_changes: list[ArtifactChange] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    migrated_ignore_patterns: list[str] = field(default_factory=list)
    confidence: float = 0.0
    notes: list[str] = field(default_factory=list)

    @property
    def files_changed(self) -> list[str]:
        return [item.path for item in self.artifact_changes if item.changed]

    @property
    def blocking_findings(self) -> list[Finding]:
        return [item for item in self.findings if item.blocking]

    @property
    def status(self) -> str:
        if self.blocking_findings:
            return "manual_review_required"
        if self.mode == "dry-run":
            return "preview_only"
        return "applied"
