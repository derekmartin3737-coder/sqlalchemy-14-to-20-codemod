# Payhip webhook setup

The live storefront uses a Cloudflare Worker wrapper so Payhip can send sale
events to:

```text
https://zippertools.org/payhip/webhook
```

## Cloudflare secret

Set this as a Cloudflare Worker secret, not a public variable and not a tracked
repo file:

```text
PAYHIP_API_KEY
```

Payhip includes a `signature` property in webhook payloads. The Worker verifies
that value against `sha256(PAYHIP_API_KEY)` before accepting an event.

## Payhip developer settings

In Payhip Developer settings:

- Webhook endpoint: `https://zippertools.org/payhip/webhook`
- Events: `paid`, `refunded`

The endpoint returns `200` only after signature verification passes. If the
secret is missing, it returns `503` so Payhip retries instead of silently
accepting unverified events.

## Current storage behavior

Accepted webhooks are logged with a redacted event summary:

- event type
- transaction or subscription id
- currency and price
- product ids, product names, product keys, quantities, coupon flag

The Worker intentionally does not log customer email or IP address.
