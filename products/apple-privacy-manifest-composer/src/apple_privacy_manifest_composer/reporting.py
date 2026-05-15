from __future__ import annotations

import html
import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, cast

from apple_privacy_manifest_composer.models import PrivacyReport


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


def report_to_json(report: PrivacyReport) -> str:
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


def _location(path: str, line: int | None) -> str:
    suffix = f":{line}" if line else ""
    return html.escape(f"{path}{suffix}")


def _source_link(url: str, label: str) -> str:
    if not url:
        return html.escape(label or "not available")
    return f'<a href="{html.escape(url)}">{html.escape(label)}</a>'


def report_to_html(report: PrivacyReport) -> str:
    findings = "\n".join(
        f"""
        <article class="finding">
          <div class="finding-head">
            <strong>{html.escape(item.rule_id)} - {html.escape(item.title)}</strong>
            {_badge(item.severity)} {_badge(item.classification)}
          </div>
          <p>{html.escape(item.message)}</p>
          <dl>
            <dt>File</dt><dd>{_location(item.path, item.line)}</dd>
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

    api_rows = "\n".join(
        f"""
        <tr>
          <td>{html.escape(item.category)}</td>
          <td>{_location(item.path, item.line)}</td>
          <td>{html.escape(item.symbol)}</td>
          <td>{item.confidence:.2f}</td>
        </tr>
        """
        for item in report.api_hits
    )
    if not api_rows:
        api_rows = '<tr><td colspan="4">No required-reason API hits.</td></tr>'

    sdk_rows = "\n".join(
        f"""
        <tr>
          <td>{html.escape(item.name)}</td>
          <td>{_location(item.path, item.line)}</td>
          <td>{item.confidence:.2f}</td>
        </tr>
        """
        for item in report.sdk_hits
    )
    if not sdk_rows:
        sdk_rows = '<tr><td colspan="3">No listed SDK hits.</td></tr>'

    candidate = ""
    if report.candidate_manifest:
        candidate = (
            "<section><h2>Candidate Manifest</h2>"
            f"<p>{html.escape(report.candidate_manifest.path)}</p>"
            f"<pre>{html.escape(report.candidate_manifest.xml)}</pre></section>"
        )

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
    <title>Apple Privacy Manifest Report</title>
    <style>
      body {{
        background: #f6f8fb;
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
        <h1>Apple Privacy Manifest Report</h1>
        <p>Status: <strong>{html.escape(report.status)}</strong></p>
        <div class="summary">
          {_metric("Scanned files", len(report.scanned_files))}
          {_metric("API hits", len(report.api_hits))}
          {_metric("SDK hits", len(report.sdk_hits))}
          {_metric("Findings", len(report.findings))}
        </div>
      </header>
      <section>
        <h2>Required-Reason API Hits</h2>
        <table><thead><tr><th>Category</th><th>Location</th>
        <th>Symbol</th><th>Confidence</th></tr></thead><tbody>{api_rows}</tbody></table>
      </section>
      <section>
        <h2>Listed SDK Hits</h2>
        <table><thead><tr><th>SDK</th><th>Location</th>
        <th>Confidence</th></tr></thead><tbody>{sdk_rows}</tbody></table>
      </section>
      <section><h2>Findings</h2>{findings}</section>
      {candidate}
      <section><h2>Notes</h2><ul>{notes}</ul></section>
    </main>
  </body>
</html>
"""
