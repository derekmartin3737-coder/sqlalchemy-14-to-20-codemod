# Troubleshooting

## The report says `manual_review_required`

That is expected for unsupported patterns. The tool is supposed to fail closed
instead of guessing on risky SQLAlchemy rewrites.

## Format/typecheck/build/test failed after migration

That does not mean the codemod was useless. It means:

1. the deterministic rewrites were applied,
2. remaining breakage still exists,
3. the migration is not done yet.

Use the report to separate:

- files changed automatically,
- unsupported patterns,
- failing validation phases.

## Windows temp/cache permission weirdness

This workspace produced repeated cache/temp permission errors under hidden cache
directories. The validation runner already redirects temp, mypy cache, and
bytecode scratch output into repo-local paths to reduce that risk.

## MyPy crashes on Windows / Python 3.12

In this repo, `mypy 1.20.0` crashed the interpreter. Pinning to `mypy 1.11.2`
avoided the crash. If you hit a similar issue, downgrade first before
concluding the code is broken.

## The target repo does not use Ruff/MyPy/Pytest

Configure the repo-specific commands in `pyproject.toml` under
`[tool.sa20_pack.validation]`.
