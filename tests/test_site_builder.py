from __future__ import annotations

import json
from pathlib import Path

from scripts.build_site import build_site
from scripts.submit_indexnow import build_payload

# ruff: noqa: E501


def _build_output(name: str) -> Path:
    return Path.cwd() / "test_runs" / "site_builder" / name


def test_build_site_generates_sitemaps_and_indexnow_key() -> None:
    site_dir = _build_output("sitemaps")
    manifest = build_site(site_dir)

    assert (site_dir / "guides" / "index.html").exists()
    assert (site_dir / "products" / "index.html").exists()
    assert (site_dir / "proof" / "sqlalchemy-public-proof" / "index.html").exists()
    assert (site_dir / "proof" / "pydantic-v2-porter" / "index.html").exists()
    assert (site_dir / "proof" / "flatconfig-lift" / "index.html").exists()
    assert (site_dir / "sitemap.xml").exists()
    assert (site_dir / "sitemap-problem-pages.xml").exists()
    assert len(manifest["guides"]) >= 50
    assert len(manifest["urls"]["guides"]) >= 50
    assert (
        "https://zippertools.org/proof/sqlalchemy-public-proof/"
        in manifest["urls"]["proof"]
    )
    assert (
        "https://zippertools.org/proof/pydantic-v2-porter/" in manifest["urls"]["proof"]
    )
    assert (site_dir / f"{manifest['indexnow_key']}.txt").read_text(
        encoding="utf-8"
    ) == manifest["indexnow_key"]


def test_generated_guide_has_canonical_and_breadcrumb_schema() -> None:
    site_dir = _build_output("guide")
    build_site(site_dir)
    guide_text = (
        site_dir / "sqlalchemy" / "engine-execute-removed" / "index.html"
    ).read_text(encoding="utf-8")

    assert (
        'rel="canonical" href="https://zippertools.org/sqlalchemy/engine-execute-removed/"'
        in guide_text
    )
    assert '"@type": "BreadcrumbList"' in guide_text
    assert "How to fix engine.execute(...) removal in SQLAlchemy 2.0" in guide_text
    assert 'href="/products/sa20-pack/"' in guide_text
    assert 'href="/pricing#sa20-pack"' in guide_text
    assert 'href="/favicon.svg" type="image/svg+xml"' in guide_text


def test_error_message_pages_are_generated_and_linked() -> None:
    site_dir = _build_output("error_pages")
    build_site(site_dir)

    optionengine_text = (
        site_dir / "sqlalchemy" / "optionengine-execute-error" / "index.html"
    ).read_text(encoding="utf-8")
    checklist_text = (
        site_dir / "sqlalchemy" / "sqlalchemy-20-triage-checklist" / "index.html"
    ).read_text(encoding="utf-8")
    product_text = (site_dir / "products" / "sa20-pack" / "index.html").read_text(
        encoding="utf-8"
    )

    assert "'OptionEngine' object has no attribute 'execute'" in optionengine_text
    assert "SQLAlchemy 2.0 migration triage checklist" in checklist_text
    assert 'href="/sqlalchemy/optionengine-execute-error/"' in product_text
    assert 'href="/sqlalchemy/sqlalchemy-manual-vs-codemod/"' in product_text


def test_generated_redirects_preserve_legacy_paths_and_track_checkout() -> None:
    site_dir = _build_output("redirects")
    build_site(site_dir)
    redirects_text = (site_dir / "_redirects").read_text(encoding="utf-8")

    assert "/sqlalchemy-migration-tool /products/sa20-pack/ 301" in redirects_text
    assert (
        "/sqlalchemy-query-get-migration /sqlalchemy/session-query-get/ 301"
        in redirects_text
    )
    assert "/favicon.ico /favicon.svg 301" in redirects_text
    assert "/pricing /pricing.html 301" not in redirects_text
    assert "/pricing.html /pricing 301" in redirects_text
    assert "/policies.html /policies 301" in redirects_text
    assert (
        "/sqlalchemy-14-to-20-migration-pack.html /products/sa20-pack/ 301"
        in redirects_text
    )
    assert "/sqlalchemy-preset-bundle.html /pricing 301" in redirects_text
    assert (
        "/pydantic-basesettings-migration.html /pydantic/basesettings-moved/ 301"
        in redirects_text
    )
    assert "/products/sa20-pack/index.html /products/sa20-pack/ 301" in redirects_text
    assert (
        "/go/free-scan https://github.com/derekmartin3737-coder/sqlalchemy-14-to-20-codemod/blob/main/docs/quickstart.md"
        in redirects_text
    )
    assert (
        "/go/pydantic-free-scan https://github.com/derekmartin3737-coder/sqlalchemy-14-to-20-codemod/blob/main/products/pydantic-v2-porter/README.md"
        in redirects_text
    )
    assert (
        "/go/flatconfig-free-scan https://github.com/derekmartin3737-coder/sqlalchemy-14-to-20-codemod/blob/main/products/flatconfig-lift/README.md"
        in redirects_text
    )
    assert "utm_campaign=free_scan" in redirects_text
    assert (
        "/go/github-release https://github.com/derekmartin3737-coder/sqlalchemy-14-to-20-codemod/releases/tag/v0.1.0"
        in redirects_text
    )
    assert "/scan.html /scan 301" in redirects_text
    assert "/sqlalchemy-2-migration-scan /scan 301" in redirects_text
    assert "/go/fit-report /pricing#fit-report 302" in redirects_text
    assert "/go/fit-review /pricing#fit-report 301" in redirects_text
    assert "/go/sa20-pack /pricing#sa20-pack 302" in redirects_text
    assert "/go/sa20-preset /pricing#sa20-preset 302" in redirects_text
    assert (
        "/go/pydantic-v2-porter /pricing#pydantic-v2-porter 302"
        in redirects_text
    )
    assert "pay.zippertools.org" not in redirects_text
    assert (
        "/optionengine-object-has-no-attribute-execute /sqlalchemy/optionengine-execute-error/ 301"
        in redirects_text
    )
    assert (
        "/optionengine-object-has-no-attribute-execute.html /sqlalchemy/optionengine-execute-error/ 301"
        in redirects_text
    )
    assert (
        "/sqlalchemy-2-migration-checklist /sqlalchemy/sqlalchemy-20-triage-checklist/ 301"
        in redirects_text
    )


def test_product_pages_link_to_trackable_checkout_routes() -> None:
    site_dir = _build_output("product_pages")
    build_site(site_dir)

    sa20_text = (site_dir / "products" / "sa20-pack" / "index.html").read_text(
        encoding="utf-8"
    )
    pydantic_text = (
        site_dir / "products" / "pydantic-v2-porter" / "index.html"
    ).read_text(encoding="utf-8")

    assert 'href="/go/sa20-pack/product-products-sa20-pack"' in sa20_text
    assert (
        'href="/go/pydantic-v2-porter/product-products-pydantic-v2-porter"'
        in pydantic_text
    )
    assert (
        'href="/go/pydantic-free-scan/product-products-pydantic-v2-porter"'
        in pydantic_text
    )
    assert 'href="/go/free-scan/product-products-sa20-pack"' in sa20_text
    assert "Run the free scan first" in sa20_text
    assert "Buy cleanup pack - $299.99" in sa20_text
    assert "Buy cleanup pack - $249.99" in pydantic_text
    assert 'href="/go/fit-report/product-products-sa20-pack"' in sa20_text
    assert "SQLAlchemy 1.4 to 2.0 Migration Cleanup Pack" in sa20_text
    assert "Pydantic v1 to v2 Migration Cleanup Pack" in pydantic_text
    assert 'href="/proof/sqlalchemy-public-proof/"' in sa20_text
    assert 'href="/proof/pydantic-v2-porter/"' in pydantic_text
    assert 'href="/pricing#pydantic-v2-porter"' in pydantic_text


def test_generated_links_and_sitemaps_use_clean_public_urls() -> None:
    site_dir = _build_output("clean_urls")
    build_site(site_dir)

    pricing_text = (site_dir / "sitemap-pages.xml").read_text(encoding="utf-8")
    product_text = (site_dir / "products" / "sa20-pack" / "index.html").read_text(
        encoding="utf-8"
    )

    assert "https://zippertools.org/pricing.html" not in pricing_text
    assert "https://zippertools.org/pricing" in pricing_text
    assert "https://zippertools.org/scan" in pricing_text
    assert "index.html" not in product_text
    assert 'href="/products/"' in product_text


def test_static_indexable_pages_use_clean_canonicals_and_links() -> None:
    pricing_text = Path("site/pricing.html").read_text(encoding="utf-8")
    demo_text = Path("site/demo.html").read_text(encoding="utf-8")
    index_text = Path("site/index.html").read_text(encoding="utf-8")
    config_text = Path("site/config.js").read_text(encoding="utf-8")

    assert 'href="https://zippertools.org/pricing"' in pricing_text
    assert 'content="https://zippertools.org/pricing"' in pricing_text
    assert 'href="https://zippertools.org/demo"' in demo_text
    assert 'content="https://zippertools.org/demo"' in demo_text
    assert 'href="pricing.html"' not in index_text
    assert 'href="sqlalchemy-migration-tool.html"' not in index_text
    assert 'freeStartUrl: "/go/free-scan"' in config_text
    assert 'paidPackUrl: "/go/sa20-pack"' in config_text
    assert 'presetBundleUrl: "/go/sa20-preset"' in config_text
    assert 'pydanticPackUrl: "/go/pydantic-v2-porter"' in config_text
    assert 'fitReportUrl: "/go/fit-report"' in config_text
    assert 'href="/scan"' in index_text


def test_indexnow_payload_uses_generated_manifest_groups() -> None:
    site_dir = _build_output("indexnow")
    build_site(site_dir)
    manifest = json.loads(
        (site_dir / "_site_manifest.json").read_text(encoding="utf-8")
    )

    payload = build_payload(manifest, ["static", "guides"])

    assert payload["host"] == "zippertools.org"
    assert payload["keyLocation"].endswith(".txt")
    assert "https://zippertools.org/" in payload["urlList"]
    assert any("/sqlalchemy/" in url for url in payload["urlList"])

    proof_payload = build_payload(manifest, ["proof"])

    assert (
        "https://zippertools.org/proof/sqlalchemy-public-proof/"
        in proof_payload["urlList"]
    )
    assert (
        "https://zippertools.org/proof/pydantic-v2-porter/" in proof_payload["urlList"]
    )
    assert "https://zippertools.org/proof/flatconfig-lift/" in proof_payload["urlList"]
