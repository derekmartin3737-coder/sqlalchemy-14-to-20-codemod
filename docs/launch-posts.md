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
  `https://zippertools.org/products/sa20-pack/`
- `Query.get()` page:
  `https://zippertools.org/sqlalchemy/session-query-get/`
- `session.query` page:
  `https://zippertools.org/sqlalchemy/session-query-migration/`
- `select([..])` page:
  `https://zippertools.org/sqlalchemy/select-list-syntax/`
- declarative import page:
  `https://zippertools.org/sqlalchemy/declarative-imports/`
- string join page:
  `https://zippertools.org/sqlalchemy/string-join-paths/`
- string loader page:
  `https://zippertools.org/sqlalchemy/string-loader-options/`
- joinedload_all page:
  `https://zippertools.org/sqlalchemy/joinedload-all-removed/`
- `engine.execute(...)` page:
  `https://zippertools.org/sqlalchemy/engine-execute-removed/`
- DML keyword page:
  `https://zippertools.org/sqlalchemy/insert-values-kwargs/`

## Exact-Problem Outreach Posts

### Post For String Joins

I built a narrow SQLAlchemy 1.4 -> 2.0 migration tool for one of the ugly
repetitive cases: simple string relationship joins like
`session.query(User).join("addresses")`.

It starts with a free scan, only automates the documented safe subset, and
pushes unsupported cases into a manual-review bucket instead of guessing.

Issue page:
https://zippertools.org/sqlalchemy/string-join-paths/

### Post For String Loader Options

One SQLAlchemy 2.0 cleanup I kept seeing was old string loader options like
`joinedload("addresses")`.

I put together a scanner-first migration tool that qualifies the repo first,
rewrites the supported loader-option cases, and leaves dotted or ambiguous
paths visible instead of pretending they are safe.

Issue page:
https://zippertools.org/sqlalchemy/string-loader-options/

### Post For DML Constructor Keywords

I built a narrow SQLAlchemy migration tool for supported DML constructor
keyword cleanup, including patterns like `insert(table, values=...)` and
simple `update(..., whereclause=..., values=...)`.

The point is not to promise a full migration. The point is to remove the
boring edits, emit a machine-readable report, and tell you when the repo still
needs deliberate manual review.

Issue page:
https://zippertools.org/sqlalchemy/insert-values-kwargs/

### Post For Broad SQLAlchemy Migration Queries

If you are in the middle of a SQLAlchemy 1.4 -> 2.0 upgrade and want something
more trustworthy than a generic "AI refactor" pitch, I built a scanner-first
migration tool for a narrow documented subset.

Run the free scan first, inspect the supported candidates and unsupported
bucket, then buy the apply pack only if the repo actually fits.

Overview:
https://zippertools.org/products/sa20-pack/

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

## Current Outreach Targets (2026-04-12)

Use these first. They are closer to real migration pain than a generic
"check out my tool" blast.

### Owned Post 1: DEV Community

Channel:
https://dev.to/t/python/

Title:
SQLAlchemy 1.4 -> 2.0 migration tool for repetitive legacy patterns

Body:

I built a scanner-first SQLAlchemy 1.4 -> 2.0 migration tool for a narrow
documented subset of legacy patterns.

It is intentionally not a full "AI migration" promise. It handles supported
patterns like:

- `select([..])`
- `session.query(Model).get(pk)`
- simple string relationship joins
- simple string loader options
- legacy declarative imports
- simple DML constructor keyword rewrites

Unsupported patterns stay visible in a manual-review bucket, so the free scan
can tell you whether a repo is even a fit before you pay for anything.

Overview:
https://zippertools.org/products/sa20-pack/

### Owned Post 2: GitHub Discussion In Our Repo

Why this one matters:
GitHub Discussions is explicitly meant for announcements, questions, and
ongoing community conversation around a repository.

Source:
https://docs.github.com/discussions/collaborating-with-your-community-using-discussions/about-discussions

Suggested title:
SQLAlchemy 1.4 -> 2.0 migration pain tracker and free scan

Suggested body:

If you are upgrading a SQLAlchemy 1.4 codebase and keep running into old
legacy Core or ORM patterns, reply with the exact warning or API shape.

The current public scanner covers a narrow safe subset and intentionally sends
unsupported cases to manual review instead of guessing.

Broad overview:
https://zippertools.org/products/sa20-pack/

Exact issue pages:
- https://zippertools.org/sqlalchemy/session-query-get/
- https://zippertools.org/sqlalchemy/select-list-syntax/
- https://zippertools.org/sqlalchemy/string-join-paths/
- https://zippertools.org/sqlalchemy/string-loader-options/
- https://zippertools.org/sqlalchemy/insert-values-kwargs/
- https://zippertools.org/sqlalchemy/declarative-imports/

### Reply Target 1: SQLAlchemy joinedload_all Discussion

Thread:
https://github.com/sqlalchemy/sqlalchemy/discussions/11356

Why it fits:
The discussion is directly about replacing deprecated `joinedload_all(...)`
without creating duplicate joins. That is close enough to the storefront's
loader-cleanup story to be useful, but only if the reply stays explicit about
manual-review boundaries.

Reply:

A lot of this migration pain is not just "swap one API for another", it is
figuring out which old eager-loading paths are simple cleanup and which ones
are tied up with manual joins or `contains_eager()`.

I built a narrow scanner-first tool for that kind of SQLAlchemy 1.4 -> 2.0
cleanup. It does not claim to auto-resolve duplicate-join semantics, but it
does separate supported loader cleanup from the cases that still need manual
review before anyone buys the pack.

Exact page:
https://zippertools.org/sqlalchemy/joinedload-all-removed/

### Reply Target 2: SQLAlchemy Incremental Type-System Discussion

Thread:
https://github.com/sqlalchemy/sqlalchemy/discussions/10949

Why it fits:
This is a softer fit. The thread is really about typing and the mypy plugin,
which the storefront does not solve. Post only if the reply stays honest and
frames the tool as adjacent runtime-API cleanup, not a typing answer.

Reply:

If part of the migration work here is still the repetitive 1.4-era runtime API
cleanup, I built a narrow scanner-first tool for that side of the move.

It does not solve the typing or mypy-plugin part. What it does do is qualify a
repo for supported legacy cleanup like `Query.get()`, `select([..])`, simple
string joins and loader paths, and declarative import moves while keeping
unsupported cases visible instead of pretending the whole migration is
automated.

Overview:
https://zippertools.org/products/sa20-pack/

### Avoid: SQLAlchemy DeclarativeMeta Metaclass Discussion

Thread:
https://github.com/sqlalchemy/sqlalchemy/discussions/10972

Why to skip it:
That thread is about custom metaclasses and `DeclarativeBaseNoMeta`, which is
outside current product scope. Dropping a link there will read as self-promo
instead of help.

### Avoid For Cold Promotion

Python Discourse explicitly says spam or blatant self-promotion will be
removed, so do not use it for a cold launch blast.

Source:
https://discuss.python.org/guidelines
