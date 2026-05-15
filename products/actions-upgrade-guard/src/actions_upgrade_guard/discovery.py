from __future__ import annotations

from pathlib import Path


def discover_workflow_files(root: Path) -> list[Path]:
    workflow_root = root / ".github" / "workflows"
    if not workflow_root.exists():
        return []
    candidates = [
        *workflow_root.glob("*.yml"),
        *workflow_root.glob("*.yaml"),
    ]
    return sorted(path for path in candidates if path.is_file())


def discover_local_action_files(root: Path) -> list[Path]:
    actions_root = root / ".github" / "actions"
    if not actions_root.exists():
        return []
    candidates = [
        *actions_root.glob("**/action.yml"),
        *actions_root.glob("**/action.yaml"),
    ]
    return sorted(path for path in candidates if path.is_file())
