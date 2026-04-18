from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Opportunity:
    label: str
    clicks: int
    impressions: int
    ctr: float
    position: float
    missed_clicks: float
    recommendation: str


def normalize_header(value: str) -> str:
    return value.strip().lower().replace(" ", "_")


def parse_int(value: str) -> int:
    cleaned = value.strip().replace(",", "")
    if not cleaned:
        return 0
    return int(float(cleaned))


def parse_float(value: str) -> float:
    cleaned = value.strip().replace(",", "").replace("%", "")
    if not cleaned:
        return 0.0
    return float(cleaned)


def parse_ctr(value: str) -> float:
    cleaned = value.strip()
    if not cleaned:
        return 0.0
    parsed = parse_float(cleaned)
    if "%" in cleaned:
        return parsed / 100
    if parsed > 1:
        return parsed / 100
    return parsed


def pick_label(row: dict[str, str]) -> str:
    for key in ("top_pages", "pages", "page", "top_queries", "queries", "query"):
        if row.get(key):
            return row[key].strip()
    return ""


def recommendation_for(ctr: float, position: float) -> str:
    if position <= 12 and ctr < 0.02:
        return "Rewrite title/meta and lead with the exact answer."
    if position <= 30 and ctr < 0.04:
        return "Sharpen snippet copy and add stronger internal links."
    if position > 30:
        return "Improve topical support and external/internal links before CTR tuning."
    return "Monitor; not the first rewrite candidate."


def read_opportunities(
    path: Path,
    *,
    min_impressions: int,
    target_ctr: float,
) -> list[Opportunity]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            return []
        rows = [
            {normalize_header(key): value for key, value in row.items() if key}
            for row in reader
        ]

    opportunities: list[Opportunity] = []
    for row in rows:
        label = pick_label(row)
        impressions = parse_int(row.get("impressions", "0"))
        if not label or impressions < min_impressions:
            continue
        clicks = parse_int(row.get("clicks", "0"))
        ctr = parse_ctr(row.get("ctr", "0"))
        position = parse_float(row.get("position", row.get("average_position", "0")))
        missed_clicks = max(0.0, (target_ctr - ctr) * impressions)
        opportunities.append(
            Opportunity(
                label=label,
                clicks=clicks,
                impressions=impressions,
                ctr=ctr,
                position=position,
                missed_clicks=missed_clicks,
                recommendation=recommendation_for(ctr, position),
            )
        )

    return sorted(
        opportunities,
        key=lambda item: (item.missed_clicks, item.impressions),
        reverse=True,
    )


def render_markdown(items: list[Opportunity], *, limit: int) -> str:
    lines = [
        "| Page or query | Clicks | Impressions | CTR | Position | "
        "Missed clicks at target | Recommendation |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for item in items[:limit]:
        lines.append(
            "| "
            + " | ".join(
                (
                    item.label.replace("|", "\\|"),
                    str(item.clicks),
                    str(item.impressions),
                    f"{item.ctr:.2%}",
                    f"{item.position:.1f}",
                    f"{item.missed_clicks:.1f}",
                    item.recommendation,
                )
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Find Search Console pages or queries with impressions but weak CTR."
        )
    )
    parser.add_argument("csv_path", help="Search Console CSV export path.")
    parser.add_argument("--min-impressions", type=int, default=10)
    parser.add_argument("--target-ctr", type=float, default=0.05)
    parser.add_argument("--limit", type=int, default=25)
    args = parser.parse_args()

    items = read_opportunities(
        Path(args.csv_path),
        min_impressions=args.min_impressions,
        target_ctr=args.target_ctr,
    )
    print(render_markdown(items, limit=args.limit), end="")


if __name__ == "__main__":
    main()
