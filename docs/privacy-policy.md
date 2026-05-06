# Privacy Policy

Last updated: 2026-05-01

This policy covers the public `sa20-pack` website, the free public repo, and
related checkout and support flows.

This is a plain-English operational policy, not legal advice.

## What we collect

### Website traffic

If enabled on the public site, Cloudflare Web Analytics collects privacy-focused
website analytics such as page views, referrers, and traffic trends.

### Checkout and order information

Paid checkout is handled by Stripe Checkout. Orders, receipts, payment status,
and related customer information are processed through Stripe under Stripe's
own policies and legal obligations.

Zipper Tools controls the `/go/...` checkout routes through the Cloudflare
Worker, but Stripe handles secure payment entry and payment records. Zipper
Tools does not receive or store full card numbers.

### Payment and payout operations

Seller-side payout operations use Stripe. Buyers do not send payout
information to `sa20-pack`.

### Direct support messages

If you contact the seller directly, the seller receives the information you send
in that message, such as your email address, order reference, and repo problem
description.

Support email: `support@zippertools.org`.

## What we do not collect by default

- no hidden CLI telemetry
- no default background reporting from the codemod
- no production credentials from your environment
- no source-code upload for normal scanner or paid-product use

## How information is used

Information is used to:

- operate the public site
- process purchases
- deliver paid digital products
- answer support requests
- understand traffic and conversion trends

## Data minimization

Do not send secrets, production credentials, regulated data, or full private
application dumps in support requests.

If a repo example is needed for support, sanitize it first unless a separate
written support arrangement says otherwise.

## Third parties used in the launch stack

- Cloudflare Pages
- Cloudflare Web Analytics
- Stripe
- GitHub

## Policy updates

If the analytics or delivery setup changes, update this file and the public site
before those changes go live.
