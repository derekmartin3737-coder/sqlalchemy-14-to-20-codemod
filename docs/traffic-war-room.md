# Traffic War Room

This is the daily control room for the `1000` qualified visits/day push.

Qualified traffic means visitors landing on exact-problem pages that can
reasonably move to a product page, the free scan, or a tracked checkout route.
Do not use homepage visits or bot-heavy request counts as the main signal.

## Current Target

- Baseline from 2026-04-15 01:03-21:03 PDT: `128` Cloudflare visits in
  `20` hours, roughly `154` visits/day extrapolated.
- Goal: `1000` qualified visits/day.
- Latest Cloudflare snapshot from 2026-04-16 22:22 PDT: `1446` page views and
  `1311` qualified visits in the previous `24` hours.
- Remaining qualified-visit gap: `0` in Cloudflare's raw site analytics, but
  Search Console still has to confirm organic indexing and impressions.
- Current bottleneck: product/proof traffic is present, but paid Stripe
  checkout intent is still thin. Compare paid `/go/sa20-pack`,
  `/go/sa20-preset`, `/go/pydantic-v2-porter`, and `/go/fit-report` requests
  against product visits, not total site traffic or free-scan clicks.

## Daily Morning Checklist

Run this once each morning, not hour by hour.

1. Open Google Search Console.
2. Inspect each priority URL below.
3. Record whether Google says the page is indexed.
4. Record Google-selected canonical, impressions, clicks, and average position.
5. Re-submit only pages that are not indexed or have a bad canonical.
6. Check Cloudflare for guide visits, product visits, and `/go/...` requests.
7. Decide the page's current bottleneck using the decision rules below.

Cloudflare command:

```powershell
$env:CLOUDFLARE_API_TOKEN = "<token with zone analytics read>"
$env:CLOUDFLARE_ZONE_ID = "<zippertools.org zone id>"
node scripts\cloudflare_traffic_snapshot.mjs --hours 24
```

Stripe checkout health check:

```powershell
node --check worker\index.mjs
python -m pytest tests\test_worker_routes.py -p no:cacheprovider
```

Use this when paid `/go/...` requests look broken. The check verifies that the
Worker creates Stripe Checkout Sessions and that post-payment delivery verifies
the Stripe session before opening an artifact URL.

## Priority Pages

| Page | Indexed? | Google canonical | Impressions | Clicks | Avg position | Product clicks | Free-scan clicks | `/go` clicks | Diagnosis | Next action |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `https://zippertools.org/` |  |  |  |  |  |  |  |  |  |  |
| `https://zippertools.org/products/sa20-pack/` |  |  |  |  |  |  |  |  |  |  |
| `https://zippertools.org/proof/sqlalchemy-public-proof/` |  |  |  |  |  |  |  |  |  |  |
| `https://zippertools.org/sqlalchemy/engine-execute-removed/` |  |  |  |  |  |  |  |  |  |  |
| `https://zippertools.org/sqlalchemy/optionengine-execute-error/` |  |  |  |  |  |  |  |  |  |  |
| `https://zippertools.org/sqlalchemy/session-query-get/` |  |  |  |  |  |  |  |  |  |  |
| `https://zippertools.org/sqlalchemy/session-query-migration/` |  |  |  |  |  |  |  |  |  |  |
| `https://zippertools.org/sqlalchemy/joinedload-all-removed/` |  |  |  |  |  |  |  |  |  |  |
| `https://zippertools.org/sqlalchemy/sqlalchemy-20-triage-checklist/` |  |  |  |  |  |  |  |  |  |  |
| `https://zippertools.org/pydantic/basesettings-import-error/` |  |  |  |  |  |  |  |  |  |  |
| `https://zippertools.org/eslint/eslintrc-to-flat-config/` |  |  |  |  |  |  |  |  |  |  |
| `https://zippertools.org/demo` |  |  |  |  |  |  |  |  |  |  |

## Decision Rules

Use one diagnosis per page.

- `not indexed`: resubmit the URL, verify the sitemap includes it, and add one
  internal link from a related hub or product page.
- `indexed, no impressions`: tighten topical alignment and consider one exact
  external citation later.
- `impressions, weak clicks`: rewrite title/meta around the exact error or API
  breakage users are searching.
- `clicks, weak product movement`: improve the bridge from the direct answer to
  the matching product and free scan.
- `product clicks, weak /go`: add proof and clearer deliverable language before
  checkout.
- `/go rises, purchases weak`: review price framing, checkout trust, and whether
  the page promise matches the Stripe checkout product.

## Stripe Checkout Triage

Stripe Checkout visits are not the same as Zipper Tools page views.

- Cloudflare `/go/...` requests show checkout intent before Stripe conversion.
- Stripe Checkout Sessions show whether visitors reached payment.
- Stripe completed sessions show real purchases.
- Webhook logs confirm whether checkout completion reached the Worker.
- If Cloudflare shows paid `/go/...` requests but Stripe has no sessions,
  inspect Worker logs and the `STRIPE_SECRET_KEY` secret first.

## Current Week Plan

| Day | Operator move | Status | Notes |
| --- | --- | --- | --- |
| 1 | GSC audit for priority URLs, resubmit only final clean URLs | pending | Do manually in Search Console. |
| 2 | Edit controllable public replies to canonical URLs | pending | Use clean URLs, never `.html`. |
| 3 | Sharpen GitHub topics and repo discovery wording | done | Repo About now points to `https://zippertools.org/` and uses exact-intent migration topics. |
| 4 | Publish one proof asset | done | `/proof/sqlalchemy-public-proof/` links supported and fail-closed public-file examples. |
| 5 | Place one exact-fit outreach reply | pending | One canonical URL, exact problem only. |
| 6 | Recheck GSC and diagnose each priority page | pending | Pick the next lever by bucket. |
| 7 | Second outreach shot or conversion repair | pending | Depends on Day 6 diagnosis. |

## Canonical URL Rules

- Submit only final clean URLs to Google and Bing.
- Do not submit `.html` or `/index.html` URLs.
- Public replies should use exact canonical URLs.
- Legacy `.html` URLs may redirect, but they should not be the URLs we promote.

## Daily Notes

| Date | What changed | Signal | Decision |
| --- | --- | --- | --- |
| 2026-04-16 | War-room tracker created; sitemap/canonical audit added to repo workflow; SQLAlchemy public proof page added. | Pending GSC baseline. | Start with indexing and proof, not more pages. |
| 2026-04-16 21:24 PDT | Cloudflare GraphQL snapshot added via `scripts/cloudflare_traffic_snapshot.mjs`. | `1173` page views, `942` qualified visits, `84` product visits, `6` proof visits, `5` `/go` requests in prior `24` hours. | Raw 1000/day is reached, qualified visits are close, checkout intent is still thin; next lever is indexing attribution and product-to-checkout trust. |
| 2026-04-16 22:03 PDT | GitHub repo About description, website, and topics updated. | Public repo now carries the same narrow SQLAlchemy migration positioning as the storefront. | Keep all future public links pointed at canonical clean URLs. |
| 2026-04-16 22:08 PDT | GitHub release `v0.1.0` created for the public scanner/discovery baseline. | Release URL: `https://github.com/derekmartin3737-coder/sqlalchemy-14-to-20-codemod/releases/tag/v0.1.0`. | Use the release as a public trust marker, not as a broad migration claim. |
| 2026-04-16 22:21 PDT | Product-to-intent repair deployed through Cloudflare Worker version `3a69b325-0b4d-40e9-b9b0-e081dc9227bd`. | Static buttons now route through `/go/free-scan`, `/go/sa20-pack`, `/go/sa20-preset`, and `/go/pydantic-v2-porter`; product pages now lead with a decision block and tracked CTAs. | Compare `/go/free-scan` and product-specific `/go/...` requests over the next 24 hours before changing pricing. |
| 2026-04-16 22:22 PDT | Cloudflare 24-hour snapshot after the conversion repair. | `1446` page views, `1311` qualified visits, `106` product visits, `13` proof visits, `4` `/go/...` requests. | The traffic goal is crossed in Cloudflare, so the operating metric is now paid checkout-route intent per product visit. |
