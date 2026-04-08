# Product Spec

## Product

**`sa20-pack`**: a repo-native codemod CLI for migrating the most common
SQLAlchemy 1.4 legacy Core/ORM patterns to SQLAlchemy 2.0-compatible code.

## Supported Versions

- Supported source code style: SQLAlchemy 1.4-era Python code that still uses
  selected legacy Core/ORM APIs.
- Target runtime: SQLAlchemy 2.0.x, validated against SQLAlchemy `2.0.48`.
- Python runtime for this tool: Python 3.10+.

This product does **not** promise to fully modernize a codebase to typed
`DeclarativeBase` or exhaustive 2.0-style `select()` querying.

## V1 Scope

### Deterministic transforms we will apply

1. Rewrite legacy declarative imports:
   - `from sqlalchemy.ext.declarative import declarative_base`
   - `from sqlalchemy.ext.declarative import declared_attr`
   - to `sqlalchemy.orm`
2. Rewrite `select([a, b, c])` to `select(a, b, c)`.
3. Rewrite `session.query(Model).get(pk)` to `session.get(Model, pk)`.
4. Rewrite simple string relationship joins when the root entity is obvious:
   - `session.query(User).join("addresses")`
   - to `session.query(User).join(User.addresses)`
5. Rewrite simple string loader options when the root entity is obvious:
   - `joinedload("addresses")`
   - to `joinedload(User.addresses)`
6. Rewrite simple DML constructor kwargs:
   - `insert(table, values={...})` -> `insert(table).values({...})`
   - `update(table, whereclause=expr, values={...})`
     -> `update(table).where(expr).values({...})`
   - `delete(table, whereclause=expr)` -> `delete(table).where(expr)`

### Patterns we will detect and flag for manual review

1. `engine.execute(...)` / connectionless execution removal
2. Dotted relationship strings such as `joinedload("orders.items")`
3. Multi-hop string joins such as `join("orders", "items")`
4. Mixed safe/unsafe declarative imports from `sqlalchemy.ext.declarative`
5. `from_self()` and other removed legacy `Query` helpers not yet covered
6. Parse failures or files the CST layer cannot safely rewrite

### Explicit exclusions

1. Full `Session.query(...)` to `select()` conversion
2. Automatic transaction-bound rewrites for `engine.execute(...)`
3. Semantic rewrites that need schema introspection or runtime inspection
4. Visual or data-level regression analysis
5. Framework-specific SQLAlchemy wrappers
6. Async SQLAlchemy migration
7. ORM typing migration to `Mapped[...]` / `DeclarativeBase`

## Done Definition

`sa20-pack` is "done" for a repo run only when all of the following are true:

1. The codemod finished scanning the target repo.
2. All deterministic rewrites were applied or previewed.
3. Unsupported patterns were listed explicitly for manual review.
4. Validation commands were run or explicitly skipped with a reason.
5. A machine-generated report was written.
6. The report does not claim success if validation failed.

## Architecture

### Parser / AST layer

- `libcst`
- Reason: preserve formatting, comments, imports, and safe source-to-source
  rewrites.

### Deterministic transform engine

- One pass for supported SQLAlchemy 2.0 migration rules
- Fixed confidence per rule
- Fail closed on unsupported or ambiguous structures

### Edge-case classifier

- Visitor-based unsupported-pattern detector
- Emits manual-review findings instead of risky edits

### Validation runner

- Reads validation commands from `pyproject.toml` when available
- Falls back to simple repo heuristics
- Captures formatter, typecheck, build, and test results separately

### Report generator

- JSON report with:
  - files changed
  - transforms applied
  - unsupported findings
  - validation outcomes
  - remaining TODOs
  - overall confidence

### GitHub Action wrapper

- Composite action around the CLI
- Zero paid infrastructure
- Suitable for public-repo distribution

## Distribution Shape

- CLI first
- GitHub Action second
- Static docs and demo materials in-repo
- No hosted backend required
