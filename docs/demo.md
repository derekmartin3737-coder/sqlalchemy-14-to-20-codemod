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

The paid path is still intentionally narrow: it previews supported rewrites,
applies only documented transforms, records validation results, and leaves
unsupported work in the report instead of claiming a complete SQLAlchemy 2.0
migration.

### Preview Diff

```diff
- user = session.query(User).get(user_id)
+ user = session.get(User, user_id)

- stmt = select([User.name])
+ stmt = select(User.name)
```

### Apply Output

```text
paid apply run
files_changed: 4
transforms_applied:
  query_get, select_list_syntax, string_join,
  string_loader, dml_kwargs
manual_review_findings: 0
report_written: migration-report.json
```

### Validation Result

```text
validation summary
python -m compileall fixtures/demo_repo ... passed
python -m pytest fixtures/demo_repo/tests ... passed
buyer_repo_validation: required before merge
```

### Final Manager Report

```text
final manager report
Supported cleanup findings: 6
Manual-review findings: 0
Changed files: 4
Next step: review branch diff and run normal CI
```

### Exact ZIP Contents

```text
sa20-pack-edge-case-pack.zip
- paid cleanup CLI
- preview/apply commands
- supported rewrite table
- JSON report schema
- rollback checklist
- manager summary template
- license and support terms
```

## Buyer-visible takeaway

The demo value is not only that the scanner finds patterns. The value is:

- fast fit assessment
- machine-generated report
- explicit unsupported bucket
- a clear handoff into the paid apply pack when the repo fits scope
