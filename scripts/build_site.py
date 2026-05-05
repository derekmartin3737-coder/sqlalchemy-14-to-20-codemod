from __future__ import annotations

import argparse
import json
import posixpath
import sys
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from datetime import date
from html import escape
from pathlib import Path, PurePosixPath
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.site_catalog import (
    CHECKOUT_LANGUAGE,
    DELIVERY_LANGUAGE,
    FAMILY_DESCRIPTIONS,
    FAMILY_TITLES,
    FIT_REPORT_CTA,
    FIT_REPORT_LABEL,
    FIT_REPORT_PRICE,
    FIT_REPORT_PRODUCT_SLUGS,
    FIT_REPORT_ROUTE,
    GUIDES,
    INDEXNOW_KEY,
    FLATCONFIG_INSTALL_URL,
    LOCAL_NO_UPLOAD_LANGUAGE,
    PRODUCTS,
    PROOF_ONLY_CHECKOUT_NOTE,
    PYDANTIC_INSTALL_URL,
    REFUND_LANGUAGE,
    REPO_URL,
    SA20_INSTALL_URL,
    SA20_PRESET_CHECKOUT_PATH,
    SA20_PRESET_NAME,
    SA20_PRESET_PRICE,
    SECURE_CHECKOUT_NOTE,
    SITE_NAME,
    SITE_URL,
    STATUS_AVAILABLE,
    STATUS_NOT_PURCHASABLE,
    STATUS_PROOF_ONLY,
    SUPPORT_EMAIL,
    GuidePage,
    ProductPage,
)

# ruff: noqa: E501

INDEXABLE_STATIC_PAGES = (
    ("", "Home"),
    ("scan.html", "Scan"),
    ("pricing.html", "Pricing"),
    ("demo.html", "Demo"),
    ("guides/index.html", "Guides"),
    ("products/index.html", "Products"),
)

STATIC_PAGE_PATHS = (
    "scan.html",
    "pricing.html",
    "demo.html",
    "policies.html",
    "success.html",
    "cancel.html",
    "404.html",
)

FREE_SCAN_URL = (
    f"{REPO_URL}/blob/main/docs/quickstart.md"
    "?utm_source=zippertools&utm_medium=site&utm_campaign=free_scan&utm_content=quickstart"
)
PYDANTIC_FREE_SCAN_URL = (
    f"{REPO_URL}/blob/main/products/pydantic-v2-porter/README.md"
    "?utm_source=zippertools&utm_medium=site&utm_campaign=free_scan&utm_content=pydantic-v2-porter"
)
FLATCONFIG_FREE_SCAN_URL = (
    f"{REPO_URL}/blob/main/products/flatconfig-lift/README.md"
    "?utm_source=zippertools&utm_medium=site&utm_campaign=free_scan&utm_content=flatconfig-lift"
)
RELEASE_URL = (
    f"{REPO_URL}/releases/tag/v0.1.0"
    "?utm_source=zippertools&utm_medium=site&utm_campaign=trust&utm_content=v0.1.0"
)

PRICING_SECTION_IDS = {
    "sa20-pack": "sa20-pack",
    "sa20-preset": "sa20-preset",
    "pydantic-v2-porter": "pydantic-v2-porter",
}

FIT_REPORT_ADDON_LANGUAGE = (
    f"{FIT_REPORT_PRICE} {FIT_REPORT_LABEL} add-on is the lower-friction step "
    "when SQLAlchemy or Pydantic scan output is ambiguous."
)

REDIRECTS = (
    ("/favicon.ico", "/favicon.svg", 301),
    ("/go/free-scan", FREE_SCAN_URL, 302),
    ("/go/pydantic-free-scan", PYDANTIC_FREE_SCAN_URL, 302),
    ("/go/flatconfig-free-scan", FLATCONFIG_FREE_SCAN_URL, 302),
    ("/go/github-release", RELEASE_URL, 302),
    # Paid checkout /go routes are owned by worker/index.mjs so they fail closed
    # instead of silently redirecting to pricing when the Worker is absent.
    ("/sqlalchemy-2-migration-scan", "/scan", 301),
    ("/sqlalchemy-2-migration-scan.html", "/scan", 301),
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
    (
        "/sqlalchemy-joinedload-string-migration",
        "/sqlalchemy/string-loader-options/",
        301,
    ),
    (
        "/sqlalchemy-joinedload-string-migration.html",
        "/sqlalchemy/string-loader-options/",
        301,
    ),
    ("/sqlalchemy-query-get-migration", "/sqlalchemy/session-query-get/", 301),
    ("/sqlalchemy-query-get-migration.html", "/sqlalchemy/session-query-get/", 301),
    (
        "/sqlalchemy-declarative-import-migration",
        "/sqlalchemy/declarative-imports/",
        301,
    ),
    (
        "/sqlalchemy-declarative-import-migration.html",
        "/sqlalchemy/declarative-imports/",
        301,
    ),
    ("/sqlalchemy-insert-values-migration", "/sqlalchemy/insert-values-kwargs/", 301),
    (
        "/sqlalchemy-insert-values-migration.html",
        "/sqlalchemy/insert-values-kwargs/",
        301,
    ),
    (
        "/sqlalchemy-joinedload-all-migration",
        "/sqlalchemy/joinedload-all-removed/",
        301,
    ),
    (
        "/sqlalchemy-joinedload-all-migration.html",
        "/sqlalchemy/joinedload-all-removed/",
        301,
    ),
    (
        "/sqlalchemy-session-query-migration",
        "/sqlalchemy/session-query-migration/",
        301,
    ),
    (
        "/sqlalchemy-session-query-migration.html",
        "/sqlalchemy/session-query-migration/",
        301,
    ),
    ("/sqlalchemy-engine-execute-removed", "/sqlalchemy/engine-execute-removed/", 301),
    (
        "/sqlalchemy-engine-execute-removed.html",
        "/sqlalchemy/engine-execute-removed/",
        301,
    ),
    ("/pydantic-v2-migration-pack", "/products/pydantic-v2-porter/", 301),
    ("/pydantic-v2-migration-pack.html", "/products/pydantic-v2-porter/", 301),
    (
        "/pydantic-validator-v2-migration",
        "/pydantic/validator-to-field-validator/",
        301,
    ),
    (
        "/pydantic-validator-v2-migration.html",
        "/pydantic/validator-to-field-validator/",
        301,
    ),
    ("/pydantic-basesettings-migration", "/pydantic/basesettings-moved/", 301),
    ("/pydantic-basesettings-migration.html", "/pydantic/basesettings-moved/", 301),
    ("/pydantic-root-validator-pre-migration", "/pydantic/root-validator-pre/", 301),
    (
        "/pydantic-root-validator-pre-migration.html",
        "/pydantic/root-validator-pre/",
        301,
    ),
    (
        "/optionengine-object-has-no-attribute-execute",
        "/sqlalchemy/optionengine-execute-error/",
        301,
    ),
    (
        "/optionengine-object-has-no-attribute-execute.html",
        "/sqlalchemy/optionengine-execute-error/",
        301,
    ),
    (
        "/sqlalchemy-optionengine-object-has-no-attribute-execute",
        "/sqlalchemy/optionengine-execute-error/",
        301,
    ),
    (
        "/attributeerror-optionengine-object-has-no-attribute-execute",
        "/sqlalchemy/optionengine-execute-error/",
        301,
    ),
    (
        "/engine-object-has-no-attribute-execute",
        "/sqlalchemy/engine-attribute-error-execute/",
        301,
    ),
    (
        "/engine-object-has-no-attribute-execute.html",
        "/sqlalchemy/engine-attribute-error-execute/",
        301,
    ),
    (
        "/sqlalchemy-engine-object-has-no-attribute-execute",
        "/sqlalchemy/engine-attribute-error-execute/",
        301,
    ),
    ("/legacyapiwarning-query-get", "/sqlalchemy/legacyapiwarning-query-get/", 301),
    (
        "/legacyapiwarning-query-get.html",
        "/sqlalchemy/legacyapiwarning-query-get/",
        301,
    ),
    (
        "/sqlalchemy-legacyapiwarning-query-get",
        "/sqlalchemy/legacyapiwarning-query-get/",
        301,
    ),
    (
        "/sqlalchemy-select-legacy-mode-warning",
        "/sqlalchemy/select-legacy-mode-warning/",
        301,
    ),
    (
        "/sqlalchemy-select-legacy-mode-warning.html",
        "/sqlalchemy/select-legacy-mode-warning/",
        301,
    ),
    ("/joinedload-all-is-not-defined", "/sqlalchemy/joinedload-all-nameerror/", 301),
    (
        "/joinedload-all-is-not-defined.html",
        "/sqlalchemy/joinedload-all-nameerror/",
        301,
    ),
    (
        "/sqlalchemy-2-migration-checklist",
        "/sqlalchemy/sqlalchemy-20-triage-checklist/",
        301,
    ),
    (
        "/sqlalchemy-2-migration-checklist.html",
        "/sqlalchemy/sqlalchemy-20-triage-checklist/",
        301,
    ),
    ("/sqlalchemy-2-codemod", "/sqlalchemy/sqlalchemy-manual-vs-codemod/", 301),
    ("/sqlalchemy-2-codemod.html", "/sqlalchemy/sqlalchemy-manual-vs-codemod/", 301),
    (
        "/basesettings-import-error-pydantic-v2",
        "/pydantic/basesettings-import-error/",
        301,
    ),
    (
        "/basesettings-import-error-pydantic-v2.html",
        "/pydantic/basesettings-import-error/",
        301,
    ),
    ("/pydantic-validator-deprecated", "/pydantic/validator-deprecation-warning/", 301),
    (
        "/pydantic-validator-deprecated.html",
        "/pydantic/validator-deprecation-warning/",
        301,
    ),
    (
        "/pydantic-class-config-deprecated",
        "/pydantic/config-class-deprecated-warning/",
        301,
    ),
    (
        "/pydantic-class-config-deprecated.html",
        "/pydantic/config-class-deprecated-warning/",
        301,
    ),
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
        f'<a href="{relative_href(path, "scan.html")}">Scan</a>'
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
        f'<a href="{relative_href(path, "scan.html")}">Scan</a>'
        f'<a href="{relative_href(path, "guides/index.html")}">Guides</a>'
        f'<a href="{relative_href(path, "products/index.html")}">Products</a>'
        f'<a href="{relative_href(path, "pricing.html")}">Pricing</a>'
        f'<a href="{relative_href(path, "demo.html")}">Demo</a>'
        f'<a href="{relative_href(path, "policies.html")}">Policies</a>'
        '<a href="#" data-repo-link>Repo</a>'
        f'<a href="mailto:{SUPPORT_EMAIL}" data-contact-link>Contact</a>'
        "</div>"
        f'<p class="caption footer-note">Support: '
        f'<a href="mailto:{SUPPORT_EMAIL}" data-contact-link>'
        f'<span data-contact-email>{SUPPORT_EMAIL}</span></a></p>'
        "</div></footer>"
    )


def breadcrumb_html(path: str, crumbs: list[tuple[str, str]]) -> str:
    items: list[str] = []
    for href, label in crumbs[:-1]:
        items.append(
            f'<li><a href="{relative_href(path, href)}">{escape(label)}</a></li>'
        )
    items.append(f'<li aria-current="page">{escape(crumbs[-1][1])}</li>')
    return (
        '<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>'
        + "".join(items)
        + "</ol></nav>"
    )


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


def software_application_schema(product: ProductPage, path: str) -> dict[str, object]:
    schema: dict[str, object] = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": product.name,
        "applicationCategory": "DeveloperApplication",
        "operatingSystem": "Windows, macOS, Linux",
        "description": product.description,
        "url": canonical_url(path),
    }
    if product.price:
        schema["offers"] = {
            "@type": "Offer",
            "price": product.price,
            "priceCurrency": product.currency,
            "availability": f"https://schema.org/{product.availability}",
            "url": canonical_url(path),
        }
    return schema


def faq_schema(items: tuple[tuple[str, str], ...]) -> dict[str, object]:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": answer,
                },
            }
            for question, answer in items
        ],
    }


def code_block(value: str) -> str:
    return f'<pre class="code-block"><code>{escape(value)}</code></pre>'


def clean_list_html(items: Iterable[str]) -> str:
    return (
        '<ul class="clean">'
        + "".join(f"<li>{escape(item)}</li>" for item in items)
        + "</ul>"
    )


def action_list_html(actions: Iterable[str]) -> str:
    filtered = [action for action in actions if action]
    if not filtered:
        return ""
    return (
        '<ul class="action-list">'
        + "".join(f'<li>{action}<span class="sr-only">.</span></li>' for action in filtered)
        + "</ul>"
    )


def product_by_slug(slug: str) -> ProductPage | None:
    return next((product for product in PRODUCTS if product.slug == slug), None)


def tracking_source(path: str, context: str) -> str:
    normalized = path.strip("/")
    normalized = normalized.removesuffix("/index.html").removesuffix(".html")
    normalized = normalized.replace("/", "-") or "home"
    return f"{context}-{normalized}"[:120]


def tracked_go_path(path: str, source: str) -> str:
    if not path.startswith("/go/"):
        return path
    return f"{path}/{source}"


def free_scan_go_path(product: ProductPage | None, source: str) -> str:
    """Public buyer-path scan target.

    SQLAlchemy / generic free-scan CTAs route to the controlled `/scan` page
    so buyers stay on-site for the first step. Pydantic and ESLint CTAs keep
    their dedicated `/go/...` redirects to the matching public README so the
    user lands on the right scanner instead of the SQLAlchemy quickstart.
    """
    if product is not None and product.slug == "pydantic-v2-porter":
        return tracked_go_path("/go/pydantic-free-scan", source)
    if product is not None and product.slug == "flatconfig-lift":
        return tracked_go_path("/go/flatconfig-free-scan", source)
    # SQLAlchemy + generic: keep buyers on /scan instead of jumping to GitHub.
    # `?source=` keeps attribution; `/scan` itself still links out to the
    # GitHub quickstart as a secondary trust path.
    return f"/scan?source={source}" if source else "/scan"


def supports_fit_report(product: ProductPage | None) -> bool:
    return product is not None and product.slug in FIT_REPORT_PRODUCT_SLUGS


def free_scan_cta_label(product: ProductPage | None) -> str:
    if product is None:
        return "Run the free local scanner"
    if product.slug == "pydantic-v2-porter":
        return "Run the Pydantic scan first"
    if product.slug == "flatconfig-lift":
        return "Run the static-config scan"
    return "Run the SQLAlchemy scan first"


def checkout_cta_label(product: ProductPage) -> str:
    if product.slug == "pydantic-v2-porter":
        return "Buy Pydantic cleanup pack"
    return "Buy cleanup pack"


def product_price_line(product: ProductPage) -> str:
    return f"${product.price} per team" if product.price else STATUS_NOT_PURCHASABLE


def product_buy_cta(product: ProductPage) -> str:
    return f"{checkout_cta_label(product)} - ${product.price}"


def product_page_path(product: ProductPage) -> str:
    return f"products/{product.slug}/index.html"


def product_proof_path(product: ProductPage) -> str:
    if product.slug == "sa20-pack":
        return "proof/sqlalchemy-public-proof/index.html"
    return f"proof/{product.slug}/index.html"


def pricing_section_href(path: str, product: ProductPage) -> str | None:
    anchor = PRICING_SECTION_IDS.get(product.slug)
    if anchor is None:
        return None
    return f"{relative_href(path, 'pricing.html')}#{anchor}"


@dataclass(frozen=True)
class ProductPageTemplate:
    headline: str
    subheadline: str
    cta_heading: str
    cta_copy: str
    what_this_fixes: tuple[str, ...]
    what_you_get: tuple[str, ...]
    use_this_if: tuple[str, ...]
    do_not_use_if: tuple[str, ...]
    delivery_steps: tuple[str, ...]
    support_note: str


def product_page_template(product: ProductPage) -> ProductPageTemplate:
    if product.slug == "sa20-pack":
        return ProductPageTemplate(
            headline="Clean up repeated SQLAlchemy 1.4 to 2.0 migration edits on a local branch",
            subheadline=(
                "A deterministic paid workflow for the SQLAlchemy cleanup that is repetitive, review-heavy, and safe to stage: Query.get, select([..]), simple string relationship paths, declarative imports, and legacy DML constructor syntax."
            ),
            cta_heading="Buy the apply workflow when the scan shows repeated supported cleanup.",
            cta_copy=(
                "The pack turns the supported scan buckets into a preview/apply migration run with a report your team can review before merge."
            ),
            what_this_fixes=(
                "session.query(Model).get(pk) to Session.get(Model, pk).",
                "select([columns]) legacy list syntax to direct select(columns).",
                "Simple string joins and loader options when the root mapped class is obvious.",
                "sqlalchemy.ext.declarative imports for declarative_base and declared_attr.",
                "Direct insert/update/delete constructor kwargs moved onto statement methods.",
            ),
            what_you_get=(
                "Commercial ZIP with the paid cleanup workflow and local CLI.",
                "Preview/apply commands, diff output, and JSON migration report.",
                "Supported rewrite table plus manual-review findings for unsupported SQLAlchemy patterns.",
                "Rollback checklist, manager summary, license/support terms, and buyer terms.",
            ),
            use_this_if=(
                "The free scan finds repeated supported SQLAlchemy cleanup across enough files to matter.",
                "You want a branch-local migration run with reviewable diffs and a structured report.",
                "Your team can run typecheck, tests, or build after the migration before merging.",
            ),
            do_not_use_if=product.not_for,
            delivery_steps=(
                CHECKOUT_LANGUAGE,
                DELIVERY_LANGUAGE,
                LOCAL_NO_UPLOAD_LANGUAGE,
                "Run the pack on a branch, inspect the diff/report, then use your normal validation commands before merge.",
            ),
            support_note=(
                f"{REFUND_LANGUAGE} Support is by email; include the scanner report and checkout email so the issue can be matched to the published scope."
            ),
        )
    if product.slug == "pydantic-v2-porter":
        return ProductPageTemplate(
            headline="Move repetitive Pydantic v1 to v2 cleanup out of code review",
            subheadline=(
                "A deterministic paid workflow for direct imports, BaseSettings moves, simple validators, safe Config blocks, validate_arguments, and pre root validators in the documented Pydantic v2 subset."
            ),
            cta_heading="Buy the cleanup pack when direct v1 patterns are slowing the upgrade.",
            cta_copy=(
                f"The pack handles the mechanical Pydantic v2 edits locally and leaves alias-heavy or signature-heavy cases in manual review. The free scan link on this page opens the Pydantic scanner, not the SQLAlchemy scanner. The {FIT_REPORT_PRICE} {FIT_REPORT_LABEL} add-on covers SQLAlchemy and Pydantic scan output."
            ),
            what_this_fixes=(
                "Direct pydantic and pydantic.v1 imports when the imported symbols stay in the supported v2 subset.",
                "BaseSettings imports moved to pydantic-settings.",
                "Simple @validator decorators converted to @field_validator with classmethod handling.",
                "Supported class Config keys converted to model_config / ConfigDict with v2 key names.",
                "validate_arguments and root_validator(pre=True) cases in the safe subset.",
            ),
            what_you_get=(
                "Commercial ZIP with the paid Pydantic cleanup workflow and local CLI.",
                "Preview/apply commands for supported import, settings, validator, root-validator, and config rewrites.",
                "Supported rewrite table plus manual-review findings for alias-heavy imports, removed config keys, and signature-heavy validators.",
                "Demo report, public proof, rollback checklist, manager summary, and license/support terms.",
            ),
            use_this_if=(
                "The repo has repeated direct pydantic imports, BaseSettings usage, simple validators, or safe Config blocks.",
                "The migration pain is repetitive v1-to-v2 cleanup, not a custom semantic rewrite.",
                "Your team accepts explicit manual-review findings for validators that depend on values, field, config, each_item, or always.",
            ),
            do_not_use_if=product.not_for,
            delivery_steps=(
                CHECKOUT_LANGUAGE,
                DELIVERY_LANGUAGE,
                LOCAL_NO_UPLOAD_LANGUAGE,
                "Run the pack on a branch, inspect the diff/report, then use your normal validation commands before merge.",
            ),
            support_note=(
                f"{REFUND_LANGUAGE} Support is by email; include the scanner report and checkout email so the issue can be matched to the published scope."
            ),
        )
    return ProductPageTemplate(
        headline="Turn static legacy ESLint config into a flat-config starting point",
        subheadline=(
            "A proof-first workflow for the narrow static-config subset: .eslintrc JSON/YAML, package.json eslintConfig, and simple ignore migration. Dynamic JS config logic stays out of the automatic path."
        ),
        cta_heading="Use the proof page to qualify static-config fit before this is listed.",
        cta_copy=(
            "The public package identifies whether a repo belongs in the deterministic static-config subset; checkout is not listed for this product yet."
        ),
        what_this_fixes=(
            "Static .eslintrc JSON or YAML config discovery.",
            "package.json eslintConfig discovery for repos that have not moved to flat config.",
            "Simple ignore-pattern migration candidates.",
            "Manual-review findings for JS config logic, multiple config sources, existing flat config, and negated ignores.",
        ),
        what_you_get=(
            "Public scanner and proof page for static legacy ESLint config fit.",
            "Commercial-case notes for the FlatCompat bridge subset.",
            "Planned commercial deliverable: generated eslint.config.cjs and dependency guidance for supported static configs.",
            "Fail-closed reporting when the repo does not fit the static subset.",
        ),
        use_this_if=(
            "Your repo still uses a static .eslintrc JSON/YAML file or package.json eslintConfig.",
            "You want the first flat-config bridge pass before hand-tuning plugin behavior.",
            "You are comfortable treating JS-backed config and plugin-specific behavior as manual review.",
        ),
        do_not_use_if=product.not_for,
        delivery_steps=(
            "Use the public README and proof page today; no checkout is listed for this product.",
            "Run the scanner locally to decide whether the repo is in the static-config subset.",
            "When listed, delivery should follow the same local ZIP workflow as the paid cleanup packs.",
        ),
        support_note=(
            "No purchase is available from this page yet, so there is no paid refund path. Use the proof, README, and contact link for fit questions."
        ),
    )


def product_purchase_details(product: ProductPage) -> dict[str, tuple[str, ...]]:
    if product.slug == "sa20-pack":
        return {
            "buy_if": (
                "The free scan shows repeated Query.get, select([..]), string join, string loader, declarative import, or DML constructor findings.",
                "The remaining supported cleanup is still expensive enough to justify a controlled local migration workflow.",
                "The team can run the migration on a branch and validate locally before merge.",
            ),
            "includes": (
                "Installable local CLI workflow, not a hosted black box.",
                "Preview/apply modes, diff output, and JSON migration report.",
                "Coverage notes, rollback checklist, manager summary, and buyer terms.",
            ),
            "reassurance": (
                CHECKOUT_LANGUAGE,
                DELIVERY_LANGUAGE,
                LOCAL_NO_UPLOAD_LANGUAGE,
                FIT_REPORT_ADDON_LANGUAGE,
                REFUND_LANGUAGE,
            ),
        }
    if product.slug == "pydantic-v2-porter":
        return {
            "buy_if": (
                "The repo has direct pydantic or pydantic.v1 imports, BaseSettings usage, safe Config blocks, or simple validators.",
                "The migration pain is repetitive v1-to-v2 cleanup, not a custom semantic rewrite.",
                "The team accepts manual-review findings for alias-heavy imports and signature-heavy validators.",
            ),
            "includes": (
                "Installable local CLI workflow, not a hosted black box.",
                "Supported validator, settings, import, and config rewrites.",
                "Demo report, public proof, coverage notes, rollback checklist, and buyer terms.",
            ),
            "reassurance": (
                CHECKOUT_LANGUAGE,
                DELIVERY_LANGUAGE,
                LOCAL_NO_UPLOAD_LANGUAGE,
                FIT_REPORT_ADDON_LANGUAGE,
                REFUND_LANGUAGE,
            ),
        }
    return {
        "buy_if": product.who_it_is_for,
        "includes": product.proof_points,
        "reassurance": (
            "Use proof and docs before treating this as a purchase candidate.",
        ),
    }


def render_purchase_panel(product: ProductPage, path: str, *, context: str) -> str:
    if not product.checkout_path or not product.price:
        return ""

    details = product_purchase_details(product)
    source = tracking_source(path, context)
    checkout_path = tracked_go_path(product.checkout_path, source)
    free_scan_path = free_scan_go_path(product, source)
    fit_report_action = (
        f'<a class="button secondary" href="{tracked_go_path(FIT_REPORT_ROUTE, source)}">{FIT_REPORT_CTA}</a>'
        if supports_fit_report(product)
        else ""
    )
    product_href = relative_href(path, product_page_path(product))
    proof_href = relative_href(path, product_proof_path(product))
    proof_action = f'<a class="button secondary" href="{proof_href}">Read proof</a>'
    pricing_href = pricing_section_href(path, product)
    pricing_action = (
        f'<a class="button secondary" href="{pricing_href}">See pricing</a>'
        if pricing_href
        else ""
    )

    heading = "Choose the lowest-risk next step."
    intro = (
        "Buy only after your local report shows repeated supported findings and a validation path the team can review."
        if context == "product"
        else "One matching page is not enough by itself. Run the local scan, then use the matching fit report add-on where listed or buy only when the same supported pattern appears often enough to matter."
    )
    if context != "product":
        primary_action = f'<a class="button" href="{free_scan_path}">{escape(free_scan_cta_label(product))}</a>'
        secondary_actions = (
            f'<a class="button secondary" href="{product_href}">Open product fit and price</a>',
            fit_report_action,
            proof_action,
            pricing_action,
            f'<a class="button secondary" href="{escape(checkout_path)}">{escape(checkout_cta_label(product))}</a>',
        )
    else:
        primary_action = (
            fit_report_action.replace('class="button secondary"', 'class="button"', 1)
            if fit_report_action
            else f'<a class="button" href="{escape(checkout_path)}">Buy {escape(product.name)} - ${escape(product.price)}</a>'
        )
        secondary_actions = (
            f'<a class="button secondary" href="{escape(checkout_path)}">Buy {escape(product.name)} - ${escape(product.price)}</a>',
            proof_action,
            pricing_action,
        )
    secondary_actions_html = action_list_html(secondary_actions)

    return f"""      <section class="section">
        <article class="page-panel purchase-panel">
          <p class="kicker">Purchase fit</p>
          <h2>{escape(heading)}</h2>
          <p>{escape(intro)}</p>
          <div class="purchase-columns">
            <div>
              <h3>Buy if</h3>
              <ul class="clean">{"".join(f"<li>{escape(item)}</li>" for item in details["buy_if"])}</ul>
            </div>
            <div>
              <h3>What the workflow includes</h3>
              <ul class="clean">{"".join(f"<li>{escape(item)}</li>" for item in details["includes"])}</ul>
            </div>
            <div>
              <h3>Before checkout</h3>
              <ul class="clean">{"".join(f"<li>{escape(item)}</li>" for item in details["reassurance"])}</ul>
            </div>
          </div>
          <div class="page-actions purchase-actions">
            <div class="primary-cta">{primary_action}</div>
            <div class="secondary-cta-group">
              <p class="caption cta-group-label">Secondary options</p>
              {secondary_actions_html}
            </div>
          </div>
        </article>
      </section>"""


def guide_faq_items(
    guide: GuidePage,
    product: ProductPage | None,
) -> tuple[tuple[str, str], ...]:
    product_name = (
        product.name if product is not None else "the matching migration pack"
    )
    automation_answer = (
        "Automate only the supported subset: "
        + " ".join(guide.covers)
        + " Keep these cases in manual review: "
        + " ".join(guide.manual_review)
    )
    if supports_fit_report(product):
        buy_answer = (
            f"Use {product_name} only when this pattern repeats across enough files that manual cleanup is still costly. "
            f"Run the public scan or read the proof first. If the report shows ten or more supported findings, buy the pack or use the {FIT_REPORT_PRICE} {FIT_REPORT_LABEL} add-on; if unsupported findings dominate, keep the work manual."
        )
    else:
        buy_answer = (
            f"Use {product_name} only when this pattern repeats across enough files that manual cleanup is still costly. "
            "Run the public scan or read the proof first. The fit-report add-on is not listed for this proof-only product yet; if unsupported findings dominate, keep the work manual."
        )
    return (
        (f"What is the safest fix for {guide.search_term}?", guide.answer),
        (f"Can {guide.search_term} be automated?", automation_answer),
        (f"When should I buy {product_name}?", buy_answer),
    )


def render_faq_section(items: tuple[tuple[str, str], ...]) -> str:
    return f"""      <section class="section">
        <article class="page-panel">
          <p class="kicker">FAQ</p>
          <h2>Fast answers before you decide</h2>
          <div class="faq-list">
            {"".join(f"<div><h3>{escape(question)}</h3><p>{escape(answer)}</p></div>" for question, answer in items)}
          </div>
        </article>
      </section>"""


def render_direct_fix_section(guide: GuidePage) -> str:
    manual_boundary = " ".join(guide.manual_review[:2])
    return f"""      <section class="section">
        <article class="page-panel answer-panel">
          <p class="kicker">Start here</p>
          <div class="answer-grid">
            <div>
              <h2>The safe first move</h2>
              <p>{escape(guide.answer)}</p>
              <p class="caption">Stop before automation when: {escape(manual_boundary)}</p>
            </div>
            <div>
              <h3>Target shape</h3>
              {code_block(guide.after_code)}
            </div>
          </div>
        </article>
      </section>"""


def render_problem_scan_cta(
    guide: GuidePage,
    product: ProductPage | None,
    path: str,
) -> str:
    source = tracking_source(path, "guide-scan")
    free_scan_path = free_scan_go_path(product, source)
    product_href = (
        relative_href(path, product_page_path(product))
        if product is not None
        else relative_href(path, "products/index.html")
    )
    scan_intro = (
        f"Run the matching scanner locally first. If the report shows 10+ supported findings for this kind of cleanup, compare the paid workflow or use the {FIT_REPORT_PRICE} {FIT_REPORT_LABEL} add-on before buying the full pack."
        if supports_fit_report(product)
        else "Run the matching scanner locally first. The fit-report add-on is not listed for this proof-only product yet, so use the proof page and scanner output before treating it as a purchase candidate."
    )
    fit_report_action = (
        f'<a class="button secondary" href="{tracked_go_path(FIT_REPORT_ROUTE, source)}">{FIT_REPORT_CTA}</a>'
        if supports_fit_report(product)
        else ""
    )
    report_preview = (
        "Example scan summary\n"
        "supported_findings: 38\n"
        "manual_review_findings: 6\n"
        "files_uploaded: 0\n"
        "confidence: reviewable"
    )
    return f"""      <section class="section">
        <article class="conversion-panel">
          <div class="conversion-copy">
            <p class="kicker">Repo fit check</p>
            <h2>Want to know if your repo has this pattern?</h2>
            <p>{escape(scan_intro)}</p>
            <ul class="clean decision-list">
              <li>Local scan; no repository upload.</li>
              <li>Supported findings are separated from manual-review findings.</li>
              <li>Buy only when the repeated pattern is worth automating.</li>
            </ul>
          </div>
          <div class="conversion-actions">
            <a class="button" href="{free_scan_path}">{escape(free_scan_cta_label(product))}</a>
            <a class="button secondary" href="{relative_href(path, "demo.html")}">View example report</a>
            {fit_report_action}
            <a class="button secondary" href="{product_href}">See when to buy</a>
            {code_block(report_preview)}
          </div>
        </article>
      </section>"""


def render_evaluation_path_section(
    guide: GuidePage,
    product: ProductPage | None,
    path: str,
) -> str:
    if product is None:
        return ""

    details = product_purchase_details(product)
    product_href = relative_href(path, product_page_path(product))
    proof_href = relative_href(path, product_proof_path(product))
    pricing_href = pricing_section_href(path, product)
    fit_report_note = (
        f"If the scan output is ambiguous, use the {FIT_REPORT_PRICE} {FIT_REPORT_LABEL} add-on before buying the full pack."
        if supports_fit_report(product)
        else "The fit-report add-on is not listed for this proof-only product yet; use the proof page and scanner output before treating this as purchasable."
    )
    fit_report_action = (
        f'<a class="button secondary" href="{tracked_go_path(FIT_REPORT_ROUTE, tracking_source(path, "guide-fit"))}">{FIT_REPORT_CTA}</a>'
        if supports_fit_report(product)
        else ""
    )
    price_line = (
        f"Published cleanup-pack price: ${escape(product.price)} one time."
        if product.price
        else "Current listed price is not published on the pricing page yet."
    )
    extra_action = ""
    if product.slug == "sa20-pack":
        extra_action = f'<a class="button secondary" href="{relative_href(path, "demo.html")}">See demo report</a>'
    actions_html = action_list_html(
        (
            f'<a class="button" href="{product_href}">Open product page</a>',
            fit_report_action,
            f'<a class="button secondary" href="{pricing_href}">See pricing</a>'
            if pricing_href
            else "",
            f'<a class="button secondary" href="{proof_href}">Read proof</a>',
            extra_action,
        )
    )
    return f"""      <section class="section">
        <div class="grid two">
          <article class="page-panel bridge-panel">
            <p class="kicker">Decision path</p>
            <h2>If this repeats across the repo, open the evaluation pages next.</h2>
            <p>{escape(product.summary)}</p>
            <ul class="clean">
              {"".join(f"<li>{escape(item)}</li>" for item in details["buy_if"][:2])}
              <li>{escape(fit_report_note)}</li>
            </ul>
          </article>
          <article class="page-panel bridge-panel">
            <p class="kicker">Before checkout</p>
            <h2>Product fit, proof, and price should all be one click away.</h2>
            <p>{escape(price_line)}</p>
            <div class="page-actions">
              {actions_html}
            </div>
          </article>
        </div>
      </section>"""


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
            {
                "@context": "https://schema.org",
                "@type": "WebSite",
                "name": SITE_NAME,
                "url": f"{SITE_URL}/",
            },
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
    <script type="module" src="{relative_href(path, "app.js")}"></script>
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
    product = product_by_slug(guide.product_slug)
    faq_items = guide_faq_items(guide, product)
    proof_cta = ""
    qualification_cta = ""
    if guide.product_slug == "sa20-pack":
        qualification_cta = (
            f'<a class="button secondary" href="/scan?source={tracking_source(path, "guide")}">'
            "Run the free scan first</a>"
        )
        proof_cta = (
            f'<a class="button secondary" href="{relative_href(path, "proof/sqlalchemy-public-proof/index.html")}">'
            "Read public proof</a>"
        )
    narrow_actions = action_list_html(
        (
            f'<a class="button" href="{relative_href(path, f"products/{guide.product_slug}/index.html")}">Open the matching product page</a>',
            qualification_cta,
            proof_cta,
        )
    )
    # Get related guides from same family (top 3 as cards)
    related = [
        item
        for item in GUIDES
        if item.family == guide.family and item.slug != guide.slug
    ][:3]
    related_cards = "".join(
        f'<a class="topic-card" href="{relative_href(path, f"{item.family}/{item.slug}/index.html")}">'
        f"<strong>{escape(item.h1)}</strong><span>{escape(item.description)}</span></a>"
        for item in related
    )
    # Get all guides from same product for quick links
    product_guides = [
        item
        for item in GUIDES
        if item.product_slug == guide.product_slug and item.slug != guide.slug
    ]
    quick_links = ", ".join(
        f'<a href="{relative_href(path, f"{item.family}/{item.slug}/index.html")}">{escape(item.title.split(" in ")[0].split(" for ")[0])}</a>'
        for item in product_guides[:8]
    )
    more_fixes_html = ""
    if quick_links:
        product_label = product.name if product is not None else guide.product_slug
        more_fixes_html = f"""
      <section class="section">
        <article class="page-panel">
          <h3>More fixes in this product</h3>
          <p class="quick-links">{quick_links}</p>
          <p><a href="{relative_href(path, f"products/{guide.product_slug}/index.html")}">View all {escape(product_label)} guides</a></p>
        </article>
      </section>"""
    guide_purchase_html = (
        render_purchase_panel(product, path, context="guide")
        if product is not None
        else ""
    )
    extra_sections = (
        f"{render_faq_section(faq_items)}{guide_purchase_html}{more_fixes_html}"
    )
    body = f"""
{render_direct_fix_section(guide)}
{render_problem_scan_cta(guide, product, path)}
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
{render_evaluation_path_section(guide, product, path)}
      <section class="section">
        <div class="grid three">
          <article class="page-panel"><h3>Typical symptoms</h3><ul class="clean">{"".join(f"<li>{escape(item)}</li>" for item in guide.symptoms)}</ul></article>
          <article class="page-panel"><h3>What the product covers</h3><ul class="clean">{"".join(f"<li>{escape(item)}</li>" for item in guide.covers)}</ul></article>
          <article class="page-panel"><h3>Manual-review boundary</h3><ul class="clean">{"".join(f"<li>{escape(item)}</li>" for item in guide.manual_review)}</ul></article>
        </div>
      </section>
      <section class="section">
        <div class="grid two">
          <article class="page-panel">
            <h3>Keep the migration narrow</h3>
            <p>Use the exact-problem guides as a triage layer, then decide whether the repo is inside the supported subset.</p>
            <div class="page-actions">
              {narrow_actions}
            </div>
          </article>
          <article class="page-panel">
            <h3>Related guides</h3>
            <div class="topic-list">{related_cards}</div>
          </article>
        </div>
      </section>
{extra_sections}
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
        schemas=[faq_schema(faq_items)],
    )
    return path, html


def render_family_hub(family: str, guides: list[GuidePage]) -> tuple[str, str]:
    path = f"{family}/index.html"
    product_links = action_list_html(
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
        crumbs=[
            ("index.html", "Home"),
            ("guides/index.html", "Guides"),
            (path, FAMILY_TITLES[family]),
        ],
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


def render_product_workflow_section(product: ProductPage, path: str) -> str:
    command_note = ""
    if product.slug == "pydantic-v2-porter":
        command = (
            f'python -m pip install "{PYDANTIC_INSTALL_URL}"\n'
            "python -m pydantic_v2_porter.cli path/to/repo --report migration-report.json"
        )
        command_note = (
            '<p class="caption">If installation fails, retry from the GitHub '
            f"quickstart or contact support at {SUPPORT_EMAIL}.</p>"
        )
        report = (
            "Scan complete\n"
            "supported_findings: 24\n"
            "manual_review_findings: 5\n"
            "files_uploaded: 0\n"
            "next_step: review diff preview"
        )
        diff = (
            "- from pydantic import BaseSettings, validator\n"
            "+ from pydantic import field_validator\n"
            "+ from pydantic_settings import BaseSettings\n"
            "\n"
            '-     @validator("email")\n'
            '+     @field_validator("email")\n'
            "+     @classmethod"
        )
        rows = (
            ("BaseSettings imports", "rewrite"),
            ("simple @validator", "rewrite"),
            ("safe class Config keys", "rewrite"),
            ("signature-heavy validators", "manual review"),
        )
    elif product.slug == "flatconfig-lift":
        command = (
            f'python -m pip install "{FLATCONFIG_INSTALL_URL}"\n'
            "python -m flatconfig_lift.cli path/to/repo --report migration-report.json"
        )
        command_note = (
            '<p class="caption">If installation fails, retry from the GitHub '
            f"quickstart or contact support at {SUPPORT_EMAIL}.</p>"
        )
        report = (
            "Scan complete\n"
            "supported_static_configs: 1\n"
            "manual_review_findings: 2\n"
            "files_uploaded: 0\n"
            "next_step: generate FlatCompat bridge in paid pack"
        )
        diff = (
            "- .eslintrc.json\n"
            "+ eslint.config.cjs\n"
            "\n"
            '+ const { FlatCompat } = require("@eslint/eslintrc");\n'
            '+ const legacyConfig = require("./.eslintrc.json");\n'
            "+ const compat = new FlatCompat({ baseDirectory: __dirname });\n"
            "+ module.exports = [...compat.config(legacyConfig)];"
        )
        rows = (
            ("static .eslintrc JSON/YAML", "rewrite"),
            ("package.json eslintConfig", "rewrite"),
            (".eslintignore", "migrate when simple"),
            (".eslintrc.js logic", "manual review"),
        )
    else:
        command = (
            f'python -m pip install "{SA20_INSTALL_URL}"\n'
            "python -m sa20_pack.cli . --report migration-report.json"
        )
        command_note = (
            '<p class="caption">If installation fails, retry from the GitHub '
            f"quickstart or contact support at {SUPPORT_EMAIL}.</p>"
        )
        report = (
            "Scan complete\n"
            "supported_findings: 38\n"
            "manual_review_findings: 6\n"
            "files_uploaded: 0\n"
            "next_step: preview deterministic rewrites"
        )
        diff = (
            "- user = session.query(User).get(user_id)\n"
            "+ user = session.get(User, user_id)\n"
            "\n"
            "- stmt = select([User.id, User.email])\n"
            "+ stmt = select(User.id, User.email)"
        )
        rows = (
            ("Query.get primary-key lookups", "rewrite"),
            ("select([..]) list syntax", "rewrite"),
            ("simple string joins/loaders", "rewrite"),
            ("engine.execute transaction choices", "manual review"),
        )

    workflow_heading = (
        "See the migration deliverable before checkout."
        if product.checkout_path
        else "See the deliverable shape before it is listed."
    )
    workflow_caption = (
        "The value is the controlled workflow: scan, preview, apply supported rewrites, review manual findings, and validate on your branch."
        if product.checkout_path
        else "The public page is proof-first today; the commercial shape is a generated FlatCompat bridge for supported static configs."
    )
    table_rows = "".join(
        f"<tr><td>{escape(pattern)}</td><td>{escape(status)}</td></tr>"
        for pattern, status in rows
    )
    return f"""      <section class="section" id="example-workflow">
        <div class="section-heading">
          <p class="kicker">Example before/after</p>
          <h2>{escape(workflow_heading)}</h2>
        </div>
        <div class="grid two">
          <article class="page-panel">
            <h3>{"Free scan commands" if product.slug in ("sa20-pack", "pydantic-v2-porter") else "Local command"}</h3>
            {code_block(command)}
            {command_note}
            <h3>Sample report</h3>
            {code_block(report)}
          </article>
          <article class="page-panel">
            <h3>Before/after diff preview</h3>
            {code_block(diff)}
            <p class="caption">{escape(workflow_caption)}</p>
          </article>
        </div>
        <div class="table-wrap">
          <table class="table">
            <thead><tr><th>Pattern</th><th>Behavior</th></tr></thead>
            <tbody>{table_rows}</tbody>
          </table>
        </div>
      </section>"""


def render_product(product: ProductPage) -> tuple[str, str]:
    path = f"products/{product.slug}/index.html"
    template = product_page_template(product)
    product_source = tracking_source(path, "product")
    checkout_path = tracked_go_path(product.checkout_path, product_source)
    free_scan_path = free_scan_go_path(product, product_source)
    proof_href = relative_href(path, product_proof_path(product))
    proof_link = (
        f'<a class="button secondary" href="{proof_href}">Read public proof</a>'
    )
    release_button = ""
    if product.slug == "sa20-pack":
        release_button = '<a class="button secondary" href="/go/github-release">Read v0.1.0 release</a>'
    pricing_href = pricing_section_href(path, product)
    pricing_button = (
        f'<a class="button secondary" href="{pricing_href}">See pricing</a>'
        if pricing_href
        else ""
    )
    guides = [guide for guide in GUIDES if guide.slug in product.guide_slugs]
    guide_cards = "".join(
        f'<a class="topic-card" href="{relative_href(path, f"{guide.family}/{guide.slug}/index.html")}">'
        f"<strong>{escape(guide.h1)}</strong><span>{escape(guide.description)}</span></a>"
        for guide in guides
    )
    supporting_docs = tuple(
        (label, doc_path)
        for label, doc_path in product.docs
        if label != "Public proof" and not (label == "Pricing" and pricing_href)
    )
    docs_buttons = tuple(
        f'<a class="button secondary" href="#" data-doc-path="{escape(doc_path)}">{escape(label)}</a>'
        for label, doc_path in supporting_docs
    )
    docs_links = "".join(docs_buttons)
    if product.checkout_path:
        price_suffix = f" - ${escape(product.price)}" if product.price else ""
        checkout_label = checkout_cta_label(product)
        checkout_button = (
            f'<a class="button" href="{escape(checkout_path)}">'
            f"{escape(checkout_label)}{price_suffix}</a>"
        )
        free_scan_button = (
            f'<a class="button secondary" href="{free_scan_path}">'
            f"{escape(free_scan_cta_label(product))}</a>"
        )
        fit_report_button = (
            f'<a class="button secondary" href="{tracked_go_path(FIT_REPORT_ROUTE, product_source)}">'
            f"{FIT_REPORT_CTA}</a>"
            if supports_fit_report(product)
            else ""
        )
        top_primary_action = checkout_button
        top_secondary_actions = (free_scan_button, fit_report_button)
        checkout_heading = "Buy the cleanup pack"
        checkout_copy = "Use checkout when the repo matches the supported subset and the cleanup is expensive enough to justify an apply workflow."
        checkout_secondary_actions = (free_scan_button, fit_report_button)
    else:
        checkout_button = '<span class="button disabled">Checkout not listed yet</span>'
        free_scan_button = (
            f'<a class="button secondary" href="{free_scan_path}">'
            "Run the free static-config scan</a>"
        )
        fit_report_button = ""
        top_primary_action = proof_link
        top_secondary_actions = (free_scan_button, *docs_buttons)
        checkout_heading = "Checkout is not listed yet"
        checkout_copy = "Use the public proof and scanner to qualify the static-config subset before treating this as a purchase candidate."
        checkout_secondary_actions = (proof_link, free_scan_button, *docs_buttons)

    top_secondary_actions = (*top_secondary_actions, '<a class="button secondary" href="#example-workflow">View example before/after</a>')
    top_secondary_actions_html = action_list_html(top_secondary_actions)
    secondary_actions_note = (
        '<p class="caption cta-group-label">Secondary options</p>'
        if top_secondary_actions_html
        else ""
    )
    checkout_secondary_actions_html = action_list_html(checkout_secondary_actions)
    checkout_secondary_note = (
        '<p class="caption cta-group-label">Secondary options</p>'
        if checkout_secondary_actions_html
        else ""
    )

    price_line = (
        f'<p class="price-line">Published workflow price: <strong>${escape(product.price)}</strong>.</p>'
        if product.price
        else '<p class="price-line">Checkout is not listed yet.</p>'
    )
    proof_actions = action_list_html(
        (proof_link, pricing_button, release_button, *docs_buttons)
    )
    workflow_section = render_product_workflow_section(product, path)
    deliverables_heading = (
        "After purchase, you receive"
        if product.checkout_path
        else "What this proof includes"
    )

    body = f"""
      <section class="section">
        <article class="conversion-panel product-hero-panel">
          <div class="conversion-copy">
            <p class="kicker">Primary CTA</p>
            <h2>{escape(template.cta_heading)}</h2>
            <p>{escape(template.cta_copy)}</p>
            <ul class="clean decision-list">
              <li>Local workflow with no repo upload.</li>
              <li>Previewable changes and a structured report.</li>
              <li>Manual-review findings stay visible instead of hidden.</li>
            </ul>
            {price_line}
          </div>
          <div class="conversion-actions">
            <div class="primary-cta">{top_primary_action}</div>
            <div class="secondary-cta-group">
              {secondary_actions_note}
              {top_secondary_actions_html}
            </div>
            {f'<p class="small">{escape(SECURE_CHECKOUT_NOTE)}</p>' if product.checkout_path else ""}
          </div>
        </article>
      </section>
      <section class="section">
        <div class="grid two">
          <article class="page-panel">
            <h2>What this fixes</h2>
            {clean_list_html(template.what_this_fixes)}
          </article>
          <article class="page-panel deliverables-box">
            <h2>{escape(deliverables_heading)}</h2>
            {clean_list_html(template.what_you_get)}
          </article>
        </div>
      </section>
{workflow_section}
      <section class="section">
        <div class="grid two">
          <article class="page-panel use-fit-box">
            <h2>Use this if</h2>
            {clean_list_html(template.use_this_if)}
          </article>
          <article class="page-panel">
            <h2>Public proof and fit signals</h2>
            {clean_list_html(product.proof_points)}
            <div class="page-actions">{proof_actions}</div>
          </article>
        </div>
      </section>
      <section class="section">
        <article class="page-panel">
          <h2>Do not use this if</h2>
          {clean_list_html(template.do_not_use_if)}
        </article>
      </section>
      <section class="section">
        <div class="grid two">
          <article class="page-panel">
            <h2>How delivery works</h2>
            {clean_list_html(template.delivery_steps)}
          </article>
          <article class="page-panel">
            <h2>Refund/support note</h2>
            <p>{escape(template.support_note)}</p>
            <p class="caption">Support: <a href="mailto:{SUPPORT_EMAIL}" data-contact-link><span data-contact-email>{SUPPORT_EMAIL}</span></a></p>
          </article>
        </div>
      </section>
      <section class="section">
        <article class="conversion-panel checkout-panel">
          <div class="conversion-copy">
            <p class="kicker">Checkout CTA</p>
            <h2>{escape(checkout_heading)}</h2>
            <p>{escape(checkout_copy)}</p>
          </div>
          <div class="conversion-actions">
            <div class="primary-cta">{checkout_button}</div>
            <div class="secondary-cta-group">
              {checkout_secondary_note}
              {checkout_secondary_actions_html}
            </div>
            <p class="small">{escape(SECURE_CHECKOUT_NOTE if product.checkout_path else PROOF_ONLY_CHECKOUT_NOTE)}</p>
          </div>
        </article>
      </section>
      <section class="section">
        <div class="section-heading"><p class="kicker">Related fixes</p><h2>Exact-problem guides for this product</h2></div>
        <div class="topic-list">{guide_cards}</div>
      </section>
"""
    html = layout(
        path=path,
        title=product.name,
        description=template.subheadline,
        kicker="Product",
        heading=template.headline,
        body=body,
        crumbs=[
            ("index.html", "Home"),
            ("products/index.html", "Products"),
            (path, product.name),
        ],
        schemas=[
            product_schema(product, path),
            software_application_schema(product, path),
        ],
    )
    return path, html


def render_products_hub() -> tuple[str, str]:
    path = "products/index.html"
    catalog_source = tracking_source(path, "catalog-card")
    product_lookup = {product.slug: product for product in PRODUCTS}
    available_cards = (
        {
            "name": product_lookup["sa20-pack"].name,
            "status": STATUS_AVAILABLE,
            "status_class": "available",
            "outcome": "Apply repeated safe SQLAlchemy 1.4 to 2.0 cleanup patterns locally after the free scan proves fit.",
            "price": product_price_line(product_lookup["sa20-pack"]),
            "href": tracked_go_path(
                product_lookup["sa20-pack"].checkout_path, catalog_source
            ),
            "cta": product_buy_cta(product_lookup["sa20-pack"]),
            "checkout_note": SECURE_CHECKOUT_NOTE,
        },
        {
            "name": product_lookup["pydantic-v2-porter"].name,
            "status": STATUS_AVAILABLE,
            "status_class": "available",
            "outcome": "Clean up supported Pydantic v1 to v2 imports, validators, config, and BaseSettings moves.",
            "price": product_price_line(product_lookup["pydantic-v2-porter"]),
            "href": tracked_go_path(
                product_lookup["pydantic-v2-porter"].checkout_path, catalog_source
            ),
            "cta": product_buy_cta(product_lookup["pydantic-v2-porter"]),
            "checkout_note": SECURE_CHECKOUT_NOTE,
        },
        {
            "name": SA20_PRESET_NAME,
            "status": STATUS_AVAILABLE,
            "status_class": "available",
            "outcome": "Add reusable SQLAlchemy rollout presets, richer report templates, and manager-ready migration notes.",
            "price": f"${SA20_PRESET_PRICE} per team",
            "href": tracked_go_path(SA20_PRESET_CHECKOUT_PATH, catalog_source),
            "cta": f"Buy preset bundle - ${SA20_PRESET_PRICE}",
            "checkout_note": SECURE_CHECKOUT_NOTE,
        },
    )
    proof_cards = (
        {
            "name": product_lookup["flatconfig-lift"].name,
            "status": STATUS_PROOF_ONLY,
            "status_class": "proof-only",
            "outcome": "Review the static ESLint config migration proof and fit boundaries before this becomes a listed checkout product.",
            "price": product_price_line(product_lookup["flatconfig-lift"]),
            "href": relative_href(path, "proof/flatconfig-lift/index.html"),
            "cta": "Read proof page",
            "note": "Proof only - checkout not live yet.",
        },
    )
    coming_soon_cards: tuple[dict[str, str], ...] = ()

    def render_catalog_card(card: dict[str, str]) -> str:
        checkout_note = (
            f'<p class="small">{escape(card["checkout_note"])}</p>'
            if card.get("checkout_note")
            else ""
        )
        status_note = (
            f'<p class="small status-note">{escape(card["note"])}</p>'
            if card.get("note")
            else ""
        )
        return f"""
          <article class="catalog-card">
            <div class="catalog-card-top">
              <span class="status-label {escape(card["status_class"])}">{escape(card["status"])}</span>
              <span class="catalog-price">{escape(card["price"])}</span>
            </div>
            <h3>{escape(card["name"])}</h3>
            <p>{escape(card["outcome"])}</p>
            {status_note}
            <a class="button secondary" href="{escape(card["href"])}">{escape(card["cta"])}</a>
            {checkout_note}
          </article>"""

    available_html = "".join(render_catalog_card(card) for card in available_cards)
    coming_soon_html = "".join(render_catalog_card(card) for card in coming_soon_cards)
    proof_html = "".join(render_catalog_card(card) for card in proof_cards)
    coming_soon_section = (
        f"""
      <section class="section">
        <div class="section-heading"><p class="kicker">Coming soon</p><h2>Future products stay separate until checkout is ready.</h2></div>
        <div class="catalog-grid">{coming_soon_html}</div>
      </section>"""
        if coming_soon_html
        else ""
    )
    preset_deliverables = (
        '<section class="section">'
        '<article class="page-panel deliverables-box">'
        '<p class="kicker">Migration Preset Bundle</p>'
        '<h2>After purchase, you receive</h2>'
        '<ul class="clean">'
        '<li>Rollout checklist for staged SQLAlchemy 1.4-to-2.0 cleanup work.</li>'
        '<li>Manager summary template that turns scan findings into a status update.</li>'
        '<li>Migration-triage presets for common repo shapes.</li>'
        '<li>Review buckets for supported / manual / unsupported findings.</li>'
        '<li>Handoff notes for engineering teams picking up the cleanup.</li>'
        '<li>License and support terms; no human delivery dependency.</li>'
        '</ul>'
        '<h3>Sample preview</h3>'
        '<pre class="code-block"><code>Manager summary excerpt\n'
        'Supported cleanup findings: 38\n'
        'Manual-review findings: 6\n'
        'Rollout bucket: safe mechanical rewrites first\n'
        'Review buckets: supported / manual-review / unsupported\n'
        'Next step: run branch validation before merge</code></pre>'
        f'<p class="caption">Support: '
        f'<a href="mailto:{SUPPORT_EMAIL}" data-contact-link>'
        f'<span data-contact-email>{SUPPORT_EMAIL}</span></a></p>'
        '</article>'
        '</section>'
    )
    body = f"""
      <section class="section">
        <div class="section-heading"><p class="kicker">{escape(STATUS_AVAILABLE)}</p><h2>Buy only after the local scan proves fit.</h2></div>
        <div class="catalog-grid">{available_html}</div>
      </section>
{preset_deliverables}
{coming_soon_section}
      <section class="section">
        <div class="section-heading"><p class="kicker">{escape(STATUS_PROOF_ONLY)}</p><h2>Useful proof, not a listed checkout product.</h2></div>
        <div class="catalog-grid proof-grid">{proof_html}</div>
      </section>
"""
    html = layout(
        path=path,
        title="Migration Products",
        description="Available scanner-first migration products, pricing status, and proof-only pages for future migration packs.",
        kicker="Products",
        heading="Migration cleanup products that are ready to buy",
        body=body,
        crumbs=[("index.html", "Home"), (path, "Products")],
        schemas=[],
    )
    return path, html


def render_sqlalchemy_public_proof() -> tuple[str, str]:
    path = "proof/sqlalchemy-public-proof/index.html"
    proof_actions = action_list_html(
        (
            f'<a class="button" href="{relative_href(path, "products/sa20-pack/index.html")}">Open SQLAlchemy cleanup pack</a>',
            '<a class="button secondary" href="/scan?source=proof-sqlalchemy-public-proof">Run the free scan first</a>',
        )
    )
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
              <li>The free scanner is the qualification step before any paid cleanup workflow.</li>
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
              {proof_actions}
            </div>
          </article>
        </div>
      </section>
"""
    html = layout(
        path=path,
        title="SQLAlchemy public proof",
        description="Public SQLAlchemy migration proof for the supported cleanup subset, including validated supported files and fail-closed manual-review examples.",
        kicker="Public proof",
        heading="SQLAlchemy migration proof on public files",
        body=body,
        crumbs=[
            ("index.html", "Home"),
            ("products/sa20-pack/index.html", "SQLAlchemy cleanup pack"),
            (path, "Public proof"),
        ],
        schemas=[],
    )
    return path, html


def render_generic_product_proof(product: ProductPage) -> tuple[str, str]:
    path = product_proof_path(product)
    guides = [guide for guide in GUIDES if guide.slug in product.guide_slugs][:8]
    guide_cards = "".join(
        f'<a class="topic-card" href="{relative_href(path, f"{guide.family}/{guide.slug}/index.html")}">'
        f"<strong>{escape(guide.h1)}</strong><span>{escape(guide.description)}</span></a>"
        for guide in guides
    )
    docs_buttons = tuple(
        f'<a class="button secondary" href="#" data-doc-path="{escape(doc_path)}">{escape(label)}</a>'
        for label, doc_path in product.docs
    )
    pricing_button = (
        f'<a class="button secondary" href="{pricing_section_href(path, product)}">See pricing</a>'
        if pricing_section_href(path, product)
        else ""
    )
    product_button = f'<a class="button" href="{relative_href(path, product_page_path(product))}">Open {escape(product.name)}</a>'
    decision_actions = action_list_html(
        (product_button, pricing_button, *docs_buttons)
    )
    body = f"""
      <section class="section">
        <div class="grid three">
          <article class="page-panel">
            <h2>{len(guides)} exact-problem pages</h2>
            <p>The proof page is tied to specific migration error pages, not a generic refactor promise.</p>
          </article>
          <article class="page-panel">
            <h2>{len(product.proof_points)} fit signals</h2>
            <p>The product stays inside the supported subset and keeps fail-closed boundaries visible.</p>
          </article>
          <article class="page-panel">
            <h2>{len(product.not_for)} stop signals</h2>
            <p>The proof is also a way to say no before a buyer spends money on the wrong repo.</p>
          </article>
        </div>
      </section>
      <section class="section">
        <div class="grid two">
          <article class="page-panel">
            <h2>What this proof covers</h2>
            <ul class="clean">{"".join(f"<li>{escape(item)}</li>" for item in product.proof_points)}</ul>
          </article>
          <article class="page-panel">
            <h2>What stays out of scope</h2>
            <ul class="clean">{"".join(f"<li>{escape(item)}</li>" for item in product.not_for)}</ul>
          </article>
        </div>
      </section>
      <section class="section">
        <div class="grid two">
          <article class="page-panel">
            <h2>Start from the live problem pages</h2>
            <div class="topic-list">{guide_cards}</div>
          </article>
          <article class="page-panel">
            <h2>Decision path</h2>
            <p>{escape(product.summary)}</p>
            <div class="page-actions">
              {decision_actions}
            </div>
          </article>
        </div>
      </section>
"""
    html = layout(
        path=path,
        title=f"{product.name} proof and fit",
        description=f"Public proof and fit boundaries for {product.name}, including supported scope and exact-problem entry pages.",
        kicker="Public proof",
        heading=f"{product.name} proof and fit",
        body=body,
        crumbs=[
            ("index.html", "Home"),
            (product_page_path(product), product.name),
            (path, "Public proof"),
        ],
        schemas=[],
    )
    return path, html


def write_sitemap(
    output_dir: Path, filename: str, urls: Iterable[str], lastmod: str
) -> None:
    items = "".join(
        f"<url><loc>{escape(url)}</loc><lastmod>{lastmod}</lastmod></url>"
        for url in urls
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + items
        + "</urlset>"
    )
    (output_dir / filename).write_text(xml, encoding="utf-8")


def write_sitemap_index(
    output_dir: Path, filenames: Iterable[str], lastmod: str
) -> None:
    items = "".join(
        f"<sitemap><loc>{SITE_URL}/{name}</loc><lastmod>{lastmod}</lastmod></sitemap>"
        for name in filenames
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        + '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + items
        + "</sitemapindex>"
    )
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


def write_redirects(
    output_dir: Path, redirects: Iterable[tuple[str, str, int]]
) -> None:
    lines = [f"{source} {target} {status}" for source, target, status in redirects]
    (output_dir / "_redirects").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_site(output_dir: Path) -> dict[str, Any]:
    grouped: dict[str, list[GuidePage]] = defaultdict(list)
    for guide in GUIDES:
        grouped[guide.family].append(guide)

    proof_pages = [
        render_sqlalchemy_public_proof(),
        *[
            render_generic_product_proof(product)
            for product in PRODUCTS
            if product.slug != "sa20-pack"
        ],
    ]
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
    static_urls = [
        canonical_url(path) for path, _label in INDEXABLE_STATIC_PAGES
    ] + proof_urls
    hub_urls = [
        canonical_url("guides/index.html"),
        canonical_url("products/index.html"),
        *[canonical_url(f"{family}/index.html") for family in grouped],
    ]
    guide_urls = [
        canonical_url(f"{guide.family}/{guide.slug}/index.html") for guide in GUIDES
    ]
    product_urls = [
        canonical_url(f"products/{product.slug}/index.html") for product in PRODUCTS
    ]

    write_sitemap(output_dir, "sitemap-pages.xml", static_urls, lastmod)
    write_sitemap(output_dir, "sitemap-hubs.xml", hub_urls, lastmod)
    write_sitemap(output_dir, "sitemap-problem-pages.xml", guide_urls, lastmod)
    write_sitemap(output_dir, "sitemap-products.xml", product_urls, lastmod)
    write_sitemap_index(
        output_dir,
        (
            "sitemap-pages.xml",
            "sitemap-hubs.xml",
            "sitemap-problem-pages.xml",
            "sitemap-products.xml",
        ),
        lastmod,
    )

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
    (output_dir / "_site_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build static discovery pages for the site."
    )
    parser.add_argument(
        "--output-dir", default="site", help="Directory to write generated pages into."
    )
    args = parser.parse_args()
    build_site(Path(args.output_dir))


if __name__ == "__main__":
    main()
