# Deployment

This is the repo-side deployment guide for launching the public storefront and
viewing progress after launch.

## Fastest free public deployment

The repo now includes a GitHub Pages workflow in
[`deploy-site.yml`](../.github/workflows/deploy-site.yml).

That is the fastest zero-cost way to get a public URL online from this repo.
Current live URL:

- `https://derekmartin3737-coder.github.io/sqlalchemy-14-to-20-codemod/`

For Cloudflare, the repo now also includes
[`wrangler.jsonc`](../wrangler.jsonc)
so the static storefront can be deployed with `npx wrangler deploy` instead of
re-entering asset settings by hand. Right now the public site exists, but paid
checkout is still blocked on the first two Lemon products being created and
their hosted checkout URLs being added to `site/config.js`.

## 1. Fill the launch config

Edit [`site/config.js`](../site/config.js) and replace:

- `sellerName`
- `contactEmail`
- `repoUrl`
- `paidPackUrl`
- `presetBundleUrl`

Use [`site/config.example.js`](../site/config.example.js) as the reference format.

## 2. Create the checkout products

In Lemon Squeezy:

1. create the one-time migration-pack product
2. create the preset-bundle product
3. set the return URLs to:
   - `https://YOUR-SITE.pages.dev/success.html`
   - `https://YOUR-SITE.pages.dev/cancel.html`
4. copy the hosted checkout URLs into `site/config.js`

## 3. Deploy the storefront

Use Cloudflare and connect the GitHub repo.

Recommended settings:

- Build command: leave empty
- Deploy command: `npx wrangler deploy`
- Path: `/`
- Repo config: `wrangler.jsonc` already points at `./site`

That makes the static `site/` folder the public website.

## 4. Turn on analytics

In Cloudflare Web Analytics:

1. create the analytics property for the site
2. if you use the Pages project one-click Web Analytics setup, no repo change is
   needed
3. if you prefer manual snippet mode, copy the analytics token into
   `site/config.js`
4. redeploy if you changed the repo config

The site script already knows how to load the analytics beacon once the token is
present.

## 5. Publish the repo

Make the GitHub repo public and confirm the `repoUrl` in `site/config.js`
matches the real public repo URL.

## 6. Verify the launch path

Before announcing anything:

1. open the public site
2. verify free CTA, paid CTA, and preset-bundle CTA all work
3. verify success and cancel pages load
4. verify policy links work
5. verify analytics appear in Cloudflare
6. verify at least one real checkout works end to end
7. run `python -m sa20_pack.launch_readiness`

## 7. Where to view progress

After launch, check:

- Cloudflare Web Analytics for site traffic
- Lemon Squeezy for orders, revenue, refunds, and payouts
- GitHub traffic for repo views and clones
- the manual KPI tracker in [kpi-dashboard.md](kpi-dashboard.md)
