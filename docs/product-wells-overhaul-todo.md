# Product Wells Overhaul To-Do

This is the ordered checklist for moving Zipper Tools from the current
SQLAlchemy-first storefront into the Product Wells model.

Goal: put the first demand product front and center, move the existing packages
into a secondary library/archive position, verify Cloudflare and Stripe, and
launch only when the funnel can prove demand and fulfill a paid order.

## Current Decision

- [x] Confirm GitHub Actions Upgrade Guard as the first front-page demand
  product.
- [x] Decide the public tagline. Current candidate:
  `Autonomous deadline-readiness tools for software teams.`
- [x] Decide the old-package label:
  - `Migration Library`
  - `Legacy Proof`
  - `Archive`
  - another buyer-facing name
- [x] Decide whether the first Action Guard paid CTA appears immediately or
  stays hidden until the proof page shows demand.

Decision notes:

- Public tagline: `Autonomous deadline-readiness tools for software teams.`
- Old-package label: `Migration Library`.
- Action Guard paid CTA: hidden until proof-page and free-scanner demand show a
  clear paid boundary.
- Floating major-tag and reusable-workflow detection are not blockers for the
  site pivot; revisit them if demand centers on those risks.

## Phase 1 - Storefront Repositioning

- [x] Rewrite the homepage around the current Product Well instead of
  SQLAlchemy-first migration packages.
- [x] Put GitHub Actions Upgrade Guard above the fold as the current Well of the
  Month.
- [x] Add a clear primary CTA for the free scanner/report path.
- [x] Add a secondary CTA for proof/results.
- [x] Move SQLAlchemy, Pydantic, and flatconfig products out of the homepage
  flagship slot.
- [x] Create a secondary package-library/archive page for existing products.
- [x] Keep existing SQLAlchemy, Pydantic, flatconfig, pricing, policy, success,
  cancel, and checkout URLs alive.
- [x] Update nav so the site can support many wells without reading like a
  generic blog.
- [x] Remove or demote the old Migration Sprint Sale language if it distracts
  from the Product Wells pivot.

## Phase 2 - New Product Wells Pages

- [x] Add `/wells/` as the archive of monthly wells.
- [x] Add `/wells/github-actions-upgrade-guard/` as the first Well of the
  Month.
- [x] Add `/products/actions-upgrade-guard/` as the product detail page.
- [x] Add `/proof/actions-upgrade-guard/` as the public proof page.
- [x] Add `/framework/` to explain the Product Wells method.
- [x] Add sitemap entries for all new pages.
- [x] Add canonical URLs for all new pages.
- [x] Add internal links from the homepage, product library, proof pages, and
  framework page.
- [x] Verify old internal links do not point users back into SQLAlchemy as the
  flagship offer.

## Phase 3 - Action Guard Proof Package

- [x] Build `products/actions-upgrade-guard/`.
- [x] Generate JSON and HTML reports.
- [x] Generate patch previews.
- [x] Add fixture coverage and tests.
- [x] Publish the generated proof artifacts through the new proof page.
- [x] Add a buyer-readable example report excerpt.
- [x] Add a "do not buy this if" section.
- [x] Add a "why this is not just actionlint" note if the proof page needs it.
- [ ] Add a "why not wait for GitHub?" note only if buyers raise that objection.
- [x] Decide whether floating major-tag detection is required before launch.
- [x] Decide whether reusable workflow detection is required before launch.

## Phase 4 - Analytics And Demand Tracking

- [x] Confirm live `site/config.js` uses `support@zippertools.org`.
- [x] Set the Cloudflare Web Analytics token in `site/config.js` if the live
  site needs the static token.
- [x] Add route-click tracking for the homepage well CTA.
- [x] Add route-click tracking for the free scanner/download CTA.
- [x] Add route-click tracking for the product page CTA.
- [x] Add route-click tracking for the proof page CTA.
- [x] Add route-click tracking for checkout intent.
- [x] Replace the Worker `CONVERSION_EVENTS` binding with structured
  `conversion_route` Worker logs and tracked `/go/...` paths so click events
  can be checked without enabling another Cloudflare account feature.
- [x] Update the live funnel verifier for Product Wells routes.
- [x] Rerun the live funnel verifier after deployment.
- [ ] Track GitHub repo views, clones, releases, and downloads for Action Guard.
- [ ] Record all outreach and responses in `docs/lead-tracker.md` or a
  well-specific lead tracker.

Deployment note: Cloudflare Worker version
`895a399d-6943-4857-92d2-737b8182fb4f` is live on `zippertools.org` and
`www.zippertools.org`; live `config.js` contains `support@zippertools.org`.
The static Cloudflare Web Analytics token remains blank because the current
demand test uses tracked `/go/...` paths plus structured Worker logs.

## Phase 5 - Stripe And Paid Fulfillment

- [ ] Define the first Action Guard paid SKU:
  - one-time repo scan bundle
  - annual rule-pack subscription
  - team license
  - another downloadable offer
- [ ] Define the free vs paid boundary for Action Guard.
- [ ] Define exact Action Guard deliverables.
- [ ] Create a sample paid deliverable ZIP.
- [ ] Add Action Guard to `site/product_catalog.mjs` only after the SKU is
  clear.
- [ ] Add `/go/actions-upgrade-guard` checkout intent routing.
- [ ] Add Stripe product metadata for Action Guard only after proof demand
  exists, unless launching an explicit early-access SKU.
- [ ] Store the paid ZIP in the private Cloudflare KV namespace bound as
  `PAID_ARTIFACTS`.
- [ ] Verify `/stripe/delivery` can stream the Action Guard artifact from KV.
- [ ] Deploy the Worker with Stripe test secrets.
- [ ] Run one Stripe test-mode checkout for Action Guard.
- [ ] Create or verify the live Stripe webhook endpoint:
  `https://zippertools.org/stripe/webhook`.
- [ ] Confirm webhook events are enabled:
  - `checkout.session.completed`
  - `checkout.session.async_payment_succeeded`
  - `checkout.session.async_payment_failed`
- [ ] Replace test secrets with live secrets only when ready.
- [ ] Make one low-risk live purchase and refund it if needed.
- [ ] Verify the paid deliverable downloads without manual intervention.
- [ ] Write down the real Stripe payout schedule and threshold.
- [ ] Resolve the docs conflict about whether the Stripe payout path is already
  verified.

Blocker note: Action Guard paid fulfillment is intentionally paused. The first
paid SKU, free-vs-paid boundary, exact deliverables, and paid ZIP are not
defined yet, and no live Stripe settings or purchases were changed during this
deploy.

## Phase 6 - Cloudflare Deployment

- [x] Keep Cloudflare as the canonical storefront for `zippertools.org`.
- [x] Keep GitHub Pages as redirect or backup only.
- [x] Confirm `wrangler.jsonc` routes still cover:
  - `zippertools.org`
  - `www.zippertools.org`
  - `/go/*`
  - `/stripe/*`
  - `/cancel`
- [x] Decide whether to rename the Worker from `sa20-pack` later. This is not a
  launch blocker if routing works.
- [x] Deploy the updated site and Worker to Cloudflare.
- [x] Run the local site URL audit.
- [x] Run the live URL audit.
- [x] Confirm sitemap URLs, canonical URLs, and internal links pass.
- [x] Confirm the live homepage shows Product Wells and Action Guard, not the
  old SQLAlchemy-first storefront.
- [x] Confirm success and cancel pages still work.

Deployment note: keep the Worker name `sa20-pack` for now because both custom
domains route correctly; rename only as a later cleanup if it becomes confusing
in Cloudflare.

## Phase 7 - Policy, Legal, And Public Trust

- [x] Update Terms of Sale for a multi-product Product Wells storefront.
- [x] Update Refund Policy for downloadable product wells.
- [x] Update Privacy Policy if analytics or checkout copy changes.
- [x] Update License Terms for Action Guard deliverables.
- [x] Update Support Scope for Action Guard and the product library.
- [ ] Confirm seller name consistency across:
  - `site/config.js`
  - Stripe Dashboard
  - policy docs
  - public footer
- [ ] Record the launch seller decision:
  real legal name now, branded DBA later, or another path.
- [ ] Confirm Oregon/state/local software-sales requirements before first real
  sale if seller identity changes.
- [x] Review public claims so the site does not promise full autonomous
  migration or guaranteed fixes.

Legal note: public policy copy and `site/config.js` now use `Zipper Tools`, but
Stripe Dashboard seller details, the real legal-name/DBA decision, and
Oregon/state/local requirements still need owner confirmation before the first
new paid Action Guard sale.

## Phase 8 - Seven-Day Demand Test

- [ ] Find 20 exact-fit public GitHub Actions deprecation or upgrade examples.
- [ ] Publish only replies or notes where the proof page directly helps.
- [ ] Track every source, reply, click, scanner run, and checkout click.
- [ ] Promote the well if at least one success threshold is met:
  - 3 people run the free scanner
  - 1 serious buyer asks about pricing or scope
  - product/proof pages show repeated qualified movement from exact sources
- [ ] Pause the well if traffic arrives but nobody runs the artifact.
- [ ] Pause the well if checkout intent stays near zero after targeted outreach.
- [ ] Record the promote/pause/kill decision in a monthly decision log.

## Phase 9 - After The First Well Is Stable

- [ ] Decide whether Python 3.14 Readiness becomes the second public well.
- [ ] Keep ranks 3-6 paid checkout paused until each has proof pages and demand
  tests.
- [ ] Build shared templates for wells, products, proof pages, and archives.
- [ ] Build shared report components across product wells.
- [ ] Build shared rule-pack metadata conventions.
- [ ] Add a monthly well review document generated from the scoring rubric.
- [ ] Add a kill/promote decision log so the portfolio stays intentional.

## Not Blockers For The Overhaul

- [x] Core MVPs for ranks 3 through 6 already exist.
- [x] Action Guard already has product code, reports, fixtures, and tests.
- [x] Python 3.14 Readiness already exists as the second new well.
- [ ] Floating major-tag detection can be added after the site pivot unless it
  becomes central to the first proof page.
- [ ] Reusable workflow detection can be added after the site pivot unless it
  becomes central to the first proof page.
