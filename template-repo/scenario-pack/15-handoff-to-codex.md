# Передача в Codex (handoff)

Перед handoff проверь:
- готов ли `codex-input.md`;
- заполнен ли `evidence-register.md`;
- закрыт ли `codex_handoff_allowed` в `stage-state.yaml`;
- валиден ли `task-index.yaml`.

## Обязательное правило inline handoff
Если handoff уже допустим и задача достаточно определена, handoff нужно выдать в том же ответе. Нельзя останавливаться на аналитике, если change-class требует handoff или если optional handoff уже безопасно нормализуется.

Handoff пользователю нужно выдавать только как один цельный блок для вставки в Codex. Нельзя заменять его ссылкой на файл, набором отдельных фрагментов, несколькими handoff-блоками или формулой "возьми данные из `codex-task-pack.md` / `codex-input.md`".

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
- `apply_mode: manual-ui (default)` для интерактивного VS Code Codex extension workflow;
- короткую manual UI apply-инструкцию: открыть новое окно/чат Codex, вручную выбрать `selected_model` и `selected_reasoning_effort` в picker, затем вставить handoff;
- явную оговорку, что уже открытая live session не является надежным auto-switch механизмом и что "новый чат + вставка handoff" не равны executable launch path;
- `strict_launch_mode: optional` и launch command как дополнительный strict block для automation / reproducibility / shell-first / scripted launch;
- границы scope и что не делать;
- список обязательных артефактов и файлов для обновления;
- verify expectations;
- риски и ограничения;
- указание, нужен ли defect/factory feedback follow-up.

Человекочитаемые пояснения в handoff, self-handoff и completion package для `factory-template` пишутся на русском языке. Технические ключи вроде `selected_profile`, `apply_mode`, `strict_launch_mode`, имена команд, файлов и literal values допускаются как идентификаторы, но описательные заголовки и инструкции должны быть русскоязычными.

Каждый copy-paste handoff в Codex обязан явно содержать строку `Язык ответа Codex: русский` и прямую инструкцию отвечать пользователю по-русски. Без этого handoff считается language-contract defect, даже если остальные routing поля корректны.

Это правило относится и к upstream ChatGPT-generated handoff, который попадает в `.chatgpt/codex-input.md`. Запрещены англоязычные человекочитаемые разделы вроде `Goal`, `Hard constraints`, `Required implementation`, `Expected artifacts`, `Verification commands`, `Completion requirements`. Если такой input пришел извне, это language-contract defect: сначала зафиксируй defect-capture, затем нормализуй handoff на русский.

## Нормализованные routing fields
Для любого handoff или self-handoff дополнительно фиксируй:
- `launch_source`: `chatgpt-handoff` или `direct-task`;
- `task_class`: `quick` / `build` / `deep` / `review`;
- `selected_profile`;
- `selected_model`;
- `selected_reasoning_effort`;
- `selected_plan_mode_reasoning_effort`;
- `apply_mode`;
- `strict_launch_mode`;
- `project_profile`;
- `selected_scenario`;
- `pipeline_stage`;
- `artifacts_to_update`;
- `handoff_allowed`;
- `defect_capture_path`.

Эти поля являются общим стандартом и для ChatGPT Project handoff, и для direct Codex self-handoff.
При этом `selected_profile` — исполнимая граница маршрутизации, а `selected_model` / `selected_reasoning_effort` описывают repo-configured mapping выбранного profile. Advisory или handoff text сами по себе не выполняют switch.

## Model availability auto-check / авто-проверка доступности моделей
Repo-configured mapping хранится в `codex-model-routing.yaml`, а live catalog проверяется отдельно через `scripts/check-codex-model-catalog.py` / `codex debug models`.

Handoff должен явно различать:
- repo-configured mapping из `codex-model-routing.yaml`;
- live Codex catalog;
- manual UI picker selection;
- strict launcher profile selection.

Если live catalog check stale или недоступен, handoff не должен утверждать, что `selected_model` точно live-available. Формулировка должна быть честной: selected_model repo-configured and requires live validation.

Если live catalog показывает новый model ID, но repo mapping еще не обновлен, сначала создается proposal через `--write-proposal`. Автоматическая promotion существующего profile на новую model запрещена без manual review.

## Пользовательские режимы маршрутизации
Во всех source-facing handoff/completion artifacts различай три режима:
- `manual-ui (default)`: основной путь для интерактивной работы через VS Code Codex extension;
- `launcher-first strict mode (optional)`: путь для automation, reproducibility, shell-first и scripted launch;
- `already-open session fallback`: non-canonical режим, допустимый только с прямой оговоркой про отсутствие надежного auto-switch.

Для `manual-ui (default)` handoff должен прямо говорить:
- открыть новое окно/чат Codex;
- вручную выбрать `selected_model` и `selected_reasoning_effort` в picker;
- затем вставить один цельный handoff block;
- не считать этот путь эквивалентом executable launcher path.

## VPS Remote SSH-first orchestration для full handoff

Если handoff большой и содержит несколько независимых child subtasks, default path для `factory-template`:

1. Browser ChatGPT Project создает один цельный handoff.
2. Operator открывает VS Code Remote SSH window на VPS и repo root.
3. Codex extension получает handoff в этом VPS/repo context.
4. Repo-native orchestrator раскладывает parent handoff в child subtask specs.
5. Отдельные Codex CLI sessions запускаются на VPS/repo context с явными `selected_profile`, `selected_model`, `selected_reasoning_effort`, `selected_plan_mode_reasoning_effort` и `selected_scenario`.
6. Parent orchestration report собирает child results, blockers и final closeout.

`Codex App / Cloud Director` допускается только как optional, not default. Cloud delegation нельзя описывать как default path и нельзя включать без явного выбора пользователя и разрешенной repo/security boundary.

Already-open live session не является reliable auto-switch boundary. Parent orchestrator не выполняет specialist work inline, если subtask routing требует separate session/profile.

Orchestration guardrails:
- один parent handoff для copy-paste; multi-block handoff запрещен;
- child session не наследует parent route by default;
- parent plan должен фиксировать `user_actions_policy: defer-to-final-closeout`;
- все user-required actions, external UI actions, runtime approvals, real downstream inputs and secret-entry steps переносятся в конец parent plan как `deferred_user_actions`;
- если subtask можно выполнить без реальных внешних данных, используй safe temporary placeholders и занеси их в `placeholder_replacements`;
- финальный closeout обязан напомнить, какие placeholders заменить на реальные данные и какие checks повторить после замены;
- child subtasks не должны блокироваться на пользовательском действии, если есть safe placeholder path;
- secrets, `.env` content, private transcripts и tokens запрещены в handoff, fixtures и reports;
- если model availability не проверена live catalog check, писать `requires live validation`;
- stale/missing model mapping нужно report/fail, а не silently fallback.

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

## Диагностика sticky state
- Если пользователь работает через manual UI apply, но оставил старую live session, route может остаться на last-used profile/model/reasoning.
- В таком случае сначала закрыть текущую сессию и открыть новое окно/чат Codex; затем заново выставить picker или использовать optional strict launch command из handoff package.
- Если новый launch или новый manual UI apply все еще выглядит устаревшим, проверить именованный profile в local Codex config и сверить `selected_model` с live `codex debug models`.

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

Для блока `Нужно ли обновлять repo-first инструкции battle ChatGPT Projects` используй правило:
- `нет` по умолчанию, если downstream уже работает в чистом repo-first режиме;
- `да` только для legacy/hybrid fallback, где ChatGPT Project все еще держит дублированный source/instruction layer вне репо.

Для блока `Нужно ли обновлять repo-first инструкцию factory-template ChatGPT Project` используй правило:
- `нет` по умолчанию, если canonical repo, repo/path setting, entrypoint и короткая repo-first instruction text не менялись;
- `да` только если реально изменился instruction contract для `factory-template` ChatGPT Project.
