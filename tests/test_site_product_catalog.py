from __future__ import annotations

import json
import subprocess
from pathlib import Path

from scripts.build_site import build_site


def test_product_catalog_order_status_and_ctas() -> None:
    site_dir = Path.cwd() / "site"
    build_site(site_dir)

    html = (site_dir / "products" / "index.html").read_text(encoding="utf-8")

    fit_pos = html.index("SQLAlchemy/Pydantic Fit Report Add-on")
    sqlalchemy_pos = html.index("SQLAlchemy 1.4 to 2.0 Migration Cleanup Pack")
    pydantic_pos = html.index("Pydantic v1 to v2 Migration Cleanup Pack")
    preset_pos = html.index("Migration Preset Bundle")
    eslint_pos = html.index("ESLint Flat Config Migration Cleanup Pack")

    assert fit_pos < sqlalchemy_pos < pydantic_pos < preset_pos < eslint_pos
    assert html.count('class="status-label available">Available now') == 4
    assert "Example/proof page only" in html
    assert "$99 per team" in html
    assert "$299.99 per team" in html
    assert "$249.99 per team" in html
    assert "$149.99 per team" in html
    assert "Not currently purchasable" in html
    assert "Read proof page" in html
    assert "/products/fit-report/" in html
    assert "/products/sa20-pack/" in html
    assert "/products/pydantic-v2-porter/" in html
    assert "/products/sa20-preset/" in html
    assert "/go/fit-report/catalog-card-products" in html
    assert "/go/sa20-pack/catalog-card-products" in html
    assert "/go/pydantic-v2-porter/catalog-card-products" in html
    assert "/go/sa20-preset/catalog-card-products" in html
    assert "View fit report details" in html
    assert "View rollout kit details" in html
    assert "Buy automated fit report - $99" in html
    assert "Buy cleanup pack - $299.99" in html
    assert "Buy Pydantic cleanup pack - $249.99" in html
    assert "Buy preset bundle - $149.99" in html
    assert html.count("Secure checkout is handled by Stripe.") == 4
    assert "Labs and proofs" in html
    catalog_text = Path("site/product_catalog.mjs").read_text(encoding="utf-8")
    assert "Buy automated fit report" in catalog_text
    assert "prices.fitReport.display" in catalog_text
    assert "SQLAlchemy/Pydantic Fit Report Add-on" in (catalog_text)
    assert "Use this only with SQLAlchemy or Pydantic scanner output" in (catalog_text)
    assert 'secureCheckoutNote: "Secure checkout is handled by Stripe."' in (
        catalog_text
    )
    assert "commerce.secureCheckoutNote" in Path("site/app.js").read_text(
        encoding="utf-8"
    )
    assert "Open fit report details" not in html
    assert "Open checkout" not in html
    assert "Open fit report checkout" not in (
        Path("site/product_catalog.mjs").read_text(encoding="utf-8")
    )
    assert "Coming soon / proof page only" not in html
    nav_html = html.split('<nav class="nav-links" aria-label="Primary">', 1)[1].split(
        "</nav>", 1
    )[0]
    expected_nav = ("Scan", "Guides", "Products", "Pricing", "Demo", "Policies", "Repo")
    positions = [nav_html.index(f">{label}<") for label in expected_nav]
    assert positions == sorted(positions)
    footer_html = html.split('<div class="footer-links">', 1)[1].split("</div>", 1)[0]
    footer_positions = [footer_html.index(f">{label}<") for label in expected_nav]
    assert footer_positions == sorted(footer_positions)


def test_site_config_matches_product_catalog_constants() -> None:
    script = """
import fs from 'node:fs';
import vm from 'node:vm';
import {
  checkoutProducts,
  commerce,
  goRoutes,
  products,
} from './site/product_catalog.mjs';

const sandbox = { window: {} };
vm.runInNewContext(fs.readFileSync('./site/config.js', 'utf8'), sandbox);
const config = sandbox.window.SA20_SITE_CONFIG;
console.log(JSON.stringify({
  supportEmail: commerce.supportEmail,
  configEmail: config.contactEmail,
  configRoutes: {
    freeScan: config.freeStartUrl,
    sa20: config.paidPackUrl,
    sa20Preset: config.presetBundleUrl,
    pydantic: config.pydanticPackUrl,
    fitReport: config.fitReportUrl,
  },
  productRoutes: {
    freeScan: products.freeScan.checkoutUrl,
    sa20: products.sa20.checkoutUrl,
    sa20Preset: products.sa20Preset.checkoutUrl,
    pydantic: products.pydantic.checkoutUrl,
    fitReport: products.fitReport.checkoutUrl,
  },
  checkoutAmounts: Object.fromEntries(
    Object.entries(checkoutProducts).map(
      ([slug, product]) => [slug, product.amountCents],
    ),
  ),
  ctaLabels: {
    fitReport: products.fitReport.ctaLabel,
    sa20: products.sa20.ctaLabel,
    sa20Preset: products.sa20Preset.ctaLabel,
    pydantic: products.pydantic.ctaLabel,
  },
  goRouteLabels: Object.fromEntries(
    Object.entries(goRoutes).map(([route, value]) => [route, value.label]),
  ),
}));
"""
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        capture_output=True,
        check=False,
        cwd=Path.cwd(),
        text=True,
    )

    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)

    assert data["configEmail"] == data["supportEmail"]
    assert data["supportEmail"] == "zippers3737@gmail.com"
    assert data["configRoutes"] == data["productRoutes"]
    assert data["checkoutAmounts"] == {
        "fit-report": 9900,
        "pydantic-v2-porter": 24999,
        "sa20-pack": 29999,
        "sa20-preset": 14999,
    }
    assert data["ctaLabels"] == {
        "fitReport": "Buy automated fit report - $99",
        "pydantic": "Buy Pydantic cleanup pack - $249.99",
        "sa20": "Buy cleanup pack - $299.99",
        "sa20Preset": "Buy preset bundle - $149.99",
    }
    assert data["goRouteLabels"]["/go/fit-report"] == "fit-report"
    assert data["goRouteLabels"]["/go/pydantic-v2-porter"] == "pydantic-v2-porter"
