# SQLAlchemy 1.4 to 2.0 Cleanup Sample Manager Summary

## Decision

The sample fixture is a good fit for the paid cleanup workflow. The scan found repeated supported patterns, the preview diff was narrow, the apply run changed four files, and validation passed on the fixture commands.

## What Changed

- Replaced `session.query(User).get(user_id)` with `session.get(User, user_id)`.
- Replaced `select([User.name])` with `select(User.name)`.
- Replaced simple string relationship joins and loader options with attribute references.
- Rewrote legacy DML constructor kwargs into SQLAlchemy 2.0-style chained calls.

## Risk Notes

- No private source code was uploaded.
- No unsupported findings were hidden.
- This does not claim a full SQLAlchemy 2.0 migration for every repo.
- Buyer should still run normal CI before merge.

## Recommended Next Step

Use the paid cleanup pack when the buyer's real scanner output shows repeated supported findings across enough files to justify branch review time.
