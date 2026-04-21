# Передача в Codex (handoff)

Перед handoff проверь:
- готов ли `codex-input.md`;
- заполнен ли `evidence-register.md`;
- закрыт ли `codex_handoff_allowed` в `stage-state.yaml`;
- валиден ли `task-index.yaml`.

## Обязательное правило inline handoff
Если handoff уже допустим и задача достаточно определена, handoff нужно выдать в том же ответе. Нельзя останавливаться на аналитике, если change-class требует handoff или если optional handoff уже безопасно нормализуется.

Handoff пользователю нужно выдавать только как один цельный блок для copy-paste в Codex. Нельзя заменять его ссылкой на файл, набором отдельных фрагментов, несколькими handoff-блоками или формулой "возьми данные из `codex-task-pack.md` / `codex-input.md`".

Post-remediation follow-up handoff тоже является нормальным и обязательным handoff case, если remaining work еще остается внутренней Codex-eligible работой repo.

Допустимые типы такого handoff включают:
- `release-followup`
- `closeout-sync`
- `release-facing-consistency`
- `source-pack-refresh`
- `export-refresh`

Допустимые причины отложить handoff:
- обязательные gate'ы еще не закрыты;
- не хватает обязательных артефактов;
- задача остается реально неоднозначной;
- нужен выбор архитектурной развилки.

## Минимальная структура handoff-блока
Готовый handoff в Codex должен как минимум содержать:
- цель изменения;
- явное правило, что в рамках этого repo приоритет у repo rules, AGENTS, runbook и policy files репозитория; общие рабочие инструкции применяются только там, где не противоречат правилам repo и старшим системным ограничениям среды;
- границы scope и что не делать;
- список обязательных артефактов и файлов для обновления;
- verify expectations;
- риски и ограничения;
- указание, нужен ли defect/factory feedback follow-up.

## После handoff
Если remaining work еще внутренний и Codex-eligible, handoff должен быть выдан раньше любого user footer.

Если handoff выдается в ответ пользователю, это должен быть ровно один блок. Все дополнительные пояснения по внешним шагам допускаются только после него в `## Инструкция пользователю`, но не в виде второго handoff-блока.

Сразу после handoff, если дальше нужен внешний шаг пользователя, возврат в ChatGPT Project, внешнее действие или ожидание внешнего артефакта, добавь финальный раздел `## Инструкция пользователю`.

Если внешний шаг связан с source update flows, `## Инструкция пользователю` должен содержать completion package со следующими блоками:
- `Что изменено`
- `Какие файлы обновлены в repo`
- `Нужно ли обновлять Sources factory-template ChatGPT Project`
- `Нужно ли обновлять downstream template in battle repos`
- `Нужно ли обновлять Sources battle ChatGPT Projects`
- `Готовые артефакты для скачивания`
- `Команды/скрипты для repo-level sync`
- `Удалить перед заменой`
- `Пошаговая инструкция по окнам`
- `Что прислать обратно после внешнего шага`

Внутренние prepare-команды для такого completion package Codex должен по умолчанию выполнить сам до финального ответа. Не проси пользователя запускать `EXPORT_FACTORY_TEMPLATE_SOURCES.sh`, `GENERATE_BOUNDARY_ACTIONS.sh` или аналогичные внутренние repo-команды, если можно просто передать готовые артефакты и внешний upload/replace flow.

Если change использует repo-side sync в dedicated Google Drive folder, это тоже внутренний prepare/sync step:

- Codex сам выполняет export и connector sync request/report preparation;
- в completion package передаются уже готовые report paths и итог статусов `create/update/delete/skipped`;
- это не должно формулироваться как обещание автоматического refresh Sources внутри ChatGPT Project UI.
