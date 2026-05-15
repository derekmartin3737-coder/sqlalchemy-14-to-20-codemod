# CRA Evidence Builder Product Spec

## Product Promise

CRA Evidence Builder gives software vendors a local evidence-readiness dossier
for Cyber Resilience Act preparation. It scans a repo for the technical
artifacts needed before compliance review: dependency manifests, SBOM outputs,
vulnerability disclosure paths, incident response docs, release traceability,
security update policy, and container base-image pinning.

It is not a legal assessment and does not certify compliance.

## Buyer

- EU-facing software vendors.
- Commercial OSS maintainers.
- Small SaaS teams preparing security and reporting processes.
- Platform/security teams that need a repeatable release evidence packet.

## Rule Set

- `CRA000`: input manifest could not be parsed.
- `CRA001`: no dependency manifest inventory found.
- `CRA002`: no SBOM artifact found.
- `CRA003`: no vulnerability disclosure contact path found.
- `CRA004`: no incident handling playbook found.
- `CRA005`: no release traceability artifact found.
- `CRA006`: no security update policy found.
- `CRA007`: container base image is not digest pinned.
- `CRA008`: evidence template generated.

## Safe Template Outputs

When `--write-templates` is passed, the tool writes:

- `SECURITY.md.cra-template`
- `docs/incident-response.cra-template.md`
- `docs/cra-release-evidence.cra-template.md`

These are templates only. They must be reviewed before becoming company policy.

## Sources

- EU CRA summary:
  `https://digital-strategy.ec.europa.eu/en/policies/cra-summary`
- EU CRA reporting obligations:
  `https://digital-strategy.ec.europa.eu/en/policies/cra-reporting`
- Regulation (EU) 2024/2847:
  `https://eur-lex.europa.eu/eli/reg/2024/2847/oj`

## Exit Codes

- `0`: no blocking findings
- `1`: blocking findings exist
- `2`: scanner could not run

## Premium Boundary

The paid value is the repeatable evidence dossier and gap inventory, not a legal
opinion. Findings are source-linked and fail closed where interpretation belongs
to counsel or compliance owners.
