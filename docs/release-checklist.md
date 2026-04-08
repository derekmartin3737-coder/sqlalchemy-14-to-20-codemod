# Release Checklist

Use this before tagging the first public release.

## Release gate

- CI is green on `main`.
- The site copy matches current product reality.
- Demo artifacts still match the current CLI output.
- Pricing docs match the intended product ladder.
- Policy docs still match the site and support scope.
- `python -m sa20_pack.launch_readiness` is run and the only blockers are
  understood.

## Tag contents

Release assets should include:

- wheel
- sdist
- demo report JSON
- demo diff

## Release notes should answer

- What changed in free coverage?
- What still goes to manual review?
- What evidence got stronger?
- What should new users run first?

## Post-release steps

- add the release to launch posts
- update the launch log
- update the KPI dashboard at the end of the week

