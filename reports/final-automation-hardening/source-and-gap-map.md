# Карта source и gap

Дата: 2026-05-05

## Карта источников

- advanced automation substrate: `.github/workflows/issue-autofix.yml`, `template-repo/scripts/issue-autofix-gate.py`, `template-repo/scripts/create-issue-codex-handoff.py`, `template-repo/scripts/run-issue-autofix.sh`;
- bounded runner: `template-repo/scripts/bounded-task-runner.py`, `docs/operator/factory-template/bounded-runner.md`;
- workflow spec: `WORKFLOW.md`, `docs/operator/factory-template/symphony-compatible-workflow.md`;
- curator: `template-repo/scripts/factory-curator.py`, `docs/operator/factory-template/factory-curator.md`;
- downstream materialization: `template-repo/template/.github/workflows/issue-autofix.yml`, `template-repo/template/docs/operator/*`, generated-project smoke in `verify-all quick`;
- release state: `RELEASE_NOTES.md`, `reports/advanced-automation/final-readout.md`, `reports/advanced-automation/release-readiness.md`.

## Классификация gaps

| Gap | Class | Resolution |
|---|---|---|
| Synthetic issue-autofix proof was not fixture-driven | internal | Added positive/negative fixtures and `issue-autofix-smoke.py`. |
| Label/trust model was documented but not cross-validated | internal | Added permission model docs and label validator. |
| Parallel runner refusal needed explicit worktree policy | internal | Added root/template worktree isolation policy and validator. |
| Automation runs needed a durable dry-run audit trail | internal | Added append-only ledger helper, docs and validator. |
| Rollback policy needed operator-ready recovery path | internal | Added root/template rollback docs and dry-run helper. |
| Curator promotion path needed review-gated FT-TASK draft | internal | Added promotion docs, fixture and conversion helper. |
| Real release approval/deploy remains human boundary | external | Not required for current closeout. |
| Full autonomous mode | not-needed | Remains disabled by default. |

Internal gaps are included in this continuous hardening scope.
