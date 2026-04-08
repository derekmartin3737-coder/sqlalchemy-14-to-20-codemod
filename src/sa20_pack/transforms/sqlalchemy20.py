from __future__ import annotations

import re

from sa20_pack.models import ManualReviewFinding, TransformApplication

SUPPORTED_TRANSFORMS: dict[str, tuple[str, float, re.Pattern[str]]] = {
    "declarative_imports": (
        "Commercial pack can rewrite legacy declarative imports to sqlalchemy.orm",
        0.96,
        re.compile(
            r"from\s+sqlalchemy\.ext(?:\.declarative)?\s+import\s+.*\b(declarative_base|declared_attr)\b"
        ),
    ),
    "select_list_syntax": (
        "Commercial pack can rewrite select([..]) list syntax",
        0.95,
        re.compile(r"\bselect\(\s*\["),
    ),
    "query_get": (
        "Commercial pack can rewrite Query.get(...) to Session.get(...)",
        0.94,
        re.compile(r"\.query\(\s*[^)\n]+\)\.get\("),
    ),
    "string_join": (
        "Commercial pack can rewrite simple string join()/outerjoin() paths",
        0.9,
        re.compile(r"\.(?:join|outerjoin)\(\s*['\"][A-Za-z_][\w.]*['\"]\s*\)"),
    ),
    "string_loader_option": (
        "Commercial pack can rewrite simple string loader-option paths",
        0.88,
        re.compile(
            r"\b(?:joinedload|lazyload|selectinload|subqueryload|contains_eager)\(\s*['\"][A-Za-z_][\w.]*['\"]\s*\)"
        ),
    ),
    "dml_constructor_kwargs": (
        "Commercial pack can rewrite simple DML constructor kwargs",
        0.9,
        re.compile(r"\b(?:insert|update|delete)\([^\n]*\b(?:values|whereclause)\s*="),
    ),
}

BLOCKED_PATTERNS: tuple[tuple[str, str, re.Pattern[str]], ...] = (
    (
        "engine_execute_removed",
        "engine.execute(...) needs a transaction-aware manual rewrite.",
        re.compile(r"\bengine\.execute\("),
    ),
    (
        "query_from_self_removed",
        "Query.from_self() is outside the public community scanner scope.",
        re.compile(r"\.from_self\("),
    ),
)


def _parse_error(source: str) -> str | None:
    try:
        compile(source, "<sa20-scan>", "exec")
    except SyntaxError as exc:
        return str(exc)
    return None


def _line_number(source: str, match_start: int) -> int:
    return source.count("\n", 0, match_start) + 1


def scan_sqlalchemy20_patterns(
    source: str,
) -> tuple[str, list[TransformApplication], list[ManualReviewFinding], str | None]:
    parse_error = _parse_error(source)
    if parse_error is not None:
        return source, [], [], parse_error

    transforms: list[TransformApplication] = []
    findings: list[ManualReviewFinding] = []

    for transform_id, (
        description,
        confidence,
        pattern,
    ) in SUPPORTED_TRANSFORMS.items():
        occurrences = len(pattern.findall(source))
        if occurrences:
            transforms.append(
                TransformApplication(
                    transform_id=transform_id,
                    description=description,
                    confidence=confidence,
                    occurrences=occurrences,
                )
            )

    for code, message, pattern in BLOCKED_PATTERNS:
        for match in pattern.finditer(source):
            findings.append(
                ManualReviewFinding(
                    code=code,
                    message=message,
                    line=_line_number(source, match.start()),
                )
            )

    return source, transforms, findings, None
