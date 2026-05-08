# Guided launcher nested project root bug

## Summary

When `factory-launcher.py --guided` was run from `/projects/factory-template`,
the launcher created the downstream repo at
`/projects/factory-template/<project_slug>` instead of canonical
`/projects/<project_slug>`.

## Impact

- Downstream repo could be nested inside the factory repo.
- Factory worktree received an untracked generated project directory.
- Preflight output and generated feature workspace paths referenced the wrong
  root.

## Root cause

`factory-launcher.py` and `first-project-wizard.py` used `Path.cwd() /
project_slug` as the default project base. That is correct for isolated smoke
directories, but wrong for the canonical VPS layout when the command is launched
from the factory repo root under `/projects`.

## Fix

- Added default project-base detection:
  - if current working directory is the factory repo under `/projects`, create
    downstream projects directly under `/projects`;
  - otherwise preserve existing current-directory behavior for smoke tests and
    custom project bases.
- Added `--project-base` to both launcher layers.
- Added route-only regression coverage in `verify-all.sh`.
- Fixed generated `deploy-dry-run.sh` fallback to use `scripts/validate-operator-env.py`
  when a downstream repo does not have `template-repo/scripts`.

## Verification

- `python3 template-repo/scripts/factory-launcher.py --mode greenfield --project-name "Canonical Root Smoke" --project-slug canonical-root-smoke --route-only`
  reports target `/projects/canonical-root-smoke`.
- `python3 template-repo/scripts/first-project-wizard.py --template-repo-root template-repo --project-base /tmp/factory-project-base-smoke --route-only`
  reports target under the explicit base.
- Downstream `bash scripts/deploy-dry-run.sh` passes in `/projects/health-sync-bridge`.

