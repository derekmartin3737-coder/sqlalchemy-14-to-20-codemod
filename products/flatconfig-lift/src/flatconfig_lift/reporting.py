from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, cast


def _normalize(value: Any) -> Any:
    if is_dataclass(value):
        data = asdict(cast(Any, value))
        dataclass_value = cast(Any, value)
        if hasattr(dataclass_value, "status"):
            data["status"] = dataclass_value.status
        if hasattr(dataclass_value, "files_changed"):
            data["files_changed"] = dataclass_value.files_changed
        return _normalize(data)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _normalize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    return value


def report_to_json(report: Any) -> str:
    return json.dumps(_normalize(report), indent=2, sort_keys=True)
