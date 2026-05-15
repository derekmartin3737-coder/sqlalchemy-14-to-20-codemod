# Apple Privacy Manifest Composer Public Proof

## Proof Claim

The v0.1 scanner can inspect a local Apple app tree, detect required-reason API
usage, detect listed SDK dependency names, parse existing privacy manifests,
generate JSON/HTML reports, and write a candidate `PrivacyInfo.xcprivacy` file
only when requested.

## Fixture Coverage

- `risky_app`: required-reason API usage, listed SDK dependencies, no existing
  privacy manifest.
- `partial_manifest_app`: existing manifest covers `UserDefaults` but misses a
  file timestamp category.
- `clean_app`: no required-reason API or listed SDK findings.
- `broken_manifest_app`: invalid manifest blocks readiness claims.

## Verified Commands

Run from `products/apple-privacy-manifest-composer/`:

```bash
python -m pytest -q -p no:cacheprovider
python -m ruff check . --no-cache
PYTHONPATH=src python -m mypy src tests --cache-dir .mypy-cache-local
PYTHONPATH=src python -m apple_privacy_manifest_composer.build_runner
python -m hatchling build -t wheel
```

## Safe Output Boundary

The generated candidate plist uses `REVIEW_REQUIRED` placeholders. That is
intentional. The product detects categories and prepares the work surface; a
developer still has to choose valid Apple reason codes before submission.
