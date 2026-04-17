from __future__ import annotations

import argparse
import json
import posixpath
from collections import defaultdict
from dataclasses import asdict
from datetime import date
from html import escape
from pathlib import Path, PurePosixPath
from typing import Iterable

if __package__ in {None, ""}:
    from site_catalog import (  # type: ignore[no-redef]
        FAMILY_DESCRIPTIONS,
        FAMILY_TITLES,
        GUIDES,
        INDEXNOW_KEY,
        PRODUCTS,
        SITE_NAME,
        SITE_URL,
        GuidePage,
        ProductPage,
    )
else:
    from scripts.site_catalog import (
        FAMILY_DESCRIPTIONS,
        FAMILY_TITLES,
        GUIDES,
        INDEXNOW_KEY,
        PRODUCTS,
        SITE_NAME,
        SITE_URL,
        GuidePage,
        ProductPage,
    )

INDEXABLE_STATIC_PAGES = (
    ("", "Home"),
    ("pricing.html", "Pricing"),
    ("demo.html", "Demo"),
    ("guides/index.html", "Guides"),
    ("products/index.html", "Products"),
)

STATIC_PAGE_PATHS = (
    "pricing.html",
    "demo.html",
    "policies.html",
    "success.html",
    "cancel.html",
    "404.html",
)

PAYHIP_CHECKOUTS = {
    "sa20-pack": "https://pay.zippertools.org/b/QimJ6?utm_source=zippertools&utm_medium=site&utm_campaign=checkout&utm_content=sa20-pack",
    "sa20-preset": "https://pay.zippertools.org/b/wh2Ro?utm_source=zippertools&utm_medium=site&utm_campaign=checkout&utm_content=sa20-preset",
    "pydantic-v2-porter": "https://pay.zippertools.org/b/KamA1?utm_source=zippertools&utm_medium=site&utm_campaign=checkout&utm_content=pydantic-v2-porter",
}

REDIRECTS = (
    ("/favicon.ico", "/favicon.svg", 301),
    ("/go/sa20-pack", PAYHIP_CHECKOUTS["sa20-pack"], 302),
    ("/go/sa20-preset", PAYHIP_CHECKOUTS["sa20-preset"], 302),
    ("/go/pydantic-v2-porter", PAYHIP_CHECKOUTS["pydantic-v2-porter"], 302),
    ("/sqlalchemy-14-to-20-migration-pack", "/products/sa20-pack/", 301),
    ("/sqlalchemy-14-to-20-migration-pack.html", "/products/sa20-pack/", 301),
    ("/sqlalchemy-preset-bundle", "/pricing", 301),
    ("/sqlalchemy-preset-bundle.html", "/pricing", 301),
    ("/sqlalchemy-migration-tool", "/products/sa20-pack/", 301),
    ("/sqlalchemy-migration-tool.html", "/products/sa20-pack/", 301),
    ("/sqlalchemy-select-list-migration", "/sqlalchemy/select-list-syntax/", 301),
    ("/sqlalchemy-select-list-migration.html", "/sqlalchemy/select-list-syntax/", 301),
    ("/sqlalchemy-string-join-migration", "/sqlalchemy/string-join-paths/", 301),
    ("/sqlalchemy-string-join-migration.html", "/sqlalchemy/string-join-paths/", 301),
    ("/sqlalchemy-joinedload-string-migration", "/sqlalchemy/string-loader-options/", 301),
    ("/sqlalchemy-joinedload-string-migration.html", "/sqlalchemy/string-loader-options/", 301),
    ("/sqlalchemy-query-get-migration", "/sqlalchemy/session-query-get/", 301),
    ("/sqlalchemy-query-get-migration.html", "/sqlalchemy/session-query-get/", 301),
    ("/sqlalchemy-declarative-import-migration", "/sqlalchemy/declarative-imports/", 301),
    ("/sqlalchemy-declarative-import-migration.html", "/sqlalchemy/declarative-imports/", 301),
    ("/sqlalchemy-insert-values-migration", "/sqlalchemy/insert-values-kwargs/", 301),
    ("/sqlalchemy-insert-values-migration.html", "/sqlalchemy/insert-values-kwargs/", 301),
    ("/sqlalchemy-joinedload-all-migration", "/sqlalchemy/joinedload-all-removed/", 301),
    ("/sqlalchemy-joinedload-all-migration.html", "/sqlalchemy/joinedload-all-removed/", 301),
    ("/sqlalchemy-session-query-migration", "/sqlalchemy/session-query-migration/", 301),
    ("/sqlalchemy-session-query-migration.html", "/sqlalchemy/session-query-migration/", 301),
    ("/sqlalchemy-engine-execute-removed", "/sqlalchemy/engine-execute-removed/", 301),
    ("/sqlalchemy-engine-execute-removed.html", "/sqlalchemy/engine-execute-removed/", 301),
    ("/pydantic-v2-migration-pack", "/products/pydantic-v2-porter/", 301),
    ("/pydantic-v2-migration-pack.html", "/products/pydantic-v2-porter/", 301),
    ("/pydantic-validator-v2-migration", "/pydantic/validator-to-field-validator/", 301),
    ("/pydantic-validator-v2-migration.html", "/pydantic/validator-to-field-validator/", 301),
    ("/pydantic-basesettings-migration", "/pydantic/basesettings-moved/", 301),
    ("/pydantic-basesettings-migration.html", "/pydantic/basesettings-moved/", 301),
    ("/pydantic-root-validator-pre-migration", "/pydantic/root-validator-pre/", 301),
    ("/pydantic-root-validator-pre-migration.html", "/pydantic/root-validator-pre/", 301),
    ("/optionengine-object-has-no-attribute-execute", "/sqlalchemy/optionengine-execute-error/", 301),
    ("/optionengine-object-has-no-attribute-execute.html", "/sqlalchemy/optionengine-execute-error/", 301),
    ("/sqlalchemy-optionengine-object-has-no-attribute-execute", "/sqlalchemy/optionengine-execute-error/", 301),
    ("/attributeerror-optionengine-object-has-no-attribute-execute", "/sqlalchemy/optionengine-execute-error/", 301),
    ("/engine-object-has-no-attribute-execute", "/sqlalchemy/engine-attribute-error-execute/", 301),
    ("/engine-object-has-no-attribute-execute.html", "/sqlalchemy/engine-attribute-error-execute/", 301),
    ("/sqlalchemy-engine-object-has-no-attribute-execute", "/sqlalchemy/engine-attribute-error-execute/", 301),
    ("/legacyapiwarning-query-get", "/sqlalchemy/legacyapiwarning-query-get/", 301),
    ("/legacyapiwarning-query-get.html", "/sqlalchemy/legacyapiwarning-query-get/", 301),
    ("/sqlalchemy-legacyapiwarning-query-get", "/sqlalchemy/legacyapiwarning-query-get/", 301),
    ("/sqlalchemy-select-legacy-mode-warning", "/sqlalchemy/select-legacy-mode-warning/", 301),
    ("/sqlalchemy-select-legacy-mode-warning.html", "/sqlalchemy/select-legacy-mode-warning/", 301),
    ("/joinedload-all-is-not-defined", "/sqlalchemy/joinedload-all-nameerror/", 301),
    ("/joinedload-all-is-not-defined.html", "/sqlalchemy/joinedload-all-nameerror/", 301),
    ("/sqlalchemy-2-migration-checklist", "/sqlalchemy/sqlalchemy-20-triage-checklist/", 301),
    ("/sqlalchemy-2-migration-checklist.html", "/sqlalchemy/sqlalchemy-20-triage-checklist/", 301),
    ("/sqlalchemy-2-codemod", "/sqlalchemy/sqlalchemy-manual-vs-codemod/", 301),
    ("/sqlalchemy-2-codemod.html", "/sqlalchemy/sqlalchemy-manual-vs-codemod/", 301),
    ("/basesettings-import-error-pydantic-v2", "/pydantic/basesettings-import-error/", 301),
    ("/basesettings-import-error-pydantic-v2.html", "/pydantic/basesettings-import-error/", 301),
    ("/pydantic-validator-deprecated", "/pydantic/validator-deprecation-warning/", 301),
    ("/pydantic-validator-deprecated.html", "/pydantic/validator-deprecation-warning/", 301),
    ("/pydantic-class-config-deprecated", "/pydantic/config-class-deprecated-warning/", 301),
    ("/pydantic-class-config-deprecated.html", "/pydantic/config-class-deprecated-warning/", 301),
)


def canonical_url(path: str) -> str:
    return f"{SITE_URL}{public_path(path)}"


def is_page_path(path: str) -> bool:
    normalized = path.strip("/")
    return (
        normalized in {"", "index.html"}
        or normalized.endswith("/index.html")
        or normalized.endswith(".html")
    )


def public_path(path: str) -> str:
    normalized = path.strip("/")
    if normalized in {"", "index.html"}:
        return "/"
    if normalized.endswith("/index.html"):
        return f"/{normalized.removesuffix('index.html')}"
    if normalized.endswith(".html"):
        return f"/{normalized.removesuffix('.html')}"
    return f"/{normalized}"


def relative_href(from_path: str, to_path: str) -> str:
    if is_page_path(to_path):
        return public_path(to_path)
    start = posixpath.dirname(from_path) or "."
    return posixpath.relpath(to_path, start).replace("\\", "/")


def nav_html(path: str) -> str:
    repo_link = '<a href="#" data-repo-link>Repo</a>'
    return (
        '<header class="site-header"><div class="wrap nav">'
        f'<a class="brand" href="{relative_href(path, "index.html")}">Zipper Tools</a>'
        '<nav class="nav-links" aria-label="Primary">'
        f'<a href="{relative_href(path, "guides/index.html")}">Guides</a>'
        f'<a href="{relative_href(path, "products/index.html")}">Products</a>'
        f'<a href="{relative_href(path, "pricing.html")}">Pricing</a>'
        f'<a href="{relative_href(path, "demo.html")}">Demo</a>'
        f'<a href="{relative_href(path, "policies.html")}">Policies</a>'
        f"{repo_link}</nav></div></header>"
    )


def footer_html(path: str) -> str:
    return (
        '<footer class="site-footer"><div class="wrap footer-grid">'
        '<div><p class="footer-title">Zipper Tools</p>'
        '<p class="caption">Exact-problem migration guides and narrow codemod products.</p>'
        "</div>"
        '<div class="footer-links">'
        f'<a href="{relative_href(path, "guides/index.html")}">Guides</a>'
        f'<a href="{relative_href(path, "products/index.html")}">Products</a>'
        f'<a href="{relative_href(path, "pricing.html")}">Pricing</a>'
        f'<a href="{relative_href(path, "demo.html")}">Demo</a>'
        '<a href="#" data-repo-link>GitHub repo</a>'
        '<a href="#" data-contact-link>Contact</a>'
        "</div>"
        '<p class="caption footer-note">Questions: '
        '<a href="#" data-contact-link><span data-contact-email>email</span></a></p>'
        "</div></footer>"
    )


def breadcrumb_html(path: str, crumbs: list[tuple[str, str]]) -> str:
    items: list[str] = []
    for href, label in crumbs[:-1]:
        items.append(
            f'<li><a href="{relative_href(path, href)}">{escape(label)}</a></li>'
        )
    items.append(f'<li aria-current="page">{escape(crumbs[-1][1])}</li>')
    return '<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>' + "".join(items) + "</ol></nav>"


def breadcrumb_schema(crumbs: list[tuple[str, str]]) -> dict[str, object]:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": idx,
                "name": label,
                "item": canonical_url(href),
            }
            for idx, (href, label) in enumerate(crumbs, start=1)
        ],
    }


def webpage_schema(title: str, description: str, path: str) -> dict[str, object]:
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": description,
        "url": canonical_url(path),
        "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": f"{SITE_URL}/"},
    }


def product_schema(product: ProductPage, path: str) -> dict[str, object]:
    schema: dict[str, object] = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product.name,
        "category": "DeveloperApplication",
        "description": product.description,
        "url": canonical_url(path),
        "brand": {"@type": "Brand", "name": SITE_NAME},
    }
    if product.price:
        schema["offers"] = {
            "@type": "Offer",
            "price": product.price,
            "priceCurrency": product.currency,
            "availability": f"https://schema.org/{product.availability}",
            "url": canonical_url(path),
            "seller": {"@type": "Organization", "name": SITE_NAME},
        }
    return schema


def code_block(value: str) -> str:
    return f'<pre class="code-block"><code>{escape(value)}</code></pre>'


def layout(
    *,
    path: str,
    title: str,
    description: str,
    kicker: str,
    heading: str,
    body: str,
    crumbs: list[tuple[str, str]],
    schemas: Iterable[dict[str, object]],
) -> str:
    schema_json = json.dumps(
        [
            {"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": f"{SITE_URL}/"},
            webpage_schema(title, description, path),
            *schemas,
            breadcrumb_schema(crumbs),
        ],
        indent=2,
    )
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{escape(title)} | {SITE_NAME}</title>
    <meta name="description" content="{escape(description)}" />
    <meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1" />
    <link rel="canonical" href="{canonical_url(path)}" />
    <meta property="og:title" content="{escape(title)}" />
    <meta property="og:description" content="{escape(description)}" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{canonical_url(path)}" />
    <meta property="og:image" content="{SITE_URL}/og-preview.svg" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{escape(title)}" />
    <meta name="twitter:description" content="{escape(description)}" />
    <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
    <link rel="stylesheet" href="{relative_href(path, "styles.css")}" />
    <script src="{relative_href(path, "config.js")}"></script>
    <script defer src="{relative_href(path, "app.js")}"></script>
    <script type="application/ld+json">
{schema_json}
    </script>
  </head>
  <body>
    {nav_html(path)}
    <main class="wrap">
      <section class="warning" id="launch-warning" aria-live="polite"></section>
      <section class="page-title">
        {breadcrumb_html(path, crumbs)}
        <p class="kicker">{escape(kicker)}</p>
        <h1>{escape(heading)}</h1>
        <p>{escape(description)}</p>
      </section>
      {body}
    </main>
    {footer_html(path)}
  </body>
</html>
"""


def clean_generated_text(value: str) -> str:
    return "\n".join(line.rstrip() for line in value.splitlines()) + "\n"


def render_guide(guide: GuidePage) -> tuple[str, str]:
    path = f"{guide.family}/{guide.slug}/index.html"
    proof_cta = ""
    if guide.product_slug == "sa20-pack":
        proof_cta = (
            f'<a class="button secondary" href="{relative_href(path, "proof/sqlalchemy-public-proof/index.html")}">'
            "Read public proof</a>"
        )
    # Get related guides from same family (top 3 as cards)
    related = [item for item in GUIDES if item.family == guide.family and item.slug != guide.slug][:3]
    related_cards = "".join(
        f'<a class="topic-card" href="{relative_href(path, f"{item.family}/{item.slug}/index.html")}">'
        f"<strong>{escape(item.h1)}</strong><span>{escape(item.description)}</span></a>"
        for item in related
    )
    # Get all guides from same product for quick links
    product_guides = [
        item for item in GUIDES
        if item.product_slug == guide.product_slug and item.slug != guide.slug
    ]
    quick_links = ", ".join(
        f'<a href="{relative_href(path, f"{item.family}/{item.slug}/index.html")}">{escape(item.title.split(" in ")[0].split(" for ")[0])}</a>'
        for item in product_guides[:8]
    )
    more_fixes_html = ""
    if quick_links:
        more_fixes_html = f"""
      <section class="section">
        <article class="page-panel">
          <h3>More fixes in this product</h3>
          <p class="quick-links">{quick_links}</p>
          <p><a href="{relative_href(path, f'products/{guide.product_slug}/index.html')}">View all {guide.product_slug} guides</a></p>
        </article>
      </section>"""
    body = f"""
      <section class="section">
        <div class="grid two">
          <article class="page-panel">
            <p class="kicker">Search intent</p>
            <h2>{escape(guide.search_term)}</h2>
            <p>{escape(guide.summary)}</p>
          </article>
          <article class="page-panel">
            <p class="kicker">Direct answer</p>
            <h2>What changes</h2>
            <p>{escape(guide.answer)}</p>
          </article>
        </div>
      </section>
      <section class="section">
        <div class="section-heading"><p class="kicker">Example</p><h2>Before and after</h2></div>
        <div class="grid two">
          <article class="page-panel"><h3>Before</h3>{code_block(guide.before_code)}</article>
          <article class="page-panel"><h3>After</h3>{code_block(guide.after_code)}</article>
        </div>
      </section>
      <section class="section">
        <div class="grid three">
          <article class="page-panel"><h3>Typical symptoms</h3><ul class="clean">{''.join(f'<li>{escape(item)}</li>' for item in guide.symptoms)}</ul></article>
          <article class="page-panel"><h3>What the product covers</h3><ul class="clean">{''.join(f'<li>{escape(item)}</li>' for item in guide.covers)}</ul></article>
          <article class="page-panel"><h3>Manual-review boundary</h3><ul class="clean">{''.join(f'<li>{escape(item)}</li>' for item in guide.manual_review)}</ul></article>
        </div>
      </section>
      <section class="section">
        <div class="grid two">
          <article class="page-panel">
            <h3>Keep the migration narrow</h3>
            <p>Use the exact-problem guides as a triage layer, then decide whether the repo is inside the supported subset.</p>
            <div class="page-actions">
              <a class="button" href="{relative_href(path, f'products/{guide.product_slug}/index.html')}">Open the matching product page</a>
              <a class="button secondary" href="#" data-free-link>Run the free scan first</a>
              {proof_cta}
            </div>
          </article>
          <article class="page-panel">
            <h3>Related guides</h3>
            <div class="topic-list">{related_cards}</div>
          </article>
        </div>
      </section>
{more_fixes_html}
"""
    html = layout(
        path=path,
        title=guide.title,
        description=guide.description,
        kicker=FAMILY_TITLES[guide.family],
        heading=guide.h1,
        body=body,
        crumbs=[
            ("index.html", "Home"),
            ("guides/index.html", "Guides"),
            (f"{guide.family}/index.html", FAMILY_TITLES[guide.family]),
            (path, guide.h1),
        ],
        schemas=[],
    )
    return path, html


def render_family_hub(family: str, guides: list[GuidePage]) -> tuple[str, str]:
    path = f"{family}/index.html"
    product_links = "".join(
        f'<a class="button secondary" href="{relative_href(path, f"products/{product.slug}/index.html")}">Open {escape(product.name)}</a>'
        for product in PRODUCTS
        if any(guide.product_slug == product.slug for guide in guides)
    )
    cards = "".join(
        f'<a class="topic-card" href="{relative_href(path, f"{guide.family}/{guide.slug}/index.html")}">'
        f"<strong>{escape(guide.h1)}</strong><span>{escape(guide.description)}</span></a>"
        for guide in guides
    )
    body = f"""
      <section class="section">
        <div class="section-heading"><p class="kicker">Problem pages</p><h2>{escape(FAMILY_DESCRIPTIONS[family])}</h2></div>
        <div class="page-actions">{product_links}</div>
        <div class="topic-list">{cards}</div>
      </section>
"""
    html = layout(
        path=path,
        title=FAMILY_TITLES[family],
        description=FAMILY_DESCRIPTIONS[family],
        kicker="Guides",
        heading=FAMILY_TITLES[family],
        body=body,
        crumbs=[("index.html", "Home"), ("guides/index.html", "Guides"), (path, FAMILY_TITLES[family])],
        schemas=[],
    )
    return path, html


def render_guides_hub(grouped: dict[str, list[GuidePage]]) -> tuple[str, str]:
    path = "guides/index.html"
    cards = "".join(
        f'<a class="topic-card" href="{relative_href(path, f"{family}/index.html")}">'
        f"<strong>{escape(FAMILY_TITLES[family])}</strong><span>{escape(FAMILY_DESCRIPTIONS[family])} {len(guides)} pages.</span></a>"
        for family, guides in grouped.items()
    )
    body = f"""
      <section class="section">
        <div class="section-heading"><p class="kicker">Categories</p><h2>Exact-problem entry pages built for discovery</h2></div>
        <div class="topic-list">{cards}</div>
      </section>
"""
    html = layout(
        path=path,
        title="Migration Guides",
        description="Exact-problem migration guides for SQLAlchemy, Pydantic, and ESLint upgrade pain queries.",
        kicker="Guides",
        heading="Exact-problem migration guides",
        body=body,
        crumbs=[("index.html", "Home"), (path, "Guides")],
        schemas=[],
    )
    return path, html


def render_product(product: ProductPage) -> tuple[str, str]:
    path = f"products/{product.slug}/index.html"
    proof_link = ""
    if product.slug == "sa20-pack":
        proof_link = (
            f'<a class="button secondary" href="{relative_href(path, "proof/sqlalchemy-public-proof/index.html")}">'
            "Read public proof</a>"
        )
    guides = [guide for guide in GUIDES if guide.slug in product.guide_slugs]
    guide_cards = "".join(
        f'<a class="topic-card" href="{relative_href(path, f"{guide.family}/{guide.slug}/index.html")}">'
        f"<strong>{escape(guide.h1)}</strong><span>{escape(guide.description)}</span></a>"
        for guide in guides
    )
    docs_links = "".join(
        f'<a class="button secondary" href="#" data-doc-path="{escape(doc_path)}">{escape(label)}</a>'
        for label, doc_path in product.docs
    )
    checkout_link = ""
    if product.checkout_path:
        checkout_link = (
            f'<a class="button" href="{escape(product.checkout_path)}">'
            f"Buy {escape(product.name)}</a>"
            '<a class="button secondary" href="#" data-free-link>'
            "Run the free scan first</a>"
        )
    body = f"""
      <section class="section">
        <div class="grid two">
          <article class="page-panel">
            <h2>What this product is for</h2>
            <p>{escape(product.summary)}</p>
            <ul class="clean">{''.join(f'<li>{escape(item)}</li>' for item in product.who_it_is_for)}</ul>
            <div class="page-actions">{checkout_link}</div>
          </article>
          <article class="page-panel">
            <h2>Public proof and fit signals</h2>
            <ul class="clean">{''.join(f'<li>{escape(item)}</li>' for item in product.proof_points)}</ul>
            <div class="page-actions">{proof_link}</div>
          </article>
        </div>
      </section>
      <section class="section">
        <div class="grid two">
          <article class="page-panel"><h2>Exact-problem guides</h2><div class="topic-list">{guide_cards}</div></article>
          <article class="page-panel">
            <h2>Do not use this for</h2>
            <ul class="clean">{''.join(f'<li>{escape(item)}</li>' for item in product.not_for)}</ul>
            <div class="page-actions">{docs_links}</div>
          </article>
        </div>
      </section>
"""
    html = layout(
        path=path,
        title=product.name,
        description=product.description,
        kicker="Product",
        heading=f"{product.name} for {product.family}",
        body=body,
        crumbs=[("index.html", "Home"), ("products/index.html", "Products"), (path, product.name)],
        schemas=[product_schema(product, path)],
    )
    return path, html


def render_products_hub() -> tuple[str, str]:
    path = "products/index.html"
    cards = "".join(
        f'<a class="topic-card" href="{relative_href(path, f"products/{product.slug}/index.html")}">'
        f"<strong>{escape(product.name)}</strong><span>{escape(product.description)}</span></a>"
        for product in PRODUCTS
    )
    body = f"""
      <section class="section">
        <div class="section-heading"><p class="kicker">Products</p><h2>Narrow migration products with scanner-first qualification</h2></div>
        <div class="topic-list">{cards}</div>
      </section>
"""
    html = layout(
        path=path,
        title="Migration Products",
        description="Scanner-first migration products for SQLAlchemy, Pydantic, and ESLint upgrade paths.",
        kicker="Products",
        heading="Downloadable migration products",
        body=body,
        crumbs=[("index.html", "Home"), (path, "Products")],
        schemas=[],
    )
    return path, html


def render_sqlalchemy_public_proof() -> tuple[str, str]:
    path = "proof/sqlalchemy-public-proof/index.html"
    proof_rows = (
        (
            "Bogdanp/flask_dramatiq_example",
            "Query.get plus declarative import cleanup",
            "supported and validated on copied public input",
            "https://github.com/Bogdanp/flask_dramatiq_example/blob/a2f2c2baf7bdd7e1044ec6d241556f6333a6e397/app.py",
        ),
        (
            "dunossauro/live-de-python",
            "select([table]) list syntax cleanup",
            "supported and validated on copied public input",
            "https://github.com/dunossauro/live-de-python/blob/c0c83d3cb1271b0e55de2f83ad3a2aa4a57b53a8/codigo/Live011/core_select.py",
        ),
        (
            "nylas/sync-engine",
            "Query.get plus string loader cleanup",
            "supported and validated on copied public input",
            "https://github.com/nylas/sync-engine/blob/b91b94b9a0033be4199006eb234d270779a04443/inbox/transactions/search.py",
        ),
    )
    blocked_rows = (
        (
            "nylas/sync-engine",
            "engine.execute(...)",
            "manual_review_required",
            "https://github.com/nylas/sync-engine/blob/b91b94b9a0033be4199006eb234d270779a04443/inbox/ignition.py",
        ),
        (
            "teamclairvoyant/airflow-maintenance-dags",
            "Query.from_self()",
            "manual_review_required",
            "https://github.com/teamclairvoyant/airflow-maintenance-dags/blob/fe592a5cb90508804b589652ef7fedc624bff595/db-cleanup/airflow-db-cleanup.py",
        ),
    )
    proof_cards = "".join(
        '<article class="page-panel">'
        f'<h3><a href="{escape(source_url)}">{escape(repo)}</a></h3>'
        f"<p>{escape(pattern)}</p>"
        f'<p class="caption">{escape(result)}</p>'
        "</article>"
        for repo, pattern, result, source_url in proof_rows
    )
    blocked_cards = "".join(
        '<article class="page-panel">'
        f'<h3><a href="{escape(source_url)}">{escape(repo)}</a></h3>'
        f"<p>{escape(pattern)}</p>"
        f'<p class="caption">{escape(result)}</p>'
        "</article>"
        for repo, pattern, result, source_url in blocked_rows
    )
    body = f"""
      <section class="section">
        <div class="grid three">
          <article class="page-panel">
            <h2>3 supported public-file passes</h2>
            <p>Copied public inputs landed inside the documented SQLAlchemy automation subset.</p>
          </article>
          <article class="page-panel">
            <h2>2 blocked manual-review cases</h2>
            <p>Risky execution and query-shape patterns were reported instead of guessed through.</p>
          </article>
          <article class="page-panel">
            <h2>0 broad migration promises</h2>
            <p>The proof covers the narrow legacy query and syntax subset, not every SQLAlchemy 2.0 change.</p>
          </article>
        </div>
      </section>
      <section class="section">
        <div class="section-heading"><p class="kicker">Supported examples</p><h2>Public files that matched the automation subset</h2></div>
        <div class="grid three">{proof_cards}</div>
      </section>
      <section class="section">
        <div class="section-heading"><p class="kicker">Fail-closed examples</p><h2>Public files that stayed in manual review</h2></div>
        <div class="grid two">{blocked_cards}</div>
      </section>
      <section class="section">
        <div class="grid two">
          <article class="page-panel">
            <h2>What this proves</h2>
            <ul class="clean">
              <li>Direct Query.get, select list, declarative import, and simple loader cleanup can be classified on real public input.</li>
              <li>Unsafe execution and query-shape patterns stay visible as manual-review findings.</li>
              <li>The free scanner is the qualification step before any paid apply pack.</li>
            </ul>
          </article>
          <article class="page-panel">
            <h2>What it does not prove</h2>
            <ul class="clean">
              <li>Full engine.execute(...) automation.</li>
              <li>Full Query API migration to select().</li>
              <li>Package, test, or database integration success for every repo with one supported snippet.</li>
            </ul>
            <div class="page-actions">
              <a class="button" href="{relative_href(path, "products/sa20-pack/index.html")}">Open sa20-pack</a>
              <a class="button secondary" href="#" data-free-link>Run the free scan first</a>
            </div>
          </article>
        </div>
      </section>
"""
    html = layout(
        path=path,
        title="SQLAlchemy public proof",
        description="Public SQLAlchemy migration proof for the supported sa20-pack subset, including validated supported files and fail-closed manual-review examples.",
        kicker="Public proof",
        heading="SQLAlchemy migration proof on public files",
        body=body,
        crumbs=[("index.html", "Home"), ("products/sa20-pack/index.html", "sa20-pack"), (path, "Public proof")],
        schemas=[],
    )
    return path, html


def write_sitemap(output_dir: Path, filename: str, urls: Iterable[str], lastmod: str) -> None:
    items = "".join(f"<url><loc>{escape(url)}</loc><lastmod>{lastmod}</lastmod></url>" for url in urls)
    xml = '<?xml version="1.0" encoding="UTF-8"?>' + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + items + "</urlset>"
    (output_dir / filename).write_text(xml, encoding="utf-8")


def write_sitemap_index(output_dir: Path, filenames: Iterable[str], lastmod: str) -> None:
    items = "".join(
        f"<sitemap><loc>{SITE_URL}/{name}</loc><lastmod>{lastmod}</lastmod></sitemap>"
        for name in filenames
    )
    xml = '<?xml version="1.0" encoding="UTF-8"?>' + '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + items + "</sitemapindex>"
    (output_dir / "sitemap.xml").write_text(xml, encoding="utf-8")


def clean_page_redirects(page_paths: Iterable[str]) -> list[tuple[str, str, int]]:
    redirects: list[tuple[str, str, int]] = []
    seen: set[tuple[str, str, int]] = set()
    for path in page_paths:
        if not is_page_path(path):
            continue
        source = f"/{path.strip('/')}"
        target = public_path(path)
        if source == target:
            continue
        item = (source, target, 301)
        if item not in seen:
            seen.add(item)
            redirects.append(item)
    return sorted(redirects)


def write_redirects(output_dir: Path, redirects: Iterable[tuple[str, str, int]]) -> None:
    lines = [f"{source} {target} {status}" for source, target, status in redirects]
    (output_dir / "_redirects").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_site(output_dir: Path) -> dict[str, object]:
    grouped: dict[str, list[GuidePage]] = defaultdict(list)
    for guide in GUIDES:
        grouped[guide.family].append(guide)

    proof_pages = [render_sqlalchemy_public_proof()]
    pages = [
        render_guides_hub(grouped),
        render_products_hub(),
        *[render_family_hub(family, guides) for family, guides in grouped.items()],
        *[render_guide(guide) for guide in GUIDES],
        *[render_product(product) for product in PRODUCTS],
        *proof_pages,
    ]
    for rel_path, html in pages:
        path = output_dir / PurePosixPath(rel_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(clean_generated_text(html), encoding="utf-8")

    lastmod = date.today().isoformat()
    proof_urls = [canonical_url(path) for path, _html in proof_pages]
    static_urls = [canonical_url(path) for path, _label in INDEXABLE_STATIC_PAGES] + proof_urls
    hub_urls = [canonical_url("guides/index.html"), canonical_url("products/index.html"), *[canonical_url(f"{family}/index.html") for family in grouped]]
    guide_urls = [canonical_url(f"{guide.family}/{guide.slug}/index.html") for guide in GUIDES]
    product_urls = [canonical_url(f"products/{product.slug}/index.html") for product in PRODUCTS]

    write_sitemap(output_dir, "sitemap-pages.xml", static_urls, lastmod)
    write_sitemap(output_dir, "sitemap-hubs.xml", hub_urls, lastmod)
    write_sitemap(output_dir, "sitemap-problem-pages.xml", guide_urls, lastmod)
    write_sitemap(output_dir, "sitemap-products.xml", product_urls, lastmod)
    write_sitemap_index(output_dir, ("sitemap-pages.xml", "sitemap-hubs.xml", "sitemap-problem-pages.xml", "sitemap-products.xml"), lastmod)

    (output_dir / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n",
        encoding="utf-8",
    )
    (output_dir / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")
    page_paths = [
        "index.html",
        *STATIC_PAGE_PATHS,
        *(path for path, _label in INDEXABLE_STATIC_PAGES if path),
        *(path for path, _html in pages),
    ]
    all_redirects = [*REDIRECTS, *clean_page_redirects(page_paths)]
    write_redirects(output_dir, all_redirects)

    manifest = {
        "site_url": SITE_URL,
        "indexnow_key": INDEXNOW_KEY,
        "indexnow_key_location": canonical_url(f"{INDEXNOW_KEY}.txt"),
        "redirects": [
            {"source": source, "target": target, "status": status}
            for source, target, status in all_redirects
        ],
        "generated_on": lastmod,
        "urls": {
            "static": static_urls,
            "hubs": hub_urls,
            "guides": guide_urls,
            "products": product_urls,
            "proof": proof_urls,
        },
        "products": [asdict(product) for product in PRODUCTS],
        "guides": [asdict(guide) for guide in GUIDES],
    }
    (output_dir / "_site_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Build static discovery pages for the site.")
    parser.add_argument("--output-dir", default="site", help="Directory to write generated pages into.")
    args = parser.parse_args()
    build_site(Path(args.output_dir))


if __name__ == "__main__":
    main()
