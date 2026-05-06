# Bug: untracked runtime env was present inside repo directory

Date: 2026-05-06
Status: remediated by operator before implementation continued

## Summary

During Stage 0 of the VPS project hosting topology work, an untracked `deploy/.env` file was physically present inside the repo directory. The file was ignored by Git and not tracked, but its location still violated the `secrets outside repo` boundary for this task.

No secret values were reproduced in this report.

## Evidence

- `git ls-files deploy/.env deploy/.env.example` showed only `deploy/.env.example`.
- `deploy/.env` existed in the working tree during the first Stage 0 check.
- Work stopped under the security stop rule.
- The operator later confirmed that real env was moved outside repo to `/etc/factory-template/deploy.env`, permissions were set to `root:root` and `chmod 600`, and `deploy/.env` was removed.

## Layer classification

- Layer: runtime env / operator VPS boundary.
- Defect class: incidental security boundary violation.
- Owner boundary: mixed.
  - Repo standard must forbid real env inside repo paths and provide validators.
  - Operator owns real env creation and secret values outside repo.

## Impact

- Even ignored env files can be accidentally read, copied into transcripts or included in ad hoc archives.
- Repo-first implementation must not depend on real env files inside `deploy/`.

## Remediation

- The operator moved the real env outside repo.
- This implementation adds secret-boundary documentation and `scripts/validators/validate-project-secrets-boundary.sh`.

## Verification

- Before continuing, `git status --short --branch` was clean against `origin/main`.
- `git ls-files deploy/.env deploy/.env.example` showed only `deploy/.env.example`.
- `deploy/.env` was absent.
