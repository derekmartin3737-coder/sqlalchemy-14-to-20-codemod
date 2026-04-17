from __future__ import annotations

import json
from pathlib import Path

from scripts.build_site import build_site
from scripts.submit_indexnow import build_payload


def test_build_site_generates_sitemaps_and_indexnow_key() -> None:
    tmp_path = Path.cwd() / "site"
    manifest = build_site(tmp_path)

    assert (tmp_path / "guides" / "index.html").exists()
    assert (tmp_path / "products" / "index.html").exists()
    assert (tmp_path / "proof" / "sqlalchemy-public-proof" / "index.html").exists()
    assert (tmp_path / "sitemap.xml").exists()
    assert (tmp_path / "sitemap-problem-pages.xml").exists()
    assert len(manifest["guides"]) >= 50
    assert len(manifest["urls"]["guides"]) >= 50
    assert "https://zippertools.org/proof/sqlalchemy-public-proof/" in manifest["urls"]["proof"]
    assert (tmp_path / f"{manifest['indexnow_key']}.txt").read_text(encoding="utf-8") == manifest["indexnow_key"]


def test_generated_guide_has_canonical_and_breadcrumb_schema() -> None:
    tmp_path = Path.cwd() / "site"
    build_site(tmp_path)
    guide_text = (tmp_path / "sqlalchemy" / "engine-execute-removed" / "index.html").read_text(encoding="utf-8")

    assert 'rel="canonical" href="https://zippertools.org/sqlalchemy/engine-execute-removed/"' in guide_text
    assert '"@type": "BreadcrumbList"' in guide_text
    assert "How to fix engine.execute(...) removal in SQLAlchemy 2.0" in guide_text
    assert 'href="/products/sa20-pack/"' in guide_text
    assert 'href="/favicon.svg" type="image/svg+xml"' in guide_text


def test_error_message_pages_are_generated_and_linked() -> None:
    tmp_path = Path.cwd() / "site"
    build_site(tmp_path)

    optionengine_text = (tmp_path / "sqlalchemy" / "optionengine-execute-error" / "index.html").read_text(encoding="utf-8")
    checklist_text = (tmp_path / "sqlalchemy" / "sqlalchemy-20-triage-checklist" / "index.html").read_text(encoding="utf-8")
    product_text = (tmp_path / "products" / "sa20-pack" / "index.html").read_text(encoding="utf-8")

    assert "'OptionEngine' object has no attribute 'execute'" in optionengine_text
    assert "SQLAlchemy 2.0 migration triage checklist" in checklist_text
    assert 'href="/sqlalchemy/optionengine-execute-error/"' in product_text
    assert 'href="/sqlalchemy/sqlalchemy-manual-vs-codemod/"' in product_text


def test_generated_redirects_preserve_legacy_paths_and_track_checkout() -> None:
    tmp_path = Path.cwd() / "site"
    build_site(tmp_path)
    redirects_text = (tmp_path / "_redirects").read_text(encoding="utf-8")

    assert "/sqlalchemy-migration-tool /products/sa20-pack/ 301" in redirects_text
    assert "/sqlalchemy-query-get-migration /sqlalchemy/session-query-get/ 301" in redirects_text
    assert "/favicon.ico /favicon.svg 301" in redirects_text
    assert "/pricing /pricing.html 301" not in redirects_text
    assert "/pricing.html /pricing 301" in redirects_text
    assert "/policies.html /policies 301" in redirects_text
    assert "/sqlalchemy-14-to-20-migration-pack.html /products/sa20-pack/ 301" in redirects_text
    assert "/sqlalchemy-preset-bundle.html /pricing 301" in redirects_text
    assert "/pydantic-basesettings-migration.html /pydantic/basesettings-moved/ 301" in redirects_text
    assert "/products/sa20-pack/index.html /products/sa20-pack/ 301" in redirects_text
    assert "/go/free-scan https://github.com/derekmartin3737-coder/sqlalchemy-14-to-20-codemod/blob/main/docs/quickstart.md" in redirects_text
    assert "utm_campaign=free_scan" in redirects_text
    assert "/go/github-release https://github.com/derekmartin3737-coder/sqlalchemy-14-to-20-codemod/releases/tag/v0.1.0" in redirects_text
    assert "/go/sa20-pack https://pay.zippertools.org/b/QimJ6" in redirects_text
    assert "utm_content=sa20-pack 302" in redirects_text
    assert "/optionengine-object-has-no-attribute-execute /sqlalchemy/optionengine-execute-error/ 301" in redirects_text
    assert "/optionengine-object-has-no-attribute-execute.html /sqlalchemy/optionengine-execute-error/ 301" in redirects_text
    assert "/sqlalchemy-2-migration-checklist /sqlalchemy/sqlalchemy-20-triage-checklist/ 301" in redirects_text


def test_product_pages_link_to_trackable_checkout_routes() -> None:
    tmp_path = Path.cwd() / "site"
    build_site(tmp_path)

    sa20_text = (tmp_path / "products" / "sa20-pack" / "index.html").read_text(encoding="utf-8")
    pydantic_text = (tmp_path / "products" / "pydantic-v2-porter" / "index.html").read_text(encoding="utf-8")

    assert 'href="/go/sa20-pack"' in sa20_text
    assert 'href="/go/pydantic-v2-porter"' in pydantic_text
    assert 'href="/go/free-scan"' in sa20_text
    assert "Run the free scan first" in sa20_text
    assert "Buy sa20-pack - $299.99" in sa20_text
    assert "Buy pydantic-v2-porter - $249.99" in pydantic_text
    assert 'href="/proof/sqlalchemy-public-proof/"' in sa20_text


def test_generated_links_and_sitemaps_use_clean_public_urls() -> None:
    tmp_path = Path.cwd() / "site"
    build_site(tmp_path)

    pricing_text = (tmp_path / "sitemap-pages.xml").read_text(encoding="utf-8")
    product_text = (tmp_path / "products" / "sa20-pack" / "index.html").read_text(encoding="utf-8")

    assert "https://zippertools.org/pricing.html" not in pricing_text
    assert "https://zippertools.org/pricing" in pricing_text
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


def test_indexnow_payload_uses_generated_manifest_groups() -> None:
    tmp_path = Path.cwd() / "site"
    build_site(tmp_path)
    manifest = json.loads((tmp_path / "_site_manifest.json").read_text(encoding="utf-8"))

    payload = build_payload(manifest, ["static", "guides"])

    assert payload["host"] == "zippertools.org"
    assert payload["keyLocation"].endswith(".txt")
    assert "https://zippertools.org/" in payload["urlList"]
    assert any("/sqlalchemy/" in url for url in payload["urlList"])

    proof_payload = build_payload(manifest, ["proof"])

    assert proof_payload["urlList"] == [
        "https://zippertools.org/proof/sqlalchemy-public-proof/"
    ]
