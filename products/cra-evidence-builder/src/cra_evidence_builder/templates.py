from __future__ import annotations

from cra_evidence_builder.models import TemplateFile


def build_templates() -> list[TemplateFile]:
    return [
        TemplateFile(
            path="SECURITY.md.cra-template",
            title="Vulnerability Disclosure Policy",
            content="""# Security Policy

## Reporting A Vulnerability

Contact: security@example.com

Include affected product, version, reproduction details, impact, and any known
active exploitation indicators.

## Supported Versions

Document supported release lines and expected security update windows here.
""",
        ),
        TemplateFile(
            path="docs/incident-response.cra-template.md",
            title="Incident And Vulnerability Reporting Playbook",
            content="""# Incident And Vulnerability Reporting Playbook

## Intake

- Record reporter, product, version, affected component, and exploit status.
- Assign severity and owner.

## CRA Reporting Review

- Determine whether the issue is an actively exploited vulnerability or serious
  incident affecting product security.
- Escalate to legal/compliance before external reporting.

## Customer Communication

- Track affected versions, mitigations, fixed releases, and advisory updates.
""",
        ),
        TemplateFile(
            path="docs/cra-release-evidence.cra-template.md",
            title="Release Evidence Record",
            content="""# CRA Release Evidence Record

## Release

- Product:
- Version:
- Date:
- Commit/tag:

## Evidence

- SBOM artifact:
- Vulnerability scan:
- Security fixes:
- Customer-facing advisory:
- Known residual risks:
""",
        ),
    ]
