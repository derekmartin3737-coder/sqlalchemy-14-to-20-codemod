# Distribution Playbook

This is the free acquisition plan for turning the storefront into the default
answer for a narrow migration problem.

The core rule is simple:

- win exact-problem search before broad category search
- let GitHub establish trust
- let the storefront convert
- let checkout stay boring

## Primary acquisition loop

1. Publish one indexable page for each painful query we already support.
2. Keep the homepage and pricing page focused on product trust and conversion.
3. Use the public repo as proof, not as the only discoverability surface.
4. Submit the sitemap to search engines and watch what actually gets
   impressions.
5. Expand only into issue pages we can honestly support today.

## Why this aligns with the business

- free: no ads, no paid tooling, no paid hosting requirement
- max revenue: long-tail problem pages attract buyers who already feel pain
- trust: repo, demo, and explicit limits stop the site from sounding like fake
  "AI migration" marketing

## What we should try to rank for

Rank for problem-shaped queries, not only product-shaped queries.

Examples for the root SQLAlchemy product:

- `session.query get sqlalchemy 2.0`
- `select([columns]) sqlalchemy 2.0`
- `declarative_base sqlalchemy 2.0 import`
- `sqlalchemy 1.4 to 2.0 migration tool`
- `sqlalchemy upgrade codemod`

The site now has dedicated landing pages for the first three issue-shaped
queries above.

## Technical baseline

The storefront should always have:

- canonical URLs on indexable pages
- a sitemap
- `robots.txt` pointing at the sitemap
- product-detail pages for paid packs
- noindex on success/cancel/404 pages
- titles and descriptions that match the actual upgrade pain

## Manual dashboard actions

These still need to be done in dashboards, not in git:

1. Verify the Cloudflare storefront in Google Search Console.
2. Submit `https://zippertools.org/sitemap.xml` to Google.
3. Verify the storefront in Bing Webmaster Tools.
4. Submit the same sitemap to Bing.
5. Turn on Cloudflare Web Analytics in the Cloudflare dashboard if it is not
   already enabled.

## GitHub discoverability

The public repo should help discovery but not leak paid value.

Manual repo settings to keep aligned:

- description:
  `Free SQLAlchemy 1.4 to 2.0 migration scanner with buyer-visible reports and commercial apply packs.`
- topics:
  - `sqlalchemy`
  - `sqlalchemy-2`
  - `python`
  - `codemod`
  - `migration`
  - `orm`
  - `developer-tools`

The README should keep exact supported-issue language near the top so repo
search and external linking stay specific.

## Content loop

Every time we add a supported pattern:

1. update the product spec
2. add or tighten a proof example
3. publish or refresh one issue-shaped landing page
4. note the change in release notes
5. mention the exact issue wording in the README

## What not to do

- do not chase broad "AI code migration" keywords
- do not create pages for unsupported patterns just to capture traffic
- do not promise full-repo automation
- do not let checkout pages become the only product explanation

## Success metrics

Watch these first:

- search impressions on issue pages
- click-through rate from issue pages
- free scan clicks from issue pages
- paid checkout clicks from issue pages
- orders tied to the main SQLAlchemy pack

If issue pages get impressions but no clicks, fix titles and descriptions.
If they get clicks but no checkout movement, tighten the fit explanation and
buying rule.
