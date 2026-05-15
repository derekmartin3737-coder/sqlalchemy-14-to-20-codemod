# CRA Evidence Builder Public Proof

## Proof Claim

The v0.1 scanner can inspect a local software repo, inventory evidence
artifacts, flag missing CRA-prep inputs, generate JSON/HTML reports, and write
safe policy/evidence templates only when requested.

## Fixture Coverage

- `risky_product`: dependency manifest and Dockerfile exist, but SBOM,
  disclosure, incident, release, and update-policy evidence are missing.
- `clean_product`: dependency manifest, SBOM, security policy, incident doc,
  changelog, and digest-pinned Dockerfile are present.
- `broken_manifest_product`: invalid package metadata blocks trust in the
  evidence dossier.

## Verified Commands

Run from `products/cra-evidence-builder/`:

```bash
python -m pytest -q -p no:cacheprovider
python -m ruff check . --no-cache
PYTHONPATH=src python -m mypy src tests --cache-dir .mypy-cache-local
PYTHONPATH=src python -m cra_evidence_builder.build_runner
python -m hatchling build -t wheel
```

## Deadline Signal

The EU summary states that CRA reporting obligations apply from September 11,
2026 and the CRA becomes fully applicable on December 11, 2027. This product
turns that timeline into a repo-local preparation artifact.
