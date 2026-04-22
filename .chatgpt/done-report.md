# Итоговый отчёт по закрытию изменения

## Что было запрошено
- Оформить отдельный bug report на verified-sync process miss со stale commit message.
- Исправить automation layer, чтобы post-done non-lightweight diff не мог использовать metadata от предыдущего change.

## Что реально сделано
- Создан bug report `reports/bugs/bug-014-verified-sync-stale-task-index-commit-message.md`.
- Создан factory feedback `reports/factory-feedback/feedback-014-verified-sync-stale-task-index-commit-message.md`.
- В `template-repo/scripts/factory_automation_common.py` добавлен guard для post-done non-lightweight verified sync:
  - если новый diff не является lightweight follow-up;
  - и stage уже `done`;
  - и `.chatgpt/task-index.yaml` не обновлен;
  - verified sync prereqs завершаются blocker'ом вместо использования stale commit metadata.
- Текущие `.chatgpt` artifacts обновлены под новый change, чтобы sync path мог фиксировать корректный `change.title`.

## Какие артефакты обновлены
- `template-repo/scripts/factory_automation_common.py`
- `reports/bugs/bug-014-verified-sync-stale-task-index-commit-message.md`
- `reports/factory-feedback/feedback-014-verified-sync-stale-task-index-commit-message.md`
- `.chatgpt/task-index.yaml`
- `.chatgpt/codex-input.md`
- `.chatgpt/verification-report.md`
- `.chatgpt/done-report.md`

## Что осталось вне объёма
- Более глубокая автоматическая синхронизация всех `.chatgpt` task artifacts при каждом new internal follow-up без отдельного refresh.

## Итог закрытия
- Verified-sync больше не должен silently re-use stale task metadata для нового post-done non-lightweight change.
- Вместо неверного commit message оператор получает явный blocker и обязан сначала обновить task metadata под новый change.
