from __future__ import annotations

import ast
import re
import tomllib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from python314_readiness.discovery import discover_python_files, discover_workflow_files
from python314_readiness.models import Finding, Patch, ReadinessReport, SourceSummary
from python314_readiness.patching import (
    Replacement,
    add_314_to_inline_matrix,
    apply_patches,
    build_patches,
)
from python314_readiness.rules import RULE_PACK_VERSION, rule

PRODUCT = "python-314-readiness"
VERSION = "0.1.0"
DEFAULT_JSON_REPORT = "python314-readiness-report.json"
DEFAULT_HTML_REPORT = "python314-readiness-report.html"


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


def _load_pyproject(
    root: Path,
) -> tuple[Path | None, dict[str, Any] | None, list[Finding]]:
    path = root / "pyproject.toml"
    if not path.exists():
        return None, None, []
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        finding = _finding(
            "PY314000",
            root,
            path,
            f"Could not parse pyproject.toml: {exc}",
            current=str(exc),
            confidence=1.0,
        )
        return path, None, [finding]
    return path, data, []


def _bound_excludes_314(value: str) -> bool:
    parts = [part.strip() for part in value.split(",")]
    for part in parts:
        match = re.match(r"(<=?|==|~=)\s*3\.(\d+)(?:\.\*)?", part)
        if not match:
            continue
        operator, minor_text = match.groups()
        minor = int(minor_text)
        if operator == "<" and minor <= 14:
            return True
        if operator == "<=" and minor < 14:
            return True
        if operator == "==" and minor < 14:
            return True
        if operator == "~=" and minor < 14:
            return True
    return False


def _dependency_name(specifier: str) -> str:
    match = re.match(r"\s*([A-Za-z0-9_.-]+)", specifier)
    if not match:
        return ""
    return match.group(1).lower().replace("_", "-")


def _is_pydantic_v1_pin(specifier: str) -> bool:
    lowered = specifier.lower().replace(" ", "")
    return bool(
        re.search(r"pydantic(?:\[[^\]]+\])?(?:==|~=)1\.", lowered)
        or re.search(r"pydantic(?:\[[^\]]+\])?<2(?:[,\s]|$)", lowered)
        or re.search(r"pydantic(?:\[[^\]]+\])?<=1\.", lowered)
    )


def _is_old_pydantic_v2_pin(specifier: str) -> bool:
    lowered = specifier.lower().replace(" ", "")
    if _is_pydantic_v1_pin(lowered):
        return False
    return bool(
        re.search(r"pydantic(?:\[[^\]]+\])?==2\.(?:[0-9]|10|11)(?:\.|$)", lowered)
        or re.search(r"pydantic(?:\[[^\]]+\])?~=2\.(?:[0-9]|10|11)(?:\.|$)", lowered)
        or re.search(r"pydantic(?:\[[^\]]+\])?<2\.12(?:[,\s]|$)", lowered)
    )


def _iter_project_dependencies(data: dict[str, Any]) -> list[str]:
    dependencies: list[str] = []
    project = data.get("project")
    if isinstance(project, dict):
        raw = project.get("dependencies")
        if isinstance(raw, list):
            dependencies.extend(str(item) for item in raw)
        optional = project.get("optional-dependencies")
        if isinstance(optional, dict):
            for values in optional.values():
                if isinstance(values, list):
                    dependencies.extend(str(item) for item in values)

    poetry = (
        data.get("tool", {})
        if isinstance(data.get("tool"), dict)
        else {}
    ).get("poetry", {})
    if isinstance(poetry, dict):
        raw_poetry_deps = poetry.get("dependencies")
        if isinstance(raw_poetry_deps, dict):
            for name, value in raw_poetry_deps.items():
                if str(name).lower() == "python":
                    continue
                dependencies.append(f"{name}{value}")

    return dependencies


def _scan_metadata(root: Path) -> list[Finding]:
    path, data, parse_findings = _load_pyproject(root)
    findings = list(parse_findings)
    if path is None or data is None:
        return findings

    project = data.get("project")
    if isinstance(project, dict):
        requires_python = project.get("requires-python")
        if isinstance(requires_python, str) and _bound_excludes_314(requires_python):
            findings.append(
                _finding(
                    "PY314001",
                    root,
                    path,
                    "Project metadata excludes Python 3.14.",
                    current=requires_python,
                    confidence=0.98,
                )
            )

    for dependency in _iter_project_dependencies(data):
        if _dependency_name(dependency) != "pydantic":
            continue
        if _is_pydantic_v1_pin(dependency):
            findings.append(
                _finding(
                    "PY314004",
                    root,
                    path,
                    "Dependency metadata pins Pydantic to the v1 line.",
                    current=dependency,
                    confidence=0.96,
                )
            )
        elif _is_old_pydantic_v2_pin(dependency):
            findings.append(
                _finding(
                    "PY314005",
                    root,
                    path,
                    "Dependency metadata pins Pydantic before the 2.12 line.",
                    current=dependency,
                    confidence=0.92,
                )
            )

    return findings


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = _call_name(node.value)
        if prefix:
            return f"{prefix}.{node.attr}"
        return node.attr
    return ""


class _SourceVisitor(ast.NodeVisitor):
    def __init__(self, root: Path, path: Path) -> None:
        self.root = root
        self.path = path
        self.findings: list[Finding] = []
        self.annotation_risks = 0
        self.multiprocessing_risks = 0
        self.pydantic_risks = 0
        self._aliases: dict[str, str] = {}
        self._class_depth = 0

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            local = alias.asname or alias.name.split(".")[0]
            self._aliases[local] = alias.name
            if alias.name == "pydantic.v1" or alias.name.startswith("pydantic.v1."):
                self._add_pydantic_v1(node.lineno, f"import {alias.name}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module or ""
        for alias in node.names:
            local = alias.asname or alias.name
            full_name = f"{module}.{alias.name}" if module else alias.name
            self._aliases[local] = full_name
        if module == "pydantic.v1" or module.startswith("pydantic.v1."):
            self._add_pydantic_v1(node.lineno, f"from {module} import ...")
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._class_depth += 1
        self.generic_visit(node)
        self._class_depth -= 1

    def visit_Assign(self, node: ast.Assign) -> None:
        self._check_class_partial(node.value, node.lineno)
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if node.value is not None:
            self._check_class_partial(node.value, node.lineno)
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if node.attr == "__annotations__":
            self._add_annotation_risk(
                node.lineno,
                "Code reads __annotations__ at runtime.",
                current="__annotations__",
            )
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        if node.id == "__annotations__":
            self._add_annotation_risk(
                node.lineno,
                "Code references __annotations__ directly.",
                current="__annotations__",
            )
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        name = self._resolved_name(_call_name(node.func))
        if name in {"typing.get_type_hints", "get_type_hints"}:
            self._add_annotation_risk(
                node.lineno,
                "Code calls get_type_hints(), which can depend on runtime "
                "annotation evaluation behavior.",
                current=name,
            )
        if name in {"inspect.get_annotations", "get_annotations"}:
            self._add_annotation_risk(
                node.lineno,
                "Code calls inspect.get_annotations(), which should be "
                "reviewed under Python 3.14 annotation semantics.",
                current=name,
            )
        if name in {
            "multiprocessing.Pool",
            "multiprocessing.Process",
            "mp.Pool",
            "mp.Process",
            "Pool",
            "Process",
        }:
            self._add_multiprocessing_risk(
                node.lineno,
                "Process-based multiprocessing call should be reviewed for "
                "explicit start-method behavior.",
                current=name,
            )
        if name in {
            "concurrent.futures.ProcessPoolExecutor",
            "ProcessPoolExecutor",
        } and not any(keyword.arg == "mp_context" for keyword in node.keywords):
            self._add_multiprocessing_risk(
                node.lineno,
                "ProcessPoolExecutor is created without an explicit "
                "mp_context.",
                current=name,
            )
        self.generic_visit(node)

    def _resolved_name(self, name: str) -> str:
        if "." not in name:
            return self._aliases.get(name, name)
        head, _, tail = name.partition(".")
        return f"{self._aliases.get(head, head)}.{tail}"

    def _check_class_partial(self, value: ast.AST, line: int) -> None:
        if self._class_depth == 0 or not isinstance(value, ast.Call):
            return
        if self._resolved_name(_call_name(value.func)) in {
            "functools.partial",
            "partial",
        }:
            selected = rule("PY314007")
            self.findings.append(
                _finding(
                    selected.id,
                    self.root,
                    self.path,
                    "Class body assigns functools.partial; review descriptor "
                    "behavior under Python 3.14.",
                    line=line,
                    current="functools.partial",
                    recommended=selected.recommendation,
                    confidence=0.9,
                )
            )

    def _add_annotation_risk(
        self,
        line: int,
        message: str,
        *,
        current: str,
    ) -> None:
        self.annotation_risks += 1
        self.findings.append(
            _finding(
                "PY314003",
                self.root,
                self.path,
                message,
                line=line,
                current=current,
                confidence=0.88,
            )
        )

    def _add_pydantic_v1(self, line: int, current: str) -> None:
        self.pydantic_risks += 1
        self.findings.append(
            _finding(
                "PY314004",
                self.root,
                self.path,
                "Source imports through pydantic.v1.",
                line=line,
                current=current,
                confidence=0.97,
            )
        )

    def _add_multiprocessing_risk(
        self,
        line: int,
        message: str,
        *,
        current: str,
    ) -> None:
        self.multiprocessing_risks += 1
        self.findings.append(
            _finding(
                "PY314006",
                self.root,
                self.path,
                message,
                line=line,
                current=current,
                confidence=0.82,
            )
        )

    def source_summary(self) -> SourceSummary:
        return SourceSummary(
            path=_relative(self.root, self.path),
            annotation_risks=self.annotation_risks,
            multiprocessing_risks=self.multiprocessing_risks,
            pydantic_risks=self.pydantic_risks,
        )


def _scan_sources(root: Path) -> tuple[list[str], list[SourceSummary], list[Finding]]:
    scanned: list[str] = []
    summaries: list[SourceSummary] = []
    findings: list[Finding] = []
    for path in discover_python_files(root):
        scanned.append(_relative(root, path))
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            findings.append(
                _finding(
                    "PY314000",
                    root,
                    path,
                    f"Could not parse Python source: {exc.msg}",
                    line=exc.lineno,
                    current=exc.text.strip() if exc.text else exc.msg,
                    confidence=1.0,
                )
            )
            continue
        visitor = _SourceVisitor(root, path)
        visitor.visit(tree)
        findings.extend(visitor.findings)
        summary = visitor.source_summary()
        if (
            summary.annotation_risks
            or summary.multiprocessing_risks
            or summary.pydantic_risks
        ):
            summaries.append(summary)
    return scanned, summaries, findings


def _workflow_uses_setup_python(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    jobs = data.get("jobs")
    if not isinstance(jobs, dict):
        return False
    for job in jobs.values():
        if not isinstance(job, dict):
            continue
        steps = job.get("steps")
        if not isinstance(steps, list):
            continue
        for step in steps:
            if not isinstance(step, dict):
                continue
            uses = step.get("uses")
            if isinstance(uses, str) and uses.lower().startswith(
                "actions/setup-python@"
            ):
                return True
    return False


def _extract_python_versions(data: Any) -> list[str]:
    versions: list[str] = []

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                if str(key).lower() == "python-version":
                    collect_version(item)
                else:
                    visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    def collect_version(value: Any) -> None:
        if isinstance(value, str):
            versions.extend(re.findall(r"\d+\.\d+", value))
        elif isinstance(value, list):
            for item in value:
                collect_version(item)

    visit(data)
    return versions


def _scan_workflows(root: Path) -> tuple[list[str], list[Finding], list[Replacement]]:
    scanned: list[str] = []
    findings: list[Finding] = []
    replacements: list[Replacement] = []
    selected = rule("PY314002")
    for path in discover_workflow_files(root):
        scanned.append(_relative(root, path))
        text = path.read_text(encoding="utf-8")
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            findings.append(
                _finding(
                    "PY314000",
                    root,
                    path,
                    f"Could not parse workflow YAML: {exc}",
                    current=str(exc),
                    confidence=1.0,
                )
            )
            continue
        if not _workflow_uses_setup_python(data):
            continue
        versions = _extract_python_versions(data)
        if "3.14" in versions:
            continue
        findings.append(
            _finding(
                selected.id,
                root,
                path,
                "Workflow uses actions/setup-python but does not expose a "
                "Python 3.14 version in its matrix or direct configuration.",
                current=", ".join(sorted(set(versions))) or "no static versions",
                recommended=selected.recommendation,
                confidence=0.86 if versions else 0.7,
            )
        )
        replacement = add_314_to_inline_matrix(text)
        if replacement is None:
            continue
        before, after = replacement
        replacements.append(
            Replacement(
                rule_id=selected.id,
                title=selected.title,
                path=path,
                before=before,
                after=after,
                description="Add Python 3.14 to the simple CI version matrix.",
            )
        )
    return scanned, findings, replacements


def _confidence(findings: list[Finding], patches_available: int) -> float:
    if any(finding.classification == "blocked" for finding in findings):
        return 0.35
    if not findings:
        return 0.95
    manual = sum(1 for finding in findings if finding.classification == "manual_review")
    autofix = sum(1 for finding in findings if finding.classification == "autofix")
    score = 0.92 - (manual * 0.06) - (autofix * 0.03) + (patches_available * 0.02)
    return max(0.45, min(0.92, round(score, 2)))


def scan_repo(root: Path | str, *, apply: bool = False) -> ReadinessReport:
    root_path = Path(root).resolve()
    if not root_path.exists() or not root_path.is_dir():
        raise FileNotFoundError(f"Repository path does not exist: {root_path}")

    scanned_files: list[str] = []
    findings: list[Finding] = []
    notes = [
        "This report is local-only and does not prove dependency compatibility.",
        "Patch mode is limited to simple GitHub Actions Python-version matrices.",
    ]

    metadata_findings = _scan_metadata(root_path)
    findings.extend(metadata_findings)
    if (root_path / "pyproject.toml").exists():
        scanned_files.append("pyproject.toml")

    source_files, source_summaries, source_findings = _scan_sources(root_path)
    scanned_files.extend(source_files)
    findings.extend(source_findings)

    workflow_files, workflow_findings, replacements = _scan_workflows(root_path)
    scanned_files.extend(workflow_files)
    findings.extend(workflow_findings)

    patches = build_patches(root_path, replacements)
    files_changed: list[str] = []
    if apply and replacements:
        files_changed = apply_patches(root_path, replacements)
        applied_paths = set(files_changed)
        patches = [
            Patch(
                path=patch.path,
                rule_id=patch.rule_id,
                title=patch.title,
                description=patch.description,
                replacements=patch.replacements,
                diff=patch.diff,
                applied=patch.path in applied_paths,
            )
            for patch in patches
        ]

    unique_scanned = sorted(set(scanned_files))
    confidence = _confidence(findings, len(patches))
    return ReadinessReport(
        product=PRODUCT,
        version=VERSION,
        rule_pack_version=RULE_PACK_VERSION,
        root_path=str(root_path),
        mode="apply" if apply else "scan",
        created_at=_utc_now(),
        scanned_files=unique_scanned,
        source_summaries=source_summaries,
        findings=sorted(
            findings,
            key=lambda item: (item.path, item.line or 0, item.rule_id),
        ),
        patches=patches,
        files_changed=files_changed,
        confidence=confidence,
        notes=notes,
    )


__all__ = [
    "DEFAULT_HTML_REPORT",
    "DEFAULT_JSON_REPORT",
    "PRODUCT",
    "VERSION",
    "scan_repo",
]
