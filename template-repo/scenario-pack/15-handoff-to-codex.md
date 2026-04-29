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
- нормализованное поле `handoff_shape` со значением `single-agent-handoff` или `parent-orchestration-handoff`.

Человекочитаемые пояснения в handoff, self-handoff и completion package для `factory-template` пишутся на русском языке. Технические ключи вроде `selected_profile`, `apply_mode`, `strict_launch_mode`, имена команд, файлов и literal values допускаются как идентификаторы, но описательные заголовки и инструкции должны быть русскоязычными.

Каждый copy-paste handoff в Codex обязан явно содержать строку `Язык ответа Codex: русский` и прямую инструкцию отвечать пользователю по-русски. Без этого handoff считается language-contract defect, даже если остальные routing поля корректны.

Это правило относится и к upstream ChatGPT-generated handoff, который попадает в `.chatgpt/codex-input.md`. Запрещены англоязычные человекочитаемые разделы вроде `Goal`, `Hard constraints`, `Required implementation`, `Expected artifacts`, `Verification commands`, `Completion requirements`. Если такой input пришел извне, это language-contract defect: сначала зафиксируй defect-capture, затем нормализуй handoff на русский.

## Нормализованные routing fields
Для любого handoff, handoff receipt или self-handoff дополнительно фиксируй:
- `launch_source`: `chatgpt-handoff` или `direct-task`;
- `handoff_shape`: `single-agent-handoff` или `parent-orchestration-handoff`;
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

Эти поля являются общим стандартом для ChatGPT Project handoff receipt и для direct Codex self-handoff.
При этом `selected_profile` — исполнимая граница маршрутизации, а `selected_model` / `selected_reasoning_effort` описывают repo-configured mapping выбранного profile. Advisory или handoff text сами по себе не выполняют switch.

## Выбор вида handoff / handoff_shape

`handoff_shape` выбирается до выдачи handoff.

Allowed values:
- `single-agent-handoff`;
- `parent-orchestration-handoff`.

Default: `single-agent-handoff`.

Выбирай `single-agent-handoff`, если задача:
- цельная и может быть выполнена одним route/profile;
- затрагивает один основной слой или небольшое число тесно связанных файлов;
- не требует параллельных child subtasks;
- не требует разных `task_class`, `selected_profile`, `selected_model` или `selected_reasoning_effort` для отдельных частей;
- не требует orchestration cockpit / parent status tracking;
- не содержит длинной цепочки зависимостей между независимыми доработками.

Для `single-agent-handoff` handoff остается одним агентским handoff и должен явно фиксировать, почему parent orchestration не требуется.

Выбирай `parent-orchestration-handoff`, если сработал хотя бы один hard trigger:
- задача явно большая, многоэтапная или roadmap-like;
- есть две или больше независимые подзадачи, которые можно или нужно выполнять отдельными child sessions;
- разные части задачи требуют разных `task_class`, `selected_profile`, `selected_model` или `selected_reasoning_effort`;
- одновременно нужны audit/deep analysis, implementation/build, docs normalization, validators/tests и final review как отдельные workstreams;
- есть dependency queue между доработками, где одни задачи должны быть выше других в очереди реализации;
- нужен визуальный контроль статуса в orchestration cockpit/dashboard;
- есть `deferred_user_actions`, `placeholder_replacements`, runtime/downstream boundaries или `external-user-action`, которые нужно перенести в final closeout через `defer-to-final-closeout`;
- пользователь явно просит parent handoff, orchestrator, оркестр агентов или full orchestration.

Если hard trigger не сработал, но есть три или больше soft signals, выбирай `parent-orchestration-handoff`:
- больше трех артефактов к обновлению;
- требуется обновление scenario-pack + scripts + tests/validators;
- ожидается больше одного verification contour;
- есть высокий риск архитектурного drift;
- нужно синхронизировать template-facing и downstream-facing wording;
- есть несколько вариантов реализации и требуется route explanation.

Для `parent-orchestration-handoff` handoff должен содержать:
- parent plan expectations;
- child subtask boundaries;
- `defer-to-final-closeout`;
- `deferred_user_actions`;
- `placeholder_replacements`;
- `owner_boundary`;
- route explanation;
- final continuation outcome.

Запрещено:
- выдавать parent handoff только потому, что задача важная, если она реально цельная и один deep/build агент достаточен;
- выдавать single-agent handoff для большой задачи, где есть независимые child subtasks с разными профилями;
- утверждать, что parent handoff сам переключает model/profile/reasoning в уже открытой live session;
- смешивать advisory/policy layer с executable routing layer.

## Подтверждение handoff vs self-handoff
Если `launch_source: chatgpt-handoff`, Codex не переписывает и не заменяет входящий handoff.

Допустимое первое подтверждение для такого запуска называется `handoff receipt` или `route receipt`. Оно только фиксирует:
- выбранный профиль проекта;
- выбранный сценарий;
- текущий pipeline stage;
- artifacts to update;
- `handoff_allowed`;
- `defect_capture_path`;
- selected profile/model/reasoning routing fields.

`handoff receipt` не является self-handoff, новым handoff, новым source-of-truth или executable launch boundary.

Термин `self-handoff` используй только когда:
- `launch_source: direct-task`, то есть внешнего ChatGPT handoff нет;
- incidental defect выделен в отдельную remediation-задачу или требует явного current-route continuation decision.

Если upstream ChatGPT handoff при `launch_source: chatgpt-handoff` использует формулировку "visible self-handoff", Codex должен трактовать ее как "visible handoff receipt" и дальше исполнять исходный ChatGPT handoff.

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

Для full orchestration handoff пользовательский default должен быть one-paste autopilot:
- пользователь вставляет parent handoff один раз;
- parent Codex сам выводит `handoff receipt`;
- parent Codex сам materializes/reads parent orchestration plan;
- parent Codex сам запускает `orchestrate-codex-handoff.py --execute` после validation gate;
- ручной запуск shell-команды пользователем остается только troubleshooting / strict reproduction fallback.

Plan №6 productization layer adds a beginner-readable status and validation contour:
- parent Codex normalizes the large ChatGPT handoff into a checkable `codex-orchestration/v1` parent artifact before child session writes;
- parent Codex may use `template-repo/template/.chatgpt/parent-orchestration-plan.yaml.template` as the normalization template;
- `validate-parent-orchestration-plan.py` validates the parent artifact and keeps existing `validate-codex-orchestration.py` as the core runner contract;
- `render-orchestration-cockpit.py` and `validate-orchestration-cockpit.py` maintain `orchestration-cockpit-lite` status for parent id, child tasks, blockers, deferred user actions, placeholder replacements and next action;
- `explain-codex-route.py` records deterministic keyword/rule-based route explanation for task class/profile/model/reasoning and live catalog boundary;
- `validate-beginner-handoff-ux.py` checks one copy-paste block, no file-based handoff, no hidden second operator shell step, no fake auto-switch claim, deferred user actions and final continuation outcome.

Do not claim a semantic classifier when route explanation is deterministic/keyword/rule-based.
Do not claim advisory handoff text switches model/profile/reasoning inside an already-open session.

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

## Закрытие handoff implementation register

При завершении Codex-задачи, которая пришла из ChatGPT handoff или породила Codex self-handoff, Codex должен обновить `.chatgpt/handoff-implementation-register.yaml`, если artifact существует в проекте или задача относится к межчатовой очереди.

Обязательный closeout path:
- найти matching item по `id`, title/source_handoff_path или route receipt;
- обновить `status` без false green;
- добавить `evidence` для `implemented`, `verified`, `not_applicable` или `archived`;
- если выполнение породило новый self-handoff, добавить новый item, а не оставлять его только в чате;
- если задача больше не актуальна, не удалять item, а выполнить deactivation path: `status: not_applicable`, `closeout_reason`, evidence или `accepted_reason`;
- если item зависит от незакрытых dependencies, он остается visible `blocked`, а не `ready`;
- после изменения register обновить dashboard render output.

Этот register не заменяет `.chatgpt/handoff-rework-register.yaml`: rework register остается KPI по rework loops, а implementation register хранит жизненный цикл handoff/self-handoff задач до verified closeout, deactivation или archive.

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
