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
