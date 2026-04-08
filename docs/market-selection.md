# Market Selection

## Goal

Pick one breaking upgrade path that is painful enough to buy, narrow enough to
own, deterministic enough for AST transforms, and cheap enough to distribute as
a zero-infrastructure CLI plus GitHub Action.

## Rubric

Weights reflect revenue potential under the hard constraints.

| Criterion | Weight | What high means |
| --- | ---: | --- |
| Pain severity | 15 | Upgrade blocks releases, breaks CI, or creates real prod risk |
| Install base / ecosystem proxy | 15 | Massive package usage, stars, dependents, or active footprint |
| Edge-case frequency | 10 | Enough messy real-world cases to justify a paid pack |
| Weak existing tooling | 15 | Official/open-source automation is missing or obviously incomplete |
| AST suitability | 15 | High share of changes can be done deterministically |
| Public demo value | 10 | Clear failing-before / passing-after story |
| Willingness to pay | 10 | Teams will pay to de-risk this instead of hand-editing |
| Support burden | 5 | Narrow enough to support asynchronously without becoming a service biz |
| $0 distribution feasibility | 5 | CLI/GitHub Action/static docs are enough |

Scoring is 1-5 per row. Weighted total is normalized to 100.

## Candidate Scorecard

| Candidate | Pain | Base | Edge | Tooling gap | AST fit | Demo | Pay | Support | $0 | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| SQLAlchemy 1.4 -> 2.0 legacy Core/ORM API pack | 5 | 4 | 5 | 5 | 4 | 4 | 5 | 3 | 5 | 89 |
| Pydantic 1 -> 2 migration pack | 5 | 5 | 5 | 3 | 4 | 4 | 4 | 2 | 5 | 83 |
| ESLint `.eslintrc*` -> flat config for v9 | 4 | 5 | 4 | 2 | 5 | 5 | 3 | 4 | 5 | 78 |
| Tailwind CSS v3 -> v4 upgrade pack | 4 | 5 | 5 | 2 | 2 | 5 | 4 | 2 | 5 | 73 |

## Evidence Notes

### 1. SQLAlchemy 1.4 -> 2.0 legacy Core/ORM API pack

Why it scores high:

- SQLAlchemy remains huge: `sqlalchemy` showed 76,400,908 downloads in the last
  week on PyPI when checked on April 6, 2026.
- Buyer pain is real and expensive because it touches the database layer, not a
  cosmetic config file.
- The official migration path is documentation plus warnings, not a codemod.
- The 2.0 migration guide lists multiple removed or changed patterns that are
  structurally detectable: `select()` constructor changes, connectionless
  execution removal, stricter `execute()`, string relationship paths removed,
  legacy declarative imports moved, and other ORM shifts.
- Public demo value is good even with a narrow scope: broken examples can fail
  under SQLAlchemy 2.0 before migration and pass after deterministic rewrites.

What keeps it from a perfect 100:

- Full migration coverage is impossible in a narrow v1 pack.
- Some high-pain cases like `engine.execute()` need careful transaction-aware
  rewrites and should default to manual review.

### 2. Pydantic 1 -> 2 migration pack

Why it is strong:

- `pydantic` showed 168,367,775 downloads in the last week on PyPI when checked
  on April 6, 2026.
- The official v2 migration guide explicitly says `bump-pydantic` exists but is
  still beta.
- Edge cases are plentiful, and backend teams do care about correctness here.

Why it lost:

- There is already an official codemod-like starting point.
- Semantic changes create a heavier support burden than the ideal narrow paid
  pack.
- It is a good business, but not the cleanest "default tool for one painful
  upgrade path" opportunity.

### 3. ESLint `.eslintrc*` -> flat config

Why it matters:

- ESLint has a huge footprint; the npm ecosystem still shows millions of weekly
  downloads and nearly 24k npm dependents.
- The official migration guide says the migrator creates only a starting point,
  is not guaranteed to work immediately, and does not work well for
  `.eslintrc.js`.
- AST automation is excellent.

Why it lost:

- Buyer pain is more "annoying infra churn" than "risky business-critical
  upgrade."
- Teams are less likely to pay for migration packs around lint config than for
  database-layer migration risk.

### 4. Tailwind CSS v3 -> v4

Why it matters:

- `tailwindcss` showed 18,877,764 weekly npm downloads when checked on April 6,
  2026.
- Official upgrade tooling exists, and the v4 launch post explicitly says
  Tailwind ships an automated upgrade tool.
- Public issues show the official tool can still break real projects,
  especially around config/CSS transitions and monorepos.

Why it lost:

- Visual regressions are expensive but harder to validate deterministically with
  zero infrastructure.
- Official tooling is strong enough that a new entrant has to fight a tougher
  competitor from day one.
- Revenue would likely drift toward bespoke design-system work instead of a
  repeatable downloadable product.

## Competitor Landscape For The Chosen Target

Chosen target: **SQLAlchemy 1.4 -> 2.0 legacy Core/ORM API pack**

### Official codemods

- None from the SQLAlchemy project that I could find in public sources on
  April 6, 2026.

### Official upgrade tools

- Official path is the migration guide plus warning-driven cleanup, especially
  enabling `RemovedIn20Warning`, resolving warnings, switching on `future=True`,
  and then testing against an actual 2.0 release.

### Open-source codemods

- I could not find a maintained dedicated SQLAlchemy 2.0 codemod in public
  search results on April 6, 2026. This is an inference from the absence of a
  surfaced maintained project, not a proof that no private or obscure tool
  exists.

### Obvious substitute workflows

- Manual grep + edit + run tests
- Local warning gates with custom scripts
- One-off internal codemods that are never polished into a reusable product
- Internal follow-up work on unsupported findings

## Decision

Build **one product only**:

**`sa20-pack`: a SQLAlchemy 1.4 -> 2.0 migration pack for high-frequency legacy
Core/ORM breakages, with deterministic rewrites first and manual-review
findings for risky cases.**

This is intentionally narrower than "fully migrate any SQLAlchemy app."

## Short Memo

SQLAlchemy is the best revenue target because it sits in a sweet spot the other
finalists miss:

1. The install base is massive enough to matter.
2. The upgrade pain is close to the money because it touches data access and
   release risk.
3. The official migration path is strong on documentation but weak on
   automation.
4. The work is structured enough for deterministic source transforms to prove
   value in public.
5. The product can stay zero-cost to distribute as a CLI, GitHub Action, and
   static documentation.
6. The monetization ladder is clear:
   free scanner -> paid wider-coverage pack -> paid preset bundle.

That combination makes SQLAlchemy the highest-income option under the hard
constraints.

## Sources

- [SQLAlchemy 2.0 migration guide](https://docs.sqlalchemy.org/20/changelog/migration_20.html)
- [SQLAlchemy GitHub repo](https://github.com/sqlalchemy/sqlalchemy)
- [SQLAlchemy PyPI stats](https://pypistats.org/packages/sqlalchemy)
- [SQLAlchemy migration discussion example](https://github.com/sqlalchemy/sqlalchemy/discussions/9214)
- [Pydantic v2 migration guide](https://docs.pydantic.dev/2.0/migration/)
- [Bump Pydantic repo](https://github.com/pydantic/bump-pydantic)
- [Pydantic PyPI stats](https://pypistats.org/packages/pydantic)
- [Pydantic V2 issue example](https://github.com/pydantic/pydantic/issues/9516)
- [ESLint migration guide](https://eslint.org/docs/latest/use/configure/migration-guide)
- [ESLint configuration migrator announcement](https://eslint.org/blog/2024/05/eslint-configuration-migrator/)
- [ESLint npm package](https://www.npmjs.com/package/eslint)
- [Tailwind v4 launch post](https://tailwindcss.com/blog/tailwindcss-v4)
- [Tailwind upgrade guide](https://tailwindcss.com/docs/upgrade-guide)
- [Tailwind upgrade issue example](https://github.com/tailwindlabs/tailwindcss/issues/15120)
- [Tailwind npm package](https://www.npmjs.com/package/tailwindcss)
