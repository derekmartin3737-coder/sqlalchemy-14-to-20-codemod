# Claims and Safeguards

Last updated: 2026-04-30

This is the practical launch guardrail document for `sa20-pack`.

This is not legal advice.

## Current operating posture

- launch as a sole proprietor, not an LLC
- keep claims narrow and provable
- require the free scan before paid purchase
- fail closed on unsupported patterns
- treat validation failures as failures, not soft wins
- keep paid offers software-only and autonomous

## Claims we can make

- The tool applies deterministic rewrites for the currently documented legacy
  SQLAlchemy patterns.
- The tool emits a machine-generated migration report.
- The tool flags unsupported patterns for follow-up by the buyer in their own
  repo, using their own engineering workflow.
- The tool runs validation after apply mode when validation commands are
  configured.
- The product is a narrow helper for one upgrade path, not a full migration
  service.
- The $99 fit-report offer, if listed, must be an autonomous software add-on
  that runs on local scanner output. It must not require a person to review a
  customer's repo or report.

## Claims we must not make

- full SQLAlchemy 2.0 migration automation
- guaranteed passing application behavior
- guaranteed production correctness
- compatibility with every SQLAlchemy codebase
- no manual review required
- no engineering judgment required
- that any human-assisted migration, consulting, or PR service is part of the
  product

## Required public qualifiers

Keep these ideas visible in site copy, product copy, and launch posts:

- specific legacy patterns only
- unsupported patterns go to follow-up by the buyer, not to a vendor service
- validation results must be read before claiming success
- buyers should use version control and backups
- run the free scan first
- paid offers must remain downloadable or autonomous software workflows, not
  custom service engagements

## Seller identity safeguard

No LLC is planned for launch.

That means:

- the cleanest zero-cost path is selling under the real legal name as a sole
  proprietor
- if the public-facing seller name is not the legal name, Oregon may require an
  assumed business name filing before public paid launch

Do not assume a product label is automatically safe to use as the legal seller
name.

## Order handling safeguards

- keep order confirmations
- keep payout records
- keep refund records
- keep delivered version numbers
- keep launch-date and price-change notes
- keep the published scope for each paid offer

## Engineering safeguards

- use version control before applying changes
- use backups before applying changes
- review the report before shipping changes
- do not treat a failed validation run as a success
- do not send secrets or regulated data through ordinary support channels

## Launch stop conditions

Pause launch if any of these are still unclear:

- seller identity is unresolved
- public claims overstate product scope
- paid deliverable is not ready for automatic delivery
- refund and support boundaries are not published
- checkout links are live but success/cancel paths are broken
- Stripe Checkout or post-payment delivery fails live testing
- there is no written answer for what happens when validation fails
