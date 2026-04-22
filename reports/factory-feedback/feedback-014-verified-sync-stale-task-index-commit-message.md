# Factory Feedback: verified sync can reuse stale task metadata after done-stage

## Исходный bug report
`reports/bugs/bug-014-verified-sync-stale-task-index-commit-message.md`

## Почему это проблема фабрики
Фабрика уже требует честный verified sync и различает lightweight follow-up от full cycle. Но post-done non-lightweight diff всё ещё мог пройти в full mode на metadata предыдущего change, если `.chatgpt/task-index.yaml` не был обновлен. Это создаёт риск коммита и push с неправильным `change_id`, `title` и commit message.

## Где проявилось
`factory-template`, verified-sync closeout после отдельного internal follow-up change.

## Повторяемый паттерн
- предыдущий change уже закрылся и оставил `stage.current = done`;
- новый diff не является lightweight follow-up;
- `.chatgpt/task-index.yaml` остаётся от прошлого change;
- verified-sync использует stale `task-index` как будто это metadata текущего change;
- commit message и sync report получают неверный intent.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- verified-sync automation
- task metadata freshness
- closeout safety
- commit intent integrity

## Как проверить исправление
1. В состоянии `stage.current = done` создать новый non-lightweight diff без обновления `.chatgpt/task-index.yaml`.
2. Запустить `bash VALIDATE_VERIFIED_SYNC_PREREQS.sh`.
3. Убедиться, что скрипт падает с явным сообщением про обязательное обновление `task-index.yaml`, а не печатает stale commit message.
4. После обновления `task-index.yaml` или перевода diff в допустимый lightweight path prereqs должны снова проходить.

## Статус
зафиксировано
