from __future__ import annotations

from pathlib import Path

from scripts.audit_site_urls import parse_page, run_audit
from scripts.build_site import build_site


def test_parser_reads_bom_prefixed_self_closing_canonical() -> None:
    parser = parse_page(
        '\ufeff<!doctype html><link rel="canonical" href="https://zippertools.org/" />'
    )

    assert parser.canonical == "https://zippertools.org/"


def test_local_site_url_audit_passes_for_generated_sitemaps() -> None:
    site_dir = Path.cwd() / "site"
    build_site(site_dir)

    issues = run_audit(
        site_dir=site_dir,
        base_url="https://zippertools.org",
        live=False,
    )

    assert issues == []
