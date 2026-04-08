# Launch Readiness

This file is the practical truth table for whether the business is actually
ready to go public.

## Repo-side assets completed

- storefront pages exist under `site/`
- checkout/seller/analytics values are centralized in `site/config.js`
- Cloudflare deployment config exists in `wrangler.jsonc`
- policy docs exist
- claims-and-safeguards doc exists
- pricing, demo, and deployment docs exist
- product, fulfillment, release, sales-ops, and legal docs now exist
- KPI tracking doc exists
- launch-check command exists at `python -m sa20_pack.launch_readiness`

## External actions still required before live revenue

- create the Cloudflare production project or keep the current GitHub Pages site
- create the Lemon Squeezy products
- paste the live checkout URLs into `site/config.js`
- enable storefront traffic analytics
- make one real test purchase

## When to call it live

Call the business live only after:

1. the public site is deployed
2. the repo is public
3. the paid checkout buttons are live
4. analytics are visible
5. one real order completes end to end
6. the paid deliverable path has been tested without manual intervention

## Launch-day checks

- homepage loads
- pricing page loads
- policy page loads
- demo page loads
- repo link works
- free CTA works
- paid CTA works
- preset-bundle CTA works
- success/cancel pages work
- policy docs match site copy
