# Codex handoff input

## Контекст
- Repo: `factory-template`
- Изменение уровня factory-template, а не project-only.
- Нужно встроить automation для verified sync и отдельного release contour без перехода к always-auto-release.

## Что должен сделать исполнитель
- Добавить reusable automation scripts и validators.
- Сохранить verify-first модель и отдельный release decision.
- Обновить runbook, AGENTS, functional state и change artifacts.

## Ограничения
- Git operations только последовательно.
- Без silent partial success.
- Без публикации release при failed verify.
- Без хранения секретов в repo.
