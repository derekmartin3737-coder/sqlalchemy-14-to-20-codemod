# Product Spec

## Supported Source

- Pydantic v1-style code that uses direct `from pydantic import ...` imports
- Pydantic v1 compatibility imports through `from pydantic.v1 import ...`
- Python source files only

## Target

- Pydantic v2-compatible imports and validator decorators for the supported
  subset

## Deterministic Transforms

- `from pydantic.v1 import ...` -> `from pydantic import ...`
- `BaseSettings` import move to `from pydantic_settings import BaseSettings`
- nested `Config` -> `model_config = {...}` when values are safe literals
- config key renames:
  - `allow_population_by_field_name` -> `populate_by_name`
  - `anystr_lower` -> `str_to_lower`
  - `anystr_strip_whitespace` -> `str_strip_whitespace`
  - `anystr_upper` -> `str_to_upper`
  - `keep_untouched` -> `ignored_types`
  - `max_anystr_length` -> `str_max_length`
  - `min_anystr_length` -> `str_min_length`
  - `orm_mode` -> `from_attributes`
  - `schema_extra` -> `json_schema_extra`
  - `validate_all` -> `validate_default`
- `allow_mutation = False` -> `frozen = True`
- `allow_mutation = True` -> `frozen = False`
- `@validator("field")` -> `@field_validator("field")` for exact
  two-parameter classmethod signatures like `(cls, v)`
- `@validator(..., pre=True)` -> `@field_validator(..., mode="before")`
- `@root_validator(pre=True)` -> `@model_validator(mode="before")` for exact
  two-parameter classmethod signatures like `(cls, values)`
- bare `@validate_arguments` -> `@validate_call`

## Flag Only

- aliased pydantic imports
- star imports
- `import pydantic` style usage
- validator signatures with extra parameters
- `each_item=True`
- `always=True`
- unknown validator kwargs
- post `root_validator`
- removed config keys
- classes that already define `model_config`

## Exclusions

- data-model semantic fixes
- automatic dependency-file edits beyond reporting that
  `pydantic-settings` is required
- generic code modernization outside the migration path

## Done Means

- machine-generated report exists
- supported files are rewritten deterministically
- unsupported files stay untouched
- lint, typecheck, tests, and compile-based build verification pass
