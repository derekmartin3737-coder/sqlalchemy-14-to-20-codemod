# Ranks 3-6 Product Task List

This is the active build ledger for the next four Autonomous Product Wells.
If work stops, resume at the first unchecked item in the current product.

## Rank 3 - Apple Privacy Manifest Composer

Product path: `products/apple-privacy-manifest-composer/`

- [x] Verify official Apple privacy-manifest and required-reason API sources.
- [x] Create product scaffold, README, and package metadata.
- [x] Build a local scanner for Swift, Objective-C, C/C++, plists, Podfiles,
  SwiftPM manifests, and bundled privacy manifests.
- [x] Detect required-reason API categories:
  - UserDefaults
  - file timestamps
  - disk space
  - system boot time
  - active keyboards
- [x] Detect listed third-party SDK names from dependency manifests.
- [x] Parse existing `PrivacyInfo.xcprivacy` files and identify missing API
  category declarations.
- [x] Generate JSON and HTML reports with confidence and source links.
- [x] Generate a candidate `PrivacyInfo.xcprivacy` patch/manifest for missing
  required-reason API categories.
- [x] Add fail-closed findings where the tool cannot know the human reason.
- [x] Add proof fixtures and tests.
- [x] Run tests, lint, typecheck, compile/build verification.
- [x] Add product spec, public proof, and commercial case docs.

## Rank 4 - CRA Evidence Builder

Product path: `products/cra-evidence-builder/`

- [x] Verify official Cyber Resilience Act reporting and obligation sources.
- [x] Create product scaffold, README, and package metadata.
- [x] Build a local scanner for dependency manifests, container files,
  security policy files, release metadata, and disclosure/contact artifacts.
- [x] Generate a CRA evidence inventory:
  - SBOM source readiness
  - vulnerability handling process
  - incident contact path
  - release/version traceability
  - security update policy
  - known public reporting obligations
- [x] Generate a deterministic evidence dossier in JSON and HTML.
- [x] Generate missing-template files only where safe.
- [x] Add fail-closed findings for legal/compliance interpretation.
- [x] Add proof fixtures and tests.
- [x] Run tests, lint, typecheck, compile/build verification.
- [x] Add product spec, public proof, and commercial case docs.

## Rank 5 - ESLint v10 Migration Radar

Product path: `products/eslint-v10-radar/`

- [x] Verify official ESLint v10 and flat-config migration sources.
- [x] Create product scaffold, README, and package metadata.
- [x] Build a local scanner for package metadata, ESLint configs, ignore files,
  CLI scripts, environment flags, and ESLint API usage.
- [x] Detect v10 blockers:
  - `.eslintrc*` usage
  - `package.json#eslintConfig`
  - `.eslintignore`
  - `ESLINT_USE_FLAT_CONFIG=false`
  - `v10_config_lookup_from_file` feature flag
  - `LegacyESLint`, `FlatESLint`, or `configType: "eslintrc"`
- [x] Generate JSON and HTML reports.
- [x] Generate safe patch previews for env flag/script cleanup and simple
  ignore/config migration notes.
- [x] Add fail-closed findings for dynamic JS configs.
- [x] Add proof fixtures and tests.
- [x] Run tests, lint, typecheck, compile/build verification.
- [x] Add product spec, public proof, and commercial case docs.

## Rank 6 - Package Publisher Hardening Pack

Product path: `products/package-publisher-hardening/`

- [x] Verify official npm, PyPI, and trusted-publishing/attestation sources.
- [x] Create product scaffold, README, and package metadata.
- [x] Build a local scanner for GitHub/GitLab workflows, npm package metadata,
  PyPI package metadata, release scripts, token usage, and publish actions.
- [x] Detect package-publishing risks:
  - npm token publish flows
  - missing OIDC permissions
  - missing provenance/attestation flags
  - PyPI API-token publish flows
  - missing trusted publishing action setup
  - broad release permissions
- [x] Generate JSON and HTML reports.
- [x] Generate safe patch previews for GitHub Actions trusted-publishing
  workflows where the structure is simple.
- [x] Add fail-closed findings for custom publish scripts.
- [x] Add proof fixtures and tests.
- [x] Run tests, lint, typecheck, compile/build verification.
- [x] Add product spec, public proof, and commercial case docs.

## Shared Release Gate

Each product is only considered finished when:

- [x] CLI exists and documents exit codes.
- [x] JSON report exists.
- [x] HTML report exists.
- [x] Patch/manifest preview mode exists where safe.
- [x] Apply/write mode is limited to deterministic generated artifacts.
- [x] Proof fixtures include risky, clean, and fail-closed examples.
- [x] Local tests pass.
- [x] Lint passes.
- [x] Typecheck passes.
- [x] Compile/build verification passes.
- [x] Product docs state what the tool does not claim.
