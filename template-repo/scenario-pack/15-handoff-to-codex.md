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
- явную launch-инструкцию и launch command для нового task launch, если handoff отдается пользователю;
- границы scope и что не делать;
- список обязательных артефактов и файлов для обновления;
- verify expectations;
- риски и ограничения;
- указание, нужен ли defect/factory feedback follow-up.

## Нормализованные routing fields
Для любого handoff или self-handoff дополнительно фиксируй:
- `launch_source`: `chatgpt-handoff` или `direct-task`;
- `task_class`: `quick` / `build` / `deep` / `review`;
- `selected_profile`;
- `selected_model`;
- `selected_reasoning_effort`;
- `project_profile`;
- `selected_scenario`;
- `pipeline_stage`;
- `artifacts_to_update`;
- `handoff_allowed`;
- `defect_capture_path`.

Эти поля являются общим стандартом и для ChatGPT Project handoff, и для direct Codex self-handoff.
При этом `selected_profile` — исполнимая граница маршрутизации, а `selected_model` / `selected_reasoning_effort` описывают ожидаемую конфигурацию выбранного profile. Advisory или handoff text сами по себе не выполняют switch.

## Handoff для incidental defect
Если в ходе основного task найден unresolved incidental bug, handoff-пакет должен включать:
- краткий bug report summary;
- scope decision: `fixed-in-current-scope` / `continue-in-current-route` / `separate-task-required` / `deep-research-required`;
- route comparison: совпадает ли новый route с текущим live task;
- явное пояснение, что advisory layer не переключает текущую открытую сессию и что надежная единица routing — новый task launch;
- если route изменился, один цельный ready-to-copy handoff block для нового Codex task как канонический вариант и отдельный явный launch command;
- если route не изменился, явную формулировку, что продолжение в текущем chat допустимо только после self-handoff;
- если нужен research path, ChatGPT-ready bug report/prompt вместо implementation handoff.

Для user-facing формулировок используй три явных режима:
- `Продолжить в этом чате на текущем route` — только если self-handoff подтвердил тот же profile/model/reasoning;
- `Рекомендуемый путь: новый task launch / новая Codex chat-сессия через launch command` — если route отличается;
- `Нужен deep research` — если без отдельного исследования remediation сейчас ненадежен.

## Troubleshooting sticky state
- Если пользователь просто вставил handoff в случайную или уже открытую Codex-сессию, route может остаться на last-used profile/model/reasoning.
- В таком случае канонический next step: закрыть текущую сессию, выполнить launch command из handoff package и только потом вставить handoff.
- Если новый launch все еще выглядит stale, проверить local named profile и сверить `selected_model` с live `codex debug models`.

## После handoff
Если remaining work еще внутренний и Codex-eligible, handoff должен быть выдан раньше любого user footer.

Если handoff выдается в ответ пользователю, это должен быть ровно один блок. Все дополнительные пояснения по внешним шагам допускаются только после него в `## Инструкция пользователю`, но не в виде второго handoff-блока.

Сразу после handoff, если дальше нужен внешний шаг пользователя, возврат в ChatGPT Project, внешнее действие или ожидание внешнего артефакта, добавь финальный раздел `## Инструкция пользователю`.

Если внешний шаг связан с обновлением repo-first инструкций или downstream sync flows, `## Инструкция пользователю` должен содержать completion package со следующими блоками:
- `Что изменено`
- `Какие файлы обновлены в repo`
- `Нужно ли обновлять repo-first инструкцию factory-template ChatGPT Project`
- `Нужно ли обновлять downstream template in battle repos`
- `Нужно ли обновлять repo-first инструкции battle ChatGPT Projects`
- `Готовые артефакты для скачивания`
- `Команды/скрипты для repo-level sync`
- `Удалить перед заменой`
- `Пошаговая инструкция по окнам`
- `Что прислать обратно после внешнего шага`

Внутренние prepare-команды для такого completion package Codex должен по умолчанию выполнить сам до финального ответа. Не проси пользователя запускать внутренние repo-команды, если можно просто передать готовые артефакты и точный текст repo-first инструкции.
