# Funnel Fix Todo

This is the working checklist for fixing the public trust path before sending
more traffic to ZipperTools. Work through it one item at a time. Keep changes
small, verify locally, and update this file as fixes land.

## Baseline Guardrail

- [x] Confirm which pages are generated from `scripts/build_site.py` and which
  pages are hand-edited static HTML.
- [x] Treat generated source as the authority where possible, then regenerate
  site output.
- [x] Add or adjust tests so public copy cannot drift back into broken states.
- [x] Avoid unrelated copy polish until the direct trust-path blockers are done.

## Must Fix Before Sending Traffic

### 1. Free Scan Install Path

- [x] Search all public files for retired package-index install or scan
  commands.
- [x] Replace public SQLAlchemy free-scan instructions with the verified GitHub
  install path unless `sa20-pack` is actually published and installable from
  PyPI.
- [x] Use one primary public command pair:

```bash
python -m pip install "https://github.com/zippertools/sqlalchemy-14-to-20-codemod/archive/refs/tags/v0.1.1.zip"
python -m sa20_pack.cli . --report migration-report.json
```

- [x] Add the fallback/support note anywhere the install command appears:
  `If installation fails, retry from the GitHub quickstart or contact support at
  zippers3737@gmail.com.`
- [x] Verify the exact public install command and scan command from outside the
  local developer checkout.

Evidence: `tests/test_site_builder.py::test_free_scan_install_path_uses_verified_archive_command`
passes, tracked public files no longer contain stale PyPI install commands, and
the verified public command pair is the GitHub archive install plus
`python -m sa20_pack.cli . --report migration-report.json`.

### 2. Remove Retired Price Copy

- [x] Search public site, builder, product catalog, and docs for retired
  "planned price" copy.
- [x] Replace public buyer-facing copy with explicit live checkout price copy.
  During the temporary Migration Sprint Sale, public pages use sale-price copy
  instead.
- [x] Keep "planned" only in internal docs if it is still true there.

Evidence: public pricing code now uses explicit checkout/sale price copy, and
the retired "planned price" copy is covered by regression checks.

### 3. Fix Fit Report CTA Wording

- [x] Search for retired fit-report detail CTA labels.
- [x] If the link goes to checkout, rename it to a price-specific buy CTA.
- [x] If a pre-checkout detail page is preferred, create/link that page instead
  of sending a "details" CTA directly to payment.

Evidence: public generated pages and the product catalog use a price-specific
buy CTA; retired fit-report CTA labels are covered by regression checks.

### 4. Checkout Domain Consistency

- [x] Inventory every checkout CTA target, including tracked `/go/...` routes
  and final Stripe destinations.
- [x] Pick one visible buyer-facing pattern, preferably tracked `/go/...`
  routes that resolve through the Worker to Stripe.
- [x] Add reassurance near checkout CTAs where useful:
  `Secure checkout is handled by Stripe.`
- [x] Remove or explain any remaining domain inconsistency.

Evidence: buyer-facing checkout CTAs use tracked `/go/...` routes. The Worker
creates Stripe Checkout Sessions behind those routes, generated product cards
now say `Secure checkout is handled by Stripe.`, and remaining
`checkout.stripe.com` references are test/audit expectations for the Worker
redirect destination rather than public page links.

### 5. Pydantic Scan And Fit Report Scope

- [x] Clarify whether Pydantic has its own scanner, shares a public scan flow,
  or should point to proof/supported-subset docs instead.
- [x] Update the Pydantic product page so buyers are not sent to a
  SQLAlchemy-only scan without explanation.
- [x] Scope the `$99` report clearly:
  - `SQLAlchemy Fit Report - $99`
  - product-specific fit report labels
  - or explicit multi-product coverage copy if it truly applies broadly
- [x] Make checkout metadata and visible labels match the chosen scope.

Evidence: Pydantic product and guide pages now route free-scan CTAs through
`/go/pydantic-free-scan` and label them `Run the Pydantic scan first`. The
Pydantic product page explicitly says the free scan link opens the Pydantic
scanner, not the SQLAlchemy scanner. The `$99` product is now scoped as the
`SQLAlchemy/Pydantic Fit Report Add-on`, and ESLint proof-only pages do not
include `/go/fit-report` links. Verified with:

```bash
python -m pytest tests/test_site_builder.py::test_product_pages_link_to_trackable_checkout_routes tests/test_site_builder.py::test_fit_report_scope_is_not_offered_on_proof_only_eslint_pages tests/test_site_product_catalog.py tests/test_worker_routes.py::test_all_free_scan_routes_land_on_matching_public_docs tests/test_worker_routes.py::test_all_paid_go_routes_create_stripe_checkout_sessions -q -p no:cacheprovider
python -m ruff check scripts/build_site.py tests/test_site_builder.py tests/test_site_product_catalog.py
```

## Strongly Recommended Next Fixes

### 6. Homepage Buyer Path

- [x] Move exact-query/SEO blocks lower on the homepage.
- [x] Above SEO blocks, show the human buyer path:
  1. Run local scan
  2. See example report
  3. Confirm fit
  4. Choose smallest paid step
  5. Buy only if repeated supported findings exist
- [x] Keep early homepage sections focused on decision-making, not page-index
  browsing.

Evidence: the homepage now has a `Buyer path` section immediately after the
hero and before the pain/problem sections. The regression check confirms the
buyer path appears before the pain and paid-options sections.

### 7. ESLint Product Status

- [x] On the Products index, mark ESLint visibly as `Coming soon` or
  `Proof only`.
- [x] Alternatively remove ESLint from the main purchasable product grid until
  it is purchasable.
- [x] Make the product index and ESLint product page status agree.

Evidence: the Products index renders ESLint in a separate
`Example/proof page only` section with `Not currently purchasable`, and the
product catalog regression test asserts the proof-only status and absence from
the normal purchasable grid.

### 8. Navigation Consistency

- [x] Standardize primary nav everywhere:
  `Scan | Guides | Products | Pricing | Demo | Policies | Repo`
- [x] Centralize nav rendering where generated pages allow it.
- [x] Confirm static pages, generated guide pages, product pages, and footer nav
  no longer drift.

Evidence: `scripts/build_site.py` now renders the full primary and footer nav
sequence for generated pages, top-level static HTML pages use the same core
sequence, and tests assert the nav order on static pages plus the generated
Products page.

### 9. Product Page Purchase Structure

- [x] Reorder product pages into this buyer-first sequence:
  1. Outcome
  2. What it fixes
  3. What you get
  4. Proof/example
  5. Buy if
  6. Do not buy if
  7. Delivery/support/refund terms
- [x] Add a clear "After purchase, you receive" deliverables box:
  - paid cleanup workflow
  - preview/apply commands
  - supported rewrite table
  - JSON report output
  - rollback checklist
  - manager summary
  - license/support terms
- [x] Move defensive language below the value and proof sections.

Evidence: generated product pages now use an `After purchase, you receive`
deliverables box for listed checkout products, the deliverables name
preview/apply commands, supported rewrite table, JSON report output, rollback,
manager summary, and license/support terms, and tests assert that this section
appears before `Do not use this if`.

## Engineering Hygiene

### 10. Formatting Cleanup

- [x] Handle formatting as a separate formatting-only change set.
- [x] Run:

```bash
python -m ruff format . --check --no-cache
```

- [x] Format only after the funnel fixes are safely separated.

Evidence: `python -m ruff format . --no-cache` reformatted 12 Python files, and
`python -m ruff format . --check --no-cache` now reports `64 files already
formatted`. Follow-up `ruff check` and focused pytest checks passed.

### 11. Centralize Shared Constants

- [x] Centralize repeated values:
  - product names
  - prices
  - checkout routes
  - status labels
  - support email
  - payment provider text
  - delivery language
  - refund language
  - install commands
- [x] Add tests for the highest-risk strings.
- [x] Confirm pricing, checkout copy, product status, and install commands
  cannot contradict each other across pages.

Evidence: Python generation now imports support email, install URL, payment
provider copy, refund/delivery language, fit-report scope, product status
labels, preset price/route, and product prices/routes from
`scripts/site_catalog.py`. The JS catalog now centralizes routes, prices, and
status labels, and the Worker already imports that catalog for Stripe products.
Regression tests compare `site/config.js` against `site/product_catalog.mjs`
for support email and checkout routes, assert checkout amounts/CTA labels, and
continue checking generated page copy and install commands.

## Recommended Work Order

1. Free scan install path.
2. Planned price language.
3. Fit report CTA wording.
4. Checkout domain and Stripe reassurance.
5. Pydantic and fit-report scope.
6. Homepage buyer path.
7. ESLint status.
8. Navigation consistency.
9. Product page structure.
10. Formatting-only cleanup.
11. Shared constants hardening.
