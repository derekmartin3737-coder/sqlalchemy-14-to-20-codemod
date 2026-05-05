# Discovery Playbook

This is the current operator guide for the discovery bottleneck as of
2026-04-13.

## Current Truth

- The live storefront is `https://zippertools.org`.
- Checkout and delivery are being moved to Stripe-controlled Worker routes.
- Test purchases succeeded.
- The bottleneck is indexing and discovery, not fulfillment.
- Exact-problem landing pages already exist for the main SQLAlchemy pain
  queries.
- Messaging needs to stay narrow and honest while the pages age into the index.

## Current Priority

1. Get the homepage and the main SQLAlchemy issue pages indexed.
2. Get a small number of real external links from relevant public discussions.
3. Measure impressions, clicks, and product-page visits for 7-14 days before
   making pricing or scope changes.

## Indexing Queue

Submit these first in both Google Search Console and Bing Webmaster Tools:

1. The homepage.
2. The main SQLAlchemy landing page.
3. The `session.query(...)` migration page.
4. The `engine.execute(...)` removal page.
5. The `joinedload_all(...)` cleanup page.

Do not burn time requesting every page at once. Start with the pages that best
match searcher intent for active migration pain.

## GitHub Repo About

Use the repo About section to support discovery instead of leaving it generic.

- Description:
  `SQLAlchemy 1.4 to 2.0 migration scanner and exact-problem docs for session.query, engine.execute, joinedload_all, and legacy Query cleanup.`
- Website:
  `https://zippertools.org`
- Topics:
  - `sqlalchemy`
  - `sqlalchemy-2`
  - `sqlalchemy-migration`
  - `python`
  - `orm`
  - `codemod`
  - `migration-tool`
  - `engine-execute`
  - `session-query`
  - `joinedload-all`

## External-Link Rules

- Link only when the landing page directly answers the thread's exact problem.
- Link the exact issue page, not the homepage and not checkout.
- Add a concrete migration answer in the reply itself before the link.
- Disclose that the page is yours when that matters.
- Keep the tone technical and useful, not salesy.
- Stop after a small number of strong links. Relevance matters more than volume.

Draft reply copy for the current candidate threads lives in
[`discussion-replies.md`](discussion-replies.md).

## Candidate Threads Found On 2026-04-13

These are good candidates only if the reply adds real value to the thread.

1. `session.query(...)` migration urgency:
   [sqlalchemy/sqlalchemy discussion #9619](https://github.com/sqlalchemy/sqlalchemy/discussions/9619)
2. `joinedload_all(...)` migration and duplicate-join confusion:
   [sqlalchemy/sqlalchemy discussion #11356](https://github.com/sqlalchemy/sqlalchemy/discussions/11356)
3. `engine.execute(...)` / `OptionEngine.execute` breakage:
   [Stack Overflow: read_sql_query() throws "'OptionEngine' object has no attribute 'execute'" with SQLAlchemy 2.0.0](https://stackoverflow.com/questions/75309237/read-sql-query-throws-optionengine-object-has-no-attribute-execute-with/75309321)

## What To Watch

Watch weekly, not hourly:

- indexed pages in Google and Bing
- Google impressions and clicks
- visits to the homepage
- visits to the exact-problem landing pages
- paid CTA visits from those pages
- first branded and non-branded queries that start earning impressions

If impressions are rising but clicks are flat, improve titles and snippets.
If pages are not indexed, keep working the link graph and wait. If pages are
indexed and visited but product pages are cold, then revisit positioning.

## What Not To Do Yet

- Do not change pricing because of a few quiet days.
- Do not widen scope again before the current pages get a fair indexing window.
- Do not point outreach traffic at checkout pages.
- Do not blur the positioning into a general AI refactor pitch.
