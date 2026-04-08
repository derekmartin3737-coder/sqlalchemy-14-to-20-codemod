from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4

from sa20_pack.runner import run_migration
from sa20_pack.transforms.sqlalchemy20 import scan_sqlalchemy20_patterns


def test_scan_detects_supported_patterns() -> None:
    source = (
        "from sqlalchemy.ext.declarative import declarative_base\n"
        "stmt = select([User.id])\n"
        "user = session.query(User).get(user_id)\n"
        'session.query(User).options(joinedload("addresses")).join("addresses").all()\n'
    )

    _, applications, findings, parse_error = scan_sqlalchemy20_patterns(source)

    assert parse_error is None
    assert findings == []
    transform_ids = {item.transform_id for item in applications}
    assert transform_ids == {
        "declarative_imports",
        "query_get",
        "select_list_syntax",
        "string_join",
        "string_loader_option",
    }


def test_scan_flags_manual_review_patterns() -> None:
    source = "engine.execute(stmt)\nquery.from_self()\n"

    _, _, findings, parse_error = scan_sqlalchemy20_patterns(source)

    assert parse_error is None
    assert [item.code for item in findings] == [
        "engine_execute_removed",
        "query_from_self_removed",
    ]


def test_runner_reports_preview_only_for_supported_repo() -> None:
    scratch_root = Path("test_runs")
    scratch_root.mkdir(exist_ok=True)
    root = scratch_root / f"sa20_scan_{uuid4().hex}"
    root.mkdir()
    try:
        (root / "module.py").write_text(
            "from sqlalchemy import select\n\nstmt = select([users])\n",
            encoding="utf-8",
        )

        report = run_migration(root=root, apply=False, show_diff=False)

        assert report.status == "preview_only"
        assert report.files_changed == []
        assert report.transform_count == 1
        assert report.validation_results == []
    finally:
        shutil.rmtree(root, ignore_errors=True)
