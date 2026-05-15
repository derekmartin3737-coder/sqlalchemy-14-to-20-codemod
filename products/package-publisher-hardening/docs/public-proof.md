# Package Publisher Hardening Pack Public Proof

## Proof Claim

The v0.1 scanner can inspect a local repo, identify npm/PyPI publishing risks,
generate JSON/HTML reports, preview OIDC permission patches, and apply only
that narrow workflow permission patch when requested.

## Fixture Coverage

- `risky_repo`: npm token publish, PyPI token upload, missing OIDC permission,
  missing npm repository metadata, and provenance disabled.
- `clean_repo`: npm and PyPI publish workflows with `id-token: write` and
  repository metadata.
- `broken_package_repo`: invalid package metadata blocks the report.

## Verified Commands

Run from `products/package-publisher-hardening/`:

```bash
python -m pytest -q -p no:cacheprovider
python -m ruff check . --no-cache
PYTHONPATH=src python -m mypy src tests --cache-dir .mypy-cache-local
PYTHONPATH=src python -m package_publisher_hardening.build_runner
python -m hatchling build -t wheel
```
