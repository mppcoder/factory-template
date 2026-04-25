# Completed change: GitHub Actions workflow dependency backlog

## Summary
- Consolidated the stale Dependabot workflow action backlog into one human-owned remediation branch.
- Updated `.github/workflows/ci.yml` and `.github/workflows/release.yml` coherently:
  - `actions/checkout@v6`
  - `actions/setup-python@v6`
  - `actions/upload-artifact@v7`
- Classified PR #1, PR #2, and PR #3 as stale PR backlog over an already-fixed verify baseline, not three independent merge tasks.

## Verification
- `bash template-repo/scripts/verify-all.sh ci` passed before remediation on current main.
- `bash EXAMPLES_TEST.sh` passed, including `validate-versioning-layer.py`.
- Release bundle dry-run path produced a non-empty zip artifact.
- `bash template-repo/scripts/verify-all.sh ci` passed after remediation.

## Follow-up
- Publish one consolidated PR.
- Close or supersede PR #1, PR #2, and PR #3 after the consolidated PR is available.
