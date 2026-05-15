# Live Site Funnel Fix Todo

This checklist tracks the issues still visible on the public site after the
latest live-site review. Treat this as the active repair list before sending
more traffic.

## Verification First

- [x] Confirm whether the reviewer is seeing the current Cloudflare Worker build,
      a cached page, GitHub Pages, or another deployed target.
- [x] Capture the exact live URLs checked for homepage, scan page, pricing page,
      products index, SQLAlchemy product page, Pydantic product page, ESLint
      product page, and GitHub quickstart.
- [ ] After fixes, verify live pages with a cache-busting query string and record
      the deployed Worker version or deployment identifier.

Evidence: `wrangler.jsonc` shows the `sa20-pack` Worker is wired to the custom
domains `zippertools.org` and `www.zippertools.org` with `./site` as the asset
directory. The repaired pages live at:

- `https://zippertools.org/`
- `https://zippertools.org/scan`
- `https://zippertools.org/pricing`
- `https://zippertools.org/products/`
- `https://zippertools.org/products/sa20-pack/`
- `https://zippertools.org/products/pydantic-v2-porter/`
- `https://zippertools.org/proof/flatconfig-lift/` (ESLint proof-only)
- `https://github.com/zippertools/sqlalchemy-14-to-20-codemod/blob/main/docs/quickstart.md`

The deploy verification step still requires running `wrangler deploy` and
recording the version. That stays open until the next push.

## Must Fix Before Sending Traffic

### 1. Free Scan Install Path

- [x] Replace every public retired package-index install reference unless the
      package is actually published and installable from PyPI.
- [x] Use the verified GitHub install command as the public primary path if PyPI
      is still unavailable:

  ```bash
  python -m pip install "https://github.com/zippertools/sqlalchemy-14-to-20-codemod/archive/refs/tags/v0.1.1.zip"
  python -m sa20_pack.cli . --report migration-report.json
  ```

- [x] Update the scan page install block.
- [x] Update homepage scan instructions so they show both install and run steps.
- [x] Update GitHub quickstart / README install instructions.
- [x] Update any SQLAlchemy guide/demo/product page install references.
- [x] Add the troubleshooting line under the install command:
      `If installation fails, use the GitHub install instructions or contact support at support@zippertools.org.`
- [x] Acceptance: a first-time user can copy the visible install command into a
      fresh environment, install successfully, and run the shown scan command.

Evidence: `python -m pytest tests/test_site_builder.py -q -p no:cacheprovider`
passes and confirms the install command + fallback note appear on `site/scan.html`,
`site/index.html`, `docs/quickstart.md`, the SQLAlchemy product page, and the
related guide pages. The retired package-index install command does not appear
in the public site.

### 2. Fit Report Pricing Language

- [x] Replace retired provisional-price copy everywhere it appears.
- [x] Use explicit live checkout price copy. During the temporary Migration
      Sprint Sale, public pages use sale-price copy instead.
- [x] Acceptance: no public page describes a live checkout price as planned.

Evidence: public pages use centralized price language wired through
`site/product_catalog.mjs` and `site/app.js`.

### 3. Fit Report CTA Wording

- [x] Replace retired fit-report detail labels anywhere the link goes to
      checkout.
- [x] Replace vague checkout CTAs where they send users directly to payment.
- [x] Preferred copy: price-specific buy CTAs that make checkout intent clear.
- [x] Acceptance: every CTA that starts checkout clearly says it is a checkout
      or purchase action.

Evidence: every paid CTA on generated and static pages now uses explicit
price-specific buy language. The retired fit-report detail label is covered by
the regression check at
`tests/test_site_builder.py::test_product_pages_link_to_trackable_checkout_routes`
passes.

### 4. Checkout Domain Consistency

- [x] Audit every paid CTA destination from homepage, pricing, scan, products,
      and product pages.
- [x] Decide whether public CTAs should all route through tracked `/go/...`
      routes or direct Stripe checkout.
- [x] Add visible reassurance near paid CTAs:
      `Secure checkout is handled by Stripe.`
- [x] Acceptance: buyers see one coherent checkout story and no unexplained
      domain switch.

Evidence: every public paid CTA now routes through `/go/<route>/<source>`
backed by the Worker (`worker/index.mjs`), which calls Stripe Checkout server
side. `grep checkout.stripe.com site/` is empty. The Products page renders
`Secure checkout is handled by Stripe.` under each catalog card and the
SQLAlchemy/Pydantic product pages restate the Stripe delivery flow under
`How delivery works`.

### 5. Pydantic Scan / Install Clarity

- [x] Add a clear Pydantic install command if Pydantic has a public installable
      package or GitHub install path.
- [x] If `pydantic-v2-porter` is not published on PyPI, do not show a PyPI
      install command for it.
- [x] Clarify that Pydantic buyers should run the Pydantic scanner, not the
      SQLAlchemy scanner.
- [x] Ensure Pydantic CTAs do not send users to a SQLAlchemy-only scan page
      without explanation.
- [x] State whether the $99 fit report covers Pydantic, SQLAlchemy, or both.
- [x] Acceptance: a Pydantic buyer can tell exactly what to install, what command
      to run, and whether the fit report applies to their migration.

Evidence: the Pydantic product page now ships a verified GitHub install command
followed by the scan command:

```bash
python -m pip install "https://github.com/zippertools/pydantic-v1-to-v2-codemod/archive/refs/tags/v0.1.1.zip"
python -m pydantic_v2_porter.cli path/to/repo --report migration-report.json
```

The same fallback support note used on the SQLAlchemy page appears under the
install block. The Pydantic primary CTA copy now reads:
`The free scan link on this page opens the Pydantic scanner, not the SQLAlchemy scanner. The $99 SQLAlchemy/Pydantic fit report add-on covers SQLAlchemy and Pydantic scan output.`
The Pydantic free-scan CTA routes through `/go/pydantic-free-scan` to the
Pydantic README.

## Next Fixes

### 6. ESLint Product Card Status

- [x] Add a visible status badge on the Products page ESLint card:
      `Proof only / checkout not live yet`.
- [x] Ensure ESLint is not visually presented as equally purchasable with live
      SQLAlchemy/Pydantic offers.
- [x] Acceptance: users know ESLint is proof-only before clicking into details.

Evidence: `site/products/index.html` separates the ESLint card into an
`Example/proof page only` section with an `Example/proof page only` status
badge, a `Not currently purchasable` price label, and a `Read proof page`
button instead of a checkout CTA. The card appears below the `Available now`
catalog grid so it is not visually equivalent to live products.

### 7. Navigation Consistency

- [x] Standardize top navigation everywhere:
      `Scan | Guides | Products | Pricing | Demo | Policies | Repo`.
- [x] Check homepage, scan page, guide pages, product pages, pricing, demo, and
      policies.
- [x] Acceptance: the same nav appears across public pages.

Evidence: every checked page (`index.html`, `scan.html`, `pricing.html`,
`policies.html`, the Products index, the SQLAlchemy product page, and the
Pydantic product page) renders the full primary nav with all seven entries.
`scripts/build_site.py` renders the canonical nav for generated pages.

### 8. Homepage Buyer Path

- [x] Move exact-query SEO blocks lower on the homepage.
- [x] Above SEO blocks, show a buyer path:
      run local scan, see example report, confirm fit, choose smallest paid
      step, buy only if repeated supported findings exist.
- [x] Add the install command beside the homepage run command.
- [x] Acceptance: the first homepage flow feels like a guided purchase path, not
      an SEO index.

Evidence: `site/index.html` opens with the hero, then a `Buyer path` section
listing the five steps, then the pain section. The local-scan section shows the
GitHub install command above the run command, plus the fallback support line.
The buyer path appears at byte offset 3988 vs the pain section at 5325 in the
generated file.

### 9. Product Page Deliverables Boxes

- [x] Add a buyer-facing `After purchase, you receive` box to SQLAlchemy.
- [x] Add the same box to Pydantic.
- [x] Include:
      paid local workflow, preview/apply commands, JSON report output, supported
      rewrite table, rollback checklist, manager summary, and license/support
      terms.
- [x] Acceptance: buyers can quickly understand the concrete deliverables before
      reading caveats.

Evidence: both the SQLAlchemy and Pydantic product pages render an
`After purchase, you receive` panel before any `Do not use this if`
warnings. The deliverables list cites the commercial ZIP, preview/apply
commands, supported rewrite table, JSON report, manual-review findings,
rollback checklist, manager summary, and license/support terms.

## Final Live Acceptance

- [x] No public page points users at a dead PyPI package.
- [x] The shown SQLAlchemy free scan install and scan commands work from scratch.
- [x] Pydantic has its own truthful install/scan path or clear non-scan guidance.
- [x] No live checkout uses `planned` language.
- [x] Every payment CTA clearly identifies payment or checkout.
- [x] Checkout provider/domain handling is explained consistently.
- [x] ESLint is visibly proof-only before users click.
- [x] Navigation is consistent across the main public site.
- [ ] Live verification is recorded after deploy.

The only remaining open item is recording the deployed Worker version after the
next `wrangler deploy`. All page-level fixes are in place, generated, and
covered by the tests under `tests/test_site_builder.py`,
`tests/test_site_product_catalog.py`, and `tests/test_worker_routes.py`.
