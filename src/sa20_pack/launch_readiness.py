from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

PLACEHOLDER_PATTERN = re.compile(
    r"REPLACE_|YOUR_|example\.com|CHANGE_ME|PUBLIC_REPO_URL"
)

REQUIRED_SITE_FILES = (
    "site/index.html",
    "site/scan.html",
    "site/pricing.html",
    "site/demo.html",
    "site/policies.html",
    "site/success.html",
    "site/cancel.html",
    "site/config.js",
    "site/app.js",
    "site/styles.css",
    "site/og-preview.svg",
    "wrangler.jsonc",
)

REQUIRED_DOC_FILES = (
    "README.md",
    "docs/deployment.md",
    "docs/stripe-checkout.md",
    "docs/company-setup.md",
    "docs/claims-safeguards.md",
    "docs/launch-readiness.md",
    "docs/pricing.md",
    "docs/store-products.md",
    "docs/fulfillment.md",
    "docs/demo.md",
    "docs/privacy-policy.md",
    "docs/refund-policy.md",
    "docs/terms-of-sale.md",
    "docs/license-terms.md",
    "docs/support-scope.md",
    "docs/repo-fit-checklist.md",
    "docs/preset-bundle-checklist.md",
    "docs/sales-ops.md",
    "docs/lead-tracker.md",
    "docs/launch-log.md",
    "docs/legal-checklist.md",
    "docs/kpi-dashboard.md",
    "docs/release-checklist.md",
)

REQUIRED_CONFIG_KEYS = (
    "sellerName",
    "contactEmail",
    "repoUrl",
    "paidPackUrl",
    "presetBundleUrl",
    "pydanticPackUrl",
    "fitReportUrl",
)


@dataclass(frozen=True)
class LaunchReadinessResult:
    missing_files: list[str]
    missing_keys: list[str]
    placeholder_keys: list[str]

    @property
    def ready(self) -> bool:
        return (
            not self.missing_files
            and not self.missing_keys
            and not self.placeholder_keys
        )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sa20-pack-launch-check",
        description=(
            "Check whether the repo has the files and live config needed "
            "for public launch."
        ),
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root to inspect. Defaults to the current directory.",
    )
    return parser


def _extract_config_values(config_text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for key in REQUIRED_CONFIG_KEYS:
        match = re.search(rf"{re.escape(key)}:\s*\"([^\"]*)\"", config_text)
        if match:
            values[key] = match.group(1)
    return values


def check_launch_readiness(root: Path) -> LaunchReadinessResult:
    required_files = [*REQUIRED_SITE_FILES, *REQUIRED_DOC_FILES]
    missing_files = [path for path in required_files if not (root / path).exists()]

    config_path = root / "site" / "config.js"
    if not config_path.exists():
        return LaunchReadinessResult(
            missing_files=missing_files,
            missing_keys=list(REQUIRED_CONFIG_KEYS),
            placeholder_keys=[],
        )

    config_values = _extract_config_values(config_path.read_text(encoding="utf-8"))
    missing_keys = [key for key in REQUIRED_CONFIG_KEYS if key not in config_values]
    placeholder_keys = [
        key
        for key, value in config_values.items()
        if PLACEHOLDER_PATTERN.search(value) is not None
    ]

    return LaunchReadinessResult(
        missing_files=missing_files,
        missing_keys=missing_keys,
        placeholder_keys=placeholder_keys,
    )


def _print_section(title: str, items: list[str]) -> None:
    if not items:
        return

    print(title)
    for item in items:
        print(f"- {item}")


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    result = check_launch_readiness(root)

    if result.ready:
        print("Launch readiness: ready")
        print("Repo assets exist and site/config.js has live values for required keys.")
        return 0

    print("Launch readiness: blocked")
    _print_section("Missing files:", result.missing_files)
    _print_section("Missing config keys:", result.missing_keys)
    _print_section("Placeholder config values still present:", result.placeholder_keys)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
