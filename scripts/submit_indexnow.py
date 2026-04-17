from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib import request


def build_payload(manifest: dict[str, object], groups: list[str]) -> dict[str, object]:
    url_list: list[str] = []
    for group in groups:
        url_list.extend(manifest["urls"][group])
    return {
        "host": manifest["site_url"].removeprefix("https://").removeprefix("http://"),
        "key": manifest["indexnow_key"],
        "keyLocation": manifest["indexnow_key_location"],
        "urlList": sorted(set(url_list)),
    }


def submit(payload: dict[str, object]) -> None:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        "https://www.bing.com/indexnow",
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with request.urlopen(req, timeout=30) as response:  # noqa: S310
        if response.status >= 400:
            raise RuntimeError(f"IndexNow submission failed with status {response.status}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Submit generated site URLs to IndexNow.")
    parser.add_argument("--manifest", default="site/_site_manifest.json", help="Path to the generated site manifest.")
    parser.add_argument(
        "--groups",
        nargs="+",
        default=["static", "hubs", "guides", "products"],
        choices=["static", "hubs", "guides", "products", "proof"],
        help="Manifest groups to submit.",
    )
    args = parser.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    submit(build_payload(manifest, args.groups))


if __name__ == "__main__":
    main()
