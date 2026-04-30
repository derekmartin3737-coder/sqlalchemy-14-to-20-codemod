# Max Revenue To-Do

This is the working to-do list for turning `sa20-pack` from a solid proof repo
into the highest-income version of the business under the current constraints.

The detailed go-live execution plan for website, payments, analytics, payout
access, and legal readiness starts in the "Go-Live Stack Decisions" section
near the bottom of this file. That lower section is now the authoritative
checklist for getting from here to a live company that can accept purchases.

Note: Stripe Checkout is now the active checkout provider for new orders. Older
Payhip and Lemon Squeezy items remain in this file only as historical research
or fallback notes unless explicitly updated.

Priority labels:

- `P0`: blocks first sales
- `P1`: strongly increases odds of first revenue
- `P2`: increases revenue after initial traction
- `P3`: optimization after repeatable sales exist

## Current Commercial Status

- [x] Public repo is live.
- [x] Public website is live.
- [x] Stripe Checkout Worker routes are implemented.
- [ ] Stripe payout path is configured and verified.
- [ ] Stripe live-mode checkout has been tested end to end.
- [x] `site/config.js` routes exposed products through `/go/...`.

## Before New Features

These are the remaining non-feature tasks that matter most before investing more
time in wider product coverage. If these stay undone, new transforms may make
the tool better without making the business more likely to earn.

- [ ] Finalize the two paid offers as concrete SKUs:
  - exact product names
  - exact prices
  - exact deliverables
  - exact boundaries
  - exact fulfillment format
- [x] Write the SKU and fulfillment docs so product setup can be pasted into
  the active checkout provider without improvising.
- [ ] Decide whether the public storefront stays on GitHub Pages or moves to
  Cloudflare Pages before paid checkout goes live.
- [ ] Make sure analytics are visible in at least two places:
  - storefront traffic
  - orders and revenue
- [x] Create the operator system for leads and sales:
  - lead tracker
  - launch log
  - support inbox workflow
  - KPI weekly review habit
- [ ] Finish the trust package:
  - 10 public repo trials
  - coverage matrix
  - 2 more demos
  - 1 manual-review-required demo
  - GitHub Action proof on GitHub-hosted runners
- [ ] Finish the legal sanity pass:
  - seller identity decision
  - Oregon/city/county license check
  - trademark conflict search
  - FTC copy review
- [x] Write a claims-and-safeguards document and align the public policy copy
  with it.
- [ ] Tag the first public release and package the launch assets around that
  release, not around a floating branch.
- [ ] Verify the new issue-shaped landing pages in Search Console and Bing.
- [ ] Add one more SQLAlchemy issue page only after a supported pattern proves it deserves search focus.

## P0 — Must Do Before Expecting Real Sales

- [ ] Test the codemod on at least 10 real public SQLAlchemy repos.
- [ ] Build a coverage matrix of what breaks on those repos.
- [ ] Add the top 3 unsupported SQLAlchemy patterns that recur across those repos.
- [ ] Produce 2 more before/after demos beyond the included fixture.
- [ ] Add one demo that ends in `manual_review_required`, not just a happy path.
- [ ] Publish a clear support boundary for what the free tool will never automate.
- [ ] Tighten the migration report so unsupported findings are grouped by pattern and severity.
- [ ] Add a command or preset for scanning a repo without applying changes.
- [x] Add a one-page "Is this repo a fit?" qualification checklist.
- [ ] Add screenshots or copied report excerpts to the launch docs.
- [ ] Validate the GitHub Action end to end on GitHub-hosted runners.
- [ ] Confirm packaging story for public distribution:
  either keep compile-based validation as the official build check or add a clean
  wheel/sdist packaging path.

## P1 — First Revenue Engine

- [x] Turn the paid offering from concept into a concrete package list.
- [x] Define exact free vs paid feature gates in one table.
- [ ] Create a paid "edge-case preset pack" spec with named coverage bundles.
- [x] Replace the old service idea with a second downloadable preset-bundle offer.
- [ ] Write a buyer-facing migration ROI page:
  manual migration hours vs codemod + review workflow.
- [ ] Add a "why pay if the repo is open source?" answer to the pricing docs.
- [x] Create a qualification checklist for inbound leads and buyers.
- [ ] Create a preset-bundle release playbook so the paid layer stays software-only.
- [ ] Make one canonical migration report example for free tier and one for paid tier.
- [ ] Add a stronger comparison against:
  docs-only migration, contractor migration, internal scripts, and "do nothing".

## P1 — Coverage That Buyers Actually Notice

- [ ] Add better handling around `engine.execute(...)` detection and migration guidance.
- [ ] Add more removed legacy `Query` helper detection and classification.
- [ ] Add more loader option patterns where deterministic conversion is safe.
- [ ] Add richer confidence scoring based on ambiguity, not just transform type.
- [ ] Add repo-level summary counts by transform category.
- [ ] Add exit-code guidance to the docs so CI users know what `0`, `1`, and `2` mean.
- [ ] Add fixtures for monorepos and mixed package layouts.
- [ ] Add fixtures for repos that partially pass after migration but still need manual work.
- [ ] Add fixtures for intentionally scary cases that must fail closed.

## P1 — Distribution And Trust

- [x] Publish the repo publicly with a polished README and pinned demo outputs.
- [ ] Add GitHub Releases with tagged snapshots.
- [ ] Decide on PyPI release timing for the free CLI.
- [ ] Add a short video or GIF of the before/after demo.
- [x] Add a static landing page with:
  pain, command, report, before/after, pricing, and support CTA.
- [x] Add issue-shaped landing pages for supported SQLAlchemy search queries.
- [ ] Add social proof targets:
  logos, repo names, anonymized results, or quoted user feedback.
- [ ] Add a docs page specifically for engineering managers who approve migration spend.

## P1 — Launch Work

- [ ] Post in SQLAlchemy, Python, backend, and tooling communities.
- [ ] Open issues or discussions on relevant repos where the tool genuinely helps.
- [ ] Reach out directly to teams discussing 2.0 migration pain in public.
- [ ] Ask early users for sanitized migration reports.
- [ ] Track all launch feedback in one file or issue board.
- [ ] Write versioned release notes after each meaningful coverage improvement.

## P2 — Maximize Revenue After First Customers

- [ ] Create paid presets by repo type:
  Flask, FastAPI, generic service, monorepo, legacy enterprise app.
- [ ] Add richer report exports:
  markdown summary, CSV findings, manager summary, engineering checklist.
- [ ] Add a migration rollout template for multi-repo organizations.
- [ ] Add repo policy docs for safer rollout:
  branch strategy, rollback plan, CI gating, owner signoff.
- [ ] Add a "portfolio mode" for scanning many repos and ranking migration effort.
- [ ] Create an enterprise-safe review pack with docs/templates only.
- [ ] Add migration advisory notes for common ORM performance gotchas after upgrade.

## P2 — Sales Infrastructure Without Paid SaaS

- [ ] Define a lightweight zero-cost lead tracking workflow in markdown or GitHub Issues.
- [ ] Create canned responses for:
  pricing questions, skepticism, scope questions, and unsupported repos.
- [ ] Create a paid handoff checklist so buyers know exactly what they receive.
- [ ] Create a renewal/upsell path:
  new preset packs, broader coverage, and org-wide migration portfolio reviews.

## P3 — Expand Total Revenue Carefully

- [ ] Consider a second migration pack only after this one has real uptake.
- [ ] Consider organization bundles once multiple repos per customer are common.
- [ ] Consider certification-style docs:
  "repo is migrated and validated under this checklist."
- [ ] Consider audit/report-only offerings for teams that will not run a codemod automatically.

## Things We Have Not Done Yet

- [ ] No real customer repo trials yet.
- [ ] No public launch yet.
- [ ] No first paid customer yet.
- [ ] No paid tier implementation yet.
- [ ] No real testimonials or case studies yet.
- [ ] No repeatable sales motion yet.
- [ ] No real GitHub Action usage data yet.
- [ ] No wheel/sdist packaging proof yet in this workspace.
- [ ] No broad SQLAlchemy ecosystem coverage proof yet.
- [ ] No enterprise rollout templates yet.

## Revenue-Critical Assumptions To Test

- [ ] Teams will pay for edge-case coverage instead of doing manual cleanup.
- [ ] SQLAlchemy migration pain is urgent enough to justify a paid add-on.
- [ ] Free version is useful enough to spread but not so complete that paid demand collapses.
- [ ] The preset-bundle offer is differentiated enough that buyers still pay for it.
- [ ] A narrow SQLAlchemy pack can become the default recommendation for this upgrade path.

## Weekly Operator Checklist

- [ ] Add one meaningful transform or classification improvement.
- [ ] Test against at least one more real repo.
- [ ] Improve one sales asset.
- [ ] Improve one proof asset.
- [ ] Improve one paid differentiation asset.
- [ ] Record one thing learned about buyer objections.

## Current Best Next 5

- [ ] Run `sa20-pack` on 10 public SQLAlchemy repos.
- [ ] Turn repeated unsupported patterns into the first paid edge-case preset pack.
- [ ] Create 2 more public demos with stronger before/after value.
- [ ] Publish the repo and launch posts.
- [ ] Land the first paid downloadable-product customer from public migration pain.

## Go-Live Stack Decisions

Assumptions for this plan:

- U.S. seller in Oregon
- current planning date: 2026-04-06
- product remains CLI first, GitHub Action second, website as the storefront
- startup cost must remain exactly $0

Current stack in practice:

- public storefront: Cloudflare storefront at `zippertools.org`
- backup entrypoint: GitHub Pages redirect
- website analytics: Cloudflare Web Analytics path
- checkout: Stripe Checkout through the Cloudflare Worker
- payout path: configure and verify in Stripe
- revenue analytics: Stripe dashboard
- free adoption analytics: GitHub repo traffic, GitHub release downloads, later
  PyPI download proxies if we publish there
- fallback checkout if Stripe blocks us later: Gumroad or Polar

Current best future storefront stack if we want a cleaner commerce host without
paid infrastructure:

- Cloudflare Pages free plan on a `*.pages.dev` subdomain
- Cloudflare Web Analytics

Reality checks:

- No payment platform lets us sell software and withdraw money with zero
  identity, tax, or payout verification.
- "No banking info in the checkout platform" may still be possible depending on
  the configured payout method, but the payout provider itself may still
  require verification and may require a linked bank account or card depending
  on how money is used or withdrawn.
- GitHub Pages is not the right storefront host here. GitHub says Pages is not
  intended for or allowed to run an online business or e-commerce site.
- Exact active-usage analytics for a local CLI do not exist for free by
  default. At launch we can know site traffic, checkout conversions, revenue,
  repo traffic, release downloads, and paid orders. True active usage would
  require opt-in telemetry later.
- The exact $0 startup rule conflicts with some Oregon business-name choices. If
  we sell under a name that is not the seller's "real and true name", Oregon
  requires an Assumed Business Name filing, and that filing has a fee. So the
  clean $0 launch path is probably:
  - sell initially as a sole proprietor under the real legal name, or
  - wait until first revenue to fund a DBA or LLC filing.

Go-live is only complete when all of these are true:

- [x] public website is live on a free public URL
- [x] free repo is public and usable
- [ ] Stripe live checkout is live and can accept real purchases
- [x] payout path is configured and verified
- [ ] website traffic analytics are visibly confirmed in the dashboard
- [ ] order and revenue analytics are visibly confirmed in the dashboard
- [x] terms, refund, privacy, support-scope, and license docs are published
- [ ] one real order has been completed end to end
- [ ] paid deliverable can be accessed without manual intervention
- [ ] we have a written answer for "what happens if validation fails?"
- [x] we have a written answer for "what exactly is included in paid?"

## P0 - Company, Legal, and Money Path

- [ ] Decide whether the launch seller will be:
  - the real legal name as a sole proprietor to preserve the $0 rule, or
  - a branded business name after first revenue funds a filing
- [ ] Record that decision so future sessions stop re-litigating it.
- [ ] Read SBA structure guidance and choose the launch structure:
  sole proprietorship now, or LLC later after revenue justifies it.
- [ ] Check Oregon Business Xpress for any state, city, or county license or
  registration requirements that apply to selling software or digital goods from
  the actual location.
- [ ] Create a dedicated business email.
- [ ] Decide whether to get an EIN even if not strictly required on day one.
- [ ] If we later form an LLC, re-check the current FinCEN BOI rules before
  filing anything.
- [ ] Search the USPTO database and obvious web/package channels for product or
  store name conflicts before leaning into branding.
- [x] Write and publish:
  - Terms of Sale
  - Refund Policy
  - Privacy Policy
  - License Terms
  - Support Scope
  - Limitations
- [ ] Review FTC truth-in-advertising guidance before finalizing launch copy.

## P0 - Website and Public Storefront

- [x] Treat the website as a storefront, not the product itself.
- [x] Treat Cloudflare as the canonical storefront and GitHub Pages as a
  redirect-only backup entrypoint.
- [x] Upgrade `site/index.html` into a production storefront with:
  - clear problem statement
  - exact supported migration
  - before/after demo
  - sample report output
  - free tier CTA
  - paid tier CTA
  - preset bundle CTA
  - limitations
  - FAQ
  - contact path
- [x] Add a visible "Run the free scan first" primary CTA.
- [x] Add a visible "Buy the wider edge-case pack" secondary CTA.
- [x] Add a visible "Get the preset bundle" CTA.
- [x] Add direct links to `README`, demo docs, pricing docs, and limitations.
- [x] Add a policy footer with privacy, refund, terms, and support links.
- [x] Add a simple success page and cancel page for checkout returns.
- [x] Add social metadata and preview image assets.
- [x] Deploy the site publicly.
- [x] Keep the Cloudflare storefront deployed and reachable.
- [x] Write the deployment steps into the repo so another session can redeploy
  without guessing.

## P0 - Analytics and Dashboarding

- [x] Use Cloudflare Web Analytics as the live traffic analytics source.
- [ ] Confirm we can see unique visitors, page views, referrers, and trends.
- [x] Use Stripe dashboards for orders, revenue, refunds, disputes, and payouts.
- [x] Use GitHub repo traffic and release downloads as free-tier adoption
  proxies.
- [ ] If we publish to PyPI later, add PyPI download proxies to the weekly KPI
  review.
- [x] Create one markdown KPI file for weekly snapshots:
  - site visitors
  - CTA clicks
  - orders
  - revenue
  - refunds
  - payout totals
  - GitHub stars/clones/views
  - release downloads
- [ ] Explicitly defer CLI telemetry unless it is opt-in, documented, and worth
  the trust cost.

## P0 - Checkout, Payout Access, and Fulfillment

- [x] Keep Stripe account access and payout path configured.
- [x] Configure the payout method currently approved by the account.
- [ ] Write down the real payout schedule and payout threshold so there is no
  surprise after first sale.
- [ ] Set up Gumroad only as a fallback if Stripe onboarding or payout setup
  blocks us.
- [ ] Finalize the free offer:
  public CLI, public GitHub Action, basic report, limited coverage.
- [ ] Finalize the paid one-time offer:
  wider edge-case coverage, richer reports, presets, and better docs.
- [ ] Finalize the preset-bundle offer as a second downloadable SKU with a
  real versioned artifact.
- [x] Add Stripe checkout metadata for the paid pack.
- [x] Add Stripe checkout metadata for the preset bundle.
- [x] Add Stripe checkout metadata for the Pydantic apply pack.
- [ ] Define the paid deliverable format:
  versioned ZIP, private wheel, add-on pack, or private release asset.
- [ ] Prefer automatic artifact delivery through `/stripe/delivery` over manual
  email fulfillment.
- [ ] Create install/update instructions for the paid pack.
- [ ] Test one complete fulfillment path from checkout success to buyer
  download.
- [ ] Do not claim the company is open until one real purchase flow works end to
  end.

## P0 - Trust Assets Needed Before Launch

- [x] Update `README` so it points to the website, free quickstart, demo report,
  paid pack page, and support path.
- [x] Make `docs/demo.md` strong enough to act as proof, not just explanation.
- [x] Make `docs/pricing.md` match the real store products and checkout links.
- [x] Add a comparison page:
  manual migration vs free scan vs paid pack vs preset bundle.
- [x] Add a "Who should not buy this?" section.
- [x] Add a "What happens if validation fails?" section.
- [x] Add a "What the paid pack does not cover" section.
- [x] Add screenshots or pasted excerpts from machine-generated reports.

## P1 - Revenue-Proofing Before Public Launch

- [ ] Test the codemod on at least 10 real public SQLAlchemy repos.
- [ ] Build a coverage matrix of repeated breakages and unsupported patterns.
- [ ] Add the top recurring unsupported SQLAlchemy patterns.
- [ ] Produce at least 2 more public demos beyond the included fixture.
- [ ] Add one demo that ends in `manual_review_required`.
- [ ] Tighten the migration report so unsupported findings are grouped by pattern
  and severity.
- [ ] Add a command or preset for scanning without applying changes.
- [ ] Validate the GitHub Action end to end on GitHub-hosted runners.
- [ ] Decide whether compile-only build verification is enough or whether the
  free CLI needs clean wheel/sdist proof before release.

## P1 - First Sales Motion

- [x] Publish the repo publicly with a polished README.
- [ ] Create tagged GitHub Releases.
- [ ] Decide when to publish the free CLI to PyPI.
- [x] Publish the storefront site.
- [ ] Add the live checkout links.
- [ ] Post in SQLAlchemy, Python, backend, and tooling communities.
- [ ] Reach out to teams discussing SQLAlchemy 2.0 migration pain in public.
- [ ] Track every lead, objection, and conversion in one markdown file or issue
  board.
- [ ] Record where each buyer came from.
- [ ] Rewrite the site around the objections actual buyers raise.

## P2 - Repeatable Revenue

- [ ] Create paid presets by repo type:
  Flask, FastAPI, generic service, monorepo, legacy enterprise app.
- [ ] Add richer report exports:
  markdown summary, CSV findings, manager summary, engineering checklist.
- [ ] Add rollout docs for multi-repo organizations.
- [ ] Add branch strategy, rollback plan, CI gating, and owner-signoff
  templates.
- [ ] Add a support knowledge base so repeat questions do not turn into custom
  labor.
- [ ] Review monthly metrics and answer:
  - Which sources convert?
  - Which unsupported patterns drive paid purchases?
  - Which objections kill deals?
  - Which docs close deals?

## Official References Checked On 2026-04-06

- GitHub Pages limits:
  https://docs.github.com/enterprise-cloud@latest/pages/getting-started-with-github-pages/github-pages-limits
- Cloudflare Pages docs and limits:
  https://developers.cloudflare.com/pages/platform/
  https://developers.cloudflare.com/pages/platform/limits/
- Cloudflare Web Analytics:
  https://developers.cloudflare.com/web-analytics/about/
- Cloudflare Pages product page:
  https://www.cloudflare.com/developer-platform/products/pages/
- Lemon Squeezy getting paid, payments, fees, and supported countries:
  https://docs.lemonsqueezy.com/help/getting-started/getting-paid
  https://docs.lemonsqueezy.com/help/payments
  https://docs.lemonsqueezy.com/help/getting-started/fees
  https://docs.lemonsqueezy.com/help/getting-started/supported-countries
- SBA business structure and EIN guidance:
  https://www.sba.gov/business-guide/launch-your-business/choose-business-structure
  https://www.sba.gov/business-guide/launch-your-business/get-federal-state-tax-id-numbers
- IRS EIN information:
  https://www.irs.gov/formss4
- Oregon business registration, DBA rules, and license directory:
  https://sos.oregon.gov/business/Pages/doing-business-means.aspx
  https://sos.oregon.gov/business/Pages/obr-assumed-business-name-registration.aspx
  https://apps.oregon.gov/SOS/LicenseDirectory/
- FTC truth in advertising and endorsement guidance:
  https://www.ftc.gov/business-guidance/resources/advertising-faqs-guide-small-business
  https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides
- USPTO trademark search guidance:
  https://www.uspto.gov/trademarks/search
  https://www.uspto.gov/trademarks/search/federal-trademark-searching
- FinCEN BOI update:
  https://www.fincen.gov/index.php/boi/toolkit
