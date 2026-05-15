# ESLint v10 Migration Radar Public Proof

## Proof Claim

The v0.1 scanner can inspect a local repo, detect ESLint v10 migration blockers,
generate JSON/HTML reports, preview deterministic script patches, and apply
only those simple script patches when requested.

## Fixture Coverage

- `risky_repo`: `.eslintrc.js`, `.eslintignore`, `package.json#eslintConfig`,
  removed flags, and legacy ESLint API usage.
- `clean_repo`: flat config and no legacy blockers.
- `broken_package_repo`: invalid package metadata blocks the readiness claim.

## Verified Commands

Run from `products/eslint-v10-radar/`:

```bash
python -m pytest -q -p no:cacheprovider
python -m ruff check . --no-cache
PYTHONPATH=src python -m mypy src tests --cache-dir .mypy-cache-local
PYTHONPATH=src python -m eslint_v10_radar.build_runner
python -m hatchling build -t wheel
```
