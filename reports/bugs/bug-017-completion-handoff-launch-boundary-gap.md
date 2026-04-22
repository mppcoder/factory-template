# Отчет о дефекте

## Идентификатор
bug-017-completion-handoff-launch-boundary-gap

## Краткий заголовок
Completion/handoff layer смешивал advisory и executable routing: пользователю выдавался handoff-текст без обязательного launch boundary, из-за чего новый случайный Codex chat не менял profile/model/reasoning предсказуемо.

## Где найдено
Repo: `factory-template`, routing / completion / handoff layer:

- `template-repo/codex-routing.yaml`
- `template-repo/scripts/launch-codex-task.sh`
- `template-repo/scripts/bootstrap-codex-task.py`
- `template-repo/scripts/codex_task_router.py`
- `template-repo/scripts/create-codex-task-pack.py`
- `template-repo/scripts/validate-codex-routing.py`
- `template-repo/scripts/validate-codex-task-pack.py`
- `template-repo/scripts/validate-handoff-response-format.py`
- `template-repo/scenario-pack/00-master-router.md`
- `template-repo/scenario-pack/15-handoff-to-codex.md`

## Шаги воспроизведения
1. Сгенерировать handoff/completion package для задачи с `handoff_allowed=yes`.
2. Открыть новый или случайный Codex chat без явного launcher path.
3. Вставить только handoff-текст из generated response.
4. Проверить, что route в live Codex не обязан совпасть с ожидаемым `selected_profile/model/reasoning`, потому что executable switch не был выполнен.

## Ожидаемое поведение
- Handoff/completion package должен явно разделять advisory text и executable launch boundary.
- При `handoff_allowed=yes` пользователь должен получить не только handoff text, но и явную launch-инструкцию / launch command.
- `selected_profile` должен быть явно привязан к launcher path, а `selected_model` / `selected_reasoning_effort` не должны описываться как auto-switch от текста handoff.
- Должен существовать troubleshooting path для sticky last-used profile/reasoning state.

## Фактическое поведение
- Generated `handoff-response.md` давал только handoff block без отдельного launch block.
- `launch_command` в routing artifacts описывал внутренний `codex --profile ...`, но user-facing completion layer не заставлял пройти через новый task launch boundary.
- Source-facing docs местами продолжали формулировать canonical next step как "новый Codex task/chat", что смешивало новый чат и новый task launch.
- Валидаторы не проверяли, что handoff package содержит явный launch command и что docs не обещают auto-switch внутри уже открытой сессии.

## Evidence
- [PROJECT] `codex --help` в этой среде подтверждает явные executable switches `--profile` и `--model`.
- [PROJECT] `codex debug models` в этой среде подтверждает live catalog c `gpt-5.4` и `gpt-5.4-mini`, но это не меняет профиль/режим само по себе без launcher boundary.
- [PROJECT] До исправления `.chatgpt/handoff-response.md` содержал только `## Handoff в Codex` и не требовал отдельный launch step.
- [PROJECT] До исправления `template-repo/scripts/create-codex-task-pack.py` генерировал пользовательскую инструкцию "использовать подготовленный handoff-блок выше", без обязательного launch command.
- [PROJECT] До исправления source docs использовали формулировки уровня "новый Codex task/chat" без явной привязки к launcher command.

## Затронутый слой
factory-template

## Нужен ли feedback в фабрику
Да, это reusable defect source-of-truth шаблона: downstream guidance и generated completion package могли создавать ложное ожидание, что новый чат сам переключит route.

## Статус
зафиксировано
