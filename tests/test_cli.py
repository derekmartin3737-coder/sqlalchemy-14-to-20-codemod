from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from uuid import uuid4


def test_module_cli_runs_and_writes_report() -> None:
    scratch_root = Path("test_runs")
    scratch_root.mkdir(exist_ok=True)
    root = scratch_root / f"cli_repo_{uuid4().hex}"
    root.mkdir()
    repo = root / "repo"
    repo.mkdir()
    sample = repo / "example.py"
    sample.write_text(
        "\n".join(
            [
                "from sqlalchemy import select",
                "",
                "query = select([users])",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    report_path = root / "report.json"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path.cwd() / "src")
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "sa20_pack.cli",
                str(repo),
                "--report",
                str(report_path),
            ],
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )

        assert result.returncode == 0
        assert "Status: preview_only" in result.stdout
        assert report_path.exists()

        report = json.loads(report_path.read_text(encoding="utf-8"))
        assert report["status"] == "preview_only"
        assert report["files_scanned"] == 1
        assert report["transform_count"] == 1
        assert report["files_changed"] == []
        assert sample.read_text(encoding="utf-8").endswith("query = select([users])\n")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_module_cli_rejects_apply_for_public_repo() -> None:
    scratch_root = Path("test_runs")
    scratch_root.mkdir(exist_ok=True)
    root = scratch_root / f"cli_apply_repo_{uuid4().hex}"
    root.mkdir()
    repo = root / "repo"
    repo.mkdir()
    (repo / "example.py").write_text(
        "from sqlalchemy import select\n\nquery = select([users])\n",
        encoding="utf-8",
    )
    report_path = root / "report.json"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path.cwd() / "src")
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "sa20_pack.cli",
                str(repo),
                "--apply",
                "--report",
                str(report_path),
            ],
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )

        assert result.returncode == 1
        assert "Community edition is scan-only" in result.stdout
        report = json.loads(report_path.read_text(encoding="utf-8"))
        assert report["status"] == "preview_only"
    finally:
        shutil.rmtree(root, ignore_errors=True)
