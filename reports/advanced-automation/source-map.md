# Advanced automation source map / карта источников

Дата: 2026-05-05

## Baseline 1-4 / исходная готовность

- Universal Task Control is present through `template-repo/template/.chatgpt/task-registry.yaml`, task scripts, dashboard integration and `reports/universal-task-control-final-readout.md`.
- Downstream materialization is present through `template-repo/launcher.sh`, copied `scripts/*`, generated `.github/ISSUE_TEMPLATE/*.yml`, `docs/operator/universal-task-control.md` and `reports/downstream-materialization/smoke-report.md`.
- Current task queue has no open real tasks: `reports/task-queue.md` reports `open_tasks: 0`.

## Source map for 5-8 / карта источников

| Area | Current source | New target |
|---|---|---|
| GitHub Issue dispatcher | root issue forms and Universal Task Control issue bridge | `.github/workflows/issue-autofix.yml`, gate/renderer/runner scripts |
| Gate | `issue-to-task-registry.py` secret-like boundary | `issue-autofix-gate.py` |
| Normalized handoff | `task-to-codex-handoff.py` | `create-issue-codex-handoff.py` |
| Bounded runner | launcher/profile scripts | `run-issue-autofix.sh`, `bounded-task-runner.py` |
| Dashboard/readout | `reports/task-queue.md`, lifecycle dashboard | run yaml, advanced automation reports |
| Downstream propagation | `template-repo/template`, `launcher.sh` | downstream workflows, forms, support docs, `WORKFLOW.md`, `SECURITY.md` |
| Symphony-compatible spec | advisory scenario routing | root/template `WORKFLOW.md` and operator spec |
| Curator | backlog/readout artifacts | `factory-curator.py`, `reports/curator/*` |
| Advanced gates | future boundary notes | full advanced automation gates docs and validators |

## Gaps closed by this scope / закрытые gaps

- no root issue-autofix workflow before M1;
- no bounded issue gate before M1;
- no Symphony-compatible written workflow contract before M2;
- no bounded runner skeleton before M3;
- no repo-reviewed curator proposal loop before M4;
- no full automation refusal gate document before M5.
