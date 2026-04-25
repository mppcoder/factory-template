# Завершенное изменение: closeout boundary и русскоязычный слой

## Кратко
- Зафиксированы два process defects:
  - `bug-029-github-pr-merge-misclassified-as-user-step`;
  - `bug-030-human-readable-language-layer-leaked-english`.
- Closeout rules теперь требуют проверять доступный GitHub write path перед тем, как просить пользователя выполнить PR merge.
- Global/handoff/closeout rules теперь явно требуют русский язык для человекочитаемых ответов, инструкций, отчетов и generated guidance.
- User-facing output `validate-operator-env.py` русифицирован в рамках language-layer fix.

## Измененные зоны
- `template-repo/scenario-pack/00-master-router.md`
- `template-repo/scenario-pack/01-global-rules.md`
- `template-repo/scenario-pack/15-handoff-to-codex.md`
- `template-repo/scenario-pack/16-done-closeout.md`
- `template-repo/scripts/create-codex-task-pack.py`
- `template-repo/scripts/bootstrap-codex-task.py`
- `template-repo/scripts/codex_task_router.py`
- `template-repo/scripts/deploy-dry-run.sh`
- `template-repo/scripts/validate-codex-routing.py`
- `template-repo/scripts/validate-codex-task-pack.py`
- `template-repo/scripts/validate-handoff-response-format.py`
- `template-repo/scripts/validate-operator-env.py`
- `template-repo/codex-routing.yaml`
- `.chatgpt/boundary-actions.md`
- `reports/bugs/*`
- `reports/factory-feedback/*`

## Проверка
- Дефекты оформлены в `reports/bugs`.
- Reusable feedback оформлен в `reports/factory-feedback`.
- Текущие closeout artifacts переведены на русский человекочитаемый текст.
- `bash template-repo/scripts/verify-all.sh quick` проходит.
