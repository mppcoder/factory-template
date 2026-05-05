# Downstream materialization / материализация

Дата: 2026-05-05

## Что материализуется

| Artifact | Factory source | Generated path |
|---|---|---|
| Issue autofix workflow | `.github/workflows/issue-autofix.yml` | `.github/workflows/issue-autofix.yml` from `template-repo/template` |
| Issue forms | `.github/ISSUE_TEMPLATE/*.yml` | `.github/ISSUE_TEMPLATE/*.yml` |
| Support docs | `docs/support-automation.md` | `docs/support-automation.md` |
| Security boundary | `template-repo/template/SECURITY.md` | `SECURITY.md` |
| Workflow spec | `WORKFLOW.md` | `WORKFLOW.md` |
| Runner docs | `docs/operator/factory-template/bounded-runner.md` | `docs/operator/bounded-runner.md` |
| Curator docs | `template-repo/template/docs/operator/factory-curator.md` | `docs/operator/factory-curator.md` |
| Advanced gates | `template-repo/template/docs/operator/full-advanced-automation-gates.md` | `docs/operator/full-advanced-automation-gates.md` |
| Scripts | `template-repo/scripts/*` | `scripts/*` copied by launcher |

## Smoke evidence / подтверждение

`bash template-repo/scripts/verify-all.sh quick` generated a temporary project and verified:

- `.github/workflows/issue-autofix.yml`;
- required issue forms;
- `docs/support-automation.md`;
- `SECURITY.md`;
- `WORKFLOW.md`;
- bounded runner, curator and advanced gates docs;
- Universal Task Control still works through allocate -> preview -> prepare pack -> `ready_for_codex` -> queue -> dashboard validation.

## Boundaries / границы

- No GitHub API call was made by downstream smoke.
- No Codex child session was launched.
- No live labels/issues were mutated.
- No factory-only `template-repo/scripts` path is required by generated workflow; it falls back to root `scripts`.
