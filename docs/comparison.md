# Comparison Against Manual Migration

## Manual docs-only migration

What it gives you:

- no extra tooling to trust
- maximum control

What it costs:

- slow grep/edit/test loops
- inconsistent coverage across files
- no machine-generated inventory of what changed
- no reusable playbook for the next repo

## One-off internal scripts

What it gives you:

- local customization

What it costs:

- usually no reporting
- usually no packaging
- usually no documentation good enough for reuse or sale

## `sa20-pack`

What it gives you:

- deterministic AST transforms
- explicit manual-review bucket
- validation loop with structured results
- buyer-visible before/after demo value
- path from free tool to paid wider-coverage pack

What it does not give you:

- full SQLAlchemy 2.0 migration coverage
- magic for transaction semantics
- substitute for application-specific tests
