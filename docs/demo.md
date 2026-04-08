# Demo

## Goal

Show a public scanner-first demo on the included fixture repo, then make the
commercial apply path easy to understand without exposing the paid code.

## Fixture

`fixtures/demo_repo`

Pre-migration it contains:

- `select([User.name])`
- `joinedload("addresses")`
- `join("addresses")`
- `update(..., whereclause=..., values=...)`
- `session.query(User).get(...)`

## Failing Pre-Migration State

From the fixture repo:

```bash
python -m pytest -q -p no:cacheprovider
```

Expected: failures under SQLAlchemy 2.0.

## Free Scan Command

```bash
python -m sa20_pack.cli fixtures/demo_repo --report artifacts/demo-migration-report.json
```

## Report Output

See:

- `artifacts/demo-migration-report.json`

The report should show:

- supported candidates detected
- unsupported patterns found
- confidence assessment

Representative summary:

```text
Status: preview_only
Files scanned: 5
Files changed: 0
Transforms applied: 6
Unsupported findings: 0
Overall confidence: 0.935
```

Representative supported-candidate excerpt:

```text
Supported candidates:
- select([User.name])
- session.query(User).get(user_id)
- joinedload("addresses")
- join("addresses")
- update(..., whereclause=..., values=...)
```

## Commercial Apply Path

After the free scan confirms repo fit, the paid pack performs the documented
rewrites on a branch and includes rollout material in the purchased ZIP.

## Buyer-visible takeaway

The demo value is not only that the scanner finds patterns. The value is:

- fast fit assessment
- machine-generated report
- explicit unsupported bucket
- a clear handoff into the paid apply pack when the repo fits scope
