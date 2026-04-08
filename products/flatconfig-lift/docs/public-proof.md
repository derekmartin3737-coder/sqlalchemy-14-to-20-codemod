# Public Proof

Proof pass date: 2026-04-07

This pass exercised `flatconfig-lift` on public ESLint config files to verify
that the supported static subset rewrites cleanly and that unsupported config
shapes are blocked instead of guessed through.

## Supported Path Proof

- [`apache/cordova-plugin-splashscreen`](https://github.com/apache/cordova-plugin-splashscreen/blob/master/.eslintrc.yml)
  - Public file: `.eslintrc.yml`
  - Result: supported
  - Status after `--apply`: `applied`
  - Verified outcome:
    - generated `eslint.config.cjs` using `FlatCompat`
    - preserved override file globs and extends
    - updated `package.json` with flat-config bridge dependencies

- [`typestack/class-validator`](https://github.com/typestack/class-validator/blob/develop/.eslintrc.yml)
  - Public file: `.eslintrc.yml`
  - Result: supported
  - Status after `--apply`: `applied`
  - Verified outcome:
    - preserved parser, parser options, plugins, extends, and rules
    - generated bridge config instead of flattening by guesswork

- [`google/model-viewer`](https://github.com/google/model-viewer/blob/main/.eslintrc.yaml)
  - Public file: `.eslintrc.yaml`
  - Result: supported
  - Status after `--apply`: `applied`
  - Verified outcome:
    - preserved `env`, `globals`, parser, plugins, and extends
    - generated `eslint.config.cjs` with `FlatCompat`

## Fail-Closed Proof

- [`qdsang/lv_gui_builder`](https://github.com/qdsang/lv_gui_builder/blob/3402d4a3a600b974e822a6ee675ad2a69ebf08ad/.eslintrc.cjs)
  - Public file: `.eslintrc.cjs`
  - Result: blocked correctly
  - Status: `manual_review_required`
  - Findings:
    - `unsupported-js-config`
    - `no-supported-config`

- [`sablier-labs/docs`](https://github.com/sablier-labs/docs)
  - Public files:
    - `.eslintrc.yml`
    - `eslint.config.mjs`
  - Result: blocked correctly
  - Status: `manual_review_required`
  - Findings:
    - `existing-flat-config`

## Public-Proof Commands

```bash
PYTHONPATH=src python -m flatconfig_lift.cli ../../public_repo_trials/flatconfig-lift/apache-cordova --apply --report ../../public_repo_trials/flatconfig-lift/apache-cordova-report.json
PYTHONPATH=src python -m flatconfig_lift.cli ../../public_repo_trials/flatconfig-lift/typestack-class-validator --apply --report ../../public_repo_trials/flatconfig-lift/typestack-class-validator-report.json
PYTHONPATH=src python -m flatconfig_lift.cli ../../public_repo_trials/flatconfig-lift/google-model-viewer --apply --report ../../public_repo_trials/flatconfig-lift/google-model-viewer-report.json
PYTHONPATH=src python -m flatconfig_lift.cli ../../public_repo_trials/flatconfig-lift/qdsang-lv-gui-builder --report ../../public_repo_trials/flatconfig-lift/qdsang-lv-gui-builder-report.json
PYTHONPATH=src python -m flatconfig_lift.cli ../../public_repo_trials/flatconfig-lift/sablier-docs --report ../../public_repo_trials/flatconfig-lift/sablier-docs-report.json
```

## Fixes Uncovered By This Pass

- hardened `package.json` discovery and loading to handle UTF-8 BOM files
  instead of crashing during source detection

## What This Proves

- three public JSON or YAML legacy configs are inside supported scope
- two public unsupported shapes are refused explicitly
- the bridge output is stable enough to show to a team before they delete the
  legacy config file

## What This Does Not Prove

- safe evaluation of `.eslintrc.js`, `.cjs`, or `.mjs` logic
- plugin ecosystem compatibility beyond what `FlatCompat` can express from the
  source config
