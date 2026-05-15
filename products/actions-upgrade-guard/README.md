# GitHub Actions Upgrade Guard

GitHub Actions Upgrade Guard is a local-first scanner for workflow deprecations,
runner drift, permissions risk, and patchable Actions breakage.

It is the first Product Wells flagship: buy it, run it locally, get a useful
artifact, and never upload source code.

## Who This Is For

- Platform engineers responsible for many repositories.
- DevOps leads cleaning up brittle Actions workflows before deadlines.
- Repo owners who need a reviewer-friendly patch and risk report.
- Maintainers who want a CI gate for upcoming Actions breakage.

## Do Not Use This If

- You need a hosted monitoring service.
- You want the tool to log in to GitHub and mutate repos for you.
- Your workflows are generated dynamically and the generated files are not
  checked into the repo.
- You expect security hardening beyond the documented workflow-upgrade rules.

## Current Supported Rules

- `actions/upload-artifact@v3` and `actions/download-artifact@v3` detection
  with safe patch previews to v4.
- `actions/cache@v1` and `actions/cache@v2` detection with safe patch previews
  to v4.
- `ubuntu-20.04` hosted runner retirement detection.
- `macos-latest` migration-risk detection.
- Local JavaScript actions using `node20` runtime detection.
- Temporary Node 20 opt-out environment variable detection.
- Missing or broad `GITHUB_TOKEN` permissions detection.
- Composite and local action inventory.
- Fail-closed reporting for invalid workflow YAML.

## Example

```bash
python -m actions_upgrade_guard.cli path/to/repo \
  --report actions-upgrade-report.json \
  --html-report actions-upgrade-report.html
```

Apply only deterministic workflow action-version patches:

```bash
python -m actions_upgrade_guard.cli path/to/repo --apply
```

## Outputs

- `actions-upgrade-report.json`: machine-readable report for CI and dashboards.
- `actions-upgrade-report.html`: reviewer and manager-readable summary.
- patch previews in both reports before any apply step.
- exit code `0` when there are no blocking findings.
- exit code `1` when blocking findings require action.
- exit code `2` when the scanner cannot run.

## Trust Boundary

- Runs locally.
- No GitHub token required.
- No source upload.
- No repo mutation unless `--apply` is explicitly passed.
- Every finding names the source-backed rule and whether the fix is automatic,
  manual review, blocked, or informational.
