from __future__ import annotations

import html
import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, cast

from cra_evidence_builder.models import EvidenceReport


def _normalize(value: Any) -> Any:
    if is_dataclass(value):
        data = asdict(cast(Any, value))
        dataclass_value = cast(Any, value)
        if hasattr(dataclass_value, "status"):
            data["status"] = dataclass_value.status
        if hasattr(dataclass_value, "blocking_findings"):
            data["blocking_findings"] = len(dataclass_value.blocking_findings)
        return _normalize(data)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _normalize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    return value


def report_to_json(report: EvidenceReport) -> str:
    return json.dumps(_normalize(report), indent=2, sort_keys=True)


def _badge(value: str) -> str:
    safe = html.escape(value)
    return f'<span class="badge badge-{safe}">{safe}</span>'


def _metric(label: str, value: int) -> str:
    return (
        '<div class="metric">'
        f"<span>{html.escape(label)}</span><strong>{value}</strong>"
        "</div>"
    )


def _source_link(url: str, label: str) -> str:
    if not url:
        return html.escape(label or "not available")
    return f'<a href="{html.escape(url)}">{html.escape(label)}</a>'


def report_to_html(report: EvidenceReport) -> str:
    evidence_rows = "\n".join(
        f"<tr><td>{html.escape(item.kind)}</td><td>{html.escape(item.path)}</td>"
        f"<td>{html.escape(item.detail)}</td></tr>"
        for item in report.evidence_items
    )
    if not evidence_rows:
        evidence_rows = '<tr><td colspan="3">No evidence artifacts found.</td></tr>'

    findings = "\n".join(
        f"""
        <article class="finding">
          <div class="finding-head">
            <strong>{html.escape(item.rule_id)} - {html.escape(item.title)}</strong>
            {_badge(item.severity)} {_badge(item.classification)}
          </div>
          <p>{html.escape(item.message)}</p>
          <dl>
            <dt>File</dt><dd>{html.escape(item.path)}</dd>
            <dt>Current</dt><dd>{html.escape(item.current or "")}</dd>
            <dt>Recommendation</dt><dd>{html.escape(item.recommended or "")}</dd>
            <dt>Source</dt><dd>{_source_link(item.source_url, item.source_label)}</dd>
          </dl>
        </article>
        """
        for item in report.findings
    )
    if not findings:
        findings = "<p>No findings.</p>"

    templates = "\n".join(
        f"""
        <article>
          <h3>{html.escape(item.path)}</h3>
          <p>{html.escape(item.title)} - written: {str(item.written).lower()}</p>
          <pre>{html.escape(item.content)}</pre>
        </article>
        """
        for item in report.template_files
    )
    if not templates:
        templates = "<p>No templates generated.</p>"

    notes = "".join(f"<li>{html.escape(note)}</li>" for note in report.notes)
    generated_line = (
        f"Generated {html.escape(report.created_at)} with rule pack "
        f"{html.escape(report.rule_pack_version)}"
    )
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>CRA Evidence Report</title>
    <style>
      body {{
        background: #f7f8fb;
        color: #182235;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        line-height: 1.55;
        margin: 0;
      }}
      main {{ margin: 0 auto; max-width: 1080px; padding: 32px 20px 56px; }}
      header, section, article {{
        background: #fff;
        border: 1px solid #dce3ee;
        border-radius: 8px;
        margin-bottom: 18px;
        padding: 20px;
      }}
      h1, h2, h3 {{ line-height: 1.2; margin: 0 0 12px; }}
      .summary {{
        display: grid;
        gap: 12px;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      }}
      .metric {{ background: #eef5ff; border-radius: 6px; padding: 12px; }}
      .metric strong {{ display: block; font-size: 1.4rem; }}
      .badge {{
        border-radius: 999px;
        display: inline-block;
        font-size: 0.78rem;
        margin-left: 6px;
        padding: 2px 8px;
        text-transform: uppercase;
      }}
      .badge-critical, .badge-high, .badge-blocked, .badge-manual_review {{
        background: #ffe7e1;
        color: #8b1e0f;
      }}
      .badge-medium {{ background: #fff2ca; color: #684800; }}
      .badge-info, .badge-informational {{ background: #e8f4ff; color: #16456b; }}
      table {{ border-collapse: collapse; width: 100%; }}
      th, td {{ border-bottom: 1px solid #dce3ee; padding: 10px; text-align: left; }}
      pre {{
        background: #111827;
        border-radius: 6px;
        color: #e5eefb;
        overflow-x: auto;
        padding: 14px;
      }}
      dl {{ display: grid; gap: 8px 14px; grid-template-columns: max-content 1fr; }}
      dt {{ color: #53627a; font-weight: 700; }}
      dd {{ margin: 0; }}
    </style>
  </head>
  <body>
    <main>
      <header>
        <p>{generated_line}</p>
        <h1>CRA Evidence Report</h1>
        <p>Status: <strong>{html.escape(report.status)}</strong></p>
        <div class="summary">
          {_metric("Scanned files", len(report.scanned_files))}
          {_metric("Evidence items", len(report.evidence_items))}
          {_metric("Findings", len(report.findings))}
          {_metric("Templates", len(report.template_files))}
        </div>
      </header>
      <section>
        <h2>Evidence Inventory</h2>
        <table><thead><tr><th>Kind</th><th>Path</th><th>Detail</th></tr></thead>
        <tbody>{evidence_rows}</tbody></table>
      </section>
      <section><h2>Findings</h2>{findings}</section>
      <section><h2>Templates</h2>{templates}</section>
      <section><h2>Notes</h2><ul>{notes}</ul></section>
    </main>
  </body>
</html>
"""
