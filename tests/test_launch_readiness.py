from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from sa20_pack.launch_readiness import check_launch_readiness


def _required_relative_paths() -> tuple[str, ...]:
    return (
        "site/index.html",
        "site/scan.html",
        "site/pricing.html",
        "site/demo.html",
        "site/policies.html",
        "site/success.html",
        "site/cancel.html",
        "site/app.js",
        "site/styles.css",
        "site/og-preview.svg",
        "wrangler.jsonc",
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


def _normalize(path: Path) -> str:
    return path.as_posix().lower()


def _run_with_fake_files(root: Path, config_text: str) -> list[str]:
    config_path = root / "site" / "config.js"
    existing_paths = {
        _normalize(root / relative) for relative in _required_relative_paths()
    }
    existing_paths.add(_normalize(config_path))

    def fake_exists(path: Path) -> bool:
        return _normalize(path) in existing_paths

    def fake_read_text(path: Path, encoding: str = "utf-8") -> str:
        assert encoding == "utf-8"
        assert _normalize(path) == _normalize(config_path)
        return config_text

    with (
        patch.object(Path, "exists", fake_exists),
        patch.object(Path, "read_text", fake_read_text),
    ):
        result = check_launch_readiness(root)

    assert result.missing_files == []
    assert result.missing_keys == []
    return result.placeholder_keys


def test_launch_readiness_detects_placeholders() -> None:
    root = Path("C:/fake-repo")
    placeholder_keys = _run_with_fake_files(
        root,
        "\n".join(
            [
                "window.SA20_SITE_CONFIG = {",
                '  sellerName: "REPLACE_WITH_SELLER_NAME",',
                '  contactEmail: "founder@example.com",',
                '  repoUrl: "https://github.com/example/sa20-pack",',
                '  paidPackUrl: "https://store.example.com/pack",',
                '  presetBundleUrl: "https://store.example.com/bundle",',
                '  pydanticPackUrl: "https://store.example.com/pydantic",',
                '  fitReportUrl: "https://store.example.com/fit-report",',
                '  cloudflareAnalyticsToken: "",',
                "};",
            ]
        ),
    )

    assert placeholder_keys == [
        "sellerName",
        "contactEmail",
        "paidPackUrl",
        "presetBundleUrl",
        "pydanticPackUrl",
        "fitReportUrl",
    ]


def test_launch_readiness_passes_with_live_values() -> None:
    root = Path("C:/fake-repo")
    placeholder_keys = _run_with_fake_files(
        root,
        "\n".join(
            [
                "window.SA20_SITE_CONFIG = {",
                '  sellerName: "Taylor Seller",',
                '  contactEmail: "support@sa20pack.example.org",',
                '  repoUrl: "https://github.com/taylor/sa20-pack",',
                '  paidPackUrl: "https://store.sa20pack.test/pack",',
                '  presetBundleUrl: "https://store.sa20pack.test/bundle",',
                '  pydanticPackUrl: "https://store.sa20pack.test/pydantic",',
                '  fitReportUrl: "https://store.sa20pack.test/fit-report",',
                '  cloudflareAnalyticsToken: "cf-token-123",',
                "};",
            ]
        ),
    )

    assert placeholder_keys == []
