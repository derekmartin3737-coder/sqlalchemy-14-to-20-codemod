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

- [ ] Confirm live `site/config.js` uses `support@zippertools.org`.
- [ ] Set the Cloudflare Web Analytics token in `site/config.js` if the live
  site needs the static token.
- [x] Add route-click tracking for the homepage well CTA.
- [x] Add route-click tracking for the free scanner/download CTA.
- [x] Add route-click tracking for the product page CTA.
- [x] Add route-click tracking for the proof page CTA.
- [x] Add route-click tracking for checkout intent.
- [x] Bind, expose, or replace the Worker `CONVERSION_EVENTS` store so click
  events can actually be queried.
- [x] Update the live funnel verifier for Product Wells routes.
- [ ] Rerun the live funnel verifier after deployment.
- [ ] Track GitHub repo views, clones, releases, and downloads for Action Guard.
- [ ] Record all outreach and responses in `docs/lead-tracker.md` or a
  well-specific lead tracker.

Local note: `site/config.js` contains `support@zippertools.org`; live
confirmation still waits for deployment approval.

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

## Phase 6 - Cloudflare Deployment

- [ ] Keep Cloudflare as the canonical storefront for `zippertools.org`.
- [ ] Keep GitHub Pages as redirect or backup only.
- [x] Confirm `wrangler.jsonc` routes still cover:
  - `zippertools.org`
  - `www.zippertools.org`
  - `/go/*`
  - `/stripe/*`
  - `/cancel`
- [ ] Decide whether to rename the Worker from `sa20-pack` later. This is not a
  launch blocker if routing works.
- [ ] Deploy the updated site and Worker to Cloudflare.
- [x] Run the local site URL audit.
- [ ] Run the live URL audit.
- [x] Confirm sitemap URLs, canonical URLs, and internal links pass.
- [ ] Confirm the live homepage shows Product Wells and Action Guard, not the
  old SQLAlchemy-first storefront.
- [ ] Confirm success and cancel pages still work.

## Phase 7 - Policy, Legal, And Public Trust

- [ ] Update Terms of Sale for a multi-product Product Wells storefront.
- [ ] Update Refund Policy for downloadable product wells.
- [ ] Update Privacy Policy if analytics or checkout copy changes.
- [ ] Update License Terms for Action Guard deliverables.
- [ ] Update Support Scope for Action Guard and the product library.
- [ ] Confirm seller name consistency across:
  - `site/config.js`
  - Stripe Dashboard
  - policy docs
  - public footer
- [ ] Record the launch seller decision:
  real legal name now, branded DBA later, or another path.
- [ ] Confirm Oregon/state/local software-sales requirements before first real
  sale if seller identity changes.
- [ ] Review public claims so the site does not promise full autonomous
  migration or guaranteed fixes.

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
