# Quickstart

## Install

```bash
python -m pip install sa20-pack
```

For local development in this repo:

```bash
python -m pip install -e .[dev]
```

## Dry run

```bash
python -m sa20_pack.cli path/to/repo --report migration-report.json
```

What you get:

- supported-candidate detection
- machine-generated JSON report
- manual-review findings for unsupported patterns

## Paid apply path

The public repo is scanner-only. Use the free scan first, then the paid pack
for the documented apply flow.

## Validation config

The runner reads commands from `pyproject.toml`:

```toml
[tool.sa20_pack.validation]
format = ["python", "-m", "ruff", "format", ".", "--no-cache"]
typecheck = ["python", "-m", "mypy", "src", "tests"]
build = ["python", "-m", "sa20_pack.build_runner"]
test = ["python", "-m", "pytest", "-p", "no:cacheprovider"]
```

## GitHub Action

Use the local composite action:

```yaml
- uses: ./.github/actions/sa20-pack
  with:
    path: .
    report-path: migration-report.json
```
