from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections.abc import Iterable
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

# ruff: noqa: E501


DEFAULT_BASE_URL = "https://zippertools.org"
DEFAULT_SITEMAPS = (
    "sitemap-pages.xml",
    "sitemap-hubs.xml",
    "sitemap-problem-pages.xml",
    "sitemap-products.xml",
)
IGNORED_INTERNAL_PREFIXES = ("/go/",)


@dataclass(frozen=True)
class FetchedPage:
    url: str
    status: int
    location: str
    body: str
    final_url: str


@dataclass(frozen=True)
class AuditIssue:
    url: str
    issue: str
    detail: str


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: object,
        code: int,
        msg: str,
        headers: object,
        newurl: str,
    ) -> None:
        return None


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.canonical: str | None = None
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._handle_element(tag, attrs)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._handle_element(tag, attrs)

    def _handle_element(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {key.lower(): value for key, value in attrs if value is not None}
        if tag.lower() == "link":
            rel_values = attrs_dict.get("rel", "").lower().split()
            if "canonical" in rel_values:
                self.canonical = attrs_dict.get("href")
        if tag.lower() == "a":
            href = attrs_dict.get("href")
            if href:
                self.links.append(href)


def canonical_base(base_url: str) -> str:
    return base_url.rstrip("/")


def read_sitemap_urls(path: Path) -> list[str]:
    root = ET.fromstring(path.read_text(encoding="utf-8"))
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [
        element.text or ""
        for element in root.findall(".//sm:loc", namespace)
        if element.text
    ]


def collect_sitemap_urls(site_dir: Path, sitemap_names: Iterable[str]) -> list[str]:
    urls: list[str] = []
    for name in sitemap_names:
        urls.extend(read_sitemap_urls(site_dir / name))
    return sorted(set(urls))


def path_for_local_url(site_dir: Path, base_url: str, url: str) -> Path:
    parsed = urllib.parse.urlparse(url)
    base = urllib.parse.urlparse(base_url)
    if parsed.scheme and parsed.netloc and parsed.netloc != base.netloc:
        raise ValueError(f"External URL cannot be mapped locally: {url}")

    path = parsed.path or "/"
    if path == "/":
        return site_dir / "index.html"
    if path.endswith("/"):
        return site_dir / path.lstrip("/") / "index.html"
    if path.endswith(".html") or "." in Path(path).name:
        return site_dir / path.lstrip("/")
    return site_dir / f"{path.lstrip('/')}.html"


def fetch_local(site_dir: Path, base_url: str, url: str) -> FetchedPage:
    path = path_for_local_url(site_dir, base_url, url)
    if not path.exists():
        return FetchedPage(url=url, status=404, location="", body="", final_url=url)
    return FetchedPage(
        url=url,
        status=200,
        location="",
        body=path.read_text(encoding="utf-8"),
        final_url=url,
    )


def fetch_live(url: str) -> FetchedPage:
    opener = urllib.request.build_opener(NoRedirect)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 ZipperTools URL audit"},
    )
    try:
        response = opener.open(request, timeout=20)
        body = response.read().decode("utf-8", "replace")
        return FetchedPage(
            url=url,
            status=response.status,
            location=response.headers.get("Location", ""),
            body=body,
            final_url=response.url,
        )
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        return FetchedPage(
            url=url,
            status=exc.code,
            location=exc.headers.get("Location", ""),
            body=body,
            final_url=url,
        )


def parse_page(body: str) -> PageParser:
    parser = PageParser()
    if body.lstrip("\ufeff \t\r\n").startswith("<"):
        parser.feed(body)
    return parser


def is_legacy_url(url: str) -> bool:
    path = urllib.parse.urlparse(url).path
    return path.endswith(".html") or path.endswith("/index.html")


def is_internal_url(base_url: str, url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    base = urllib.parse.urlparse(base_url)
    return parsed.scheme in {"http", "https"} and parsed.netloc in {
        base.netloc,
        f"www.{base.netloc}",
    }


def ignored_internal_path(url: str) -> bool:
    path = urllib.parse.urlparse(url).path
    return any(path.startswith(prefix) for prefix in IGNORED_INTERNAL_PREFIXES)


def audit_sitemap_pages(
    *,
    urls: Iterable[str],
    base_url: str,
    site_dir: Path,
    live: bool,
) -> tuple[list[AuditIssue], set[str]]:
    issues: list[AuditIssue] = []
    internal_links: set[str] = set()
    for url in urls:
        if is_legacy_url(url):
            issues.append(AuditIssue(url, "sitemap_legacy_url", "Sitemap URL is not canonical"))
        page = fetch_live(url) if live else fetch_local(site_dir, base_url, url)
        parser = parse_page(page.body)
        if page.status != 200:
            issues.append(AuditIssue(url, "bad_status", str(page.status)))
        if page.location:
            issues.append(AuditIssue(url, "redirect", page.location))
        if page.status == 200 and parser.canonical != url:
            issues.append(
                AuditIssue(
                    url,
                    "canonical_mismatch",
                    f"found {parser.canonical!r}",
                )
            )
        for href in parser.links:
            if href.startswith("#") or href.startswith("mailto:"):
                continue
            absolute = urllib.parse.urljoin(url, href)
            parsed = urllib.parse.urlparse(absolute)
            absolute = urllib.parse.urlunparse(
                (parsed.scheme, parsed.netloc, parsed.path, "", "", "")
            )
            if is_internal_url(base_url, absolute) and not ignored_internal_path(absolute):
                internal_links.add(absolute)
    return issues, internal_links


def audit_internal_links(
    *,
    urls: Iterable[str],
    base_url: str,
    site_dir: Path,
    live: bool,
) -> list[AuditIssue]:
    issues: list[AuditIssue] = []
    for url in sorted(urls):
        if is_legacy_url(url):
            issues.append(AuditIssue(url, "internal_legacy_url", "Internal link uses redirect URL"))
        page = fetch_live(url) if live else fetch_local(site_dir, base_url, url)
        if page.status in {301, 302, 307, 308}:
            issues.append(AuditIssue(url, "internal_redirect", page.location))
        elif page.status >= 400:
            issues.append(AuditIssue(url, "internal_bad_status", str(page.status)))
    return issues


def run_audit(site_dir: Path, base_url: str, live: bool) -> list[AuditIssue]:
    sitemap_urls = collect_sitemap_urls(site_dir, DEFAULT_SITEMAPS)
    page_issues, internal_links = audit_sitemap_pages(
        urls=sitemap_urls,
        base_url=base_url,
        site_dir=site_dir,
        live=live,
    )
    return [
        *page_issues,
        *audit_internal_links(
            urls=internal_links,
            base_url=base_url,
            site_dir=site_dir,
            live=live,
        ),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit sitemap URLs, canonicals, and internal links."
    )
    parser.add_argument("--site-dir", default="site")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument(
        "--live",
        action="store_true",
        help="Fetch live URLs instead of reading the local site directory.",
    )
    args = parser.parse_args()

    issues = run_audit(
        site_dir=Path(args.site_dir),
        base_url=canonical_base(args.base_url),
        live=args.live,
    )
    if not issues:
        mode = "live" if args.live else "local"
        print(f"{mode} URL audit passed")
        return

    for issue in issues:
        print(f"{issue.issue}: {issue.url} ({issue.detail})", file=sys.stderr)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
