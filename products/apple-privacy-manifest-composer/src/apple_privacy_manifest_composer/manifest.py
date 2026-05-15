from __future__ import annotations

import plistlib
from io import BytesIO
from pathlib import Path

PLACEHOLDER_REASON = "REVIEW_REQUIRED"


def parse_declared_categories(path: Path) -> list[str]:
    data = plistlib.loads(path.read_bytes())
    if not isinstance(data, dict):
        return []
    raw_entries = data.get("NSPrivacyAccessedAPITypes", [])
    if not isinstance(raw_entries, list):
        return []
    categories: list[str] = []
    for entry in raw_entries:
        if not isinstance(entry, dict):
            continue
        value = entry.get("NSPrivacyAccessedAPIType")
        if isinstance(value, str):
            categories.append(value)
    return sorted(set(categories))


def build_candidate_manifest(categories: list[str]) -> str:
    entries = [
        {
            "NSPrivacyAccessedAPIType": category,
            "NSPrivacyAccessedAPITypeReasons": [PLACEHOLDER_REASON],
        }
        for category in sorted(set(categories))
    ]
    payload = {"NSPrivacyAccessedAPITypes": entries}
    buffer = BytesIO()
    plistlib.dump(payload, buffer, fmt=plistlib.FMT_XML, sort_keys=False)
    return buffer.getvalue().decode("utf-8")
