# Factory Feedback: structured handoff parser must tolerate markdown heading before YAML block

## Исходный bug report
`reports/bugs/bug-019-structured-handoff-yaml-block-not-parsed.md`

## Почему это проблема фабрики
Фабрика опирается на normal user-facing handoff documents, где routing metadata часто идет внутри markdown документа, а не как "чистый YAML файл". Если executable parser не умеет корректно прочитать YAML block после heading, explicit routing intent silently теряется и bootstrap пишет fallback metadata. Это reusable defect source-of-truth parser layer.

## Где проявилось
`factory-template`, `template-repo/scripts/codex_task_router.py` и generated launch artifacts.

## Повторяемый паттерн
- handoff оформлен как нормальный markdown document;
- routing fields записаны структурированным YAML block в начале документа;
- parser не извлекает block целиком;
- часть explicit overrides теряется;
- generated task-launch/handoff artifacts расходятся с исходным handoff.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- executable parser for structured handoff
- bootstrap / route resolution
- `.chatgpt/task-launch.yaml`
- normalized handoff generation

## Как проверить исправление
1. Передать router'у markdown handoff, где YAML block расположен после heading.
2. Убедиться, что parser извлекает весь YAML block, включая list fields.
3. Проверить, что `.chatgpt/task-launch.yaml` сохраняет explicit `artifacts_to_update`, `handoff_allowed` и другие overrides без fallback drift.
4. Повторно прогнать handoff/task-pack validators и убедиться, что generated artifacts согласованы.

## Статус
зафиксировано
