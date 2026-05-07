# Factory feedback 058: Persist latest GitHub Actions status

Дата: 2026-05-07

Reusable defect: repo-first GitHub triage can report no Issues/PRs while missing failing Actions because status is only visible in GitHub runtime UI/API.

Factory rule:
- factory repos with GitHub Actions need a repo-local latest observed Actions status report;
- report generation must use GitHub connector or authenticated `gh`, not public URL fallback;
- validators should check report shape and explicit blocker wording when Actions status cannot be read.

Evidence:
- `reports/bugs/2026-05-07-github-actions-status-artifact-gap.md`
- `reports/ci/latest-actions-status.md`
- `template-repo/scripts/validate-github-actions-status.py`
