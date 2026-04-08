# Commercial Case

## Budget Sentence

`sa20-pack` removes the repetitive SQLAlchemy 1.4 -> 2.0 cleanup that teams
still do by hand, then tells them exactly what remains before they pretend the
upgrade succeeded.

## Who This Is For

- Python teams still on SQLAlchemy 1.4
- repos that still contain `select([..])`, `Query.get(...)`, string relationship
  paths, or legacy declarative imports
- teams that want a deterministic first pass before doing the harder manual
  refactors

## Why This Is Worth Real Budget

- the free scan tells a team whether the repo is mostly inside supported scope
- the paid pack costs less than even a small fraction of one engineer-day
- the output is not only a diff; it is also a report plus post-run validation
- the fail-closed behavior prevents false confidence on patterns like
  `engine.execute(...)` and `Query.from_self()`

## Why This Beats Docs Plus Grep

- one run covers several high-frequency SQLAlchemy breakages at once
- the tool produces consistent rewrites instead of reviewer-by-reviewer edits
- unsupported patterns are classified immediately instead of discovered late in
  the migration
- the report is buyer-visible proof for a migration branch or internal update

## Do Not Buy This If

- your repo is already mostly on SQLAlchemy 2.0-safe APIs
- your real pain is `engine.execute(...)`, `Query.from_self()`, or large
  `Query` -> `select()` rewrites
- you want a promise that every SQLAlchemy 1.4 repo will pass automatically

## Current Honest Read

For the supported subset, this now clears the commercial bar. A careful
engineer can show the free scan, the public proof, and the generated report and
make a credible case that the pack is cheaper than burning another migration
day on repetitive edits.
