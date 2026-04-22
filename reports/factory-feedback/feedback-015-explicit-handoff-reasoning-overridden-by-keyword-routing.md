# Factory Feedback: explicit handoff routing can still be downgraded by keyword fallback

## Исходный bug report
`reports/bugs/bug-015-explicit-handoff-reasoning-overridden-by-keyword-routing.md`

## Почему это проблема фабрики
Фабрика уже различает advisory handoff layer и executable launch boundary, но router всё ещё мог проигнорировать explicit routing fields из structured handoff и пересчитать profile/reasoning только по keyword match. Это ломает доверие к нормализованному handoff и может понизить reasoning effort именно там, где handoff требовал deep/high route.

## Где проявилось
`factory-template`, handoff bootstrap и route resolution для нового Codex task launch.

## Повторяемый паттерн
- ChatGPT/оператор передаёт structured handoff с explicit `selected_*` полями;
- requested profile может не совпадать с локальным executable profile vocabulary;
- router не пытается подобрать совместимый executable profile по explicit reasoning/model;
- keyword fallback выбирает `build/medium`;
- generated task artifacts расходятся с source handoff.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- executable router
- handoff bootstrap
- `.chatgpt/task-launch.yaml`
- normalized handoff artifacts
- routing trust boundary

## Как проверить исправление
1. Передать router'у structured handoff с `selected_reasoning_effort: high`.
2. Убедиться, что explicit route не теряется в `.chatgpt/task-launch.yaml`.
3. Если requested profile не существует в routing spec, router выбирает совместимый executable profile и сохраняет `high` reasoning.
4. Generated `launch_command` соответствует выбранному executable profile, а не keyword fallback downgrade.

## Статус
зафиксировано
