# CRA Evidence Builder

CRA Evidence Builder is a local evidence-readiness scanner for teams preparing
for the EU Cyber Resilience Act. It inventories the repo artifacts a technical
team needs before a real compliance/legal review: dependency manifests, SBOM
outputs, vulnerability disclosure paths, incident handling docs, release
traceability, security update policy, and container base-image pinning.

It is not legal advice and does not certify CRA compliance.

## Who This Is For

- SaaS vendors and commercial OSS maintainers with EU customers.
- Security and platform teams preparing the 2026 reporting deadline.
- Small software vendors that need a repeatable release evidence packet.

## Do Not Use This If

- You need a legal CRA conformity assessment.
- You need hosted GRC workflows.
- You expect the tool to classify your product category or conformity route.
- You need vulnerability scanning itself; this v0.1 checks evidence readiness.

## Current Supported Checks

- dependency manifest inventory
- SBOM artifact presence
- `SECURITY.md` or `.well-known/security.txt`
- incident/vulnerability handling docs
- changelog or release traceability docs
- security update policy hints
- Dockerfile base image digest pinning
- malformed manifest fail-closed findings

## Example

```bash
python -m cra_evidence_builder.cli path/to/product \
  --report cra-evidence-report.json \
  --html-report cra-evidence-report.html
```

Write safe template files:

```bash
python -m cra_evidence_builder.cli path/to/product --write-templates
```

## Outputs

- `cra-evidence-report.json`
- `cra-evidence-report.html`
- optional `.cra-template` files for missing process artifacts
- exit code `0` when no blocking findings exist
- exit code `1` when blocking findings exist
- exit code `2` when the scanner cannot run
