# Package Publisher Hardening Pack Product Spec

## Product Promise

Package Publisher Hardening Pack gives npm and PyPI maintainers a local report
of release workflow risks before migrating to trusted publishing, provenance,
and attestations.

It does not configure npmjs.com or PyPI. It prepares the repository-side work
and points out where registry-side setup is still required.

## Buyer

- npm/PyPI maintainers.
- Internal package platform teams.
- OSS project owners moving away from long-lived release tokens.

## Rule Set

- `PPH000`: package metadata could not be parsed.
- `PPH001`: npm publish uses long-lived token flow.
- `PPH002`: npm publish workflow lacks `id-token: write`.
- `PPH003`: npm publish lacks provenance or trusted publishing posture.
- `PPH004`: PyPI publish uses long-lived token flow.
- `PPH005`: PyPI publish action lacks `id-token: write`.
- `PPH006`: publish workflow has broad write permissions.
- `PPH007`: npm package repository metadata missing.
- `PPH008`: trusted publishing on self-hosted runner needs review.
- `PPH009`: npm provenance is explicitly disabled.

## Safe Patch Boundary

The only v0.1 apply behavior adds `id-token: write` to a simple workflow
permissions block:

```yaml
permissions:
  contents: read
  id-token: write
```

Token removal, registry-side trusted-publisher configuration, and provenance
policy choices are report-only.

## Sources

- npm trusted publishing:
  `https://docs.npmjs.com/trusted-publishers`
- npm provenance:
  `https://docs.npmjs.com/generating-provenance-statements`
- PyPI Trusted Publishing:
  `https://docs.pypi.org/trusted-publishers/`
- PyPI digital attestations:
  `https://docs.pypi.org/attestations/`

## Exit Codes

- `0`: no blocking findings
- `1`: blocking findings exist
- `2`: scanner could not run
