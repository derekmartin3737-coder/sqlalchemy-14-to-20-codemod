# Autonomous Product Wells

This is the long-term direction for Zipper Tools after the SQLAlchemy launch
experiment showed traffic without enough paid intent.

Source of truth: `Autonomous Product Wells for a Solo Developer.docx`.

## Core Doctrine

Zipper Tools should build autonomous, self-serve developer products around
fresh operational pain.

The strongest product is not a broad agent, a consulting workflow, or a generic
trend report. It is a local-first tool that turns a deadline, deprecation,
policy requirement, compliance obligation, or recurring platform breakage into
a finished artifact:

- patch set
- HTML report
- JSON CI gate
- submission bundle
- compliance dossier
- manager-readable risk summary

The buyer should be able to buy, download, activate, run, and get value without
emailing, scheduling, uploading source code, or waiting on a human.

## Hard Filters

A product well is viable only if it passes these filters:

- The buyer can run it directly.
- It solves one narrow, painful, current problem.
- It does not require seller labor.
- It does not require source upload, production credentials, or broad account
  access.
- It does not require a paid API, paid model, or proprietary dataset.
- It can produce useful output from local files.
- Uncertain cases fail closed with explicit findings.
- A credible proof can be built in days, not months.
- A careful buyer can justify the product in one sentence.

Reject ideas that drift into custom service work, vague AI agents, hardware,
open-ended monitoring, or support-heavy workflows.

## Scoring Rubric

| Criterion | Weight | What high means |
| --- | ---: | --- |
| Urgency and timing | 20 | Official deadline, deprecation, release, or policy pressure is active now |
| Buyer willingness to pay | 20 | The pain blocks releases, app submissions, compliance, or platform reliability |
| Build feasibility | 15 | A solo developer can build a credible MVP with open-source tooling |
| Distribution clarity | 15 | Exact search terms, changelog links, forums, or platform channels exist |
| Competition gap | 10 | Existing tools are partial components, not a finished buyer artifact |
| Repeatability | 10 | Rules, fixtures, and reports can be reused across many buyers |
| Trust burden | 10 | The product can work locally with low permissions and no source upload |

## Product Template

Every product should converge on this architecture:

1. Parse local inputs: repo files, workflow YAML, lockfiles, manifests, app
   bundles, containers, package configs, or source files.
2. Apply a versioned rule pack.
3. Classify findings as `autofix`, `manual_review`, `blocked`, or
   `informational`.
4. Generate patches only when deterministic and safe.
5. Write a human report and machine report.
6. Document exit codes and validation commands.
7. Stamp every output with product version and rule-pack version.

The rules should be data where possible. The product core should change slowly;
value should compound through new rules, fixtures, mappings, reports, and
official-source references.

## Active Portfolio

### 1. GitHub Actions Upgrade Guard

Status: active flagship candidate.

Buyer: platform engineers, DevOps leads, repo owners, maintainers.

Pitch: scan GitHub Actions workflows and emit PR-ready patches for upcoming
Actions breakages.

Initial scope:

- deprecated artifact actions
- cache action/runtime deprecations
- runner-image drift
- Node runtime pressure on Actions runners
- broad or missing permissions blocks
- floating or fragile action references
- reusable workflow and composite action visibility

Output:

- `actions-upgrade-report.html`
- `actions-upgrade-report.json`
- patch preview
- manager risk summary
- CI gate mode

### 2. Python 3.14 Readiness Pack

Status: second portfolio candidate.

Buyer: Python team leads, maintainers, SaaS backend teams.

Pitch: turn a Python repo into a Python 3.14 readiness plan, codemod pack, and
CI gate.

Important positioning: do not sell this as only "Pydantic v1 breaks." The
stronger product is whole-repo Python 3.14 readiness: annotations,
dependencies, CI matrices, import risks, and library-specific checks.

### 3. Apple Privacy Manifest Composer

Status: high-quality future candidate, probably higher build friction.

Buyer: iOS teams, mobile agencies, indie app publishers.

Pitch: generate submission-ready privacy manifests, required-reason mappings,
and SDK evidence locally.

### 4. CRA Evidence Builder

Status: high-ticket future candidate.

Buyer: EU-facing software vendors, commercial OSS vendors, security-conscious
SMB SaaS teams.

Pitch: convert a repo, package, or container into a Cyber Resilience Act
evidence dossier and release gate.

## Legacy Product Role

SQLAlchemy, Pydantic, and flatconfig assets are not failures. They are proof
that the repo can build local scanners, deterministic transforms, reports,
fixtures, static docs, Stripe delivery, and public proof pages.

They should now be treated as:

- portfolio proof
- search assets
- examples of the product pattern
- possible secondary revenue if organic demand appears

They should not consume new build time unless direct evidence shows buyer
intent.

## Monthly Product Well Cycle

1. Collect current official pressure: changelogs, release notes, deprecation
   calendars, app-store policy pages, standards deadlines, and package registry
   shifts.
2. Score candidates using the rubric above.
3. Pick one Well of the Month.
4. Publish the analysis page and exact search-intent pages.
5. Build the smallest proof scanner or report generator.
6. Measure visits, free-run clicks, downloads, direct replies, checkout intent,
   and buyer conversations.
7. Promote, pause, or kill the well within one month.

## Promotion And Kill Rules

Promote a well when at least one of these happens:

- 3 or more serious users run the free scanner.
- A buyer asks a pricing or implementation question.
- Search pages get qualified clicks and product-page movement.
- A public proof page earns direct references from relevant communities.
- The product can clearly replace several hours of urgent engineer work.

Pause or kill a well when:

- traffic arrives but no one runs the free artifact path
- checkout intent stays near zero after exact-fit outreach
- the product requires human interpretation to be useful
- proof depends on fixtures only
- the trust burden becomes too high
- official tooling already solves the buyer's real problem

## Website Direction

The storefront should become a Product Wells site:

- homepage: current Well of the Month
- `/wells/`: archive of monthly analyses
- `/products/actions-upgrade-guard/`: active flagship product
- `/proof/actions-upgrade-guard/`: public proof artifact
- `/archive/sqlalchemy/`: legacy SQLAlchemy proof and product pages
- `/framework/`: the autonomous product-well doctrine

The homepage should not read like generic trend analysis. It should answer:

- what deadline or breakage matters this month
- what the free scanner/report proves
- what the paid product produces
- when not to buy
- what evidence would make the well worth expanding
