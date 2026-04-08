from __future__ import annotations

import ast
from collections import Counter

from sa20_pack.models import ManualReviewFinding, TransformApplication

SUPPORTED_TRANSFORMS: dict[str, tuple[str, float]] = {
    "declarative_imports": (
        "Commercial pack can rewrite legacy declarative imports to sqlalchemy.orm",
        0.96,
    ),
    "select_list_syntax": (
        "Commercial pack can rewrite select([..]) list syntax",
        0.95,
    ),
    "query_get": (
        "Commercial pack can rewrite Query.get(...) to Session.get(...)",
        0.94,
    ),
    "string_join": (
        "Commercial pack can rewrite simple string join()/outerjoin() paths",
        0.9,
    ),
    "string_loader_option": (
        "Commercial pack can rewrite simple string loader-option paths",
        0.88,
    ),
    "dml_constructor_kwargs": (
        "Commercial pack can rewrite simple DML constructor kwargs",
        0.9,
    ),
}

BLOCKED_PATTERNS: dict[str, str] = {
    "engine_execute_removed": (
        "engine.execute(...) needs a transaction-aware manual rewrite."
    ),
    "query_from_self_removed": (
        "Query.from_self() is outside the public community scanner scope."
    ),
}

DECLARATIVE_MODULES = {"sqlalchemy.ext", "sqlalchemy.ext.declarative"}
DECLARATIVE_NAMES = {"declarative_base", "declared_attr"}
JOIN_NAMES = {"join", "outerjoin"}
LOADER_NAMES = {
    "joinedload",
    "lazyload",
    "selectinload",
    "subqueryload",
    "contains_eager",
}
DML_NAMES = {"insert", "update", "delete"}


def _parse_error(source: str) -> str | None:
    try:
        ast.parse(source, "<sa20-scan>")
    except SyntaxError as exc:
        return str(exc)
    return None


def _is_name(node: ast.AST, expected: str) -> bool:
    return isinstance(node, ast.Name) and node.id == expected


def _call_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _is_string_literal(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and isinstance(node.value, str)


class _SQLAlchemy20Scanner(ast.NodeVisitor):
    def __init__(self) -> None:
        self.transform_counts: Counter[str] = Counter()
        self.findings: list[ManualReviewFinding] = []
        self._seen_findings: set[tuple[str, int | None]] = set()

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module in DECLARATIVE_MODULES and any(
            alias.name in DECLARATIVE_NAMES for alias in node.names
        ):
            self.transform_counts["declarative_imports"] += 1
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        func_name = _call_name(node.func)

        if _is_name(node.func, "select") and node.args and isinstance(
            node.args[0], ast.List
        ):
            self.transform_counts["select_list_syntax"] += 1

        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "get" and isinstance(node.func.value, ast.Call):
                inner_call = node.func.value
                if isinstance(inner_call.func, ast.Attribute) and (
                    inner_call.func.attr == "query"
                ):
                    self.transform_counts["query_get"] += 1

            if node.func.attr in JOIN_NAMES and node.args and _is_string_literal(
                node.args[0]
            ):
                self.transform_counts["string_join"] += 1

            if node.func.attr == "execute" and _is_name(node.func.value, "engine"):
                self._add_finding("engine_execute_removed", node.lineno)

            if node.func.attr == "from_self":
                self._add_finding("query_from_self_removed", node.lineno)

        if func_name in LOADER_NAMES and node.args and _is_string_literal(node.args[0]):
            self.transform_counts["string_loader_option"] += 1

        if func_name in DML_NAMES and any(
            keyword.arg in {"values", "whereclause"}
            for keyword in node.keywords
            if keyword.arg is not None
        ):
            self.transform_counts["dml_constructor_kwargs"] += 1

        self.generic_visit(node)

    def _add_finding(self, code: str, line: int | None) -> None:
        key = (code, line)
        if key in self._seen_findings:
            return
        self._seen_findings.add(key)
        self.findings.append(
            ManualReviewFinding(
                code=code,
                message=BLOCKED_PATTERNS[code],
                line=line,
            )
        )


def scan_sqlalchemy20_patterns(
    source: str,
) -> tuple[str, list[TransformApplication], list[ManualReviewFinding], str | None]:
    parse_error = _parse_error(source)
    if parse_error is not None:
        return source, [], [], parse_error

    tree = ast.parse(source, "<sa20-scan>")
    scanner = _SQLAlchemy20Scanner()
    scanner.visit(tree)

    transforms = [
        TransformApplication(
            transform_id=transform_id,
            description=SUPPORTED_TRANSFORMS[transform_id][0],
            confidence=SUPPORTED_TRANSFORMS[transform_id][1],
            occurrences=occurrences,
        )
        for transform_id, occurrences in sorted(scanner.transform_counts.items())
        if occurrences > 0
    ]

    return source, transforms, scanner.findings, None
