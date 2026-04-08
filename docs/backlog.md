# Brutally Honest Backlog

## What still blocks first sales

1. The paid edge-case surface is still conceptual.
   - The public tool is real.
   - The paid differentiation is not implemented yet.

2. Coverage is still too narrow for many real SQLAlchemy repos.
   - No transaction-aware `engine.execute(...)` migration.
   - No full `Query` -> `select()` conversion.
   - No async migration story.

3. Packaging proof is weaker than ideal.
   - Validation uses repo-local compile/build checks.
   - A clean wheel/sdist packaging path should be added later.

4. The public launch still needs real user repo trials.
   - Fixture proof is necessary but not sufficient.

5. Ruff cache warnings still appear in this workspace.
   - They do not fail validation, but they are noisy.

## Highest-leverage improvements after this handoff

1. Add one or two more high-value transforms around removed legacy query
   helpers.
2. Test against public SQLAlchemy repos or sanitized internal samples.
3. Package the first paid preset pack around a few repeated unsupported cases.
