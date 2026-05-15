# Legacy SA 1.4 Shop

This is a deliberately old SQLAlchemy 1.4 repo for exercising `sa20-pack`.
It models a tiny order/invoice workflow, but the point is the dependency shape:

- it pins `SQLAlchemy>=1.4,<2.0`
- it uses `sqlalchemy.ext.declarative.declarative_base`
- it uses legacy `select([...])`
- it uses `session.query(Model).get(...)`
- it uses string relationship joins and loader options
- it uses DML constructor kwargs such as `update(table, values=...)`

That means it should feel like a small real repo that works before the
SQLAlchemy 2.0 upgrade and needs this migration pack before the dependency can
move forward.

## Try It

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

Run the scanner from the parent repo:

```bash
python -m sa20_pack.cli fixtures/legacy_sa14_shop_repo --report test_runs/legacy-sa14-shop-report.json
```
