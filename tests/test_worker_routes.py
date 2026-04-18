from __future__ import annotations

import subprocess


def test_worker_tracks_source_tagged_go_routes() -> None:
    script = """
import worker from './worker/index.mjs';
const env = { ASSETS: { fetch: async () => new Response('asset') } };
const request = new Request('https://zippertools.org/go/sa20-pack/product-sa20-pack');
const response = await worker.fetch(request, env);
console.log(response.status);
console.log(response.headers.get('location'));
"""
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        check=True,
        capture_output=True,
        text=True,
    )

    lines = result.stdout.strip().splitlines()
    assert "conversion_route" in lines[0]
    assert lines[-2] == "302"
    assert lines[-1].startswith("https://pay.zippertools.org/b/QimJ6")
    assert "utm_content=sa20-pack" in lines[-1]
    assert "utm_term=product-sa20-pack" in lines[-1]
