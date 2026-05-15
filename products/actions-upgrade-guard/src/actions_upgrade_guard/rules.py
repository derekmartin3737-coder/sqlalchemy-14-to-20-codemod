from __future__ import annotations

from actions_upgrade_guard.models import Rule

RULE_PACK_VERSION = "2026.05.14"

ARTIFACT_V3_SOURCE = (
    "https://github.blog/changelog/2024-04-16-deprecation-notice-v3-of-the-artifact-actions/"
)
CACHE_V2_SOURCE = (
    "https://github.blog/changelog/2024-09-16-notice-of-upcoming-deprecations-and-changes-in-github-actions-services/"
)
UBUNTU_20_SOURCE = (
    "https://github.blog/changelog/2025-01-15-github-actions-ubuntu-20-runner-image-brownout-dates-and-other-breaking-changes/"
)
NODE20_SOURCE = (
    "https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/"
)
IMAGE_MIGRATIONS_SOURCE = (
    "https://github.blog/changelog/2026-05-14-github-actions-upcoming-image-migrations"
)
PERMISSIONS_SOURCE = (
    "https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication"
)

RULES: dict[str, Rule] = {
    "AUG001": Rule(
        id="AUG001",
        title="Artifact action v3 is retired on GitHub.com",
        category="deadline",
        severity="critical",
        classification="autofix",
        source_url=ARTIFACT_V3_SOURCE,
        source_label="GitHub Changelog: Deprecation notice v3 artifact actions",
        deadline="2025-01-30",
        autofix=True,
        description=(
            "actions/upload-artifact@v3 and actions/download-artifact@v3 are "
            "retired on GitHub.com and can fail workflows."
        ),
        recommendation="Update artifact actions to v4 and review v4 behavior changes.",
    ),
    "AUG002": Rule(
        id="AUG002",
        title="Actions cache v1/v2 is retired",
        category="deadline",
        severity="critical",
        classification="autofix",
        source_url=CACHE_V2_SOURCE,
        source_label="GitHub Changelog: cache v1-v2 deprecation",
        deadline="2025-03-01",
        autofix=True,
        description=(
            "actions/cache v1 and v2 are retired after the cache service "
            "architecture migration."
        ),
        recommendation="Update actions/cache to v4 and run the workflow before merge.",
    ),
    "AUG003": Rule(
        id="AUG003",
        title="Ubuntu 20.04 hosted runner is retired",
        category="runner",
        severity="high",
        classification="manual_review",
        source_url=UBUNTU_20_SOURCE,
        source_label="GitHub Changelog: Ubuntu 20 runner image closing down",
        deadline="2025-04-15",
        autofix=False,
        description=(
            "ubuntu-20.04 hosted runners were retired. Updating the label can "
            "change build tools, system packages, and compiler behavior."
        ),
        recommendation="Move to ubuntu-22.04 or ubuntu-24.04 after testing.",
    ),
    "AUG004": Rule(
        id="AUG004",
        title="Local JavaScript action still targets Node 20",
        category="runtime",
        severity="high",
        classification="manual_review",
        source_url=NODE20_SOURCE,
        source_label="GitHub Changelog: Node 20 deprecation on Actions runners",
        deadline="2026-06-02",
        autofix=False,
        description=(
            "Node20 is being deprecated on GitHub Actions runners. Local "
            "JavaScript actions should be tested on Node24 before the runner "
            "default changes."
        ),
        recommendation=(
            "Update local action metadata to node24 after compatibility testing."
        ),
    ),
    "AUG005": Rule(
        id="AUG005",
        title="Workflow opts out of the Node 24 Actions runtime",
        category="runtime",
        severity="high",
        classification="manual_review",
        source_url=NODE20_SOURCE,
        source_label="GitHub Changelog: Node 20 deprecation on Actions runners",
        deadline="2026-06-02",
        autofix=False,
        description=(
            "ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION is a temporary opt-out "
            "from the Node24 default and should not become permanent policy."
        ),
        recommendation="Remove the opt-out after action dependencies support Node24.",
    ),
    "AUG006": Rule(
        id="AUG006",
        title="Workflow does not declare GITHUB_TOKEN permissions",
        category="security",
        severity="medium",
        classification="informational",
        source_url=PERMISSIONS_SOURCE,
        source_label="GitHub Docs: automatic token authentication",
        deadline=None,
        autofix=False,
        description=(
            "Workflows without explicit permissions rely on repository or "
            "organization defaults, which makes review harder during upgrades."
        ),
        recommendation="Declare least-privilege top-level or job-level permissions.",
    ),
    "AUG007": Rule(
        id="AUG007",
        title="Broad write permission should be reviewed",
        category="security",
        severity="medium",
        classification="manual_review",
        source_url=PERMISSIONS_SOURCE,
        source_label="GitHub Docs: automatic token authentication",
        deadline=None,
        autofix=False,
        description=(
            "Broad write permissions increase blast radius and should be "
            "reviewed while touching workflow files."
        ),
        recommendation="Narrow write permissions to the workflow's required scopes.",
    ),
    "AUG008": Rule(
        id="AUG008",
        title="Floating latest runner label can hide image migrations",
        category="runner",
        severity="medium",
        classification="informational",
        source_url=IMAGE_MIGRATIONS_SOURCE,
        source_label="GitHub Changelog: upcoming image migrations",
        deadline="2026-06-15",
        autofix=False,
        description=(
            "latest runner labels can move under a workflow without a code "
            "change, which makes deadline triage harder."
        ),
        recommendation="Pin runner labels where reproducibility matters.",
    ),
}


def rule(rule_id: str) -> Rule:
    return RULES[rule_id]
