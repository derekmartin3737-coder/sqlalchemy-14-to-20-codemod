# Product Spec

## Goal

Create a reliable migration pack for moving static legacy ESLint config files to
an `eslint.config.cjs` flat-config bridge for ESLint v9-era repos.

## Supported source formats

- `.eslintrc`
- `.eslintrc.json`
- `.eslintrc.yaml`
- `.eslintrc.yml`
- `package.json` with `eslintConfig`

## Explicit exclusions

- `.eslintrc.js`
- `.eslintrc.cjs`
- `.eslintrc.mjs`
- configs that depend on runtime code, imported functions, or conditional logic
- repos with multiple legacy config sources at once
- negated ignore patterns in `.eslintignore`

## Deterministic transforms

- write `eslint.config.cjs`
- bridge the parsed legacy config through `FlatCompat`
- migrate `ignorePatterns` and simple `.eslintignore` entries into `ignores`
- remove legacy-only `root`
- optionally add `@eslint/js` and `@eslint/eslintrc` to `devDependencies`

## Flag-only behaviors

- JS config sources
- multiple legacy sources
- negated ignore patterns
- existing `eslint.config.*`
- package managers or plugin ecosystems that still need buyer follow-up

## Done means

- the repo gets a generated `eslint.config.cjs`
- the tool emits a structured report
- unsupported cases stop with explicit findings
- tests prove the claimed supported cases
