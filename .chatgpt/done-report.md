# Итоговый отчёт по закрытию изменения

## Что было запрошено
- Закрепить правило, что при отсутствии `## Инструкция пользователю` финальный ответ должен явно говорить: внешних действий не требуется.

## Что реально сделано
- Обновлен `template-repo/scenario-pack/16-done-closeout.md`.
- Обновлен `template-repo/process/definition-of-done.bugfix-feature-change.md`.
- Синхронизированы generated guidance и validator:
  - `template-repo/scripts/create-codex-task-pack.py`
  - `template-repo/scripts/validate-codex-task-pack.py`
  - `.chatgpt/boundary-actions.md`
  - `.chatgpt/done-checklist.md`

## Какие артефакты обновлены
- `template-repo/scenario-pack/16-done-closeout.md`
- `template-repo/process/definition-of-done.bugfix-feature-change.md`
- `template-repo/scripts/create-codex-task-pack.py`
- `template-repo/scripts/validate-codex-task-pack.py`
- `.chatgpt/boundary-actions.md`
- `.chatgpt/done-checklist.md`
- `.chatgpt/task-index.yaml`
- `.chatgpt/codex-input.md`
- `.chatgpt/verification-report.md`
- `.chatgpt/done-report.md`

## Что осталось вне объёма
- Автоматическая проверка самого финального assistant text вне текущего static guidance/validator слоя.

## Итог закрытия
- Если внешний шаг есть, финал должен содержать `## Инструкция пользователю`.
- Если внешнего шага нет, финал должен прямо сказать, что внешних действий не требуется.
