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

Если остается хотя бы один pending external/user step, closeout без блока `## Инструкция пользователю` недопустим.

Если `origin` настроен, verify green и canonical verified sync технически доступен, closeout без `VERIFIED_SYNC.sh` недопустим.
Вместо этого нужно:
- либо выполнить `VALIDATE_VERIFIED_SYNC_PREREQS.sh` и `VERIFIED_SYNC.sh`;
- либо явно зафиксировать реальный blocker, почему sync сейчас невозможен.

При этих prereqs commit/push не считаются отдельной ручной Git-операцией пользователя.
Ожидаемое поведение: Codex сам доводит change до canonical auto commit + auto push через `VERIFIED_SYNC.sh` или через lightweight follow-up path, если он допустим.

Ответ, который при доступном sync заканчивается только summary/done-report без verified sync или без явного blocker, считается неполным closeout.

Closeout без handoff допустим только при реальном отсутствии внутренней работы внутри repo.

Если остаются internal repo follow-up задачи, user-only closeout запрещен. К таким задачам относятся:
- release note / release-facing update внутри repo;
- source-pack и export/manifests refresh;
- closeout artifact sync;
- verify-summary / done-summary / release-facing consistency pass;
- release bundle preparation.

Наличие такого внутреннего долга блокирует `done_complete` и требует inline handoff в Codex, а не только инструкцию пользователю.

Финальный ответ должен явно зафиксировать одно из двух состояний:
- change завершен полностью;
- требуется действие пользователя или внешнее действие.

Если выбран первый вариант, это нельзя оставлять только как подразумеваемое состояние. Финальный текст должен явно сказать, что:
- change завершен полностью;
- внешних действий или следующего пользовательского шага не требуется.

Если есть и внутренние, и внешние шаги, финальный ответ должен явно разделять:
- внутренний follow-up handoff;
- внешний boundary step с блоком `## Инструкция пользователю`.

Если внешний boundary step связан с repo-first instruction/update flows, closeout считается полным только если `## Инструкция пользователю` явно покрывает все затронутые contour'ы:
- factory-template ChatGPT Project instruction;
- downstream repo template sync;
- downstream/battle ChatGPT Project instructions.

Перед таким closeout Codex обязан сам выполнить внутренний repo prep: boundary-actions generation, текстовую нормализацию инструкции и другую сборку артефактов, если она нужна для внешнего шага. Ответ, который вместо этого отправляет пользователя запускать внутренние repo-команды, считается неполным closeout.

Если replacement может создать stale duplicates в project instruction или reference/export наборе, в блоке `## Инструкция пользователю` обязателен отдельный подраздел `Удалить перед заменой` с точными именами файлов или архивов.

Closeout не считается завершенным, если обязательный внешний completion package был выдан не сразу, а только после дополнительного напоминания пользователя. Такой ответ считается неполным closeout и требует remediation.

## Incidental defect closeout rule
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
