#!/usr/bin/env node

const API_URL = "https://api.cloudflare.com/client/v4/graphql";
const QUALIFIED_PREFIXES = [
  "/sqlalchemy/",
  "/pydantic/",
  "/eslint/",
  "/products/",
  "/proof/",
  "/demo",
  "/pricing",
];
const STRIPE_CHECKOUT_PREFIXES = [
  "/go/sa20-pack",
  "/go/sa20-preset",
  "/go/pydantic-v2-porter",
];
const FIT_REPORT_GO_PREFIXES = [
  "/go/fit-report",
  "/go/fit-review",
];
const FREE_SCAN_PREFIXES = [
  "/go/free-scan",
  "/go/pydantic-free-scan",
  "/go/flatconfig-free-scan",
];

function parseArgs(argv) {
  const args = { hours: 24, limit: 1000, offsetHours: 0 };
  for (let index = 2; index < argv.length; index += 1) {
    const item = argv[index];
    if (item === "--hours") {
      args.hours = Number(argv[index + 1]);
      index += 1;
    } else if (item === "--offset-hours") {
      args.offsetHours = Number(argv[index + 1]);
      index += 1;
    } else if (item === "--limit") {
      args.limit = Number(argv[index + 1]);
      index += 1;
    } else {
      throw new Error(`Unknown argument: ${item}`);
    }
  }
  if (!Number.isFinite(args.hours) || args.hours <= 0) {
    throw new Error("--hours must be a positive number");
  }
  if (!Number.isInteger(args.limit) || args.limit <= 0) {
    throw new Error("--limit must be a positive integer");
  }
  if (!Number.isFinite(args.offsetHours) || args.offsetHours < 0) {
    throw new Error("--offset-hours must be zero or a positive number");
  }
  return args;
}

function requireEnv(name) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing ${name}`);
  }
  return value;
}

async function graphql(token, query, variables) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      authorization: `Bearer ${token}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({ query, variables }),
  });
  const payload = await response.json();
  if (!response.ok || payload.errors) {
    throw new Error(JSON.stringify(payload.errors || payload, null, 2));
  }
  return payload.data.viewer.zones[0];
}

function sortByVisitsThenRequests(left, right) {
  return right.visits - left.visits || right.requests - left.requests;
}

function isQualifiedPath(path) {
  return QUALIFIED_PREFIXES.some((prefix) => path === prefix || path.startsWith(prefix));
}

function isPathUnder(path, prefix) {
  return path === prefix || path.startsWith(`${prefix}/`);
}

function isStripeCheckoutPath(path) {
  return STRIPE_CHECKOUT_PREFIXES.some((prefix) => isPathUnder(path, prefix));
}

function isFitReportPath(path) {
  return FIT_REPORT_GO_PREFIXES.some((prefix) => isPathUnder(path, prefix));
}

function isFreeScanPath(path) {
  return FREE_SCAN_PREFIXES.some((prefix) => isPathUnder(path, prefix));
}

function classify(path) {
  if (isStripeCheckoutPath(path)) return "stripe_checkout";
  if (isFitReportPath(path)) return "fit_report";
  if (isFreeScanPath(path)) return "free_scan";
  if (isPathUnder(path, "/go/github-release")) return "trust";
  if (path.startsWith("/go/")) return "go_other";
  if (path.startsWith("/products/")) return "products";
  if (path.startsWith("/proof/")) return "proof";
  if (path.startsWith("/sqlalchemy/")) return "sqlalchemy";
  if (path.startsWith("/pydantic/")) return "pydantic";
  if (path.startsWith("/eslint/")) return "eslint";
  if (path === "/demo" || path === "/pricing") return "static_intent";
  return "other";
}

async function main() {
  const args = parseArgs(process.argv);
  const token = requireEnv("CLOUDFLARE_API_TOKEN");
  const zoneTag = requireEnv("CLOUDFLARE_ZONE_ID");
  const until = new Date(Date.now() - args.offsetHours * 60 * 60 * 1000);
  const since = new Date(until.getTime() - args.hours * 60 * 60 * 1000);
  const variables = {
    zoneTag,
    since: since.toISOString(),
    until: until.toISOString(),
    limit: args.limit,
  };

  const totalsQuery = `query ZoneTraffic($zoneTag: string, $since: Time, $until: Time) {
    viewer {
      zones(filter: { zoneTag: $zoneTag }) {
        httpRequests1hGroups(limit: 168, filter: { datetime_geq: $since, datetime_lt: $until }) {
          dimensions { datetime }
          sum { requests pageViews }
          uniq { uniques }
        }
      }
    }
  }`;
  const pathsQuery = `query TopPaths($zoneTag: string, $since: Time, $until: Time, $limit: uint64) {
    viewer {
      zones(filter: { zoneTag: $zoneTag }) {
        httpRequestsAdaptiveGroups(limit: $limit, filter: { datetime_geq: $since, datetime_lt: $until }) {
          count
          dimensions { clientRequestPath edgeResponseStatus }
          sum { visits }
        }
      }
    }
  }`;

  const [totalsZone, pathsZone] = await Promise.all([
    graphql(token, totalsQuery, variables),
    graphql(token, pathsQuery, variables),
  ]);

  const hourlyGroups = totalsZone.httpRequests1hGroups;
  const pathGroups = pathsZone.httpRequestsAdaptiveGroups.map((group) => ({
    path: group.dimensions.clientRequestPath,
    status: group.dimensions.edgeResponseStatus,
    requests: group.count,
    visits: group.sum.visits,
    class: classify(group.dimensions.clientRequestPath || ""),
  }));

  const totals = hourlyGroups.reduce(
    (acc, group) => {
      acc.requests += group.sum.requests || 0;
      acc.pageViews += group.sum.pageViews || 0;
      acc.uniquesHourlySum += group.uniq.uniques || 0;
      return acc;
    },
    { requests: 0, pageViews: 0, uniquesHourlySum: 0 },
  );

  const qualified = pathGroups.filter((group) => isQualifiedPath(group.path));
  const goPaths = pathGroups
    .filter((group) => group.path.startsWith("/go/"))
    .sort((left, right) => right.requests - left.requests);
  const checkoutGoPaths = goPaths.filter((group) => isStripeCheckoutPath(group.path));
  const fitReportGoPaths = goPaths.filter((group) => isFitReportPath(group.path));
  const freeScanPaths = goPaths.filter((group) => isFreeScanPath(group.path));
  const trustPaths = goPaths.filter((group) => isPathUnder(group.path, "/go/github-release"));

  const classTotals = {};
  for (const group of [...qualified, ...goPaths]) {
    classTotals[group.class] ||= { requests: 0, visits: 0 };
    classTotals[group.class].requests += group.requests;
    classTotals[group.class].visits += group.visits;
  }

  const snapshot = {
    sinceUtc: since.toISOString(),
    untilUtc: until.toISOString(),
    hours: args.hours,
    offsetHours: args.offsetHours,
    totals,
    qualified: {
      visits: qualified.reduce((sum, group) => sum + group.visits, 0),
      requests: qualified.reduce((sum, group) => sum + group.requests, 0),
      byClass: classTotals,
      topPaths: qualified.sort(sortByVisitsThenRequests).slice(0, 25),
    },
    checkout: {
      totalRequests: checkoutGoPaths.reduce((sum, group) => sum + group.requests, 0),
      paths: checkoutGoPaths,
    },
    fitReport: {
      totalRequests: fitReportGoPaths.reduce((sum, group) => sum + group.requests, 0),
      paths: fitReportGoPaths,
    },
    goRoutes: {
      totalRequests: goPaths.reduce((sum, group) => sum + group.requests, 0),
      stripeCheckoutRequests: checkoutGoPaths.reduce(
        (sum, group) => sum + group.requests,
        0,
      ),
      freeScanRequests: freeScanPaths.reduce((sum, group) => sum + group.requests, 0),
      fitReportRequests: fitReportGoPaths.reduce((sum, group) => sum + group.requests, 0),
      trustRequests: trustPaths.reduce((sum, group) => sum + group.requests, 0),
      paths: goPaths,
    },
  };

  console.log(JSON.stringify(snapshot, null, 2));
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
