# Python 3.14 Readiness Pack Product Spec

## Product Promise

Python 3.14 Readiness Pack gives a software team a local, source-private
readiness report before they commit engineering time to a Python 3.14 upgrade.
It answers: "What will block or complicate our first Python 3.14 CI run?"

The product does not claim full compatibility. It finds static risk signals,
generates a structured report, and safely patches only simple GitHub Actions
Python-version matrices.

## Buyer

- Python platform leads preparing a Python 3.14 migration plan.
- Backend teams with Pydantic-heavy services.
- Maintainers who need proof that CI actually tests Python 3.14.
- Managers who need a scoped readiness artifact before allocating sprint time.

## Pain

Python 3.14 is already stable, but many repos still have:

- package metadata that excludes `3.14`
- GitHub Actions matrices that stop at `3.13`
- runtime annotation readers affected by deferred annotations
- Pydantic v1 or old Pydantic v2 pins
- process-based concurrency sites affected by start-method changes
- class-level `functools.partial` patterns with descriptor behavior changes

## Current Rule Set

- `PY314000`: parse failures block readiness claims.
- `PY314001`: `requires-python` excludes Python 3.14.
- `PY314002`: GitHub Actions uses `actions/setup-python` without Python 3.14.
- `PY314003`: runtime annotation introspection needs 3.14 review.
- `PY314004`: Pydantic v1 usage needs migration review.
- `PY314005`: Pydantic v2 pin predates the 2.12 line.
- `PY314006`: process-based concurrency needs start-method review.
- `PY314007`: `functools.partial` in class bodies needs descriptor review.

## Deterministic Patch Boundary

The only v0.1 mutation is:

- add `"3.14"` to a simple inline GitHub Actions matrix like
  `python-version: ["3.11", "3.12", "3.13"]`

All Python source, dependency, and metadata changes are report-only until a
larger validated transform exists.

## Sources

- Python 3.14 What's New:
  `https://docs.python.org/3.14/whatsnew/3.14.html`
- Pydantic changelog:
  `https://docs.pydantic.dev/latest/changelog/`
- GitHub `actions/setup-python` README:
  `https://github.com/actions/setup-python`

## Exit Codes

- `0`: no blocking findings
- `1`: blocking findings exist
- `2`: scanner could not run

## Premium Boundary

The premium deliverable is not "we upgraded your repo." It is a repeatable,
private readiness artifact with source references, confidence, exact file
locations, fail-closed findings, and deterministic CI patches where safe.
