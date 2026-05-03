# Quickstart

## Install and run

```bash
python -m pip install "https://github.com/derekmartin3737-coder/sqlalchemy-14-to-20-codemod/archive/refs/heads/main.zip"
python -m sa20_pack.cli . --report migration-report.json
```

If installation fails, retry from the GitHub quickstart or contact support at
zippers3737@gmail.com.

For local development in this repo:

```bash
python -m pip install -e .[dev]
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
format = ["python", "-m", "ruff", "format", ".", "--check", "--no-cache"]
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
