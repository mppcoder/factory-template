# Feature execution lite gap

Дата: `2026-04-27`

## Кратко

В `factory-template` уже есть lightweight feature planning и traceability, но нет отдельного optional advanced path для выполнения фичи волнами с checkpoint/resume, decisions journal, reviewer/audit hints и финальной верификацией перед закрытием.

## Evidence

- `docs/feature-execution-lite.md` отсутствует.
- `template-repo/template/work-templates/execution-plan.md.template` отсутствует.
- `template-repo/template/work-templates/checkpoint.yaml.template` отсутствует.
- `template-repo/scripts/validate-feature-execution-lite.py` отсутствует.
- `template-repo/scripts/init-feature-workspace.sh` создаёт beginner workspace, но не умеет включать advanced execution artifacts отдельным флагом.

## Layer classification

- `template/process-layer`
- `work-templates`
- `validator/verify-layer`
- `docs`

## Impact

Без отдельного advanced path команда может преждевременно закрыть feature work без checkpoint, decisions и финальной verification evidence. Это повторяет полевые классы сбоев: premature closeout, evidence overclaim, generated tooling mismatch и смешение internal work / external user action / runtime backlog.

## Scope decision

`fixed-in-current-scope`.

Текущий handoff прямо требует добавить feature-execution-lite, шаблоны, validator и quick/ci verification. Отдельный task launch не нужен: профиль, сценарий и reasoning совпадают с текущей задачей.

## Remediation plan

- Добавить русскоязычную документацию `docs/feature-execution-lite.md`.
- Добавить readable templates для `execution-plan.md`, `checkpoint.yaml` и расширить task/decisions templates.
- Добавить `validate-feature-execution-lite.py`.
- Подключить validator к `verify-all.sh quick` так, чтобы starter path не требовал advanced workspace.
- Добавить `--advanced-execution` в `init-feature-workspace.sh`.
- Обновить `TEST_REPORT.md` и `CURRENT_FUNCTIONAL_STATE.md`.
