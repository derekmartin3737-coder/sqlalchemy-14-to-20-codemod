# Limitations

`sa20-pack` is intentionally narrow.

## Automated today

- legacy declarative import rewrites
- `select([..])` list-syntax rewrites
- `session.query(Model).get(pk)` rewrites
- simple string relationship `join()` rewrites
- simple string loader option rewrites
- simple DML constructor keyword rewrites

## Flagged instead of rewritten

- `engine.execute(...)`
- dotted loader paths like `"orders.items"`
- multi-hop string joins
- `from_self()` and similar removed helpers
- mixed `sqlalchemy.ext.declarative` imports
- parse failures

## Not covered

- full `Query` -> `select()` migration
- transaction-bound `engine.execute(...)` rewrites
- async SQLAlchemy migration
- ORM typing modernization to `Mapped[...]` / `DeclarativeBase`
- framework wrappers that hide SQLAlchemy internals
- runtime/data validation beyond the configured repo checks

## Practical limitation

This repo validates with repo-configured commands. If a target repo has no
formatter, typecheck, build, or test command configured, the report will mark
that phase as skipped instead of inventing a fake pass.
