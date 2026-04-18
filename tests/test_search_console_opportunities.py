from __future__ import annotations

from pathlib import Path

from scripts.search_console_opportunities import (
    read_opportunities,
    render_markdown,
)

FIXTURE = Path(__file__).with_name("fixtures") / "search_console_pages.csv"


def test_search_console_opportunities_prioritizes_low_ctr_rows() -> None:
    items = read_opportunities(FIXTURE, min_impressions=10, target_ctr=0.05)
    markdown = render_markdown(items, limit=2)

    assert items[0].label.endswith("/pydantic/basesettings-import-error/")
    assert items[0].missed_clicks == 6
    assert "Rewrite title/meta" in items[1].recommendation
    assert "https://zippertools.org/pydantic/basesettings-import-error/" in markdown
    assert "20.00%" not in markdown
