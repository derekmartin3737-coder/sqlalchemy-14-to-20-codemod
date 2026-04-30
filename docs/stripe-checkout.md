# Stripe Checkout Setup

Last updated: 2026-04-30

This replaces Payhip checkout with repo-controlled Stripe Checkout Sessions
created by the Cloudflare Worker.

## What Stripe owns

- secure card checkout
- receipts
- payment records
- refund/dispute dashboard
- webhook events

## What the Worker owns

- product names, descriptions, prices, and checkout routing
- `/go/...` conversion tracking
- Checkout Session creation
- Stripe webhook signature verification at `/stripe/webhook`
- post-payment KV artifact delivery at `/stripe/delivery`

The Worker uses inline Stripe `price_data`, so the product names and prices live
in `worker/index.mjs`. You do not need to manually create Stripe products first.

## Dashboard setup

Use the Stripe account that will receive Zipper Tools payouts.

1. In Stripe, set the public business/profile details:
   - public business name: `Zipper Tools`
   - support email: `zippers3737@gmail.com`
   - support site: `https://zippertools.org/`
   - statement descriptor: `ZIPPERTOOLS`
2. Start in test mode.
3. Copy the test secret key from **Developers -> API keys**.
4. Add a webhook endpoint in **Developers -> Webhooks**:
   - endpoint URL: `https://zippertools.org/stripe/webhook`
   - events:
     - `checkout.session.completed`
     - `checkout.session.async_payment_succeeded`
     - `checkout.session.async_payment_failed`
5. Copy the webhook signing secret.

## Cloudflare secrets

Set these as Worker secrets, never in `site/config.js` and never in git:

```powershell
npx.cmd wrangler secret put STRIPE_SECRET_KEY
npx.cmd wrangler secret put STRIPE_WEBHOOK_SECRET
```

Paid artifacts are stored as chunked base64 values in the private Cloudflare
Workers KV namespace bound as `PAID_ARTIFACTS`. The Worker verifies the Stripe
Checkout Session, reconstructs the matching ZIP from KV, and streams it to the
buyer.

Do not put paid ZIPs in the public repo or link to them directly from site
HTML.

The old `site/__stripe_paid_assets/` staging path is still blocked by the
Worker, but live delivery should use KV so no paid artifact has a public asset
URL.

Optional:

```powershell
npx.cmd wrangler secret put STRIPE_AUTOMATIC_TAX_ENABLED
```

Use `true` only after Stripe Tax is configured. Leave it unset while testing.

## Test checkout

1. Deploy the Worker with test Stripe secrets.
2. Open `https://zippertools.org/go/sa20-pack/test`.
3. Confirm Stripe Checkout shows:
   - `SQLAlchemy 1.4 to 2.0 Migration Cleanup Pack`
   - `$299.99`
   - no inventory/scarcity text
   - no ZIP-size framing
4. Pay with a Stripe test card.
5. On the success page, click `Open delivery`.
6. Confirm `/stripe/delivery` verifies the session and downloads the matching
   product ZIP.
7. Confirm the webhook event appears in Cloudflare logs as
   `stripe_checkout_paid`.

## Go live

1. Replace the test secret key with the live Stripe secret key.
2. Create the same live webhook endpoint in Stripe live mode.
3. Replace `STRIPE_WEBHOOK_SECRET` with the live webhook signing secret.
4. Confirm the `PAID_ARTIFACTS` KV namespace contains all four paid ZIP keys
   before deploy.
5. Make one low-risk live purchase and refund it from Stripe if needed.

## Ditch Payhip

After Stripe test and live checkout both work:

1. Remove or unpublish Payhip product pages.
2. Remove the Payhip webhook endpoint from Payhip developer settings.
3. Stop sending traffic to the old Payhip custom-domain checkout.
4. Keep old Payhip order records for accounting and support history.
5. Use Stripe for new orders, refunds, and payout tracking.
