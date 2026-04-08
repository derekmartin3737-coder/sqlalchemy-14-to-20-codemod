# Commercial Case

## Budget Sentence

`pydantic-v2-porter` rewrites the safe, high-frequency subset of Pydantic v1
validator, settings, and config breakages, then tells the team exactly which
files still need manual review before they call the migration done.

## Who This Is For

- Python teams blocked on Pydantic v1 -> v2
- repos with direct `pydantic` or `pydantic.v1` imports
- teams whose free scan shows mostly safe validator, settings, and config
  patterns instead of alias-heavy or custom validator signatures

## Why This Is Worth Real Budget

- the supported subset removes repetitive edits across multiple files
- the free scan gives a buyer-visible report before any purchase decision
- the blocked cases are exactly the ones a careful team should not automate by
  guesswork
- a low-hundreds pack only needs to save a sliver of one engineer-day to pay
  for itself

## Why This Beats Docs Plus Manual Edits

- it rewrites imports, settings, config, and decorator names in one pass
- it leaves unsupported files untouched and reports why
- the report gives a migration branch an honest status instead of optimistic
  prose

## Do Not Buy This If

- the repo relies on alias-heavy imports or `import pydantic` attribute access
- validators use `values`, `each_item`, `always`, or other broader signatures
- the repo depends heavily on post `root_validator` behavior

## Current Honest Read

For the supported subset, this now clears the commercial bar. It is still not a
full Pydantic v2 migration tool, but a careful engineer can credibly justify
spend once the free scan shows the repo is mostly inside the supported path.
