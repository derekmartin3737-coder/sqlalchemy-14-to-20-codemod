# pydantic-v2-porter

## Mission

Build a deterministic Pydantic v1 to v2 migration pack that:

- runs locally
- supports only a narrow, documented subset of upgrades
- rewrites high-frequency validator and config patterns safely
- fails closed when a file needs manual follow-up

## Current Supported Scope

- direct `from pydantic import ...` imports
- direct `from pydantic.v1 import ...` imports
- `BaseSettings` import move to `pydantic_settings`
- nested `Config` class to `model_config` for safe literal assignments
- `@validator` to `@field_validator` for exact two-parameter classmethod
  signatures like `(cls, v)`
- `@root_validator(pre=True)` to `@model_validator(mode="before")` for exact
  two-parameter classmethod signatures like `(cls, values)`
- bare `@validate_arguments` to `@validate_call`

## Current Non-Goals

- aliased pydantic imports
- star imports
- `import pydantic` style attribute rewrites
- validator signatures that use `values`, `field`, or `config`
- `each_item`, `always`, or unknown validator kwargs
- post `root_validator`
- removed Pydantic config keys

## Reliability Rule

If a file is outside current supported scope, report it and leave that file
untouched instead of guessing.

## Commercial Status

- Public proof now exists in `docs/public-proof.md`.
- The buyer-facing internal-budget case now lives in `docs/commercial-case.md`.
- Current commercial bar: ready for paid discussion only on the documented
  validator/settings/config subset.
- The tracked public repo now exposes the community scanner only. The full
  commercial apply engine should be delivered privately, not kept in the public
  repo.
