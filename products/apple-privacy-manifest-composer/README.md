# Apple Privacy Manifest Composer

Apple Privacy Manifest Composer is a local scanner for iOS, iPadOS, tvOS,
visionOS, and watchOS projects that need to prepare `PrivacyInfo.xcprivacy`
entries for Apple's required-reason API rules.

It scans source files, dependency manifests, and existing privacy manifests,
then emits a JSON report, an HTML report, and a candidate plist template for
missing accessed-API categories.

## Who This Is For

- iOS teams preparing App Store submissions.
- Agencies that inherit apps with mixed CocoaPods, SwiftPM, Flutter, or React
  Native dependencies.
- SDK maintainers who need an inventory before adding a privacy manifest.

## Do Not Use This If

- You expect the tool to choose the legal/business reason for an API.
- You need notarization, code signing, or binary signature verification.
- You want hosted scanning or source upload.
- You need a complete replacement for Xcode's privacy report.

## Current Supported Checks

- `UserDefaults` / `NSUserDefaults`
- file timestamp APIs such as `stat`, `lstat`, `creationDate`, and
  `contentModificationDateKey`
- disk-space APIs such as `volumeAvailableCapacityKey`, `statfs`, and
  `systemFreeSize`
- system boot-time APIs such as `systemUptime` and `mach_absolute_time`
- active-keyboard APIs such as `activeInputModes`
- listed third-party SDK names in common dependency manifests
- existing `PrivacyInfo.xcprivacy` parse and category coverage

## Example

```bash
python -m apple_privacy_manifest_composer.cli path/to/app \
  --report apple-privacy-report.json \
  --html-report apple-privacy-report.html \
  --candidate PrivacyInfo.xcprivacy.candidate
```

## Outputs

- `apple-privacy-report.json`: machine-readable findings and candidate manifest.
- `apple-privacy-report.html`: reviewer-friendly summary.
- `PrivacyInfo.xcprivacy.candidate`: generated plist candidate with placeholder
  reasons that must be reviewed before use.
- exit code `0` when no blocking findings exist.
- exit code `1` when blocking findings exist.
- exit code `2` when the scanner cannot run.

## Trust Boundary

- Runs locally.
- No Apple credentials required.
- No source upload.
- Candidate manifests are written only when requested.
- Human reason selection is explicitly required before App Store submission.
