from __future__ import annotations

import json
import subprocess
from pathlib import Path


def test_cloudflare_assets_runs_worker_for_checkout_and_webhooks() -> None:
    config = json.loads(Path("wrangler.jsonc").read_text(encoding="utf-8"))

    assert set(config["assets"]["run_worker_first"]) >= {
        "/go/*",
        "/stripe/*",
        "/payhip/*",
        "/__stripe_paid_assets/*",
    }


def test_worker_tracks_source_tagged_go_routes() -> None:
    script = """
import worker from './worker/index.mjs';
const env = {
  ASSETS: { fetch: async () => new Response('asset') },
  STRIPE_SECRET_KEY: 'sk_test_unit',
};
const originalFetch = globalThis.fetch;
globalThis.fetch = async (url, init) => {
  const params = new URLSearchParams(init.body);
  console.log([
    url,
    params.get('metadata[product_slug]'),
    params.get('metadata[source]'),
    params.get('line_items[0][price_data][unit_amount]'),
  ].join(' '));
  return new Response(
    JSON.stringify({ url: 'https://checkout.stripe.com/c/pay/cs_test_sa20' }),
    { status: 200 },
  );
};
const request = new Request('https://zippertools.org/go/sa20-pack/product-sa20-pack');
const response = await worker.fetch(request, env);
globalThis.fetch = originalFetch;
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
    assert lines[1] == (
        "https://api.stripe.com/v1/checkout/sessions "
        "sa20-pack product-sa20-pack 29999"
    )
    assert lines[-2] == "303"
    assert lines[-1] == "https://checkout.stripe.com/c/pay/cs_test_sa20"


def test_all_paid_go_routes_create_stripe_checkout_sessions() -> None:
    script = """
import worker from './worker/index.mjs';
const env = {
  ASSETS: { fetch: async () => new Response('asset') },
  STRIPE_SECRET_KEY: 'sk_test_unit',
};
const routes = [
  ['/go/fit-report', 'fit-report', '9900'],
  ['/go/sa20-pack', 'sa20-pack', '29999'],
  ['/go/sa20-preset', 'sa20-preset', '14999'],
  ['/go/pydantic-v2-porter', 'pydantic-v2-porter', '24999'],
];
const originalLog = console.log;
console.log = () => {};
const originalFetch = globalThis.fetch;
globalThis.fetch = async (_url, init) => {
  const params = new URLSearchParams(init.body);
  const product = params.get('metadata[product_slug]');
  const amount = params.get('line_items[0][price_data][unit_amount]');
  return new Response(
    JSON.stringify({ url: `https://checkout.stripe.com/c/pay/cs_test_${product}_${amount}` }),
    { status: 200 },
  );
};
for (const [route] of routes) {
  const request = new Request(`https://zippertools.org${route}/unit-test`);
  const response = await worker.fetch(request, env);
  const location = new URL(response.headers.get('location'));
  const parts = location.pathname.split('_');
  originalLog([
    response.status,
    location.host,
    parts.slice(2, -1).join('_'),
    parts.at(-1),
  ].join(' '));
}
globalThis.fetch = originalFetch;
"""
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.strip().splitlines() == [
        "303 checkout.stripe.com fit-report 9900",
        "303 checkout.stripe.com sa20-pack 29999",
        "303 checkout.stripe.com sa20-preset 14999",
        "303 checkout.stripe.com pydantic-v2-porter 24999",
    ]


def test_all_free_scan_routes_land_on_matching_public_docs() -> None:
    script = """
import worker from './worker/index.mjs';
const env = { ASSETS: { fetch: async () => new Response('asset') } };
const routes = [
  ['/go/free-scan', '/docs/quickstart.md'],
  ['/go/pydantic-free-scan', '/products/pydantic-v2-porter/README.md'],
  ['/go/flatconfig-free-scan', '/products/flatconfig-lift/README.md'],
];
const originalLog = console.log;
console.log = () => {};
for (const [route, expectedPath] of routes) {
  const request = new Request(`https://zippertools.org${route}/unit-test`);
  const response = await worker.fetch(request, env);
  const location = new URL(response.headers.get('location'));
  originalLog([
    response.status,
    location.host,
    location.pathname,
    location.searchParams.get('utm_campaign'),
    location.searchParams.get('utm_term'),
  ].join(' '));
}
"""
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.strip().splitlines() == [
        "302 github.com /derekmartin3737-coder/sqlalchemy-14-to-20-codemod/blob/main/docs/quickstart.md free_scan unit-test",
        "302 github.com /derekmartin3737-coder/sqlalchemy-14-to-20-codemod/blob/main/products/pydantic-v2-porter/README.md free_scan unit-test",
        "302 github.com /derekmartin3737-coder/sqlalchemy-14-to-20-codemod/blob/main/products/flatconfig-lift/README.md free_scan unit-test",
    ]


def test_legacy_fit_review_route_points_to_stripe_fit_report_checkout() -> None:
    script = """
import worker from './worker/index.mjs';
const env = { ASSETS: { fetch: async () => new Response('asset') } };
const originalLog = console.log;
console.log = () => {};
const request = new Request('https://zippertools.org/go/fit-review/unit-test');
const response = await worker.fetch(request, env);
const location = new URL(response.headers.get('location'));
console.log = originalLog;
console.log([response.status, location.host, location.pathname].join(' '));
"""
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.strip() == "302 zippertools.org /go/fit-report"


def test_stripe_checkout_requires_secret_before_payment() -> None:
    script = """
import worker from './worker/index.mjs';
const env = { ASSETS: { fetch: async () => new Response('asset') } };
const originalLog = console.log;
const originalWarn = console.warn;
console.log = () => {};
console.warn = () => {};
const response = await worker.fetch(
  new Request('https://zippertools.org/go/sa20-pack/unit-test'),
  env,
);
console.log = originalLog;
console.warn = originalWarn;
console.log(response.status);
console.log(await response.text());
"""
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        check=True,
        capture_output=True,
        text=True,
    )

    lines = result.stdout.strip().splitlines()
    assert lines[-2] == "503"
    assert '"stripe_not_configured"' in lines[-1]


def test_stripe_checkout_audit_passes_locally() -> None:
    result = subprocess.run(
        ["node", "scripts/audit_stripe_checkout.mjs"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "local Stripe checkout audit passed for 4 products" in result.stdout


def test_stripe_delivery_serves_asset_after_paid_session() -> None:
    script = """
import worker from './worker/index.mjs';
const assetHits = [];
const env = {
  ASSETS: { fetch: async () => new Response('asset') },
  PAID_ARTIFACTS: {
    get: async (key) => {
      assetHits.push(key);
      if (key === 'manifest:sa20-pack-edge-case-pack.zip') {
        return JSON.stringify({ chunks: 1, bytes: 9 });
      }
      if (key === 'chunk:sa20-pack-edge-case-pack.zip:0') {
        return btoa('zip-bytes');
      }
      return null;
    },
  },
  STRIPE_SECRET_KEY: 'sk_test_unit',
};
const originalLog = console.log;
console.log = () => {};
const originalFetch = globalThis.fetch;
globalThis.fetch = async (url) => {
  originalLog(url);
  return new Response(JSON.stringify({
    id: 'cs_test_paid',
    payment_status: 'paid',
    metadata: { product_slug: 'sa20-pack' },
  }), { status: 200 });
};
const response = await worker.fetch(
  new Request('https://zippertools.org/stripe/delivery?session_id=cs_test_paid'),
  env,
);
globalThis.fetch = originalFetch;
console.log = originalLog;
console.log(assetHits[0]);
console.log(response.status);
console.log(response.headers.get('content-disposition'));
console.log(await response.text());
"""
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.strip().splitlines() == [
        "https://api.stripe.com/v1/checkout/sessions/cs_test_paid",
        "manifest:sa20-pack-edge-case-pack.zip",
        "200",
        'attachment; filename="sa20-pack-edge-case-pack.zip"',
        "zip-bytes",
    ]


def test_paid_asset_paths_are_not_directly_public() -> None:
    script = """
import worker from './worker/index.mjs';
let assetFetchCount = 0;
const env = {
  ASSETS: {
    fetch: async () => {
      assetFetchCount += 1;
      return new Response('leaked');
    },
  },
};
const response = await worker.fetch(
  new Request('https://zippertools.org/__stripe_paid_assets/sa20-pack-edge-case-pack.zip'),
  env,
);
console.log(response.status);
console.log(assetFetchCount);
console.log(await response.text());
"""
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        check=True,
        capture_output=True,
        text=True,
    )

    lines = result.stdout.strip().splitlines()
    assert lines[0] == "404"
    assert lines[1] == "0"
    assert '"not_found"' in lines[2]


def test_stripe_webhook_verifies_signed_checkout_event() -> None:
    script = """
import worker from './worker/index.mjs';
const secret = 'whsec_unit';
const payload = JSON.stringify({
  id: 'evt_unit',
  type: 'checkout.session.completed',
  livemode: false,
  data: {
    object: {
      id: 'cs_test_paid',
      mode: 'payment',
      payment_status: 'paid',
      amount_total: 29999,
      currency: 'usd',
      metadata: { product_slug: 'sa20-pack', source: 'unit-test' },
    },
  },
});
const timestamp = String(Math.floor(Date.now() / 1000));
const encoder = new TextEncoder();
const key = await crypto.subtle.importKey(
  'raw',
  encoder.encode(secret),
  { name: 'HMAC', hash: 'SHA-256' },
  false,
  ['sign'],
);
const signed = await crypto.subtle.sign(
  'HMAC',
  key,
  encoder.encode(`${timestamp}.${payload}`),
);
const hex = Array.from(new Uint8Array(signed), (byte) =>
  byte.toString(16).padStart(2, '0'),
).join('');
const env = {
  ASSETS: { fetch: async () => new Response('asset') },
  STRIPE_WEBHOOK_SECRET: secret,
};
const originalLog = console.log;
console.log = () => {};
const response = await worker.fetch(
  new Request('https://zippertools.org/stripe/webhook', {
    method: 'POST',
    body: payload,
    headers: { 'stripe-signature': `t=${timestamp},v1=${hex}` },
  }),
  env,
);
console.log = originalLog;
console.log(response.status);
console.log(await response.text());
"""
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.strip().splitlines() == [
        "200",
        '{"ok":true}',
    ]
