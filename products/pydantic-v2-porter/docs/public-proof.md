# Public Proof

Proof pass date: 2026-04-07

This product was exercised against shallow clones of public GitHub repos to
check that the supported subset behaves the way the product claims, and that
unsupported patterns are reported instead of silently rewritten.

## Public repos tested

- `shahmir2004/asylum-appointment-bot`
  - Result: supported
  - Status: `preview_only` in dry-run, `applied` on a copied repo
  - Files changed: `backend/src/config.py`
  - Verified transforms:
    - `BaseSettings` move to `pydantic_settings`
    - `Config` -> `model_config`
    - `validator` -> `field_validator`

- `IT21220456/Bovitrack-System`
  - Result: supported
  - Status: `preview_only` in dry-run, `applied` on a copied repo
  - Files changed: `API/milk_yield.py`
  - Verified transforms:
    - `validator` -> `field_validator`

- `MasterGroosha/telegram-bombsweeper-bot`
  - Result: blocked correctly
  - Status: `manual_review_required`
  - Why blocked:
    - validators that use `values`
  - Safe behavior:
    - file left untouched

- `confar/ddd-reference-api-python`
  - Result: mixed repo, blocked correctly
  - Status: `manual_review_required`
  - Supported file:
    - `settings/enviroments/base.py`
  - Blocked file:
    - `settings/infra.py`
  - Why blocked:
    - validators that use `values`

- `electricitymaps/electricitymaps-contrib`
  - Result: mixed repo, blocked correctly
  - Status: `manual_review_required`
  - Supported files:
    - `electricitymap/contrib/config/data_center_model.py`
    - `tests/config/test_data_center_model.py`
  - Blocked files:
    - files with post `root_validator`
    - files with validator signatures outside the supported subset

## Fixes uncovered by the public proof pass

- broadened validator support from `(cls, value)` only to exact two-parameter
  classmethod signatures like `(cls, v)`
- made CLI diff printing safe on Windows consoles that cannot emit all Unicode
  characters directly

## What this proves

- the supported subset works on real public repo code, not only fixtures
- unsupported validator and root-validator shapes are surfaced as explicit
  manual-review findings
- repo-level status correctly stays `manual_review_required` if any targeted
  file is outside current scope

## What this does not prove

- arbitrary alias-heavy import patterns
- full support for validator signatures that use `values`, `field`, `config`,
  `each_item`, or `always`
- full Pydantic v2 migration coverage for every public repo that imports
  Pydantic
