# Pricing

## Product ladder

## Free vs paid at a glance

| Capability | Free scan | Edge-case pack | Preset bundle |
| --- | --- | --- | --- |
| Public CLI | Yes | Yes | Uses public CLI outputs |
| Core deterministic transforms | Yes | Yes | Uses public CLI outputs |
| Diff preview | Yes | Yes | Uses public CLI outputs |
| JSON migration report | Yes | Yes, plus richer buyer docs | Uses public CLI outputs plus richer templates |
| Manual-review findings | Yes | Yes | Uses public CLI outputs plus rollout guidance |
| Wider edge-case coverage | No | Yes | No |
| Preset bundles | No | Included | Yes |
| Manager summary | No | Yes | Yes |
| Rollout checklist | Basic public docs | Yes | Yes |
| Human service dependency | No | No | No |
| Full custom migration service | No | No | No |

### Free scan

Price: **$0**

Use the public repo, CLI, and GitHub Action for:

- core deterministic transforms
- manual-review findings
- JSON migration report
- diff preview
- demo fixture and public docs

The point of the free tier is qualification and trust. A buyer should know
whether the repo is a fit before paying.

### One-time edge-case pack

Product name: **`sa20-pack Edge-Case Migration Pack`**

Launch price: **$99 per team**

What it adds:

- wider edge-case coverage
- more SQLAlchemy pattern presets
- richer reports and rollout checklists
- manager-facing migration summary
- enterprise-safe docs/templates

What the buyer is really paying for:

- fewer repetitive manual fixes
- clearer unsupported buckets
- tighter rollout confidence

### Preset bundle

Product name: **`sa20-pack Preset Bundle`**

Launch price: **$49 per team**

### Pydantic apply pack

Product name: **`pydantic-v2-porter Apply Pack`**

Launch price: **$99 per team**

What it includes:

- safe validator rewrites
- `BaseSettings` migration support
- supported `root_validator(pre=True)` rewrites
- safe config conversion for the documented subset
- fail-closed unsupported findings

What it includes:

- repo-type preset files
- richer report templates
- rollout notes and manager summary templates
- downloadable add-on with no service dependency

What it does not include:

- custom repo debugging
- custom coding by a person
- guaranteed full migration ownership

## Why the split works

Free spreads because it is genuinely useful and easy to prove.

Paid differentiates on:

- wider coverage
- better presets
- better reporting
- better docs/templates
- more repeatable rollout structure

That keeps the repo public and useful without giving away the entire revenue
engine.

## Who should not buy this

Do not buy if:

- you have not run the free scan yet
- your repo needs a full custom migration service
- your repo depends on unsupported patterns being auto-rewritten today
- you expect the paid pack to guarantee a passing application without manual
  review

## What happens if validation fails

If a migration run fails validation, the result is a failed migration run. The
tool should report that clearly instead of pretending the migration succeeded.

That means the buyer still gets useful information:

- what changed
- what was unsupported
- which validation phase failed

But it does not count as a quiet success.

## What the paid pack does not cover

The paid pack still does not promise:

- full `Query` to `select()` migration coverage
- transaction-semantics decisions for legacy execution paths
- every repo-specific rollout decision
- custom framework wrappers that hide SQLAlchemy internals
- full-service debugging of application-specific failures
