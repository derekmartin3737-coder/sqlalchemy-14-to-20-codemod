# Terms of Sale

Last updated: 2026-05-15

These terms apply to paid Zipper Tools digital products sold through the public
checkout links. Zipper Tools is a Product Wells storefront: each product is a
bounded local scanner, report, patch preview, or downloadable pack for a
specific developer deadline or migration problem. Paid checkout uses Stripe
Checkout.

## What is being sold

The seller may offer:

- free local scanners and public proof artifacts
- one-time paid migration packs
- one-time preset or rollout bundles
- one-time paid product-well bundles after the free/paid boundary is published

Each product includes only the scope described on the pricing page and related
docs at the time of purchase.

GitHub Actions Upgrade Guard is currently published as the front-page Product
Well with a free scanner and public proof path. Its paid checkout remains paused
until the exact paid SKU, deliverables, and free-vs-paid boundary are published.

## What is not being sold

The seller is not promising:

- a full custom migration service
- a managed CI monitoring service
- custom pull requests or private repo work
- guaranteed compatibility with every codebase, workflow, or dependency graph
- guaranteed passing validation on every repo without manual work
- a hosted SaaS

## Buyer responsibility

The buyer is responsible for:

- reviewing the published limitations before purchase
- using version control and backups before applying changes
- validating the migrated repo in their own environment
- not sending secrets or regulated data through casual support channels

## Failed validation

If a scanner, migration run, or validation step fails, that is a failed result,
not a successful result. The tools are designed to report that failure clearly
with manual-review or blocked findings instead of guessing.

## Delivery

Paid digital goods are delivered as ZIP downloads. After a successful Stripe
payment, the success page links to `/stripe/delivery`. That route verifies the
paid Stripe Checkout Session and streams the matching ZIP from private
Cloudflare storage.

Free Product Well scanners and proof artifacts are delivered through the public
repo or public site. They do not require payment, a manual email step, private
repo access, or source-code upload.

Normal delivery does not require a manual email step, private repo access, or
source-code upload. The buyer is responsible for keeping the order reference
and receipt.

## Support

Support follows the published support-scope policy. Buying a paid product does
not create a consulting or custom-services relationship.

Support email: `support@zippertools.org`.

## Liability boundary

This product helps automate code rewrites and reporting. It does not guarantee
business outcomes, deployment success, or production correctness. Use it with
normal engineering safeguards.

Except where law requires otherwise, the seller is not promising that the
software will be error-free, uninterrupted, or fit for every codebase. The
buyer's direct financial recovery for a paid product should not exceed the
amount paid for that product.

## Use safeguards

Before applying changes, the buyer should:

- use version control
- keep backups
- review the report and limitations
- validate the migrated repo in their own environment
