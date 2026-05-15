# Python 3.14 Readiness Pack

Python 3.14 Readiness Pack is a local scanner for Python repos moving toward
Python 3.14. It produces a machine-readable report, a reviewer-friendly HTML
summary, and deterministic CI patch previews where the repo already has a
Python-version matrix.

This is not a generic "upgrade assistant." It is a Product Wells tool: local
input, deterministic checks, explicit confidence, and useful artifacts without
uploading source code.

## Who This Is For

- Python team leads preparing a 3.14 migration plan.
- Maintainers who need to know whether CI even exercises Python 3.14.
- Backend teams that use runtime annotation introspection.
- Teams with Pydantic v1 or older Pydantic v2 pins.

## Do Not Use This If

- You expect full dependency compatibility proof without running the repo's
  tests under Python 3.14.
- You need hosted monitoring or private repository access.
- You want a bot to open pull requests automatically.
- You want legal or compliance certification.

## Current Supported Checks

- `requires-python` bounds that exclude Python 3.14.
- GitHub Actions Python matrices that omit `3.14`.
- Safe CI patch preview for simple `python-version: [...]` matrices.
- `pydantic.v1` imports and direct Pydantic v1 dependency pins.
- Pydantic v2 pins older than the initial 3.14-supporting 2.12 line.
- runtime annotation readers such as `__annotations__` and `get_type_hints`.
- multiprocessing and `ProcessPoolExecutor` sites that need start-method review.
- `functools.partial` assigned in class bodies.

## Example

```bash
python -m python314_readiness.cli path/to/repo \
  --report python314-readiness-report.json \
  --html-report python314-readiness-report.html
```

Apply only deterministic CI matrix patches:

```bash
python -m python314_readiness.cli path/to/repo --apply
```

## Outputs

- `python314-readiness-report.json`: machine-readable findings and patch data.
- `python314-readiness-report.html`: human-readable migration summary.
- exit code `0` when there are no blocking findings.
- exit code `1` when blocking readiness findings exist.
- exit code `2` when the scanner cannot run.

## Trust Boundary

- Runs locally.
- No GitHub token required.
- No source upload.
- No repo mutation unless `--apply` is explicitly passed.
- Patch mode only touches simple CI Python-version matrices.
