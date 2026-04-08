from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, cast

from sa20_pack.models import (
    FileMigrationResult,
    MigrationReport,
    ValidationCommandResult,
)


def _normalize(value: Any) -> Any:
    if isinstance(value, MigrationReport):
        payload = asdict(value)
        payload.update(
            {
                "files_changed": value.files_changed,
                "manual_todos": value.manual_todos,
                "overall_confidence": value.overall_confidence,
                "parse_error_count": value.parse_error_count,
                "status": value.status,
                "transform_count": value.transform_count,
                "unsupported_count": value.unsupported_count,
                "validation_passed": value.validation_passed,
            }
        )
        return _normalize(payload)
    if isinstance(value, FileMigrationResult):
        payload = asdict(value)
        payload["confidence"] = value.confidence
        return _normalize(payload)
    if isinstance(value, ValidationCommandResult):
        payload = asdict(value)
        payload["success"] = value.success
        return _normalize(payload)
    if is_dataclass(value):
        return _normalize(asdict(cast(Any, value)))
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _normalize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    return value


def report_to_json(report: Any) -> str:
    return json.dumps(_normalize(report), indent=2, sort_keys=True)
