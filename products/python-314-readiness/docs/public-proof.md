# Python 3.14 Readiness Pack Public Proof

## Proof Claim

The v0.1 scanner can inspect a local Python repository, classify Python 3.14
readiness risks, generate JSON and HTML reports, and preview or apply one safe
CI matrix patch without uploading source code.

## Fixture Coverage

The proof fixtures cover:

- a risky repo with metadata, Pydantic v1, annotations, multiprocessing,
  `functools.partial`, and a CI matrix gap
- a clean repo with Python 3.14 already present in metadata and CI
- an old Pydantic v2 pin that should be reported separately from Pydantic v1
- a broken Python file that must block any readiness claim

## Verified Commands

Run from `products/python-314-readiness/`:

```bash
python -m pytest -q -p no:cacheprovider
python -m ruff check . --no-cache
PYTHONPATH=src python -m mypy src tests --cache-dir .mypy-cache-local
PYTHONPATH=src python -m python314_readiness.build_runner
python -m hatchling build -t wheel
```

On this Windows workspace, `python -m build --wheel --no-isolation` is blocked
by the machine's global temp-directory ACLs, so Hatchling is the package-build
verification command for this product.

## Expected Risk Findings In The Risky Fixture

- `PY314001`: `requires-python = ">=3.10,<3.14"`
- `PY314002`: GitHub Actions matrix omits `3.14`
- `PY314003`: runtime annotation introspection
- `PY314004`: `pydantic.v1` and Pydantic v1 dependency pin
- `PY314006`: `ProcessPoolExecutor` and `multiprocessing.Pool`
- `PY314007`: class-level `functools.partial`

## Safe Patch Proof

Dry-run mode leaves the fixture untouched and emits a patch preview. Apply mode
changes only `.github/workflows/ci.yml`, adding `"3.14"` to the simple inline
matrix. It does not modify `pyproject.toml` or Python source.

## Source-Backed Signals

- Python 3.14 was released on 2025-10-07 and includes deferred annotation
  changes, multiprocessing start-method changes, and a `functools.partial`
  descriptor change.
- Pydantic 2.12 introduced initial Python 3.14 support and Pydantic 2.13
  updated the `pydantic.v1` namespace to include a Python 3.14-supporting v1
  line.
- `actions/setup-python` recommends setting Python explicitly through
  `python-version` or `python-version-file`.
