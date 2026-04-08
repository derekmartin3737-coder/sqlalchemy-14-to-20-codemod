from __future__ import annotations

import re
from dataclasses import dataclass

from pydantic_v2_porter.models import Finding

RELEVANCE_MARKERS = ("pydantic", "@validator", "@root_validator", "BaseSettings")
REMOVED_CONFIG_KEYS = {
    "copy_on_model_validation",
    "error_msg_templates",
    "fields",
    "getter_dict",
    "json_dumps",
    "json_loads",
    "post_init_call",
    "smart_union",
    "underscore_attrs_are_private",
}
ALLOWED_VALIDATOR_KWARGS = {"pre", "allow_reuse"}
VALIDATOR_BLOCKING_KWARGS = {
    "each_item": "unsupported-validator-each-item",
    "always": "unsupported-validator-always",
}


@dataclass(frozen=True)
class SourceTransformResult:
    transformed_source: str
    findings: list[Finding]
    transforms_applied: list[str]
    notes: list[str]


def _add_unique_finding(
    findings: list[Finding],
    seen: set[tuple[str, int | None]],
    code: str,
    message: str,
    path: str,
    line: int | None = None,
) -> None:
    key = (code, line)
    if key in seen:
        return
    seen.add(key)
    findings.append(Finding(code=code, message=message, path=path, line=line))


def _line_number(source: str, offset: int) -> int:
    return source.count("\n", 0, offset) + 1


def _split_signature(signature: str) -> list[str]:
    return [part.strip() for part in signature.split(",") if part.strip()]


def transform_source(source: str, path: str) -> SourceTransformResult:
    if not any(marker in source for marker in RELEVANCE_MARKERS):
        return SourceTransformResult(source, [], [], [])

    findings: list[Finding] = []
    notes: list[str] = []
    transforms: set[str] = set()
    seen_findings: set[tuple[str, int | None]] = set()

    for match in re.finditer(r"^\s*import\s+pydantic(?:\s|$)", source, re.MULTILINE):
        _add_unique_finding(
            findings,
            seen_findings,
            "unsupported-import-style",
            "Attribute-style pydantic imports need manual review.",
            path,
            _line_number(source, match.start()),
        )

    import_pattern = re.compile(
        r"^\s*from\s+(pydantic(?:\.v1)?)\s+import\s+(.+)$",
        re.MULTILINE,
    )
    for match in import_pattern.finditer(source):
        module_name = match.group(1)
        imported = match.group(2)
        line = _line_number(source, match.start())
        if imported.strip() == "*":
            _add_unique_finding(
                findings,
                seen_findings,
                "unsupported-star-import",
                "Star imports from pydantic need manual review.",
                path,
                line,
            )
            continue
        if " as " in imported:
            _add_unique_finding(
                findings,
                seen_findings,
                "unsupported-import-alias",
                "Aliased pydantic imports need manual review.",
                path,
                line,
            )
            continue
        if module_name == "pydantic.v1":
            transforms.add("pydantic_v1_import_path")
        if "BaseSettings" in imported:
            transforms.add("basesettings_import_move")
            notes.append(
                "Install the pydantic-settings package before applying the "
                "commercial migration pack."
            )

    if "class Config:" in source:
        if "model_config" in source:
            _add_unique_finding(
                findings,
                seen_findings,
                "unsupported-existing-model-config",
                "Classes with both Config and model_config need manual review.",
                path,
            )
        for removed_key in REMOVED_CONFIG_KEYS:
            if re.search(rf"^\s*{removed_key}\s*=", source, re.MULTILINE):
                _add_unique_finding(
                    findings,
                    seen_findings,
                    "unsupported-removed-config-key",
                    f"Config key '{removed_key}' was removed in Pydantic v2 "
                    "and needs manual review.",
                    path,
                )
        if not any(finding.code.startswith("unsupported-") for finding in findings):
            transforms.add("config_to_model_config")

    validator_pattern = re.compile(
        r"^\s*@validator\((?P<args>[^)]*)\)\s*$\n^\s*def\s+\w+\((?P<sig>[^)]*)\):",
        re.MULTILINE,
    )
    for match in validator_pattern.finditer(source):
        args = match.group("args")
        signature = _split_signature(match.group("sig"))
        line = _line_number(source, match.start())
        keyword_names = set(re.findall(r"(\w+)\s*=", args))
        blocked = False
        for keyword, code in VALIDATOR_BLOCKING_KWARGS.items():
            if keyword in keyword_names:
                _add_unique_finding(
                    findings,
                    seen_findings,
                    code,
                    f"validator({keyword}=...) needs manual review.",
                    path,
                    line,
                )
                blocked = True
        unsupported_keywords = (
            keyword_names - ALLOWED_VALIDATOR_KWARGS - set(VALIDATOR_BLOCKING_KWARGS)
        )
        if unsupported_keywords:
            _add_unique_finding(
                findings,
                seen_findings,
                "unsupported-validator-kwargs",
                "validator kwargs outside pre/allow_reuse need manual review.",
                path,
                line,
            )
            blocked = True
        if len(signature) != 2 or signature[0] != "cls":
            _add_unique_finding(
                findings,
                seen_findings,
                "unsupported-validator-signature",
                "validator decorators only support exact two-parameter "
                "classmethod signatures like (cls, v).",
                path,
                line,
            )
            blocked = True
        if not blocked:
            transforms.add("validator_to_field_validator")

    root_validator_pattern = re.compile(
        r"^\s*@root_validator(?:\((?P<args>[^)]*)\))?\s*$\n^\s*def\s+\w+\((?P<sig>[^)]*)\):",
        re.MULTILINE,
    )
    for match in root_validator_pattern.finditer(source):
        args = match.group("args") or ""
        signature = _split_signature(match.group("sig"))
        line = _line_number(source, match.start())
        keyword_names = set(re.findall(r"(\w+)\s*=", args))
        if "pre=True" not in args.replace(" ", ""):
            _add_unique_finding(
                findings,
                seen_findings,
                "unsupported-root-validator-post",
                "Post root validators need manual review.",
                path,
                line,
            )
            continue
        unsupported_keywords = keyword_names - {"pre"}
        if unsupported_keywords:
            _add_unique_finding(
                findings,
                seen_findings,
                "unsupported-root-validator-kwargs",
                "root_validator kwargs outside pre need manual review.",
                path,
                line,
            )
            continue
        if len(signature) != 2 or signature[0] != "cls":
            _add_unique_finding(
                findings,
                seen_findings,
                "unsupported-root-validator-signature",
                "root_validator only supports exact two-parameter classmethod "
                "signatures like (cls, values).",
                path,
                line,
            )
            continue
        transforms.add("root_validator_to_model_validator")

    for _match in re.finditer(r"^\s*@validate_arguments\s*$", source, re.MULTILINE):
        transforms.add("validate_arguments_to_validate_call")
    for match in re.finditer(r"^\s*@validate_arguments\(", source, re.MULTILINE):
        _add_unique_finding(
            findings,
            seen_findings,
            "unsupported-validate-arguments",
            "Configured validate_arguments decorators need manual review.",
            path,
            _line_number(source, match.start()),
        )

    return SourceTransformResult(
        transformed_source=source,
        findings=findings,
        transforms_applied=sorted(transforms),
        notes=sorted(set(notes)),
    )
