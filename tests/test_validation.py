from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4

from sa20_pack.validation import run_validation


def test_run_validation_rejects_mutating_format_commands() -> None:
    scratch_root = Path("test_runs")
    scratch_root.mkdir(exist_ok=True)
    root = scratch_root / f"validation_{uuid4().hex}"
    root.mkdir()
    try:
        (root / "pyproject.toml").write_text(
            "\n".join(
                [
                    "[tool.sa20_pack.validation]",
                    'format = ["python", "-m", "ruff", "format", "."]',
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        results = run_validation(root)

        format_result = results[0]
        assert format_result.phase == "format"
        assert format_result.returncode == 1
        assert format_result.note is not None
        assert "Mutating format validation commands" in format_result.note
    finally:
        shutil.rmtree(root, ignore_errors=True)
