# Package Publisher Hardening Pack

Package Publisher Hardening Pack is a local scanner for npm and PyPI release
workflows. It finds long-lived token publishing, missing OIDC permissions,
missing provenance/attestation posture, repository metadata gaps, and workflow
patterns that need manual review before moving to trusted publishing.

It does not configure npmjs.com or PyPI for you. It prepares the repo-side work.

## Who This Is For

- npm and PyPI maintainers.
- Internal platform teams that own package release workflows.
- OSS maintainers migrating away from long-lived publish tokens.

## Current Supported Checks

- npm publish commands using `NODE_AUTH_TOKEN` or `NPM_TOKEN`
- npm publish workflows missing `id-token: write`
- npm publish without provenance/OIDC posture
- npm `publishConfig.provenance = false`
- missing `package.json#repository`
- PyPI `twine upload` token flows
- PyPI publish action without `id-token: write`
- self-hosted runner warnings for trusted publishing
- broad publish workflow permissions

## Example

```bash
python -m package_publisher_hardening.cli path/to/repo \
  --report publisher-hardening-report.json \
  --html-report publisher-hardening-report.html
```

Apply only narrow `permissions:` patches:

```bash
python -m package_publisher_hardening.cli path/to/repo --apply
```
