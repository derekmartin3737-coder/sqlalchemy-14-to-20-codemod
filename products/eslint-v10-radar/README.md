# ESLint v10 Migration Radar

ESLint v10 Migration Radar is a local scanner for repositories that still have
legacy ESLint configuration or API usage after the eslintrc system was removed
in ESLint v10.

It produces JSON and HTML reports, plus deterministic patch previews for simple
environment/script flags that are no longer useful.

## Who This Is For

- Frontend leads planning an ESLint v10 migration.
- JavaScript/TypeScript maintainers with mixed legacy lint config.
- Platform teams that need to inventory many repos quickly.

## Do Not Use This If

- You need a complete flat-config conversion engine.
- You expect JavaScript config evaluation.
- You want hosted repository scanning.
- You need plugin compatibility proof without running ESLint.

## Current Supported Checks

- `.eslintrc*` files
- `package.json#eslintConfig`
- `.eslintignore`
- `ESLINT_USE_FLAT_CONFIG=false`
- `v10_config_lookup_from_file`
- `LegacyESLint`, `FlatESLint`, and `configType: "eslintrc"`
- missing `eslint.config.*` when legacy config is still present

## Example

```bash
python -m eslint_v10_radar.cli path/to/repo \
  --report eslint-v10-report.json \
  --html-report eslint-v10-report.html
```

Apply only safe package-script flag removals:

```bash
python -m eslint_v10_radar.cli path/to/repo --apply
```
