from __future__ import annotations

from apple_privacy_manifest_composer.models import Rule

RULE_PACK_VERSION = "2026.05.14"

APPLE_REQUIRED_REASON_SOURCE = (
    "https://developer.apple.com/documentation/BundleResources/"
    "describing-use-of-required-reason-api"
)
APPLE_PRIVACY_MANIFEST_SOURCE = (
    "https://developer.apple.com/documentation/bundleresources/"
    "privacy_manifest_files"
)
APPLE_SDK_SOURCE = "https://developer.apple.com/support/third-party-SDK-requirements/"

RULES: dict[str, Rule] = {
    "APM000": Rule(
        id="APM000",
        title="Input file could not be parsed",
        category="scanner",
        severity="critical",
        classification="blocked",
        source_url=APPLE_PRIVACY_MANIFEST_SOURCE,
        source_label="Apple privacy manifest files",
        description="A required input could not be parsed safely.",
        recommendation="Fix the malformed file before relying on this report.",
    ),
    "APM001": Rule(
        id="APM001",
        title="Required-reason API usage lacks a privacy manifest",
        category="manifest",
        severity="high",
        classification="manual_review",
        source_url=APPLE_REQUIRED_REASON_SOURCE,
        source_label="Apple required-reason API documentation",
        description=(
            "Required-reason API usage was found, but no PrivacyInfo.xcprivacy "
            "file was found in the scanned tree."
        ),
        recommendation=(
            "Add a PrivacyInfo.xcprivacy file and choose valid reasons for "
            "each accessed API category before submission."
        ),
    ),
    "APM002": Rule(
        id="APM002",
        title="Privacy manifest is missing an accessed API category",
        category="manifest",
        severity="high",
        classification="manual_review",
        source_url=APPLE_REQUIRED_REASON_SOURCE,
        source_label="Apple required-reason API documentation",
        description="The existing privacy manifest omits a detected API category.",
        recommendation="Add the missing category with valid Apple reason codes.",
    ),
    "APM003": Rule(
        id="APM003",
        title="Required-reason API usage needs human reason selection",
        category="source",
        severity="medium",
        classification="manual_review",
        source_url=APPLE_REQUIRED_REASON_SOURCE,
        source_label="Apple required-reason API documentation",
        description=(
            "Static analysis can detect the API category, but cannot know the "
            "developer's allowed reason for using it."
        ),
        recommendation=(
            "Review the source location and choose the Apple reason code that "
            "matches actual app behavior."
        ),
    ),
    "APM004": Rule(
        id="APM004",
        title="Listed third-party SDK requires privacy-manifest review",
        category="sdk",
        severity="medium",
        classification="manual_review",
        source_url=APPLE_SDK_SOURCE,
        source_label="Apple third-party SDK requirements",
        description=(
            "A dependency name matches Apple's list of SDKs that require a "
            "privacy manifest and signature in applicable submissions."
        ),
        recommendation=(
            "Verify the SDK supplies a valid privacy manifest and, for binary "
            "dependencies, the required signature."
        ),
    ),
    "APM005": Rule(
        id="APM005",
        title="Privacy manifest is invalid or unreadable",
        category="manifest",
        severity="critical",
        classification="blocked",
        source_url=APPLE_PRIVACY_MANIFEST_SOURCE,
        source_label="Apple privacy manifest files",
        description="The privacy manifest could not be parsed as a property list.",
        recommendation="Fix or replace the manifest before App Store submission.",
    ),
    "APM006": Rule(
        id="APM006",
        title="Candidate privacy manifest generated",
        category="output",
        severity="info",
        classification="informational",
        source_url=APPLE_REQUIRED_REASON_SOURCE,
        source_label="Apple required-reason API documentation",
        description="A candidate manifest template was generated for review.",
        recommendation=(
            "Replace placeholder reason codes with valid Apple reason codes "
            "before adding the file to an app target."
        ),
    ),
}


def rule(rule_id: str) -> Rule:
    return RULES[rule_id]
