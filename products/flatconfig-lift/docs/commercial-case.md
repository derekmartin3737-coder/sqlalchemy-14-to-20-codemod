# Commercial Case

## Budget Sentence

`flatconfig-lift` turns a static legacy ESLint config into a flat-config bridge
and tells the team when it must stop and review manually, instead of wasting
time rebuilding config by hand from docs.

## Who This Is For

- teams moving from legacy `.eslintrc*` files or `package.json` `eslintConfig`
  to flat config
- repos whose config is static data, not executable JS logic
- engineers who want a generated bridge file plus explicit notes before they
  delete the old config

## Why This Is Worth Real Budget

- rebuilding ESLint config by hand is error-prone and annoying
- the free scan immediately tells a team whether the config source is supported
- the generated bridge preserves enough structure to remove several hours of
  trial-and-error setup
- the fail-closed path is valuable because it says "stop" on JS config logic or
  an already-present flat config

## Why This Beats Docs Plus Manual Rebuild

- the output is a concrete `eslint.config.cjs`, not only a checklist
- ignores, parser settings, plugins, extends, and rules move together
- `package.json` dependency updates are bundled with the migration
- blocked cases are explicit and immediate

## Do Not Buy This If

- your repo uses `.eslintrc.js`, `.cjs`, or `.mjs`
- your repo already has `eslint.config.*`
- you need the tool to interpret arbitrary JavaScript config logic

## Current Honest Read

For static JSON and YAML legacy configs, this now clears the commercial bar.
An engineer can show the public proof, generated bridge file, and demo report
and make a credible case that buying the pack is cheaper than a manual rebuild.
