# Factory Feedback / Обратная связь по фабрике

## Исходный bug report
- `reports/bugs/bug-025-resumable-planning-scenario-gap.md`

## Почему это проблема фабрики
Сценарный идентификатор handoff может уйти вперед относительно materialized файлов в `scenario-pack`, что ухудшает воспроизводимость repo-first маршрута.

## Где проявилось
- canonical repo: `factory-template`
- контур: release-2.5 / track-b / beginner-first planning remediation

## Повторяемый паттерн
При появлении нового route-name в handoff без синхронного добавления materialized path оператору приходится вручную сопоставлять сценарии.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- scenario-pack
- docs
- handoff naming conventions

## Как проверить исправление
1. Выбрать новый named scenario для handoff.
2. Проверить, что путь materialized в `template-repo/scenario-pack` (или есть зафиксированный alias map).
3. Убедиться, что router/readme не требуют ручной догадки при первом шаге.
