from __future__ import annotations

from eslint_v10_radar.models import Rule

RULE_PACK_VERSION = "2026.05.14"

ESLINT_V10_SOURCE = "https://eslint.org/blog/2026/02/eslint-v10.0.0-released/"
ESLINT_MIGRATION_SOURCE = "https://eslint.org/docs/latest/use/migrate-to-10.0.0"
ESLINT_CONFIG_MIGRATION_SOURCE = (
    "https://eslint.org/docs/latest/use/configure/migration-guide"
)

RULES: dict[str, Rule] = {
    "ESL000": Rule(
        id="ESL000",
        title="Input file could not be parsed",
        category="scanner",
        severity="critical",
        classification="blocked",
        source_url=ESLINT_MIGRATION_SOURCE,
        source_label="ESLint v10 migration guide",
        description="A package metadata file could not be parsed safely.",
        recommendation="Fix malformed package metadata before relying on the report.",
    ),
    "ESL001": Rule(
        id="ESL001",
        title="Legacy eslintrc config exists",
        category="config",
        severity="high",
        classification="manual_review",
        source_url=ESLINT_V10_SOURCE,
        source_label="ESLint v10 release notes",
        description="ESLint v10 removed the eslintrc configuration system.",
        recommendation="Move to eslint.config.js or eslint.config.mjs.",
    ),
    "ESL002": Rule(
        id="ESL002",
        title="package.json eslintConfig is no longer supported",
        category="config",
        severity="high",
        classification="manual_review",
        source_url=ESLINT_CONFIG_MIGRATION_SOURCE,
        source_label="ESLint configuration migration guide",
        description="package.json-based ESLint configuration must migrate.",
        recommendation="Move package.json eslintConfig into a flat config file.",
    ),
    "ESL003": Rule(
        id="ESL003",
        title=".eslintignore requires flat-config migration",
        category="ignore",
        severity="medium",
        classification="manual_review",
        source_url=ESLINT_CONFIG_MIGRATION_SOURCE,
        source_label="ESLint configuration migration guide",
        description="Ignore patterns move into flat config in modern ESLint.",
        recommendation="Move ignore patterns into the ignores field in flat config.",
    ),
    "ESL004": Rule(
        id="ESL004",
        title="ESLINT_USE_FLAT_CONFIG=false blocks v10 readiness",
        category="environment",
        severity="high",
        classification="autofix",
        source_url=ESLINT_V10_SOURCE,
        source_label="ESLint v10 release notes",
        description="ESLint v10 always uses flat config.",
        recommendation="Remove ESLINT_USE_FLAT_CONFIG=false from scripts.",
    ),
    "ESL005": Rule(
        id="ESL005",
        title="Removed v10_config_lookup_from_file flag is present",
        category="environment",
        severity="medium",
        classification="autofix",
        source_url=ESLINT_MIGRATION_SOURCE,
        source_label="ESLint v10 migration guide",
        description="The v10_config_lookup_from_file flag was removed in v10.",
        recommendation="Remove the v10_config_lookup_from_file flag.",
    ),
    "ESL006": Rule(
        id="ESL006",
        title="Legacy ESLint API usage needs migration",
        category="api",
        severity="high",
        classification="manual_review",
        source_url=ESLINT_MIGRATION_SOURCE,
        source_label="ESLint v10 migration guide",
        description="LegacyESLint, FlatESLint, or eslintrc configType was found.",
        recommendation="Update API usage to ESLint v10 flat-config APIs.",
    ),
    "ESL007": Rule(
        id="ESL007",
        title="Dynamic eslintrc JavaScript config needs manual conversion",
        category="config",
        severity="high",
        classification="blocked",
        source_url=ESLINT_CONFIG_MIGRATION_SOURCE,
        source_label="ESLint configuration migration guide",
        description="JavaScript eslintrc files can include dynamic behavior.",
        recommendation=(
            "Convert dynamic config manually or with official migrator review."
        ),
    ),
    "ESL008": Rule(
        id="ESL008",
        title="Legacy config exists without eslint.config.*",
        category="config",
        severity="high",
        classification="manual_review",
        source_url=ESLINT_CONFIG_MIGRATION_SOURCE,
        source_label="ESLint configuration migration guide",
        description="No flat config file was found beside legacy config.",
        recommendation="Add an eslint.config.js or eslint.config.mjs file.",
    ),
}


def rule(rule_id: str) -> Rule:
    return RULES[rule_id]
