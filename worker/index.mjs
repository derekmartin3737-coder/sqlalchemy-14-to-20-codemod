const MAX_WEBHOOK_BYTES = 64 * 1024;
const PAYHIP_WEBHOOK_PATH = "/payhip/webhook";
const GO_ROUTES = {
  "/go/free-scan": {
    kind: "free_scan",
    label: "free-scan",
    target:
      "https://github.com/derekmartin3737-coder/sqlalchemy-14-to-20-codemod/blob/main/docs/quickstart.md?utm_source=zippertools&utm_medium=site&utm_campaign=free_scan&utm_content=quickstart",
  },
  "/go/github-release": {
    kind: "trust",
    label: "github-release",
    target:
      "https://github.com/derekmartin3737-coder/sqlalchemy-14-to-20-codemod/releases/tag/v0.1.0?utm_source=zippertools&utm_medium=site&utm_campaign=trust&utm_content=v0.1.0",
  },
  "/go/sa20-pack": {
    kind: "checkout",
    label: "sa20-pack",
    target:
      "https://pay.zippertools.org/b/QimJ6?utm_source=zippertools&utm_medium=site&utm_campaign=checkout&utm_content=sa20-pack",
  },
  "/go/sa20-preset": {
    kind: "checkout",
    label: "sa20-preset",
    target:
      "https://pay.zippertools.org/b/wh2Ro?utm_source=zippertools&utm_medium=site&utm_campaign=checkout&utm_content=sa20-preset",
  },
  "/go/pydantic-v2-porter": {
    kind: "checkout",
    label: "pydantic-v2-porter",
    target:
      "https://pay.zippertools.org/b/KamA1?utm_source=zippertools&utm_medium=site&utm_campaign=checkout&utm_content=pydantic-v2-porter",
  },
};

function jsonResponse(value, init = {}) {
  const headers = new Headers(init.headers);
  headers.set("content-type", "application/json; charset=utf-8");
  headers.set("cache-control", "no-store");
  return new Response(JSON.stringify(value), { ...init, headers });
}

function matchGoRoute(pathname) {
  const candidates = Object.entries(GO_ROUTES).sort(
    ([left], [right]) => right.length - left.length,
  );
  for (const [basePath, route] of candidates) {
    if (pathname === basePath) {
      return { basePath, route, source: "unknown" };
    }
    if (pathname.startsWith(`${basePath}/`)) {
      const source = pathname.slice(basePath.length + 1) || "unknown";
      return { basePath, route, source };
    }
  }
  return null;
}

function appendTrackingParam(target, source) {
  const url = new URL(target);
  if (source && source !== "unknown") {
    url.searchParams.set("utm_term", source.slice(0, 120));
  }
  return url.toString();
}

function writeConversionEvent(env, event) {
  console.log("conversion_route", JSON.stringify(event));
  if (env.CONVERSION_EVENTS?.writeDataPoint) {
    env.CONVERSION_EVENTS.writeDataPoint({
      blobs: [
        event.kind,
        event.label,
        event.source,
        event.path,
        event.country,
        event.refererHost,
      ],
      doubles: [Date.now()],
      indexes: [event.label],
    });
  }
}

function handleGoRoute(request, env, match) {
  const url = new URL(request.url);
  const referer = request.headers.get("referer") || "";
  let refererHost = "";
  try {
    refererHost = referer ? new URL(referer).host : "";
  } catch {
    refererHost = "";
  }

  const event = {
    kind: match.route.kind,
    label: match.route.label,
    source: match.source,
    path: url.pathname,
    method: request.method,
    country: request.cf?.country || "",
    colo: request.cf?.colo || "",
    refererHost,
  };
  writeConversionEvent(env, event);

  const headers = new Headers({
    location: appendTrackingParam(match.route.target, match.source),
    "cache-control": "no-store",
  });
  return new Response(null, { status: 302, headers });
}

function hexToBytes(value) {
  if (!/^[0-9a-f]+$/i.test(value) || value.length % 2 !== 0) {
    return null;
  }

  const bytes = new Uint8Array(value.length / 2);
  for (let index = 0; index < value.length; index += 2) {
    bytes[index / 2] = Number.parseInt(value.slice(index, index + 2), 16);
  }
  return bytes;
}

function timingSafeEqual(left, right) {
  if (left.byteLength !== right.byteLength) {
    return false;
  }

  let difference = 0;
  for (let index = 0; index < left.byteLength; index += 1) {
    difference |= left[index] ^ right[index];
  }
  return difference === 0;
}

async function sha256Hex(value) {
  const encoded = new TextEncoder().encode(value);
  const digest = await crypto.subtle.digest("SHA-256", encoded);
  return Array.from(new Uint8Array(digest), (byte) =>
    byte.toString(16).padStart(2, "0"),
  ).join("");
}

async function verifyPayhipSignature(payload, apiKey) {
  const signature = typeof payload.signature === "string" ? payload.signature : "";
  const provided = hexToBytes(signature.toLowerCase());
  if (!provided) {
    return false;
  }

  const expectedHex = await sha256Hex(apiKey);
  const expected = hexToBytes(expectedHex);
  if (!expected) {
    return false;
  }

  return timingSafeEqual(provided, expected);
}

function summarizePayhipEvent(payload) {
  const items = Array.isArray(payload.items) ? payload.items : [];
  return {
    type: payload.type,
    id: payload.id || payload.subscription_id || "",
    currency: payload.currency || "",
    price: payload.price ?? null,
    amount_refunded: payload.amount_refunded ?? null,
    date: payload.date || payload.date_created || payload.date_subscription_started || null,
    products: items.map((item) => ({
      product_id: item.product_id || "",
      product_name: item.product_name || "",
      product_key: item.product_key || item.product_link || "",
      quantity: item.quantity || "",
      used_coupon: Boolean(item.used_coupon),
    })),
  };
}

async function handlePayhipWebhook(request, env) {
  if (request.method === "GET" || request.method === "HEAD") {
    return jsonResponse({
      ok: true,
      endpoint: PAYHIP_WEBHOOK_PATH,
      configured: Boolean(env.PAYHIP_API_KEY),
    });
  }

  if (request.method !== "POST") {
    return jsonResponse({ ok: false, error: "method_not_allowed" }, { status: 405 });
  }

  if (!env.PAYHIP_API_KEY) {
    console.warn("payhip_webhook_missing_api_key");
    return jsonResponse({ ok: false, error: "not_configured" }, { status: 503 });
  }

  const contentLength = Number(request.headers.get("content-length") || "0");
  if (contentLength > MAX_WEBHOOK_BYTES) {
    return jsonResponse({ ok: false, error: "payload_too_large" }, { status: 413 });
  }

  let payload;
  try {
    payload = JSON.parse(await request.text());
  } catch {
    return jsonResponse({ ok: false, error: "invalid_json" }, { status: 400 });
  }

  const valid = await verifyPayhipSignature(payload, env.PAYHIP_API_KEY);
  if (!valid) {
    console.warn("payhip_webhook_invalid_signature");
    return jsonResponse({ ok: false, error: "invalid_signature" }, { status: 401 });
  }

  const event = summarizePayhipEvent(payload);
  console.log("payhip_webhook_accepted", JSON.stringify(event));
  return jsonResponse({ ok: true });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === PAYHIP_WEBHOOK_PATH) {
      return handlePayhipWebhook(request, env);
    }

    const goRoute = matchGoRoute(url.pathname);
    if (goRoute) {
      return handleGoRoute(request, env, goRoute);
    }

    return env.ASSETS.fetch(request);
  },
};
