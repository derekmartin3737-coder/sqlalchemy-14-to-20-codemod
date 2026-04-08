# Repo Fit Checklist

Use this before buying the paid pack or preset bundle.

## Good fit

- The repo is on SQLAlchemy 1.4 and the target is SQLAlchemy 2.0.
- The free scan already found common legacy patterns the tool knows about.
- The repo still has a repeated unsupported bucket that is expensive but not
  wildly custom.
- The team already has tests or validation commands worth running after changes.
- The team wants a deterministic migration helper, not a full migration agency.
- The team is comfortable handling flagged follow-up work with its own
  engineers.

## Weak fit

- SQLAlchemy usage is heavily wrapped in private abstractions.
- The repo depends on async migration work right away.
- The repo uses many removed `Query` helpers outside current supported scope.
- The repo barely has tests, build checks, or typecheck coverage.
- The team expects one purchase to guarantee a fully passing application.

## Do not buy

- You have not run the free scan yet.
- You need `engine.execute(...)` to be automatically migrated today.
- You need transaction-semantics decisions to be automated.
- You need a contractor to own the whole migration.
- You are looking for custom coding labor instead of a downloadable tool.

## What to gather first

- current SQLAlchemy version
- target version
- migration report JSON
- unsupported findings summary
- validation failures, if any
- rough repo shape: service, monorepo, framework, test command
