# Store Products

Last updated: 2026-04-30

Use this file as the current Stripe product setup reference so product pages,
pricing, Worker checkout metadata, and storefront links stay consistent.

## Immediate checkout trust fixes

Apply these rules before sending paid traffic:

- Disable inventory/scarcity messaging for every digital product.
- Confirm no product page displays `Only -1 left` or any negative stock count.
- Rename products around migration outcomes, not internal package names.
- Replace "tiny ZIP" framing in descriptions with a migration workflow:
  sample CLI output, sample report, before/after diff, supported rewrite table,
  rollback notes, and local-only safety language.
- Keep the uploaded file, but make the visible value the controlled workflow,
  docs, reports, and deterministic rewrite behavior.

## Product 1

Name: `SQLAlchemy 1.4 to 2.0 Migration Cleanup Pack`

Current checkout price: `$299.99` one-time per team

Type: single-payment digital product

Checkout route:

- `/go/sa20-pack`

Paid KV artifact key:

- `sa20-pack-edge-case-pack.zip`

Who it is for:

- teams that already ran the free scan
- repos that are close to passing but still have repeated unsupported patterns
- buyers who want fewer repetitive manual edits without hiring a migration shop

What the buyer gets:

- a versioned local migration workflow download
- install instructions and example CLI output
- before/after diff examples and supported rewrite table
- JSON report guidance, rollback notes, rollout checklist, and manager summary

Suggested short description:

> Deterministic local rewrites for supported SQLAlchemy 1.4 to 2.0 migration
> patterns, with reports, rollback notes, and manual-review flags.

Suggested checkout summary:

> Run the free scan first. Buy this when the report shows repeated supported
> SQLAlchemy cleanup findings and your team wants a controlled local apply
> workflow instead of hand-editing every occurrence.

Suggested visual/checklist block:

- CLI: `python -m sa20_pack.cli path/to/repo --report migration-report.json`
- Report: `38 supported findings`, `6 manual-review findings`, `0 files uploaded`
- Diff: `session.query(User).get(id)` -> `session.get(User, id)`
- Safety: local-only, branch-first, deterministic transforms, validation report

Suggested confirmation modal:

- Title: `Your migration pack is ready`
- Message:
  `Download the package, read the install guide first, and keep your report from the free scan nearby.`
- Button text: `Open install guide`
- Button link:
  `https://zippertools.org/success`

Suggested receipt email button:

- Button text: `Open install guide`
- Destination:
  `https://zippertools.org/success`

## Product 2

Name: `Migration Preset Bundle`

Current checkout price: `$149.99` one-time per team

Type: single-payment digital product

Checkout route:

- `/go/sa20-preset`

Paid KV artifact key:

- `sa20-pack-preset-bundle.zip`

Who it is for:

- teams that want more repeatable rollout structure
- buyers who want richer templates without buying a service
- repos that benefit from preset guidance after the free scan

What the buyer gets:

- a versioned rollout workflow download
- preset files for common migration shapes
- richer report templates
- rollout notes and manager summary templates

Suggested short description:

> Preset guidance, report templates, and rollout docs for teams turning a local
> migration scan into repeatable SQLAlchemy cleanup work.

Suggested checkout summary:

> This is a downloadable add-on, not a service. Buy it when you want more
> repeatable rollout structure after the free scan.

Suggested confirmation modal:

- Title: `Your preset bundle is ready`
- Message:
  `Download the bundle, review the included rollout notes, and keep your free scan report nearby while applying it.`
- Button text: `Open install guide`
- Button link:
  `https://zippertools.org/success`

Suggested receipt email button:

- Button text: `Open install guide`
- Destination:
  `https://zippertools.org/success`

## Product 3

Name: `Pydantic v1 to v2 Migration Cleanup Pack`

Current checkout price: `$249.99` one-time per team

Type: single-payment digital product

Checkout route:

- `/go/pydantic-v2-porter`

Paid KV artifact key:

- `pydantic-v2-porter.zip`

Who it is for:

- teams that already ran the free fit scan for the Pydantic subset
- repos that fall within the documented validator/config/settings coverage
- buyers who want a downloadable local apply pack instead of a hosted tool

What the buyer gets:

- a versioned local migration workflow download
- install instructions
- sample CLI output, before/after diff examples, and supported rewrite table
- coverage notes, limitations, rollout checklist, and manager summary

Suggested short description:

> Deterministic local cleanup for supported Pydantic v1 to v2 imports,
> validators, config, and BaseSettings moves, with manual-review flags for
> unsafe cases.

Suggested visual/checklist block:

- CLI: `python -m pydantic_v2_porter.cli path/to/repo --report migration-report.json`
- Report: `24 supported findings`, `5 manual-review findings`, `0 files uploaded`
- Diff: `@validator("email")` -> `@field_validator("email")`
- Safety: local-only, branch-first, deterministic transforms, validation report

## Product 4

Name: `Automated Migration Fit Report Add-on`

Current checkout price: `$99` per team

Type: single-payment digital software product

Checkout route:

- `/go/fit-report`

Paid KV artifact key:

- `fit-report-add-on.zip`

Who it is for:

- buyers who ran the local scan but are unsure whether the repo fits
- teams that need an autonomous buy/do-not-buy recommendation before spending $299+
- leads from GitHub, Reddit, or email outreach who are not ready for the pack

What the buyer gets:

- local software that reads scanner JSON/output
- supported-pattern summary
- manual-review risk summary
- recommendation: use cleanup pack, use preset bundle, or do not buy

Suggested checkout summary:

> Run the free scanner locally, then use this add-on locally against the report.
> It produces an automated fit summary, supported-pattern counts,
> manual-review buckets, and a buy/do-not-buy recommendation without human
> review, source upload, consulting, or custom PR work.

## Tax and delivery notes

- keep Stripe checkout copy and prices in `worker/index.mjs`
- keep Cloudflare as the canonical storefront
- keep paid ZIPs out of git and store checkout delivery artifacts in the
  private `PAID_ARTIFACTS` KV namespace
