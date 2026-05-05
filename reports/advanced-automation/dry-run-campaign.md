# Кампания dry-run advanced automation

Дата: 2026-05-05

| Component | Evidence | Status |
|---|---|---|
| issue gate | `issue-autofix-smoke.py`, negative fixtures | dry-run covered |
| issue handoff renderer | synthetic `codex-input.md` in temp dir | dry-run covered |
| bounded runner | `bounded-task-runner.py --dry-run` | dry-run covered |
| task registry | Universal Task Control smoke | covered |
| task queue | `render-task-queue.py` smoke | covered |
| curator proposal | `factory-curator.py`, promotion fixture | covered |
| workflow spec | `validate-symphony-workflow.py` | covered |
| automation gates | `validate-advanced-automation-gates.py` | covered |
| audit ledger | `validate-automation-run-ledger.py` | covered |
| rollback plan | `validate-automation-rollback.py` | covered |
| downstream generated smoke | `downstream-task-control-materialization-smoke` | covered |

Safety campaign boundaries:
- no live mutation;
- no secrets;
- no auto-merge;
- no deployment.
