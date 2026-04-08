# flatconfig-lift

## Mission

Build a deterministic ESLint legacy-config to flat-config migration pack that:

- works locally
- avoids hosted dependencies
- supports only static config shapes we can parse safely
- fails closed on ambiguous or code-driven configs

## Current Supported Scope

- `.eslintrc`
- `.eslintrc.json`
- `.eslintrc.yaml`
- `.eslintrc.yml`
- `package.json` with `eslintConfig`

Target output:

- `eslint.config.cjs`

## Current Non-Goals

- `.eslintrc.js`
- `.eslintrc.cjs`
- `.eslintrc.mjs`
- configs that depend on functions, conditionals, or runtime logic
- automatic plugin import rewrites beyond the `FlatCompat` bridge pattern

## Reliability Rule

If a repo is outside current supported scope, report it and stop instead of
guessing.

## Commercial Status

- Public proof now exists in `docs/public-proof.md`.
- The buyer-facing internal-budget case now lives in `docs/commercial-case.md`.
- Current commercial bar: ready for paid discussion only on the documented
  static JSON/YAML subset.
- The tracked public repo now exposes the community scanner only. The full
  commercial apply engine should live in private delivery artifacts, not in the
  public tree.
