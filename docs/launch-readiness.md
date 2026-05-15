# Launch Readiness

This file is the practical truth table for whether the business is actually
ready to sell under the current Product Wells direction.

Status as of 2026-05-14: the SQLAlchemy storefront proved the checkout and
proof infrastructure, but the active launch target is moving to an autonomous
Product Wells site with GitHub Actions Upgrade Guard as the first new well.

## Repo-side assets completed

- autonomous product-well doctrine exists in
  `docs/autonomous-product-wells.md`
- active pivot checklist exists in `docs/product-wells-todo.md`
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

- keep the Cloudflare storefront deployed and current
- keep the Stripe Worker secrets and paid KV artifact ZIPs current
- enable storefront traffic analytics
- make one real test purchase
- verify the live site is serving the current support address and config
- make the Product Wells homepage, well archive, and active product page live
- publish a proof page for GitHub Actions Upgrade Guard before asking for
  checkout

## When to call it live

Call the business live only after:

1. the public site is deployed
2. the repo is public
3. the current Well of the Month has a working proof artifact
4. the active product has a free scanner/report path
5. analytics are visible
6. paid checkout buttons are live only for products with proof demand
7. one real order completes end to end
8. the paid deliverable path has been tested without manual intervention

## Launch-day checks

- homepage loads
- wells archive loads
- active well page loads
- active product proof page loads
- scan page loads
- pricing page loads
- policy page loads
- demo page loads
- repo link works
- free CTA works
- paid CTA works
- automated fit-report CTA works if exposed
- no human-assisted migration or PR-service CTA is exposed
- preset-bundle CTA works
- pydantic-pack CTA works if exposed on the site
- Stripe Checkout pages load
- `/stripe/delivery` verifies a paid test session before opening a product file
- success/cancel pages work
- policy docs match site copy
