# Fulfillment

Last updated: 2026-04-09

This file locks the delivery path before the first real sale.

## Fulfillment policy

Use automatic delivery first. Do not make manual email fulfillment the default.

Preferred delivery path:

1. upload a versioned ZIP to Payhip
2. include supporting links to docs already hosted on the public site or repo
3. let Payhip handle the download path from the receipt and customer order page

Why this path:

- zero required backend infrastructure
- lower support burden
- easier repeat purchases and updates
- no private repo access required for normal buyers

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

## Payhip notes

Payhip's live launch path for this repo is:

- products are downloadable digital goods
- customers receive receipt and download access from the checkout flow
- storefront-level redirects should stay off so buyers keep instant download
  access after purchase

That makes Payhip the active zero-cost delivery layer for the paid
downloadable offers in the current launch setup.
