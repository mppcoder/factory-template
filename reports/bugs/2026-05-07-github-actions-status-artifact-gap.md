# Bug: GitHub Actions latest status was not persisted repo-first

Дата: 2026-05-07

## Симптом
GitHub Issues and PRs were empty, but GitHub Actions had failing `CI` runs. The repo had `.github/workflows/ci.yml`, yet no repo-local latest Actions status artifact made that failure visible to the lifecycle dashboard or release evidence.

## Root cause
Actions status lived only in GitHub runtime state. Existing repo validators checked workflow structure and local verification, but did not require a persisted status readout for the latest observed authenticated GitHub Actions run.

## Remediation
- Added `template-repo/scripts/render-github-actions-status.py` to render `reports/ci/latest-actions-status.md` via authenticated `gh`.
- Added `template-repo/scripts/validate-github-actions-status.py`.
- Added the validator to `template-repo/scripts/verify-all.sh quick`.
- Captured the latest failing `CI` run and its job-level status in `reports/ci/latest-actions-status.md`.

## Boundary
The committed report records the latest run observed at render time. A commit that updates the report can trigger a newer run, so closeout must still check `gh run list` before final sync status.
