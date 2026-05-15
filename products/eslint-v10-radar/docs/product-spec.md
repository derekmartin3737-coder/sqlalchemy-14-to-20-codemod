# ESLint v10 Migration Radar Product Spec

## Product Promise

ESLint v10 Migration Radar gives JavaScript and TypeScript teams a local report
of v10 blockers before they upgrade. It detects removed eslintrc paths, legacy
ignore/config locations, removed flags, and API usage that needs manual review.

It is not a full flat-config conversion engine.

## Buyer

- Frontend leads.
- JavaScript/TypeScript maintainers.
- Platform teams inventorying many repos.

## Rule Set

- `ESL000`: input file could not be parsed.
- `ESL001`: legacy eslintrc config exists.
- `ESL002`: `package.json#eslintConfig` is no longer supported.
- `ESL003`: `.eslintignore` requires flat-config migration.
- `ESL004`: `ESLINT_USE_FLAT_CONFIG=false` blocks v10 readiness.
- `ESL005`: removed `v10_config_lookup_from_file` flag is present.
- `ESL006`: legacy ESLint API usage needs migration.
- `ESL007`: dynamic eslintrc JavaScript config needs manual conversion.
- `ESL008`: legacy config exists without `eslint.config.*`.

## Safe Patch Boundary

The only v0.1 apply behavior removes simple package-script environment flags:

- `ESLINT_USE_FLAT_CONFIG=false`
- `ESLINT_FLAGS=v10_config_lookup_from_file`

Legacy config files and ignore patterns are report-only.

## Sources

- ESLint v10 release notes:
  `https://eslint.org/blog/2026/02/eslint-v10.0.0-released/`
- ESLint v10 migration guide:
  `https://eslint.org/docs/latest/use/migrate-to-10.0.0`
- ESLint configuration migration guide:
  `https://eslint.org/docs/latest/use/configure/migration-guide`

## Exit Codes

- `0`: no blocking findings
- `1`: blocking findings exist
- `2`: scanner could not run
