# Fulfillment

Last updated: 2026-04-30

This file locks the delivery path before the first real sale.

## Fulfillment policy

Use automatic delivery first. Do not make manual email fulfillment the default.

Preferred delivery path:

1. upload each paid artifact to the private Cloudflare Workers KV namespace
   bound as `PAID_ARTIFACTS`
2. let Stripe Checkout return buyers to `/success?session_id=...`
3. let `/stripe/delivery` verify the paid Checkout Session
4. stream the matching ZIP from the KV binding only after
   payment verification

Why this path:

- checkout copy and pricing stay repo-controlled
- lower support burden
- easier repeat purchases and updates
- no private repo access required for normal buyers
- no human delivery step after purchase
- no hidden third-party download URL to keep in sync

## Paid pack artifact

Artifact name pattern:

- `sa20-pack-edge-case-pack-vX.Y.Z.zip`

Archive contents:

- `README.md`
- `INSTALL.md`
- `COVERAGE.md`
- `CHANGELOG.md`
- `manager-summary.md`
- `rollout-checklist.md`
- the paid add-on package or paid preset files

Release rules:

- version every paid pack upload
- do not silently replace a file without bumping the version
- keep one matching public changelog entry for buyer trust

## Preset bundle artifact

Artifact name pattern:

- `sa20-pack-preset-bundle-vX.Y.Z.zip`

Archive contents:

- `README.md`
- `PRESETS.md`
- `report-templates/`
- `manager-summary-template.md`
- `rollout-checklist.md`
- `limitations.md`

## What the public site should promise

Only promise:

- automatic access to the purchased file bundle
- the published scope and boundaries
- the published preset coverage and included templates

Do not promise:

- custom repo fixes on purchase
- custom coding by a person
- full migration completion

## Stripe delivery notes

Stripe is the checkout layer for new orders. The Worker owns the product
catalog and delivery redirect:

- `/go/sa20-pack` creates a Stripe Checkout Session
- `/go/sa20-preset` creates a Stripe Checkout Session
- `/go/pydantic-v2-porter` creates a Stripe Checkout Session
- `/go/fit-report` creates a Stripe Checkout Session
- `/stripe/webhook` verifies Stripe webhook signatures
- `/stripe/delivery` verifies the paid session before streaming the configured
  paid KV artifact

Required KV artifact keys:

- `sa20-pack-edge-case-pack.zip`
- `sa20-pack-preset-bundle.zip`
- `pydantic-v2-porter.zip`
- `fit-report-add-on.zip`

Do not enable a product route publicly until the matching KV key exists and
`/stripe/delivery` can fetch it after a paid session.
