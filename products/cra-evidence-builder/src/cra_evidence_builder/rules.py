from __future__ import annotations

from cra_evidence_builder.models import Rule

RULE_PACK_VERSION = "2026.05.14"

CRA_SUMMARY_SOURCE = "https://digital-strategy.ec.europa.eu/en/policies/cra-summary"
CRA_REPORTING_SOURCE = "https://digital-strategy.ec.europa.eu/en/policies/cra-reporting"
CRA_LEGAL_SOURCE = "https://eur-lex.europa.eu/eli/reg/2024/2847/oj"

RULES: dict[str, Rule] = {
    "CRA000": Rule(
        id="CRA000",
        title="Input manifest could not be parsed",
        category="scanner",
        severity="critical",
        classification="blocked",
        source_url=CRA_LEGAL_SOURCE,
        source_label="Regulation (EU) 2024/2847",
        description="A source manifest could not be parsed safely.",
        recommendation="Fix malformed metadata before relying on this dossier.",
    ),
    "CRA001": Rule(
        id="CRA001",
        title="No dependency manifest inventory found",
        category="sbom",
        severity="high",
        classification="manual_review",
        source_url=CRA_SUMMARY_SOURCE,
        source_label="EU CRA summary",
        description="No package, lockfile, or build manifest was found.",
        recommendation="Add or identify dependency manifests before generating SBOMs.",
    ),
    "CRA002": Rule(
        id="CRA002",
        title="No SBOM artifact found",
        category="sbom",
        severity="high",
        classification="manual_review",
        source_url=CRA_LEGAL_SOURCE,
        source_label="Regulation (EU) 2024/2847",
        description="Dependency inputs exist but no CycloneDX or SPDX SBOM was found.",
        recommendation="Generate and store a release SBOM artifact for each release.",
    ),
    "CRA003": Rule(
        id="CRA003",
        title="No vulnerability disclosure contact path found",
        category="vulnerability_handling",
        severity="high",
        classification="manual_review",
        source_url=CRA_REPORTING_SOURCE,
        source_label="EU CRA reporting obligations",
        description="No SECURITY.md or security.txt contact path was found.",
        recommendation=(
            "Publish a vulnerability disclosure contact and handling policy."
        ),
    ),
    "CRA004": Rule(
        id="CRA004",
        title="No incident handling playbook found",
        category="reporting",
        severity="high",
        classification="manual_review",
        source_url=CRA_REPORTING_SOURCE,
        source_label="EU CRA reporting obligations",
        description="No vulnerability or incident response process document was found.",
        recommendation=(
            "Document triage, reporting, escalation, and customer update steps."
        ),
    ),
    "CRA005": Rule(
        id="CRA005",
        title="No release traceability artifact found",
        category="release",
        severity="medium",
        classification="manual_review",
        source_url=CRA_LEGAL_SOURCE,
        source_label="Regulation (EU) 2024/2847",
        description="No changelog, release notes, or release evidence file was found.",
        recommendation=(
            "Keep release evidence linking versions, fixes, and shipped artifacts."
        ),
    ),
    "CRA006": Rule(
        id="CRA006",
        title="No security update policy found",
        category="support",
        severity="medium",
        classification="manual_review",
        source_url=CRA_SUMMARY_SOURCE,
        source_label="EU CRA summary",
        description="No supported-version or security-update policy hint was found.",
        recommendation="Document supported versions and security update expectations.",
    ),
    "CRA007": Rule(
        id="CRA007",
        title="Container base image is not digest pinned",
        category="container",
        severity="medium",
        classification="manual_review",
        source_url=CRA_LEGAL_SOURCE,
        source_label="Regulation (EU) 2024/2847",
        description="A Dockerfile base image uses a mutable tag without a digest.",
        recommendation="Pin release base images by digest or document the exception.",
    ),
    "CRA008": Rule(
        id="CRA008",
        title="Evidence template generated",
        category="output",
        severity="info",
        classification="informational",
        source_url=CRA_SUMMARY_SOURCE,
        source_label="EU CRA summary",
        description="A missing evidence-process template was generated.",
        recommendation="Review and adapt the template before treating it as policy.",
    ),
}


def rule(rule_id: str) -> Rule:
    return RULES[rule_id]
