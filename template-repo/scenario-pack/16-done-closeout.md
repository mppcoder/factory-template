# Закрытие цикла

После завершения работы обнови:
- `CURRENT_FUNCTIONAL_STATE.md`;
- `project-knowledge/`;
- `verification-report.md`;
- `done-report.md`;
- `work/completed/`.

## Правило closeout
Если change завершен полностью и внешних действий больше нет, допустим короткий closeout без блока `Инструкция пользователю`.
Но такой closeout все равно обязан явно содержать формулировку, что внешних действий больше нет: например `Внешних действий не требуется.` или эквивалентную недвусмысленную фразу.
Кроме этого, closeout обязан явно зафиксировать continuation outcome: `Следующий пользовательский шаг отсутствует; задачи текущего scope выполнены полностью.` или эквивалентную недвусмысленную формулировку.

## Goal-first закрытие

Если задача имеет `goal_contract`, closeout обязан назвать фактический `goal_status`:
- `achieved`;
- `unmet`;
- `budget_limited`;
- `tool_limited`;
- `blocked`;
- `not_applicable`.

Closeout должен сравнить evidence с `definition_of_done`.
Запрещено помечать goal как `achieved` только потому, что:
- tests passed alone;
- file exists alone;
- commit exists alone;
- green dashboard alone;
- validator passed alone.

Если goal не достигнут, closeout обязан дать continuation outcome:
- что сделано;
- что осталось;
- blockers;
- next recommended goal или follow-up handoff.

Если остановка вызвана quota/rate limit, tool/MCP failure или approval wall, фиксируй `budget_limited` или `tool_limited`, а не `achieved`.

## Project card в финальном ответе

Для `factory-template` финальный closeout по repo change обязан включать свежую compact project card из repo renderer. Это отдельный обязательный readout перед коротким summary или рядом с ним.

Перед финальным ответом Codex должен выполнить или уже иметь свежий результат:

```bash
python3 template-repo/scripts/render-project-lifecycle-dashboard.py \
  --input template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml \
  --format chatgpt-card \
  --stdout
```

В финальном ответе должен быть раздел `Карточка проекта` и в нем должны присутствовать compact card строки:
- project name / `🏭`;
- lifecycle chain;
- `Модули:`;
- `В работе:`.

Если renderer недоступен или dashboard невалиден, closeout нельзя считать fully done: нужно назвать blocker и не заменять карточку свободным пересказом. Если renderer green, не проси пользователя запускать команду вручную.

Для full handoff orchestration closeout дополнительно проверь beginner UX scorecard:
- один цельный copy-paste handoff block;
- нет file-based handoff вместо inline block;
- нет скрытого второго shell step для оператора;
- нет fake auto-switch claim для already-open live session;
- external/user actions deferred to final closeout;
- blockers named with owner boundary;
- final continuation outcome present;
- Russian human-readable layer present.

Если остается хотя бы один pending external/user step, closeout без блока `## Инструкция пользователю` недопустим.
Если остается future roadmap stage, но он не требует действия пользователя сейчас, closeout должен назвать его как future boundary, а затем отдельно сказать, что текущий scope закрыт полностью.
Если roadmap closeout или roadmap readout содержит несколько возможных следующих веток, closeout должен назвать рекомендованную ветку и fallback-ветку. Нельзя писать только `Следующий пользовательский шаг отсутствует`, если пользователь ожидает roadmap recommendation: эта формула закрывает текущий scope, но не заменяет рекомендацию следующего этапа.

Если closeout, рекомендация или troubleshooting предлагает пользователю конкретный текст для вставки, отправки, поля инструкции, сообщения, команды, URL или handoff, готовый текст должен быть выдан отдельным fenced code block для копирования. Это требование действует даже когда внешнего шага нет и блок `## Инструкция пользователю` не нужен.

Перед тем как отнести GitHub PR merge, закрытие PR или удаление branch к пользовательскому внешнему шагу, Codex обязан проверить доступный GitHub write path:
- `gh auth status` или доступный GitHub connector;
- PR принадлежит текущей задаче или явно входит в ее closeout;
- checks green;
- PR mergeable;
- нет required human review/approval;
- нет конфликтов;
- merge strategy не требует пользовательского выбора.

Если эти условия выполнены, `ready for review`, merge, удаление remote branch, синхронизация local main и cleanup local branch являются внутренней работой Codex. Завершать ответ просьбой к пользователю выполнить такой merge запрещено.

Если хотя бы одно условие не выполнено, в closeout нужно назвать конкретный blocker, а не писать общий внешний шаг.

Если текущая задача создала локальный project repo и следующий естественный шаг — GitHub repo/remote creation:
- сначала проверить `gh auth status` или доступный GitHub connector;
- GitHub repo name должен exactly совпадать с canonical `project_slug`; local repo basename тоже должен совпадать с `project_slug`;
- default visibility: `private`, если explicit release/public policy не говорит иначе;
- owner брать из explicit `--github-owner` / config, иначе из authenticated `gh`/GitHub connector user только при однозначности;
- если owner/name однозначны из project slug или task context, `gh` авторизован и repo не существует, Codex создает GitHub repo, добавляет `origin` и выполняет push сам;
- если repo уже существует и доступен, Codex добавляет `origin` и выполняет push сам;
- если repo уже существует, его можно reuse только когда подтверждено, что это тот же проект;
- нельзя silently append `-2`, `-copy`, дату или random suffix;
- просьба пользователю "создай repo на GitHub и пришли URL" допустима только при конкретном blocker: нет авторизации, нет прав, неоднозначный owner/name, repo name conflict без безопасного решения, local/GitHub naming mismatch или требуется человеческое security/release approval;
- если blocker есть, `## Инструкция пользователю` должна назвать owner/repo, точный URL/команду, ожидаемый результат и что прислать обратно.

Если `origin` настроен, verify green и canonical verified sync технически доступен, closeout без `VERIFIED_SYNC.sh` недопустим.
Вместо этого нужно:
- либо выполнить `VALIDATE_VERIFIED_SYNC_PREREQS.sh` и `VERIFIED_SYNC.sh`;
- либо явно зафиксировать реальный blocker, почему sync сейчас невозможен.

При этих prereqs commit/push не считаются отдельной ручной Git-операцией пользователя.
Ожидаемое поведение: Codex сам доводит change до canonical auto commit + auto push через `VERIFIED_SYNC.sh` или через lightweight follow-up path, если он допустим.

Перед финальным ответом Codex обязан выполнить финальный git sanity-check:
- `git status --short --branch`;
- если branch ahead относительно `origin/*`, выполнить push или назвать конкретный blocker;
- если рабочее дерево содержит незакоммиченные изменения, выполнить canonical sync или назвать конкретный blocker;
- если sync уже был выполнен, проверить, что финальный status чистый и branch не ahead.

Финальный ответ по внутренне закрытому repo change должен назвать commit hash / sync status или прямо сказать, что sync был `no-op`.
Нельзя выдавать финальный done/summary, пока локальный repo остается dirty или ahead без blocker.

Ответ, который при доступном sync заканчивается только summary/done-report без verified sync или без явного blocker, считается неполным closeout.

Closeout без handoff допустим только при реальном отсутствии внутренней работы внутри repo.

Если остаются internal repo follow-up задачи, user-only closeout запрещен. К таким задачам относятся:
- release note / release-facing update внутри repo;
- source-pack и export/manifests refresh;
- brownfield source-candidate map, reconstruction allowlist/denylist, change-map и reverse-engineering closeout внутри repo;
- closeout artifact sync;
- verify-summary / done-summary / release-facing consistency pass;
- release bundle preparation.

Наличие такого внутреннего долга блокирует `done_complete` и требует inline handoff в Codex, а не только инструкцию пользователю.
Если route текущей live-сессии совместим и внутренний follow-up можно выполнить сразу, Codex должен продолжить выполнение вместо финального ответа, который требует от пользователя ручного "продолжай".

Финальный ответ должен явно зафиксировать одно из двух состояний:
- change завершен полностью;
- требуется действие пользователя или внешнее действие.

Если выбран первый вариант, это нельзя оставлять только как подразумеваемое состояние. Финальный текст должен явно сказать, что:
- change завершен полностью;
- внешних действий или следующего пользовательского шага не требуется.

Если change не завершен полностью и есть внешний или пользовательский следующий шаг, финальный ответ обязан иметь раздел `## Инструкция пользователю`. Если внешних действий нет, но внутренний follow-up был невозможен, финальный ответ обязан назвать blocker и сказать, что именно осталось внутри repo.

Финальный человекочитаемый текст для `factory-template` должен быть на русском языке. Английские технические идентификаторы допустимы только как имена команд, файлов, полей, branch, commit, PR, actions или literal values.

Запрещены англоязычные описательные closeout-заголовки и prose-блоки вроде `What Changed`, `Model-Routing Policy`, `Validation`, `Completion Package`, `Known limitation`, если это не буквальное имя внешнего артефакта. Для таких разделов используй русские заголовки: `Что изменено`, `Политика маршрутизации моделей`, `Проверка`, `Completion package / пакет завершения`, `Известные ограничения`.

Если `factory-template ChatGPT Project instruction` не требует обновления, формулируй это как отсутствие действия: `обновление инструкции factory-template ChatGPT Project не требуется`. Нельзя писать так, будто нужен handoff обратно в ChatGPT или отдельный внешний шаг.

Если есть и внутренние, и внешние шаги, финальный ответ должен явно разделять:
- внутренний follow-up handoff;
- внешний boundary step с блоком `## Инструкция пользователю`.

Если внешний boundary step связан с repo-first instruction/update flows, сначала определи реальные действия пользователя.
Если реальных действий нет, closeout считается полным с короткой строкой `Внешних действий не требуется.` без таблицы всех contour'ов.
Если реальные внешние действия есть, closeout считается полным только если `## Инструкция пользователю` явно покрывает эти actionable contour'ы:
- factory-template ChatGPT Project instruction;
- downstream repo template sync;
- downstream/battle ChatGPT Project instructions.

Такой блок должен содержать отдельный `Реестр внешних действий` или эквивалентную таблицу. Для каждого включенного actionable contour обязательно указать:
- статус: `требуется`, `рекомендуется`, `опционально` или `только legacy/hybrid fallback`;
- причину статуса;
- точное действие пользователя;
- когда выполнять действие: сейчас, при следующем downstream sync, только для legacy/hybrid fallback или не выполнять.

Общая фраза вроде "downstream sync рекомендуется" без отдельной actionable строки не считается достаточным external boundary closeout.
Запрещено перечислять contour'ы со статусом `не требуется`, если пользователь явно не запросил полный audit-style register или задача не является release/security approval.
Если все потенциальные строки реестра имеют `действие не требуется`, реестр не нужен; напиши `Внешних действий не требуется.` и fully-done continuation outcome.
При no-op external closeout не останавливайся на этой одной фразе: добавь continuation outcome, что следующий пользовательский шаг отсутствует и текущие задачи выполнены полностью.
Если no-op external closeout завершает roadmap stage, добавь next-roadmap recommendation: например `если есть real downstream/battle app, следующий шаг P4-S5/P4-S6; если нет, следующий repo-local шаг Plan №5 / hardening contour`.

Для `factory-template ChatGPT Project instruction` по умолчанию ожидается `нет`, если repo/path/entrypoint/короткая repo-first instruction не менялись.
Отдельное обновление этого contour допустимо только при реальном изменении instruction contract.

Для `downstream/battle ChatGPT Project instructions` по умолчанию ожидается `нет`, если battle repo уже живет в чистом repo-first режиме.
Отдельное обновление этого contour допустимо только как legacy/hybrid fallback.

Перед таким closeout Codex обязан сам выполнить внутренний repo prep: boundary-actions generation, текстовую нормализацию инструкции и другую сборку артефактов, если она нужна для внешнего шага. Ответ, который вместо этого отправляет пользователя запускать внутренние repo-команды, считается неполным closeout.

Если замена может создать устаревшие дубликаты в project instruction или reference/export наборе, в блоке `## Инструкция пользователю` обязателен отдельный подраздел `Удалить перед заменой` с точными именами файлов или архивов.

Closeout не считается завершенным, если обязательный внешний completion package был выдан не сразу, а только после дополнительного напоминания пользователя. Такой ответ считается неполным closeout и требует remediation.

## Closeout rule для побочного дефекта
Если в ходе основной задачи был найден incidental / side bug, финальный closeout обязан явно зафиксировать один из исходов:
- defect исправлен в текущем scope и отражен в done/verification closeout;
- defect не исправлен, но подготовлены bug report + self-handoff, а route подтвержден как совместимый с текущим chat;
- defect не исправлен, подготовлены bug report + self-handoff, и как канонический следующий шаг рекомендован новый task launch / новая Codex chat-сессия через явный launch command из-за другого route;
- defect требует deep research, и вместо remediation-handoff подготовлен ChatGPT-ready research bug report/prompt.

Unresolved incidental defect нельзя оставлять только в narrative summary. В closeout должны быть явно перечислены:
- где лежит bug report;
- был ли выполнен self-handoff;
- можно ли продолжать в текущем chat или нужен новый task launch;
- если выбран non-canonical fallback `продолжить в этом чате`, это должно быть помечено как fallback, а не как равноправный canonical path.
