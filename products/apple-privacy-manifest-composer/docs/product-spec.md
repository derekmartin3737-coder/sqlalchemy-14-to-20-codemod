# Apple Privacy Manifest Composer Product Spec

## Product Promise

Apple Privacy Manifest Composer gives app teams a local, source-private inventory
of required-reason API usage, listed third-party SDK dependencies, existing
privacy-manifest coverage, and a candidate `PrivacyInfo.xcprivacy` template.

It does not choose a legal or business reason for an API. It identifies what
needs review and produces the artifact shell that makes the review faster.

## Buyer

- iOS teams preparing an App Store submission.
- Mobile agencies maintaining many client apps.
- SDK maintainers that need a repeatable manifest inventory.

## Current Scope

- Swift, Objective-C, C, C++, and header source scanning.
- `PrivacyInfo.xcprivacy` parsing.
- Dependency-name scanning in common manifests such as `Podfile`,
  `Package.swift`, `Cartfile`, `pubspec.yaml`, and `package.json`.
- JSON and HTML reports.
- Candidate plist generation with `REVIEW_REQUIRED` placeholders.

## Rule Set

- `APM000`: input file could not be parsed.
- `APM001`: required-reason API usage lacks a privacy manifest.
- `APM002`: existing manifest is missing an accessed API category.
- `APM003`: detected API usage needs human reason selection.
- `APM004`: listed third-party SDK requires privacy-manifest review.
- `APM005`: privacy manifest is invalid or unreadable.
- `APM006`: candidate privacy manifest generated.

## Supported API Categories

- `NSPrivacyAccessedAPICategoryUserDefaults`
- `NSPrivacyAccessedAPICategoryFileTimestamp`
- `NSPrivacyAccessedAPICategoryDiskSpace`
- `NSPrivacyAccessedAPICategorySystemBootTime`
- `NSPrivacyAccessedAPICategoryActiveKeyboards`

## Sources

- Apple required-reason API documentation:
  `https://developer.apple.com/documentation/BundleResources/describing-use-of-required-reason-api`
- Apple privacy manifest files:
  `https://developer.apple.com/documentation/bundleresources/privacy_manifest_files`
- Apple third-party SDK requirements:
  `https://developer.apple.com/support/third-party-SDK-requirements/`

## Exit Codes

- `0`: no blocking findings
- `1`: blocking findings exist
- `2`: scanner could not run

## Premium Boundary

The paid artifact is the repeatable local inventory and candidate manifest, not
an App Store guarantee. The tool intentionally fails closed when it cannot know
developer intent.
