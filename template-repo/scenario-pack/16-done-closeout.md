# Закрытие цикла

После завершения работы обнови:
- `CURRENT_FUNCTIONAL_STATE.md`;
- `project-knowledge/`;
- `verification-report.md`;
- `done-report.md`;
- `work/completed/`.

## Правило closeout
Если change завершен полностью и внешних действий больше нет, допустим короткий closeout без блока `Инструкция пользователю`.

Если остается хотя бы один pending external/user step, closeout без блока `## Инструкция пользователю` недопустим.

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

Если есть и внутренние, и внешние шаги, финальный ответ должен явно разделять:
- внутренний follow-up handoff;
- внешний boundary step с блоком `## Инструкция пользователю`.

Если внешний boundary step связан с source update flows, closeout считается полным только если `## Инструкция пользователю` явно покрывает все затронутые contour'ы:
- factory-template ChatGPT Project Sources;
- downstream repo template sync;
- downstream/battle ChatGPT Project Sources.

Если replacement в Sources может создать stale duplicates, в блоке `## Инструкция пользователю` обязателен отдельный подраздел `Удалить перед заменой` с точными именами файлов или архивов.
