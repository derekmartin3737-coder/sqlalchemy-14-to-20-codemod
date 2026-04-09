# AGENTS.md

## Mission

Build a zero-cost, repo-native codemod migration product that can become the
default tool for one painful breaking upgrade path, with deterministic
transforms first, LLM use optional only for edge cases, and a validation loop
that refuses to claim success when typecheck/build/tests fail.

## Current Decision

- Chosen target: SQLAlchemy 1.4 -> 2.0 migration pack for the highest-frequency
  legacy ORM/Core patterns.
- Product positioning: a narrow "legacy query and execution API" codemod pack,
  not a claim to fully automate every SQLAlchemy 2.0 migration.
- Reason for current bias: very high ecosystem size, painful upgrade path,
  strong buyer willingness to pay, weak existing automation compared with the
  other finalists.

## Evidence Status

- Official docs reviewed:
  - SQLAlchemy 2.0 migration guide
  - SQLAlchemy declarative mapping docs
  - ESLint flat-config migration guide and migrator announcement
  - Tailwind CSS v4 upgrade guide and v4 launch post
  - Pydantic v2 migration guide and bump-pydantic repo
  - GitHub Pages limits
  - Cloudflare Pages docs and Cloudflare Web Analytics docs
  - Lemon Squeezy getting-paid, payments, fees, and supported-countries docs
  - SBA business-structure and EIN guidance
  - IRS EIN guidance
  - Oregon business registration, assumed-business-name, and license-directory pages
  - FTC advertising and endorsement guidance
  - USPTO trademark search guidance
  - FinCEN BOI toolkit
- Public issue/discussion signal reviewed:
  - SQLAlchemy migration discussion examples
  - Tailwind upgrade issues/discussions
  - Pydantic V2 issue examples
- Install-base proxies reviewed:
  - `sqlalchemy` and `pydantic` PyPI download stats
  - `tailwindcss` npm package page
  - `eslint` npm dependents/package metadata

## Constraints

- Startup cost must remain exactly $0.
- No paid API, hosting, ads, datasets, or dev tools.
- Everything must live in a normal repository workflow.
- Deterministic transforms first; uncertain cases go to manual review.
- Every code/doc change is only "done" after local verification succeeds.

## Planned Repo Shape

- `docs/`
  - `market-selection.md`
  - `product-spec.md`
  - `pricing.md`
  - `launch-posts.md`
  - `demo.md`
- `src/sa20_pack/`
  - CLI
  - codemods
  - validation runner
  - report generator
  - fixture support
- `tests/`
- `fixtures/`
- `.github/actions/sa20-pack/`
- `.github/workflows/`

## Verification Standard

The repo should support:

- format/lint
- typecheck
- tests
- package build

And the migration runner itself should produce a structured report showing:

- files changed
- transforms applied
- unsupported/manual-review findings
- validation command results
- overall confidence

## Session Notes

- Workspace started empty and not yet initialized as a git repository.
- Python 3.12.10 is available.
- Node 22.11.0 is available.
- `uv` is not installed.
- `npm` works through `npm.cmd`.
- `mypy 1.20.0` crashed the interpreter on this machine; pinning to
  `mypy 1.11.2` fixed that.
- Windows filesystem permissions in this workspace caused repeated temp/cache
  failures. The validation runner now redirects temp, bytecode, and cache paths
  into repo-local scratch directories.

## Current State

- `docs/market-selection.md` completed with rubric, scorecard, and decision.
- `docs/product-spec.md` completed.
- `docs/max-revenue-todo.md` completed as the working revenue roadmap.
- `docs/product-ideas.txt` is the rolling tracker for future product candidates,
  filtered against the strict downloadable/autonomous/no-human-in-the-loop
  constraint.
- `docs/commercial-benchmark.md` is the product go / no-go bar. A product is
  not commercially ready until it is strong enough for a buyer to justify real
  budget to a manager.
- `docs/paid-product-checklist.md` is the release gate for every paid pack:
  boss-approval, scope, leak-prevention, commerce, verification, and
  compliance all have to pass.
- Commercial delivery artifacts are now kept outside the tracked public tree so
  the repo can stay scanner-first.
- `docs/public-proof.md` and `docs/commercial-case.md` now exist for the root
  SQLAlchemy product.
- `products/flatconfig-lift/` now exists as the second product subproject, with
  its own CLI, fixtures, tests, and product spec.
- `products/flatconfig-lift/docs/public-proof.md` and
  `products/flatconfig-lift/docs/commercial-case.md` now document public-proof
  evidence and the buyer case for the static-config subset.
- `products/pydantic-v2-porter/` now exists as the third product subproject,
  with deterministic validator/config/settings rewrites, fail-closed findings,
  and a 12-test fixture suite.
- `products/pydantic-v2-porter/docs/commercial-case.md` now exists beside the
  existing public-proof doc, so the first three products all have a
  boss-readable budget case and explicit "do not buy this if" boundaries.
- `docs/max-revenue-todo.md` now also contains the detailed go-live checklist
  for website hosting, payments, payout access, analytics, and legal readiness.
- Static storefront pages now exist under `site/` with config-based checkout
  links, success/cancel pages, policy page, and Cloudflare analytics hook.
- The public storefront has been polished and pushed live on GitHub Pages.
- `wrangler.jsonc` now exists so the same storefront can be deployed through
  Cloudflare without re-entering static asset settings by hand.
- `site/config.js` is now populated with the current seller name, contact email,
  and public GitHub repo URL.
- Payhip is now the active checkout fallback and has live unlisted product links
  for the first two products.
- Store-product copy, fulfillment docs, release checklist, repo-fit checklist,
  preset-bundle checklist, legal checklist, lead tracker, and launch log now
  exist.
- Claims-and-safeguards docs now exist, and the public/legal copy has been
  tightened to avoid broad guarantees.
- `site/config.js` now points the storefront at the live Payhip links for:
  - `sa20-pack Edge-Case Migration Pack`: `https://payhip.com/b/QimJ6`
  - `sa20-pack Preset Bundle`: `https://payhip.com/b/wh2Ro`
- The third product still needs its checkout link wired into the storefront if
  we decide to expose it there.
- Repo launch/legal docs now exist for deployment, company setup, policies, KPI
  tracking, and launch readiness.
- `sa20_pack.launch_readiness` now checks for missing launch assets and
  placeholder values in `site/config.js`.
- Core CLI, transforms, validation runner, reporting, and fixtures are working.
- Demo fixture migrates from failing pre-state to passing post-state.
- Generated demo artifacts live under `artifacts/`.
- GitHub Action wrapper and CI workflow are scaffolded.
- `flatconfig-lift` is now scaffolded under `products/flatconfig-lift` with:
  - deterministic static-config discovery
  - `eslint.config.cjs` generation through `FlatCompat`
  - ignore-pattern migration for simple cases
  - fail-closed findings for JS configs, multiple sources, and negated ignores
  - its own README, AGENTS file, fixtures, tests, and compile-based build check
- `pydantic-v2-porter` is now scaffolded under `products/pydantic-v2-porter`
  with:
  - deterministic rewrites for direct `pydantic` / `pydantic.v1` imports
  - `BaseSettings` move to `pydantic_settings`
  - safe `Config` -> `model_config` conversion with key renames
  - strict `validator` / `root_validator(pre=True)` / `validate_arguments`
    decorator rewrites
  - fail-closed findings for alias imports, removed config keys, post root
    validators, and signature-heavy validators
  - its own README, AGENTS file, fixtures, tests, and compile-based build check
  - a public proof pass documented in
    `products/pydantic-v2-porter/docs/public-proof.md`
- The first three products now meet the commercial benchmark for their
  documented supported subsets:
  - `sa20-pack` for the SQLAlchemy patterns in `docs/product-spec.md`
  - `flatconfig-lift` for static JSON/YAML ESLint configs
  - `pydantic-v2-porter` for the documented validator/settings/config subset
- The tracked public repo is now being split into community scanners only so
  public GitHub establishes trust without exposing the full commercial apply
  engines.

## Next Steps

1. Use the new "Before New Features" section in `docs/max-revenue-todo.md` as
   the current operating queue.
2. Keep the sole-proprietor / no-LLC path explicit, and resolve seller-name /
   assumed-business-name questions before first paid launch.
3. Keep `site/config.js` in sync with the live checkout provider; right now the
   root storefront uses Payhip links for product 1 and product 2.
4. Keep the paid layer software-only: edge-case pack plus preset bundle, with
   no service dependency or human coding offer.
5. Finalize the paid SKUs, deliverable format, analytics path, and legal sanity
   checks before expanding coverage again.
6. Decide whether to keep the compile-based build step or add a clean
   wheel/sdist packaging path as a separate verified command.
7. Expand transform coverage into the next most common removed legacy helpers.
8. Turn the paid edge-case split from docs into actual packaged downloadable
   offers.
9. Keep full-repo public proof running, not just public-file proof, before
   starting product 4.
10. Replace the currently published Lemon files with genuinely private
    commercial ZIPs before treating checkout as real paid delivery.
11. Keep this file updated as decisions harden or blockers appear.
