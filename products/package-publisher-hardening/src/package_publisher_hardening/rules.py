from __future__ import annotations

from package_publisher_hardening.models import Rule

RULE_PACK_VERSION = "2026.05.14"

NPM_TRUSTED_SOURCE = "https://docs.npmjs.com/trusted-publishers"
NPM_PROVENANCE_SOURCE = "https://docs.npmjs.com/generating-provenance-statements"
PYPI_TRUSTED_SOURCE = "https://docs.pypi.org/trusted-publishers/"
PYPI_ATTESTATION_SOURCE = "https://docs.pypi.org/attestations/"

RULES: dict[str, Rule] = {
    "PPH000": Rule(
        id="PPH000",
        title="Package metadata could not be parsed",
        category="scanner",
        severity="critical",
        classification="blocked",
        source_url=NPM_TRUSTED_SOURCE,
        source_label="npm trusted publishing docs",
        description="Package metadata could not be parsed safely.",
        recommendation="Fix malformed package metadata before relying on the report.",
    ),
    "PPH001": Rule(
        id="PPH001",
        title="npm publish uses long-lived token flow",
        category="npm",
        severity="high",
        classification="manual_review",
        source_url=NPM_TRUSTED_SOURCE,
        source_label="npm trusted publishing docs",
        description="npm publish appears to rely on NODE_AUTH_TOKEN or NPM_TOKEN.",
        recommendation="Migrate publish jobs to npm trusted publishing with OIDC.",
    ),
    "PPH002": Rule(
        id="PPH002",
        title="npm publish workflow lacks id-token permission",
        category="npm",
        severity="high",
        classification="autofix",
        source_url=NPM_TRUSTED_SOURCE,
        source_label="npm trusted publishing docs",
        description="Trusted publishing requires id-token: write in GitHub Actions.",
        recommendation="Add id-token: write to release workflow permissions.",
    ),
    "PPH003": Rule(
        id="PPH003",
        title="npm publish lacks provenance or trusted publishing posture",
        category="npm",
        severity="medium",
        classification="manual_review",
        source_url=NPM_PROVENANCE_SOURCE,
        source_label="npm provenance docs",
        description="npm publish was found without visible provenance/OIDC posture.",
        recommendation="Use trusted publishing or npm publish --provenance.",
    ),
    "PPH004": Rule(
        id="PPH004",
        title="PyPI publish uses long-lived token flow",
        category="pypi",
        severity="high",
        classification="manual_review",
        source_url=PYPI_TRUSTED_SOURCE,
        source_label="PyPI trusted publishing docs",
        description="PyPI upload appears to rely on TWINE_PASSWORD or API tokens.",
        recommendation="Migrate to PyPI Trusted Publishing where possible.",
    ),
    "PPH005": Rule(
        id="PPH005",
        title="PyPI publish action lacks id-token permission",
        category="pypi",
        severity="high",
        classification="autofix",
        source_url=PYPI_TRUSTED_SOURCE,
        source_label="PyPI trusted publishing docs",
        description="Trusted Publishing requires id-token: write in GitHub Actions.",
        recommendation="Add id-token: write to the publish workflow.",
    ),
    "PPH006": Rule(
        id="PPH006",
        title="Publish workflow has broad write permissions",
        category="workflow",
        severity="medium",
        classification="manual_review",
        source_url=NPM_TRUSTED_SOURCE,
        source_label="npm trusted publishing docs",
        description="Release workflow grants broad write permissions.",
        recommendation="Narrow permissions to contents: read and id-token: write.",
    ),
    "PPH007": Rule(
        id="PPH007",
        title="npm package repository metadata missing",
        category="npm",
        severity="medium",
        classification="manual_review",
        source_url=NPM_PROVENANCE_SOURCE,
        source_label="npm provenance docs",
        description="npm provenance relies on repository metadata matching source.",
        recommendation="Add a public repository URL to package.json.",
    ),
    "PPH008": Rule(
        id="PPH008",
        title="Trusted publishing on self-hosted runner needs review",
        category="workflow",
        severity="medium",
        classification="manual_review",
        source_url=NPM_TRUSTED_SOURCE,
        source_label="npm trusted publishing docs",
        description="Trusted publishing support can depend on hosted runner support.",
        recommendation="Verify provider support or move publish to hosted runners.",
    ),
    "PPH009": Rule(
        id="PPH009",
        title="npm provenance is explicitly disabled",
        category="npm",
        severity="medium",
        classification="manual_review",
        source_url=NPM_TRUSTED_SOURCE,
        source_label="npm trusted publishing docs",
        description="publishConfig disables provenance.",
        recommendation="Remove provenance=false unless a documented exception exists.",
    ),
}


def rule(rule_id: str) -> Rule:
    return RULES[rule_id]
