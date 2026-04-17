# sa20-pack

`sa20-pack` is the public trust layer for one narrow upgrade path: a
zero-infrastructure SQLAlchemy 1.4 to 2.0 migration scanner plus proof,
reports, and commercial-pack docs.

Website: [zippertools.org](https://zippertools.org/)

Public proof: [SQLAlchemy migration proof on public files](https://zippertools.org/proof/sqlalchemy-public-proof/)

## Start With The Exact Breakage

| Problem | Page |
| --- | --- |
| `OptionEngine` has no `execute` | [Fix the OptionEngine execute error](https://zippertools.org/sqlalchemy/optionengine-execute-error/) |
| `Engine` has no `execute` | [Fix the Engine execute error](https://zippertools.org/sqlalchemy/engine-attribute-error-execute/) |
| `Query.get()` warnings | [Fix LegacyAPIWarning for Query.get](https://zippertools.org/sqlalchemy/legacyapiwarning-query-get/) |
| `select([..])` legacy syntax | [Fix legacy select warnings](https://zippertools.org/sqlalchemy/select-legacy-mode-warning/) |
| `joinedload_all` removal | [Fix joinedload_all migration issues](https://zippertools.org/sqlalchemy/joinedload-all-nameerror/) |
| Unsure where to start | [SQLAlchemy 2.0 migration triage checklist](https://zippertools.org/sqlalchemy/sqlalchemy-20-triage-checklist/) |
| Automation or manual migration | [Manual migration vs codemod](https://zippertools.org/sqlalchemy/sqlalchemy-manual-vs-codemod/) |
| Pydantic `BaseSettings` import error | [Fix BaseSettings import errors](https://zippertools.org/pydantic/basesettings-import-error/) |
| Pydantic `@validator` warnings | [Fix Pydantic validator deprecation warnings](https://zippertools.org/pydantic/validator-deprecation-warning/) |

It is deliberately opinionated:

- free scanner first
- fail closed on ambiguous cases
- machine-generated migration report every run
- the public repo does not expose the commercial apply engine

## Why this exists

SQLAlchemy's official migration story is good documentation and warning-driven
cleanup, but not a maintained product workflow. This public repo establishes
trust by showing supported scope, demo value, and machine-generated findings
before a buyer ever pays for the commercial migration pack.

## Current coverage

- scans for legacy declarative imports
- scans for `select([..])` list syntax
- scans for `session.query(Model).get(pk)`
- scans for simple string relationship `join()` and loader options
- scans for simple DML constructor keyword usage
- flags unsupported legacy patterns outside safe automation

The paid commercial pack contains the full apply engine and broader coverage.

## Who This Is For

- teams still upgrading a SQLAlchemy 1.4 codebase to 2.0
- repos that still contain `select([..])`, `Query.get(...)`, string
  relationship names, or legacy declarative imports
- engineers who want a deterministic scan and a machine-generated report before
  deciding whether to buy the commercial pack

Run the free scan first. The supported subset is intentionally narrow and the
product is strongest when the report shows several supported rewrites in one
repo.

## Do Not Buy This If

- your repo is already mostly 2.0-safe
- your upgrade is dominated by `engine.execute(...)`, `Query.from_self()`, or
  broad `Query` API rewrites
- you want a tool that guesses through ambiguous SQLAlchemy behavior

## Quickstart

See [quickstart](docs/quickstart.md).

## Searchable issue pages

The storefront has exact-problem landing pages for the highest-signal queries
we already support:

- [SQLAlchemy migration tool overview](https://zippertools.org/products/sa20-pack/)
- [SQLAlchemy public proof](https://zippertools.org/proof/sqlalchemy-public-proof/)
- [`session.query` migration](https://zippertools.org/sqlalchemy/session-query-migration/)
- [`session.query(...).get()` migration](https://zippertools.org/sqlalchemy/session-query-get/)
- [`select([columns])` migration](https://zippertools.org/sqlalchemy/select-list-syntax/)
- [`declarative_base` import migration](https://zippertools.org/sqlalchemy/declarative-imports/)
- [`join("addresses")` migration](https://zippertools.org/sqlalchemy/string-join-paths/)
- [`joinedload("addresses")` migration](https://zippertools.org/sqlalchemy/string-loader-options/)
- [`engine.execute(...)` removed](https://zippertools.org/sqlalchemy/engine-execute-removed/)
- [`insert(table, values=...)` migration](https://zippertools.org/sqlalchemy/insert-values-kwargs/)

The storefront also carries Pydantic v2 migration pages for the documented
supported subset:

- [`@validator(...)` migration](https://zippertools.org/pydantic/validator-to-field-validator/)
- [`BaseSettings` migration](https://zippertools.org/pydantic/basesettings-import-error/)
- [`root_validator(pre=True)` migration](https://zippertools.org/pydantic/root-validator-pre/)

## Launch check

Before announcing the public site, run:

```bash
python -m sa20_pack.launch_readiness
```

or:

```bash
sa20-pack-launch-check
```

The command fails if required launch assets are missing or if
`site/config.js` still contains placeholder values.

## Docs

- [Market selection](docs/market-selection.md)
- [Product spec](docs/product-spec.md)
- [Demo](docs/demo.md)
- [Pricing](docs/pricing.md)
- [Public proof](docs/public-proof.md)
- [Commercial case](docs/commercial-case.md)
- [Demo summary artifact](artifacts/demo-migration-report.json)
- [Claims and safeguards](docs/claims-safeguards.md)
- [Store products](docs/store-products.md)
- [Fulfillment](docs/fulfillment.md)
- [Deployment](docs/deployment.md)
- [Company setup](docs/company-setup.md)
- [Legal checklist](docs/legal-checklist.md)
- [Launch readiness](docs/launch-readiness.md)
- [Privacy policy](docs/privacy-policy.md)
- [Refund policy](docs/refund-policy.md)
- [Terms of sale](docs/terms-of-sale.md)
- [License terms](docs/license-terms.md)
- [Support scope](docs/support-scope.md)
- [Repo fit checklist](docs/repo-fit-checklist.md)
- [Preset bundle checklist](docs/preset-bundle-checklist.md)
- [Sales ops](docs/sales-ops.md)
- [Lead tracker](docs/lead-tracker.md)
- [Launch log](docs/launch-log.md)
- [KPI dashboard](docs/kpi-dashboard.md)
- [Distribution playbook](docs/distribution-playbook.md)
- [Launch posts](docs/launch-posts.md)
- [Packaging](docs/packaging.md)
- [Release checklist](docs/release-checklist.md)
- [Limitations](docs/limitations.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Manual migration comparison](docs/comparison.md)
- [Open-source split](docs/open-source-split.md)
- [Backlog](docs/backlog.md)

## Public vs Paid

Public repo:

- free community scanner
- demo artifacts and public proof
- website/storefront assets
- buyer docs, policies, and pricing structure

Paid commercial pack:

- apply engine
- broader transform coverage
- richer rollout templates and presets
- downloadable ZIP delivery through Payhip

## License

MIT, unless the packaging strategy changes before public release.
