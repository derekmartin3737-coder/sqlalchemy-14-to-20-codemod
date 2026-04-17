from __future__ import annotations

from pathlib import Path


def test_public_action_defaults_to_scan_only() -> None:
    action_path = (
        Path(__file__).resolve().parents[1]
        / ".github"
        / "actions"
        / "sa20-pack"
        / "action.yml"
    )
    action_text = action_path.read_text(encoding="utf-8")

    assert 'default: "false"' in action_text
