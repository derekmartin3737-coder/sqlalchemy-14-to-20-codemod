# Brutally Honest Backlog

## What now blocks the new Product Wells direction

1. The website still presents the old SQLAlchemy-first business more strongly
   than the new Product Wells operating model.
   - SQLAlchemy should become proof/archive.
   - The homepage should feature the current Well of the Month.

2. GitHub Actions Upgrade Guard does not exist yet.
   - No `products/actions-upgrade-guard/` package.
   - No workflow parser.
   - No rules-as-data format.
   - No report or patch generator.

3. Analytics can now answer the first Product Well demand question.
   - Route clicks go through tracked `/go/...` paths.
   - The Worker writes structured `conversion_route` logs without requiring an
     Analytics Engine account feature.

4. The current public trust path still needs deployment cleanup.
   - Live `config.js` has previously lagged local config.
   - The live site must show the professional support address.
   - The live funnel verifier should pass after deploy.

5. The portfolio needs kill rules.
   - Do not keep building a well just because it is technically interesting.
   - Promote only after scanner runs, buyer conversations, or clear checkout
     intent.

## Highest-leverage improvements after this reset

1. Scaffold GitHub Actions Upgrade Guard.
2. Build a public proof fixture with generated report and patch output.
3. Reframe the website around Product Wells and archive SQLAlchemy as proof.
4. Keep route-click analytics visible during the next demand test.
5. Run a seven-day well test against exact GitHub Actions deprecation pain.

## Legacy SQLAlchemy blockers

Keep these only if SQLAlchemy demand returns:

1. The paid edge-case surface is still conceptual.
2. Coverage is too narrow for many real SQLAlchemy repos.
3. There is no transaction-aware `engine.execute(...)` migration.
4. There is no full `Query` -> `select()` conversion.
5. There is no async migration story.
6. Public proof exists, but buyer intent was weak.
