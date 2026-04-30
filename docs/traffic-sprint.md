# Five-Day Discovery Sprint

This is the honest version.

There is no reliable free, Codex-only method that can guarantee `1000` views per
day within `5` days on a brand-new domain with a weak link graph. What Codex can
do is maximize the things that are actually under repo control:

- publish more high-intent exact-problem pages inside the products' supported
  subset
- tighten internal linking so every page helps discovery
- generate clean crawl/indexing artifacts on every deploy
- make it easy to submit updated URLs to search engines
- keep messaging narrow so impressions are more likely to come from the right
  queries instead of broad, low-conversion traffic

If `1000/day` happens, it will come from a mix of indexing, query coverage, and
real external references. The repo can improve the first two immediately and
prepare assets for the third.

## What Codex Can Fully Do

- [x] Generate exact-problem guide pages for the live supported products
- [x] Generate family hub pages and product pages with internal links
- [x] Generate sitemap files, `robots.txt`, and a deploy-time site manifest
- [x] Add an IndexNow key file and automated IndexNow submission script
- [x] Wire the discovery build into the GitHub Pages deploy workflow
- [x] Improve homepage and pricing-page links into the discovery pages
- [x] Expand the exact-problem page set from `12` pages to `30`
- [x] Expand the exact-problem page set from `30` pages to `41`
- [x] Draft discussion-reply copy that links to issue pages instead of checkout
- [x] Add a query-to-page map so new demand can turn into new pages quickly

## What Still Requires a Human Login

- Google Search Console URL inspection / request indexing
- Bing Webmaster Tools submission checks
- GitHub repo "About" description, website, and topic edits
- Posting links into live SQLAlchemy discussions
- Reading real search-impression data from Google Search Console

Those items matter, but they are not repo-native automation tasks.

## Five-Day Queue

### Day 1

- [x] Ship the static discovery build
- [x] Publish hub pages, product pages, and exact-problem pages
- [x] Publish split sitemaps and `robots.txt`
- [x] Add deploy-time IndexNow submission

### Day 2

- [x] Add the next `10-15` exact-problem pages, but only for supported patterns
- [x] Add direct links from hub pages to the highest-intent product pages
- [x] Add product-page schema improvements with Product/Offer structured data

### Day 3

- [x] Draft exact discussion replies for the live SQLAlchemy threads already in
      `docs/discovery-playbook.md`
- [x] Add a simple "related fixes" block to every exact-problem page
- [x] Add more product-adjacent pages for Pydantic and ESLint search terms that
      match the documented supported subset

### Day 4

- [x] Review the first Cloudflare traffic read
- [x] Replace placeholder checkout URLs with tracked internal `/go/...` routes
- [x] Redirect high-traffic legacy landing-page slugs to the current guide and
      product URLs
- [x] Fix the missing favicon probe with a redirect to the SVG favicon
- [x] Add exact error-message pages for SQLAlchemy and Pydantic searches
- [x] Add SQLAlchemy triage and manual-vs-codemod decision pages
- [x] Add a README discovery table linking directly to the strongest pages
- [x] Publish a SQLAlchemy public-proof page and link it from the product,
      problem pages, homepage, and README
- [ ] Review the first indexing results and impressions if available
- [ ] Double down on any pages that are indexed but still thin on internal links
- [ ] Add the next batch of exact-problem pages based on real wording from docs,
      discussions, and issue titles

### Day 5

- [ ] Keep only the pages that are specific, honest, and linked
- [ ] Remove any broad claims that dilute intent
- [ ] Prioritize homepage visits, problem-page visits, indexed URL count,
      impressions, and clicks over vanity activity

## Rules For This Sprint

- Do not change pricing during the indexing window
- Do not broaden claims beyond the supported subset
- Do not spend time on generic blog posts
- Do not chase day-to-day indexation noise
- Do not build pages for unsupported migrations just to inflate URL count

## Success Metrics

Track these in order:

1. indexed pages
2. search impressions
3. search clicks
4. visits to the exact-problem pages
5. visits to the product pages
6. requests to `/go/sa20-pack`, `/go/sa20-preset`, and
   `/go/pydantic-v2-porter`

Do not treat orders as the first signal. On a new domain, impressions and
indexation are the leading indicators.

The daily operator table now lives in
[`traffic-war-room.md`](traffic-war-room.md). Use that file for Search Console
status, page diagnosis, and next actions by priority URL.

## 2026-04-14 Cloudflare Baseline

As of 2026-04-14 19:45 PDT, Cloudflare showed `202` visits and `891`
requests for the preceding roughly 24-hour window. The homepage had `69` visits
and the highest-volume SQLAlchemy pages were still below `25` visits each.

Fixes shipped immediately after that read:

- live checkout placeholders were replaced with tracked `/go/...` routes
- root-level legacy SQLAlchemy and Pydantic landing URLs were redirected to the
  current canonical guide/product pages
- product pages now include direct checkout CTAs
- the policy page now names the active checkout provider
- `favicon.ico` no longer returns a 404

The working query-to-page map now lives in `site/_site_manifest.json`, which
includes every generated guide slug, its search term, and its canonical URL.

## 2026-04-15 Redirect And Recovery Pass

The first four-hour follow-up showed healthy guide-page growth but still showed
avoidable redirect noise, flat product-page movement, low checkout-route volume,
and a few 404s. The follow-up fix shipped these changes:

- internal guide/product/navigation links now use clean public URLs instead of
  `index.html` or top-level `.html` URLs
- sitemaps now publish extensionless static URLs such as `/pricing` and `/demo`
- stale `index.html` and `.html` URL variants now 301 to the canonical clean
  URLs
- high-intent error-message aliases now include `.html` and common wording
  variants
- the live site now has a real `/favicon.svg` target
- Cloudflare Workers static assets now use the custom 404 page, so real 404s
  still offer links into the highest-intent migration pages
- generated guide pages now include a secondary free-scan CTA beside the
  matching product-page CTA
- product pages now pair the checkout CTA with a free-scan CTA to preserve the
  scanner-first promise

## 2026-04-16 Search Console Rejection Fix

Search Console reported redirect-related rejection on submitted pages. The
follow-up audit found two real issues:

- `/pricing` and `/demo` were submitted as clean URLs, but their page canonicals
  still pointed at `/pricing.html` and `/demo.html`
- static pages and launch docs still contained old `.html` links that resolved
  through redirects

Fixes shipped:

- static page canonicals and Open Graph URLs now use final clean URLs
- internal links on indexable static pages now avoid `.html` and `index.html`
  targets
- docs and launch copy now use clean canonical `zippertools.org` URLs
- old SKU-style URLs now 301 to the current product, pricing, or guide pages
- `scripts/audit_site_urls.py` now audits sitemap URLs, canonicals, and
  internal links so this rejection class can be caught before resubmission

Current Search Console rule: submit only final clean URLs. Treat old `.html`
pages as legacy aliases, not index targets.
