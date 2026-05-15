# Product Wells To-Do

This is the active checklist for pivoting Zipper Tools from a SQLAlchemy-first
storefront into an autonomous product-well engine.

The ordered implementation checklist for the site, Stripe, Cloudflare, proof,
analytics, legal, and demand-test overhaul lives in
`docs/product-wells-overhaul-todo.md`.

Priority labels:

- `P0`: required before this new direction is real
- `P1`: required before first serious demand test
- `P2`: improves conversion after demand appears
- `P3`: later portfolio expansion

## P0 - Strategic Reset

- [x] Make `Autonomous Product Wells for a Solo Developer.docx` the strategic
  source of truth.
- [x] Update `AGENTS.md` so future sessions follow the autonomous product-well
  framework.
- [x] Create `docs/autonomous-product-wells.md` as the repo-native doctrine.
- [x] Create this execution checklist.
- [x] Mark SQLAlchemy pages and docs as legacy proof where buyer-facing copy
  currently implies it is the flagship.
- [x] Decide whether the public brand tagline becomes:
  `Autonomous deadline-readiness tools for software teams.`
- [x] Keep SQLAlchemy, Pydantic, and flatconfig products live only as proof and
  search assets unless fresh demand appears.

## P0 - First New Well: GitHub Actions Upgrade Guard

- [x] Create `products/actions-upgrade-guard/`.
- [x] Add a product README with:
  - who this is for
  - do not use this if
  - supported workflow issues
  - unsupported workflow issues
  - example command
  - example report
- [x] Define the first rules-as-data schema:
  - rule id
  - title
  - severity
  - official source URL
  - deadline or platform signal
  - detection pattern
  - autofix availability
  - confidence level
  - docs link
- [x] Pick the implementation language:
  - Python was chosen for v0.1 because it matches the existing product package
    pattern and PyYAML is already used in the repo.
  - consider Go/Rust later only if binary distribution becomes the blocker.
- [x] Add workflow YAML parsing with structured APIs rather than regex-only
  edits.
- [x] Generate `actions-upgrade-report.json`.
- [x] Generate `actions-upgrade-report.html`.
- [x] Add patch preview mode before any apply mode.
- [x] Add CI gate exit codes:
  - `0`: no blocking findings
  - `1`: blocking findings
  - `2`: scanner cannot run

## P0 - Initial Rules

- [x] Detect deprecated `actions/upload-artifact@v3`.
- [x] Detect deprecated `actions/download-artifact@v3`.
- [x] Detect old cache action/runtime usage.
- [x] Detect Ubuntu runner labels that are likely to drift or brown out.
- [x] Detect broad workflow permissions such as `contents: write` without a
  clear need.
- [x] Detect missing top-level `permissions` blocks.
- [ ] Detect floating major tags where a buyer may prefer pinned SHAs or a
  policy exception.
- [x] Detect composite actions under `.github/actions/`.
- [ ] Detect reusable workflows under `.github/workflows/`.
- [x] Fail closed on dynamic workflow generation, remote reusable workflows, or
  syntax that cannot be safely patched.

## P1 - Proof Fixture

- [x] Create a fixture repo with at least three workflows:
  - a happy-path workflow with artifact/cache issues
  - a permissions-risk workflow
  - an unsupported/dynamic workflow that must fail closed
- [x] Capture before files.
- [x] Run the scanner.
- [x] Save the generated HTML and JSON reports.
- [x] Save patch output.
- [x] Document what changed and what was refused.
- [x] Add tests that assert both findings and generated patches.
- [x] Add one public proof page under `site/proof/actions-upgrade-guard/`.

## P1 - Website Pivot

- [x] Add `/wells/` archive page.
- [x] Add `/wells/github-actions-upgrade-guard/` as the first Well of the
  Month.
- [x] Add `/products/actions-upgrade-guard/`.
- [x] Add `/proof/actions-upgrade-guard/`.
- [x] Add `/framework/` with the product-well doctrine.
- [x] Move SQLAlchemy from homepage flagship to legacy proof/archive positioning.
- [x] Keep existing SQLAlchemy URLs alive to preserve search traffic.
- [x] Add top-nav language that supports multiple wells without feeling like a
  generic blog.
- [x] Add sitemap entries and canonical URLs for the new well/product/proof
  pages.

## P1 - Analytics And Demand Test

- [x] Add route-click tracking for:
  - well-page CTA
  - free scanner/download CTA
  - product page CTA
  - proof page CTA
  - checkout intent
- [x] Replace the Worker `CONVERSION_EVENTS` binding with structured
  `conversion_route` Worker logs and tracked `/go/...` paths so demand can be
  checked without enabling another Cloudflare account feature.
- [x] Confirm live `site/config.js` uses `support@zippertools.org`.
- [x] Rerun the live funnel verifier after deployment.
- [ ] Track GitHub repo views, clones, releases, and downloads for the new
  product.
- [ ] Record all outreach and responses in `docs/lead-tracker.md` or a new
  well-specific lead tracker.

Deployment note: Cloudflare Worker version
`895a399d-6943-4857-92d2-737b8182fb4f` is live, `config.js` serves
`support@zippertools.org`, and the live funnel verifier passes after pushing
commit `4142cb4` so GitHub README targets exist.

## P1 - Seven-Day Well Test

- [ ] Find 20 exact-fit public threads, issues, changelog comments, or repo
  examples around GitHub Actions deprecations.
- [ ] Reply or reach out only where the proof directly helps.
- [ ] Success threshold:
  - 3 people run the free scanner, or
  - 1 serious buyer asks a pricing/scope question, or
  - product/proof pages show repeated qualified movement from exact sources
- [ ] If the threshold is not met, pause the well and reassess instead of
  widening scope.

## P2 - Commercialization

- [ ] Decide the first paid SKU:
  - one-off repo scan bundle
  - annual rule-pack subscription
  - team license
- [ ] Define paid vs free boundaries.
- [ ] Create a sample paid deliverable ZIP.
- [ ] Add Stripe product metadata for the new SKU only after proof demand
  exists.
- [ ] Update terms, refund, privacy, license, and support scope for a
  multi-product Product Wells storefront.
- [ ] Add a "why not actionlint?" comparison page.
- [ ] Add a "why not wait for GitHub?" page only if demand asks for it.

## P2 - Second Product Queue

- [x] Turn Python 3.14 Readiness Pack into a one-page product spec.
- [x] Create `products/python-314-readiness/` as the second new well.
- [x] Identify the first Python 3.14 rules:
  - annotation introspection risk
  - Pydantic compatibility classification
  - dependency version pins
  - CI matrix gaps
  - package metadata blockers
- [x] Add JSON/HTML reporting, safe CI patch preview/apply mode, proof
  fixtures, tests, and commercial-case docs.
- [x] Build ranks 3-6 from the product-wells paper as MVP product packages:
  - Apple Privacy Manifest Composer
  - CRA Evidence Builder
  - ESLint v10 Migration Radar
  - Package Publisher Hardening Pack
- [x] Track rank 3-6 build status in `docs/ranks-3-6-product-task-list.md`.
- [ ] Keep rank 3-6 paid checkout scope paused until product/proof pages and
  exact-fit demand tests show buyer intent.

## P3 - Operating System

- [ ] Build shared report components that all wells can reuse.
- [ ] Build shared rule-pack metadata conventions.
- [ ] Build shared fixture/proof layout.
- [ ] Build shared static site templates for wells, products, proof, and
  archive pages.
- [ ] Add a monthly well review doc generated from the same scoring rubric.
- [ ] Add a kill/promote decision log so the portfolio does not become a pile
  of half-built ideas.
