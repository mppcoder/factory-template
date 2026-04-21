# Codex handoff input

## Контекст
- Repo: `factory-template`
- Изменение уровня factory-template, а не project-only.
- Нужно дожать verified sync так, чтобы low-risk post-verify follow-up cleanup тоже auto commit/push без отдельного ручного запроса.

## Что должен сделать исполнитель
- Добавить lightweight follow-up mode в `VERIFIED_SYNC.sh` и его validator.
- Сохранить verify-first модель и отдельный release contour без изменений.
- Обновить runbook, AGENTS, functional state, changelog и closeout artifacts.

## Ограничения
- Git operations только последовательно.
- Без silent partial success.
- Без ослабления verify для non-lightweight diff.
- Без хранения секретов в repo.
