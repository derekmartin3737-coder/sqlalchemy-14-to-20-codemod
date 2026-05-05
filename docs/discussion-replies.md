# Discussion Reply Drafts

These are drafts for relevant public threads. Use them only where the reply
genuinely helps the existing discussion. Keep the tone technical. Link the
exact issue page, not the homepage and not checkout.

## 1. `session.query(...)` migration discussion

Target: the `session.query(...)` migration thread listed in
[`discovery-playbook.md`](discovery-playbook.md).

Draft:

> `Query` itself is still present in SQLAlchemy 2.0, so the part worth doing
> first is the narrow mechanical cleanup rather than trying to rewrite every
> query to `select()` in one pass. The low-risk buckets are things like
> `session.query(Model).get(pk)` -> `session.get(Model, pk)`,
> `select([..])` -> `select(..)`, and simple string relationship paths to mapped
> attributes. We wrote up the staging logic here in case it helps:
> `https://zippertools.org/sqlalchemy/session-query-migration/`

## 2. `joinedload_all(...)` removal discussion

Target: the `joinedload_all(...)` thread listed in
[`discovery-playbook.md`](discovery-playbook.md).

Draft:

> The direct replacement is only safe when the relationship path is obvious.
> For the easy case, `joinedload_all("orders.items")` becomes
> `joinedload(User.orders).joinedload(Order.items)`. Where it gets messy is when
> the old loader option interacts with aliasing, duplicate joins, or
> `contains_eager`, because then the right replacement depends on the rest of
> the query shape instead of just the string path. I wrote up the clean-vs-manual
> boundary here:
> `https://zippertools.org/sqlalchemy/joinedload-all-removed/`

## 3. `engine.execute(...)` / `OptionEngine` breakage discussion

Target: the `engine.execute(...)` / `OptionEngine` thread listed in
[`discovery-playbook.md`](discovery-playbook.md).

Draft:

> The underlying issue is that execution moved off `Engine` and onto
> `Connection` or `Session`, so the fix is not "replace one method name with
> another." For raw SQL, use `text(...)`; for pandas-style cases, pass an actual
> connection instead of the old engine execution path. That is why this bucket
> is better treated as manual review than as a blanket codemod. I put the direct
> replacement shape and the boundary here:
> `https://zippertools.org/sqlalchemy/engine-execute-removed/`

## Posting Rules

- Add the answer first, then the link.
- Keep each reply to one link.
- Mention that the page is yours if the thread context calls for disclosure.
- Do not argue with maintainers or keep replying after the useful answer is
  already on the page.
