# Launch Posts

## Short Community Post

I built a narrow codemod pack for one annoying upgrade path: common
SQLAlchemy 1.4 legacy Core/ORM patterns to SQLAlchemy 2.0-safe code.

It starts with a free scan, dumps unsupported patterns into a manual review
bucket, and then points teams to a paid apply pack only when the repo fits
scope.

Repo includes:

- free scanner CLI
- GitHub Action
- JSON migration report
- scanner-first demo fixture

## Longer Forum Post

Most migration tooling dies in one of two ways:

1. it is too broad and becomes an unreliable "AI refactor" toy, or
2. it is too shallow and stops at regex edits.

This project goes the other direction: one painful upgrade path only,
SQLAlchemy 1.4 -> 2.0 legacy Core/ORM breakages that are structurally safe to
rewrite.

What it automates today:

- `select([..])`
- `session.query(Model).get(pk)`
- simple string relationship joins
- simple string loader options
- simple DML constructor keyword rewrites
- legacy declarative imports

What it does not fake:

- `engine.execute(...)`
- multi-hop string joins
- dotted loader paths
- removed `Query` helpers outside current coverage

The free scan emits a JSON report and tells a team whether the repo fits the
paid apply pack before anyone checks out.

## Repo Description

Scanner-first migration product for common SQLAlchemy 1.4 -> 2.0 legacy
Core/ORM breakages, with manual-review findings, public proof, and a paid
apply pack for the documented subset.

## Demo Script

1. Show the failing fixture repo test run.
2. Run `sa20-pack fixtures/demo_repo --report artifacts/demo-migration-report.json`.
3. Open the report and point to:
   - supported candidates
   - zero unsupported findings
   - fit for the paid apply pack
4. End with the limits: `engine.execute(...)` still goes to manual review.

## Before/After Post Text

Before:

- SQLAlchemy 2.0 fixture fails on legacy `select([..])`, string loader options,
  string joins, and old DML constructor kwargs.

After:

- the free scan confirms the repo is inside supported scope before purchase.

## FAQ For Skeptical Replies

### "Why not just use the migration guide?"

You still should. The tool exists to remove the repetitive edits and leave the
human attention for the dangerous parts.

### "Why not do full Query -> select migration?"

Because narrow and trustworthy beats broad and flaky for a first paid product.

### "Why not use AI for everything?"

Because deterministic transforms are easier to trust, easier to demo, and much
easier to support without infrastructure cost.

## Claims Guardrail For Public Posts

Always include at least one of these ideas when posting publicly:

- specific legacy patterns only
- unsupported patterns go to manual review
- run the free scan first
- validation is part of the outcome

Do not post language that implies:

- full SQLAlchemy 2.0 migration coverage
- guaranteed passing repos
- no manual work required

## Landing Pages To Link

Use the exact-problem page first and the product page second.

- Broad category page:
  `https://zippertools.org/sqlalchemy-migration-tool.html`
- `Query.get()` page:
  `https://zippertools.org/sqlalchemy-query-get-migration.html`
- `select([..])` page:
  `https://zippertools.org/sqlalchemy-select-list-migration.html`
- declarative import page:
  `https://zippertools.org/sqlalchemy-declarative-import-migration.html`
- string join page:
  `https://zippertools.org/sqlalchemy-string-join-migration.html`
- string loader page:
  `https://zippertools.org/sqlalchemy-joinedload-string-migration.html`
- DML keyword page:
  `https://zippertools.org/sqlalchemy-insert-values-migration.html`

## Exact-Problem Outreach Posts

### Post For String Joins

I built a narrow SQLAlchemy 1.4 -> 2.0 migration tool for one of the ugly
repetitive cases: simple string relationship joins like
`session.query(User).join("addresses")`.

It starts with a free scan, only automates the documented safe subset, and
pushes unsupported cases into a manual-review bucket instead of guessing.

Issue page:
https://zippertools.org/sqlalchemy-string-join-migration.html

### Post For String Loader Options

One SQLAlchemy 2.0 cleanup I kept seeing was old string loader options like
`joinedload("addresses")`.

I put together a scanner-first migration tool that qualifies the repo first,
rewrites the supported loader-option cases, and leaves dotted or ambiguous
paths visible instead of pretending they are safe.

Issue page:
https://zippertools.org/sqlalchemy-joinedload-string-migration.html

### Post For DML Constructor Keywords

I built a narrow SQLAlchemy migration tool for supported DML constructor
keyword cleanup, including patterns like `insert(table, values=...)` and
simple `update(..., whereclause=..., values=...)`.

The point is not to promise a full migration. The point is to remove the
boring edits, emit a machine-readable report, and tell you when the repo still
needs deliberate manual review.

Issue page:
https://zippertools.org/sqlalchemy-insert-values-migration.html

### Post For Broad SQLAlchemy Migration Queries

If you are in the middle of a SQLAlchemy 1.4 -> 2.0 upgrade and want something
more trustworthy than a generic "AI refactor" pitch, I built a scanner-first
migration tool for a narrow documented subset.

Run the free scan first, inspect the supported candidates and unsupported
bucket, then buy the apply pack only if the repo actually fits.

Overview:
https://zippertools.org/sqlalchemy-migration-tool.html

## Reply Template For Public Threads

If you are already in a discussion where someone is describing exact migration
pain, keep the reply short and point to the matching page:

I built a narrow scanner-first tool for this exact SQLAlchemy 2.0 cleanup.
It only handles the documented safe subset, pushes unsupported cases into a
manual-review bucket, and is meant to be run on a branch after a free fit
scan.

If this is the breakage you are hitting, start here:
[paste exact issue-page link]

## Free Weekly Outreach Loop

1. Find three fresh public threads about SQLAlchemy 2.0 migration pain.
2. Reply only where one of the supported pages is a real fit.
3. Link the issue page first, not the checkout page.
4. Record the thread in the launch log.
5. Watch which issue pages actually earn impressions and clicks.
