# Главный маршрутизатор сценариев

Твоя задача — классифицировать запрос, определить профиль проекта, подобрать минимально достаточный сценарий и не допустить раннего перехода к реализации.

## Что нужно указать в каждом ответе
- выбранный профиль проекта;
- выбранный сценарий;
- текущий этап pipeline;
- какие артефакты нужно обновить;
- разрешен ли handoff в Codex.
- `handoff_shape`, если handoff в Codex разрешен, готовится или обсуждается.

## Контракт первого ответа Codex

Первый substantive ответ Codex для `launch_source: direct-task` обязан начинаться с двух видимых блоков после чтения этого router и до route receipt, self-handoff, анализа или remediation:

````markdown
## Номер запроса Codex
```text
<PROJECT_CODE>-CX-<NNNN> <task-slug>
```

## Карточка проекта
<compact project status card>
````

Правила:
- `Номер запроса Codex` берется только из materialized repo reservation в `.chatgpt/codex-work-index.yaml`, созданной direct-task bootstrap / Codex work allocator. `FT-CX-....` означает Codex remediation/direct work и не расходует ChatGPT `FT-CH` counter.
- Если Codex не может надежно выполнить write в repo codex-work index и подтвердить запись, не показывай `FT-CX-....`; выведи ровно: `Нужно выделить номер через repo codex-work-index / allocator.`
- Значение под `Номер запроса Codex` всегда выводится как отдельный однострочный fenced `text` code block. Внутри code block должна быть ровно одна строка: stable Codex work title или exact allocator blocker.
- `Карточка проекта` должна соответствовать repo renderer output: `python3 template-repo/scripts/render-project-lifecycle-dashboard.py --input template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml --format chatgpt-card --stdout` для `factory-template`, либо downstream-equivalent repo-local renderer/input.
- Если карточка недоступна, это blocker, который надо назвать явно; нельзя заменять карточку свободным пересказом.
- Для `launch_source: chatgpt-handoff` Codex не создает новый `FT-CX` self-handoff; в route receipt нужно показывать входящий `chat_id/chat_title`, если он есть, и не расходовать Codex work counter без отдельной direct/incidental task boundary.

## Контракт первого ответа ChatGPT

Первый substantive ответ ChatGPT в новом project task chat обязан начинаться с двух видимых блоков до route receipt, анализа или handoff:

````markdown
## Название чата для копирования
```text
<PROJECT_CODE>-CH-<NNNN> <task-slug>
```

## Карточка проекта
<compact project status card>
````

Правила:
- `Название чата для копирования` берется только из materialized repo reservation в `.chatgpt/chat-handoff-index.yaml`, созданной write-allocator'ом. Выводимый `FT-CH-....` означает, что item уже записан в repo/GitHub index; dry-run, read-only вычисление или "следующий вероятный номер" не являются резервированием.
- Если ChatGPT не может надежно выполнить write в repo index и подтвердить запись, не показывай `FT-CH-....`; выведи ровно: `Нужно выделить номер через repo chat-handoff-index / allocator.`
- Значение под `Название чата для копирования` всегда выводится как отдельный однострочный fenced `text` code block, чтобы ChatGPT UI дал copy button и оператор мог скопировать title/blocker одним кликом. Внутри code block должна быть ровно одна строка: stable title или exact allocator blocker.
- Инвариант первого ответа: first substantive answer обязан дать один из двух видимых outcomes до route receipt, анализа или handoff: materialized allocation or allocator blocker. Первый outcome: materialized allocation confirmed, затем stable title block. Второй outcome: allocation unavailable или write not confirmed, затем exact allocator blocker.
- Порядок allocation attempt обязателен: сначала read router, затем repo-local allocator, если он исполним в текущем context; если repo-local allocator не исполним в ChatGPT connector context, но доступен GitHub connector write path, выполни connector-based materialized reservation в `.chatgpt/chat-handoff-index.yaml`, затем confirm fetch/readback и только после этого показывай stable title.
- Connector fallback должен быть connector-safe reservation patch: append one item and bump `next_chat_number`; не делай ручной full-file rewrite без сверки текущего `next_chat_number`, canonical `status_chain` и confirm fetch/readback.
- Для repo `mppcoder/factory-template` repo-first instruction authorizes configured GitHub connector: repo-first instruction является prior authorization использовать настроенный authenticated GitHub connector / repo tool для обязательного чтения repo, чтения index и connector-safe allocation attempt. не спрашивай conversational confirmation перед GitHub read, index read или reservation attempt; формулировки вроде "подтвердите доступ к GitHub" и "разрешите использовать GitHub" запрещены до materialized allocation или confirmed blocker.
- Если platform-level OAuth / connector authorization prompt сам блокирует действие, зафиксируй `external_auth_blocker` и exact allocator blocker. Если write action exposed отсутствует или write rejected, зафиксируй `write_auth_blocker` / exact allocator blocker. Не заменяй попытку доступного connector path свободным вопросом пользователю.
- Если write action exposed and confirm fetch succeeds, exact allocator blocker запрещен: сначала покажи materialized `FT-CH-.... <task-slug>`.
- Exact allocator blocker разрешен только при реальном write blocker: repo-local allocator недоступен и GitHub connector write path/repo tool/authenticated write path тоже недоступен, write rejected, permission denied или confirm fetch не подтвердил запись. blocker нельзя выводить, когда GitHub connector write path доступен и подтверждает update.
- Третье состояние запрещено: no allocation attempted / no blocker / answer continues. Нельзя продолжать route receipt, анализ, handoff или remediation, если нет materialized allocation и нет exact allocator blocker.
- Состояние `chatgpt-first-answer-allocation-not-attempted` является contract violation и defect-class для первого ответа ChatGPT. Его нужно фиксировать как bug, а не как допустимый fallback.
- Если handoff не был запущен в Codex, номер все равно остается занятым repo reservation; следующая задача не должна переиспользовать его. Закрывать такую запись можно только явным status update (`superseded`, `not_applicable`, `archived`), но не освобождением номера.
- Название содержит только stable `FT-CH-....` и slug; status/kind tokens запрещены.
- `Карточка проекта` должна соответствовать repo renderer output: `python3 template-repo/scripts/render-project-lifecycle-dashboard.py --format chatgpt-card --stdout`. Если ChatGPT не может выполнить команду, он должен прочитать свежий `reports/project-status-card.md` или компактный card block из `reports/project-lifecycle-dashboard.md`; если карточка недоступна, это blocker, который надо назвать явно.
- Project Instructions могут показать только уже материализованное repo title или allocator blocker; они не могут гарантировать auto-rename ChatGPT UI, global chat scan или write в repo index без доступного repo tool/write path.
- Этот contract действует и когда ответ продолжает route receipt / готовит handoff: title + card не заменяют handoff и не отменяют repo-first чтение router.

## Контракт маршрутизации
Всегда разделяй:
- advisory/policy layer: `AGENTS`, ChatGPT Project instructions, scenario-pack, runbooks, `.chatgpt` guidance;
- executable routing layer: named profiles в `.codex/config.toml` и task launcher/router scripts.

Нельзя считать, что advisory слой сам по себе переключает модель или reasoning mode внутри уже открытой сессии.
Надежная единица маршрутизации для executable layer: только новый task launch / новый запуск Codex под новую задачу.
Но для интерактивного VS Code Codex extension default user-facing path должен отличаться от strict automation path:
- `manual-ui (default)`: открыть новое окно/чат Codex, вручную выбрать model/reasoning в picker и только потом вставить handoff;
- `launcher-first strict mode (optional)`: использовать repo launcher, если нужна automation / reproducibility / shell-driven launch;
- `already-open live session`: только non-canonical fallback, без обещаний auto-switch.

Отдельно фиксируй, что "новый чат + вставка handoff" и "new task launch через executable launcher" — не одно и то же.
Нельзя выдавать manual UI apply за авто-переключение profile/model/reasoning внутри уже открытой live session.

## Goal-first gate нормализации

После repo-first чтения router, title/card contract и до scenario-specific execution каждая новая задача проходит goal-first normalization gate.

Goal first — это pre-routing normalization layer, а не замена lifecycle/intake/spec/handoff сценариев:
- сначала нормализуй просьбу в минимальный `goal_contract`;
- затем выбери и исполняй обычный scenario route;
- selected scenario по-прежнему владеет реализацией, remediation, handoff и closeout;
- `handoff_shape` при передаче в Codex остается `codex-task-handoff`, если нет legacy readback;
- фактический `execution_mode` выбирает Codex runtime после анализа task graph;
- advisory goal-contract не переключает модель, profile, reasoning или runtime mode внутри уже открытой live session.

Gate обязателен для:
- явных команд `goal`, `goal:`, `/goal`, `цель`, `цель:`;
- handoff и direct Codex task;
- любой новой задачи, где можно безопасно определить желаемый результат.

Минимальная форма `goal_contract` должна содержать:
- `normalized_goal`;
- измеримый `definition_of_done` или validation contour, который сначала нужно создать/найти;
- `evidence_required`;
- `scope` и `non_goals`;
- safety/budget boundaries;
- proxy-signal denylist.

Если цель уже достаточно определена, не задавай лишних вопросов: зафиксируй безопасные defaults и продолжай route.
Если цель размыта и нельзя безопасно вывести DoD, задай один короткий уточняющий вопрос.
Если задача broad/migration/architecture и не раскладывается в один измеримый контур, применяй pattern `scrappy -> PRD -> clean`: exploratory goal, затем PRD/spec, затем чистая реализация по spec.

`goal first` является обязательным template contract.
`Codex /goal runtime` является optional runtime mode: в текущем live CLI он может быть experimental feature flag и должен быть live-validated/enabled before use. Если пользователь явно выбирает experimental `goals`, разрешено пометить runtime как `codex_goal_candidate`, но нельзя утверждать, что ChatGPT Project instruction или уже открытая Codex session сами включили `/goal`.

Запрещено закрывать goal по proxy signals alone:
- tests passed alone;
- file exists alone;
- commit exists alone;
- green dashboard alone;
- validator passed alone.

Goal closure допустим только когда evidence реально удовлетворяет `definition_of_done`.

## Контракт доступа к GitHub repo

Для GitHub repo `mppcoder/factory-template` repo-first означает authenticated repo-first, а не browser/public URL by default.
Если ChatGPT или Codex должен читать, проверять или менять этот repo, primary path:
- GitHub connector;
- repo tool / installed GitHub app capability;
- authenticated `gh` access.

Для ChatGPT first-answer allocation этот repo-first contract является prior authorization на configured authenticated connector access: repo-first instruction authorizes configured GitHub connector для обязательного чтения repo, чтения `.chatgpt/chat-handoff-index.yaml` и попытки connector-safe reservation. Не спрашивай conversational confirmation перед таким read/allocation path.

Граница: repo instructions не могут отключить platform-level OAuth / connector authorization prompt. Если сама платформа требует OAuth/connector authorization или connector install, назови `external_auth_blocker`. Если connector доступен на чтение, но write action exposed отсутствует или write rejected, назови `write_auth_blocker`. В обоих случаях можно показать exact allocator blocker только после фиксации blocker; нельзя использовать free-form вопрос пользователю как замену попытки authenticated repo-first path.

Если write action exposed and confirm fetch succeeds, exact allocator blocker запрещен: ChatGPT должен показать stable materialized title.

Публичные `github.com` или `raw.githubusercontent.com` URL допускаются только как fallback при явном blocker:
- connector unavailable;
- no permission;
- repo not installed in connector;
- authenticated repo tool unavailable;
- user explicitly asks for public URL.

При таком fallback ответ обязан явно назвать blocker. Формулировки вроде "прочитай GitHub repo" или "сценарии читаются из GitHub repo" нельзя трактовать как разрешение по умолчанию открывать публичный browser/raw URL, если connector/tool доступен.

## Gate handoff и runtime execution mode

Перед выдачей handoff обязательно зафиксируй нормализованное поле `handoff_shape`.

Preferred значение:
- `codex-task-handoff`.

Backward-compatible legacy значения допускаются только при чтении старых артефактов:
- `single-agent-handoff`;
- `parent-orchestration-handoff`.

Новый user-facing contract: handoff всегда один и нейтральный. ChatGPT/handoff layer не должен заранее называть handoff "оркестровым". Codex после route receipt и анализа task graph сам выбирает фактический `execution_mode`:
- `single-session execution`;
- `orchestrated-child-sessions`.

Фиксируй orchestration candidate signals, но не подменяй ими факт исполнения.

Orchestration candidate hard triggers:
- задача явно большая, многоэтапная или roadmap-like;
- есть две или больше независимые подзадачи, которые можно или нужно выполнять отдельными child sessions;
- разные части задачи требуют разных `task_class`, `selected_profile`, `selected_model` или `selected_reasoning_effort`;
- одновременно нужны audit/deep analysis, implementation/build, docs normalization, validators/tests и final review как отдельные workstreams;
- есть dependency queue между доработками, где одни задачи должны быть выше других в очереди реализации;
- нужен визуальный контроль статуса в orchestration cockpit/dashboard;
- есть `deferred_user_actions`, `placeholder_replacements`, runtime/downstream boundaries или `external-user-action`, которые нужно перенести в final closeout через `defer-to-final-closeout`;
- пользователь явно просит parent handoff, orchestrator, оркестр агентов или full orchestration.

Если hard trigger не сработал, но есть три или больше soft signals, пометь задачу как orchestration candidate, но `handoff_shape` остается `codex-task-handoff`:
- больше трех артефактов к обновлению;
- требуется обновление scenario-pack + scripts + tests/validators;
- ожидается больше одного verification contour;
- есть высокий риск архитектурного drift;
- нужно синхронизировать template-facing и downstream-facing wording;
- есть несколько вариантов реализации и требуется route explanation.

Запрещено:
- называть handoff оркестровым только потому, что задача важная;
- заранее утверждать фактический `orchestrated-child-sessions`, пока Codex не решил запускать child/subagent sessions;
- скрывать orchestration candidate signals для большой задачи с независимыми child subtasks и разными профилями;
- в closeout называть фактическое выполнение "оркестром агентов", если child/subagent sessions не запускались; в таком случае пиши `single-session execution`, `child/subagent count: 0` и фиксируй это как correction, если ранее был заявлен parent orchestration;
- утверждать, что parent handoff сам переключает model/profile/reasoning в уже открытой live session;
- смешивать advisory/policy layer с executable routing layer.

Выбор фактического execution mode делает Codex после анализа задачи, а не ChatGPT/handoff layer до исполнения. В финальном closeout обязательно укажи actual execution mode и фактический child/subagent count.

## Правило inline handoff
Если handoff в Codex уже разрешен и задача достаточно определена, выдай готовый Codex handoff в том же ответе. Не останавливайся на одной аналитике.

Такой handoff нужно выдавать только одним цельным блоком для вставки в Codex. Нельзя заменять его ссылкой на файл, несколькими разрозненными блоками или набором "прочитай `.chatgpt/codex-*` файлы и собери сам".

Если handoff для change-class = `required`, нельзя завершать ответ только анализом, summary или списком размышлений без готового handoff.

Если handoff для change-class = `optional`, но обязательные gate'ы закрыты, обязательные артефакты уже достаточны, задача определена и можно безопасно сформировать нормализованный handoff, по умолчанию тоже выдай готовый handoff в том же ответе.

Отложить handoff допустимо только если:
- не закрыты обязательные gate'ы;
- не хватает обязательных артефактов;
- задача реально неоднозначна;
- нужен выбор архитектурной развилки.

## Правило внутреннего и внешнего follow-up
Если после remediation, verify, commit/push или closeout-stage остаются внутренние Codex-eligible задачи внутри repo, нельзя завершать ответ только инструкцией пользователю.

Если verify green, `origin` настроен и canonical verified sync технически доступен, commit/push считаются внутренней работой Codex, а не отдельным ручным шагом пользователя.
В таком случае нужно выполнить канонический sync path внутри repo, а не откладывать commit/push до дополнительного запроса.
Перед финальным ответом обязательно выполнить `git status --short --branch`: если repo dirty или branch ahead без конкретного blocker, closeout считается незавершенным.
Финальный ответ должен назвать commit hash / sync status либо явно зафиксировать blocker; простой summary без sync-state недостаточен.

К внутреннему follow-up по умолчанию относятся:
- release note и release-facing changelog/update внутри repo;
- source-pack, curated sources, export/manifests refresh;
- brownfield source-candidate map, reconstruction allowlist/denylist, change-map и reverse-engineering summary внутри repo;
- closeout artifact sync;
- verify-summary, done-summary и release-facing consistency pass;
- release bundle preparation;
- другой release-followup, который делается внутри repo без внешнего UI/manual шага.

Если remaining work относится к такому internal follow-up, выдай inline Codex handoff в том же ответе.
Если текущий route уже совместим и internal follow-up можно выполнить в той же live Codex-сессии, продолжай выполнение вместо остановки на summary или просьбе "продолжить". Остановка допустима только при реальном blocker, внешнем действии, несовместимом route или необходимости нового task launch.

User-only closeout допустим только если remaining next step действительно внешний и Codex не может выполнить его через доступные инструменты:
- GitHub UI только при реальном блокере: нет авторизации, нет прав на действие, требуется обязательный человеческий review/approval, checks red/pending, конфликт, неясная merge strategy или действие является release/security approval;
- ChatGPT Project UI;
- ручная загрузка архива;
- ввод секрета;
- другой manual step вне IDE/SSH.

Если GitHub PR создан текущей задачей или явно входит в ее closeout, `gh`/GitHub connector доступен, checks green, PR mergeable и нет required human approval, перевод PR из draft, merge, удаление branch и синхронизация local main являются внутренней работой Codex, а не пользовательским шагом.

Если GitHub repo/remote creation является частью текущей задачи и `gh`/GitHub connector доступен с write permissions, создание repo, добавление `origin` и первый push тоже являются внутренней работой Codex. Завершать ответ просьбой пользователю создать repo и вставить путь запрещено, пока не назван конкретный blocker.

Если есть и внутренние, и внешние шаги, сначала выдай inline Codex handoff на внутреннюю часть, а затем отдельно заверши ответ блоком `## Инструкция пользователю` только для внешней границы.

## Обязательный финальный блок
Если ответ требует следующего шага пользователя или любого внешнего действия, заверши ответ обязательным разделом `## Инструкция пользователю`.

Если нужны любые внешние действия пользователя, `## Инструкция пользователю` должен быть оформлен как диалоговый сценарий, а не как сухая ссылка на артефакт:
- объясни цель действия простыми словами;
- назови точное окно/сервис, где пользователь действует;
- дай последовательные шаги с ожидаемым результатом после каждого важного шага;
- предложи варианты, если есть безопасные развилки, и явно отметь рекомендованный вариант;
- если пользователь должен что-то копировать, выдай точный fenced code block для копирования в ответе; ссылка на файл или путь в repo может быть только дополнительным evidence, но не заменой copy block;
- укажи, что прислать обратно, чтобы Codex мог продолжить.

Если в любом ответе предлагается конкретный пример текста, который пользователь должен написать, вставить, отправить, сохранить как instruction или передать в другой UI/чат/CLI, этот пример обязан быть отдельным fenced code block для копирования. Это правило действует не только внутри `## Инструкция пользователю`, но и в анализе, рекомендациях, handoff-пояснениях, closeout и troubleshooting. Inline-кавычки, свободный пересказ или ссылка на файл не заменяют copy block для готового текста.

Если change затрагивает downstream-consumed template content, runbooks, scenario-pack, launcher, validators, codex-task-pack, `.chatgpt` artifacts или другой слой, сначала определи, есть ли реальное внешнее действие пользователя.
Если внешнего действия нет, не разворачивай completion package: финал должен коротко сказать `Внешних действий не требуется.`
Если внешнее действие есть, `## Инструкция пользователю` должен быть не общим footer, а структурированным, но компактным completion package только по этим действиям.
Любой финальный closeout обязан дополнительно дать continuation outcome:
- если пользователь должен что-то сделать сейчас или для продолжения, это должно быть в `## Инструкция пользователю`;
- если пользователь ничего не должен делать, финал должен явно сказать, что следующий пользовательский шаг отсутствует и задачи текущего scope полностью выполнены;
- если существует будущий roadmap stage, но он не actionable сейчас, назови его как future boundary и отдельно скажи, что текущий scope закрыт.
- если roadmap/readout содержит несколько возможных следующих веток, финал обязан назвать рекомендованную ветку и fallback-ветку; формула `следующий пользовательский шаг отсутствует` относится только к текущему закрытому scope и не должна скрывать рекомендацию следующего roadmap шага.
Финал, который говорит только `Внешних действий не требуется.` без объяснения "что дальше / полностью done", считается неполным closeout.

Для `factory-template` финальный closeout пишется по-русски. Английский допускается только для technical literal values: команды, пути, YAML/JSON keys, model IDs, commit hash и route fields.

Если для такого completion package нужны свежие exports, generated archives, boundary-actions guide, patch bundle или другой repo-артефакт, Codex должен сначала собрать их сам внутри repo. Нельзя перекладывать на пользователя запуск внутренних prepare-команд, если это может сделать Codex.

В таком случае нужно явно различить:
- обновление repo-first инструкции проекта шаблона в ChatGPT;
- обновление шаблона в downstream/battle repo;
- обновление repo-first инструкции downstream/battle ChatGPT Projects.

Для первого contour по умолчанию тоже не предполагай `да`.
Если canonical repo, repo/path setting, entrypoint и короткая repo-first instruction text не менялись, canonical answer обычно `нет`.
`Да` допустимо только если реально изменился instruction contract для `factory-template` ChatGPT Project.

Для третьего contour по умолчанию не предполагай `да`.
Если downstream уже работает в чистом repo-first режиме и source-of-truth читается из репо, canonical answer обычно `нет`.
`Да` допустимо только для legacy/hybrid fallback, где в ChatGPT Project еще живет дублированный instruction/source layer вне репо.

Не перечисляй contour'ы со статусом `не требуется`, если пользователь не запросил полный audit-style register и задача не является release/security approval, где само отсутствие действия по контуру является значимым решением.

Для downstream-consumed changes с реальными внешними действиями финальный completion package должен содержать отдельный `Реестр внешних действий` или эквивалентную таблицу. В него включаются только actionable строки: точное действие пользователя и момент выполнения. Нельзя заменять этот реестр общей фразой вроде "downstream sync рекомендуется".
`Реестр внешних действий` не должен быть audit table всех возможных contour'ов, если все строки сводятся к `действие не требуется`.

Этот completion package должен быть выдан в том же финальном ответе, где сообщается о завершении change. Нельзя считать задачу закрытой, если инструкция появилась только после дополнительного напоминания пользователя.

## Маршрут дефектов
Если задача содержит bug, regression, inconsistency, missing step, unexpected behavior или подозрение на template defect, сначала проходи defect-capture path: reproduce → evidence → bug report → layer classification → feedback при необходимости → только потом remediation.

## Правило выравнивания контуров
Если найден defect, gap, regression, inconsistency или template flaw, сначала пройдите defect-capture path: bug report → classification → factory feedback при reusable issue → handoff / remediation / Codex.

## Правило приема ChatGPT handoff
Если Codex получает уже готовый handoff с `launch_source: chatgpt-handoff`, он исполняет именно этот входящий handoff.

В первом содержательном ответе Codex может вывести только `handoff receipt` / `route receipt`: краткое подтверждение выбранного профиля проекта, сценария, pipeline stage, artifacts to update, `handoff_allowed`, `defect_capture_path` и routing fields.

Такой receipt:
- не является `self-handoff`;
- не заменяет входящий handoff;
- не создает новый task launch сам по себе;
- не должен называться `self-handoff`.

Если входящий ChatGPT handoff просит "visible self-handoff" при `launch_source: chatgpt-handoff`, нормализуй это как `handoff receipt` перед исполнением исходного handoff.

## Правило incidental / side bug
Если во время исполнения основного handoff найден побочный defect, его нельзя silently drop, даже если основной scope закрывается успешно.

Обязательное дерево решений:
- если incidental bug исправлен в рамках текущего scope, зафиксируй defect-capture и упомяни его в closeout;
- если incidental bug не исправлен, сначала создай структурированный bug report, затем выполни self-handoff именно для этого нового бага;
- self-handoff обязан отдельно определить `task_class`, `selected_profile`, `selected_model`, `selected_reasoning_effort`, `selected_scenario`, `pipeline_stage`, `artifacts_to_update`, принадлежность к текущему scope и необходимость отдельной remediation-задачи;
- если для нового бага executable routing указывает другой профиль, модель или reasoning, user-facing guidance должна различать `manual-ui (default)` и `launcher-first strict mode (optional)`, а как строго воспроизводимый путь рекомендовать новый task launch через явный launch command;
- продолжение в текущем live chat допустимо только как явно помеченная non-canonical fallback-опция с прямой оговоркой, что уже открытая сессия не является надежным механизмом автопереключения profile/model/reasoning;
- если для бага нужен deep research, вместо слабой in-session remediation попытки выдай ChatGPT-ready research bug report / prompt.

## Правило прямой задачи
Если Codex получает прямую задачу вне ChatGPT Project, сначала требуется self-handoff по тем же полям и gate'ам, что и у внешнего handoff:
- classification;
- selected project profile;
- selected scenario;
- current pipeline stage;
- artifacts to update;
- handoff allowed;
- defect-capture path, если задача defect-class.

Этот self-handoff должен быть не только внутренним артефактом, но и явным стартовым блоком в первом substantive ответе Codex.
Нельзя пропускать его только потому, что "контекст уже понятен" или "задача очевидна".

Это правило применяется только к `launch_source: direct-task` или к отдельному incidental defect task boundary. Оно не применяется к уже готовому `chatgpt-handoff`, где нужен `handoff receipt`, а не новый self-handoff.

Только после этого допустим remediation / implementation.
