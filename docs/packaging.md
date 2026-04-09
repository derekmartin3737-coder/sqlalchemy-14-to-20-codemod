# Packaging

## Public package shape

- Python CLI package
- GitHub Action wrapper
- static docs in-repo
- GitHub Releases for packaged snapshots

## Zero-cost distribution path

1. Public GitHub repo
2. PyPI package for the free CLI
3. GitHub Action from the public repo
4. GitHub Pages or static site export for demo/landing copy

## Paid packaging path

Keep the public repo as the trust layer.

Distribute paid coverage as one of:

- Payhip digital download ZIP
- paid add-on package
- customer-specific preset pack

For the current launch plan, prefer the Payhip digital download ZIP path from
[fulfillment.md](fulfillment.md)
and use the tagged release path from
[release-checklist.md](release-checklist.md)
for the free package.
