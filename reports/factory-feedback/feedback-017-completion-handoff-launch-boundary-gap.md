# Factory Feedback: completion/handoff must expose an executable launch boundary

## Исходный bug report
`reports/bugs/bug-017-completion-handoff-launch-boundary-gap.md`

## Почему это проблема фабрики
Фабрика уже различала advisory и executable routing на уровне сценариев, но completion/handoff layer все еще мог отдать пользователю только handoff-текст. Это создавало ложное ожидание, что "новый чат Codex" или простая вставка handoff сами по себе переключат profile/model/reasoning.

## Где проявилось
`factory-template`, source-of-truth routing docs, launcher artifacts и generated `.chatgpt` completion package.

## Повторяемый паттерн
- handoff уже разрешен;
- generated package пишет `selected_profile/model/reasoning`;
- user открывает новый или случайный Codex chat без explicit launch path;
- handoff вставляется как advisory text;
- live session может остаться на sticky last-used route;
- repo выглядит так, будто проблема в модели, а не в пропущенной executable boundary.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- executable routing contract
- launcher / bootstrap / routing record
- generated handoff-response and boundary-actions
- handoff-response validator
- routing validator
- source-facing scenario docs и runbooks

## Как проверить исправление
1. Сгенерировать `.chatgpt/handoff-response.md` и убедиться, что там есть отдельный `## Launch в Codex` с executable launch command.
2. Проверить, что `.chatgpt/task-launch.yaml` содержит `launch_command`, `launch_artifact_path` и `codex_profile_command`.
3. Проверить, что handoff-response и normalized handoff прямо говорят: advisory text не переключает route, надежная единица — новый task launch.
4. Проверить наличие troubleshooting для sticky last-used state.
5. Проверить `validate-codex-routing.py`, что profile существует в routing spec, а model/reasoning сверяются с live `codex debug models`.

## Статус
зафиксировано
