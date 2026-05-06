# AGENTS.md — только для проекта шаблона фабрики

## Роль Codex

Ты основной исполнитель внутри repo `factory-template`.

Не заменяй пользователя на внешних границах.

При handoff и execution planning сначала применяй правила этого repo: `AGENTS`, runbook, scenario-pack, policy files и канонические `.chatgpt`/template instructions. Общие рабочие привычки и средовые эвристики допустимы только там, где они не конфликтуют с repo rules и старшими системными ограничениями среды.

## Внешние границы

Всегда считать внешними границами:

- GitHub UI;
- ChatGPT Project UI;
- загрузку новых архивов;
- ввод секретов;
- любые ручные действия вне IDE/SSH.

На таких шагах обязательно выдавай:

1. цель;
2. где сделать;
3. точные шаги;
4. ожидаемый результат;
5. что прислать обратно.

Каноническое имя этого финального блока: `Инструкция пользователю`.

Если есть pending user/external step, ответ без финального блока `## Инструкция пользователю` считается неполным.

Если external step связан с source updates или downstream sync, сначала проверь, есть ли реальное действие пользователя.
Если действий нет, финальный ответ должен коротко сказать `Внешних действий не требуется.`
Если действия есть, `## Инструкция пользователю` должен быть расширен до компактного completion package только по этим действиям, а не оставаться общим footer.

Если такой completion package обязателен, он должен присутствовать в том же финальном ответе, где выдаётся summary change. Откладывать его до следующего сообщения пользователя запрещено.
Не перечисляй контуры со статусом `не требуется`, если пользователь явно не запросил полный audit-style register.

## Правило классификации задач

Перед каждой новой задачей классифицируй ее на launch boundary.

### quick

Использовать для:
- docs;
- triage;
- search;
- lightweight inventory.

### build

Использовать для:

- standard implementation;
- docs + scripts sync;
- launcher/validator updates;
- обычные repo changes.

### deep

Использовать для:

- RCA test failure;
- mismatch between runbook, scripts, examples, validators;
- scenario architecture analysis;
- feedback ingestion from downstream projects.

### review

Использовать для:
- review;
- tests;
- cleanup;
- final verification.

## Правило переключения профиля

1. Не полагайся на mid-session auto-switch внутри старой сессии.
2. Для новой задачи используй новый Codex launch через `--profile`.
3. `AGENTS`, project instructions и scenario-pack сами по себе профиль не переключают.
4. Для direct task сначала создай self-handoff по repo-сценариям.
5. Проверяемый выбор хранится в `.chatgpt/task-launch.yaml`.
6. Для direct task self-handoff должен быть явно показан в первом substantive ответе, а не оставаться только внутренним артефактом или неявным рассуждением.
7. Первый substantive ответ Codex для direct task должен до route receipt/remediation показать `Номер запроса Codex` из `.chatgpt/codex-work-index.yaml` и `Карточка проекта` из repo renderer.

## Правило inline handoff

Если handoff в Codex уже разрешен и задача достаточно определена, выдай готовый handoff в том же ответе.

Формат handoff для пользователя: только один цельный блок для copy-paste в Codex. Запрещено заменять handoff ссылкой на файл, выдавать его несколькими блоками или требовать собирать handoff из repo-файлов вручную.

Если handoff обязателен по change-class, нельзя завершать ответ только аналитикой.

Если handoff опционален, но gate'ы и артефакты уже достаточны и handoff можно безопасно нормализовать, по умолчанию тоже выдай handoff сразу.

Если remaining work еще находится внутри repo и остается Codex-eligible, нельзя завершать ответ только пользовательским footer.

К internal repo follow-up относятся:
- release notes и release-facing docs;
- source-pack / curated sources refresh;
- export / manifests refresh;
- closeout artifact sync;
- verify / done / release-facing consistency pass;
- release bundle preparation.

Если есть и внутренние, и внешние шаги, сначала выдай inline handoff на внутреннюю часть, затем отдельный `## Инструкция пользователю` на внешнюю границу.

Для changes, затрагивающих ChatGPT Project guidance, в completion package обязательно различай:
- factory template ChatGPT Project instruction;
- downstream repo template sync;
- downstream ChatGPT Project instructions.

Если replacement может создать дубль или stale Source, всегда добавляй точный раздел `Удалить перед заменой`.

Если для внешней границы нужны exports, generated archives, manifest refresh или boundary-actions guide, сначала собери их сам внутри repo. Не проси пользователя запускать внутренние repo-команды ради подготовки этих артефактов.

ChatGPT Project не является каноническим хранилищем сценариев.
Если меняется repo-first инструкция, пользователю передается точный обновленный текст для вставки в проект, а не указание пересказать сценарии вручную.

## Правило по release

Никогда не считать релиз готовым без:

- self-tests;
- verify summary;
- release notes;
- явной фиксации, что изменилось в шаблоне.

## Правило verified sync

После green verify используйте `VERIFIED_SYNC.sh` как канонический путь commit/push.

Требования:

- без green verify commit/push запрещены;
- при отсутствии diff sync должен завершаться как no-op;
- git-команды выполнять только последовательно;
- fallback push через прямой SSH допустим только как deterministic fallback, а не как silent branch.
- если основной green verify уже зафиксирован, а текущий diff состоит только из low-risk `.gitignore`/docs/closeout follow-up правок, Codex должен сам выполнить lightweight follow-up verify и сразу запустить `VERIFIED_SYNC.sh`, а не спрашивать отдельное разрешение на commit/push.

## Правило release decision

Используйте отдельный `.chatgpt/release-decision.yaml`.

- `decision=no-release` означает только verified sync без tag/release;
- `decision=release` разрешает `EXECUTE_RELEASE_DECISION.sh`;
- auto release без явного decision запрещен.
