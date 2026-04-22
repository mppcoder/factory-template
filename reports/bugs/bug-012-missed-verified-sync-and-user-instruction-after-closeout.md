# Отчет о дефекте

## Идентификатор
bug-012-missed-verified-sync-and-user-instruction-after-closeout

## Краткий заголовок
Factory-template process still allowed a closeout response that stopped before mandatory verified sync and emitted `## Инструкция пользователю` only after a follow-up question.

## Где найдено
Repo: `factory-template`, reusable closeout / verified-sync / boundary-output layer:

- final response after remediation
- verified sync follow-up discipline
- mandatory `## Инструкция пользователю` rule
- defect-capture compliance for reusable process failures

## Шаги воспроизведения
1. Выполнить change в `factory-template`, который затрагивает downstream-consumed docs/runbook/template content.
2. Дойти до локального verification и обновить closeout artifacts.
3. Завершить ответ summary без немедленного запуска canonical `VERIFIED_SYNC.sh`, хотя prereqs already green и remote configured.
4. Не выдать `## Инструкция пользователю` в том же финальном ответе, несмотря на pending external update contours.
5. Дождаться, пока пользователь отдельно спросит, почему auto commit/push и дальнейшая инструкция не были сделаны.

## Ожидаемое поведение
- После green verify и допустимого diff Codex должен сам пройти canonical verified sync path без отдельного напоминания пользователя.
- Если change затрагивает repo-first instruction layer или downstream template consumers, финальный ответ должен в том же сообщении содержать `## Инструкция пользователю` с completion package.
- Если это правило нарушено, reusable process defect должен быть явно зафиксирован.

## Фактическое поведение
- Change был локально завершён и верифицирован, но canonical verified sync не был выполнен в основном closeout flow.
- Обязательный внешний next step не был выдан в том же финальном ответе.
- Исправление произошло только после follow-up вопроса пользователя, когда были вручную запущены `VALIDATE_VERIFIED_SYNC_PREREQS.sh` и `VERIFIED_SYNC.sh`, а затем добавлена инструкция пользователю.

## Evidence
- [PROJECT] Пользовательский вопрос: почему по завершении задачи не был сделан auto commit/push и не была выдана инструкция для дальнейших действий пользователя.
- [PROJECT] Фактический verified sync был выполнен только после follow-up:
  - `bash VALIDATE_VERIFIED_SYNC_PREREQS.sh`
  - `bash VERIFIED_SYNC.sh`
  - commit: `4682aafb621c301995ff6a5ec1e05234803da7e2`
- [PROJECT] Scenario/runbook rules already required both behaviors:
  - `template-repo/scenario-pack/00-master-router.md`
  - `template-repo/scenario-pack/01-global-rules.md`
  - `template-repo/scenario-pack/16-done-closeout.md`
  - `factory_template_only_pack/02-runbook-dlya-codex-factory-template.md`
  - `factory_template_only_pack/07-AGENTS-factory-template.md`

## Затронутый слой
factory-template

## Нужен ли feedback в фабрику
Да, потому что это reusable process failure в source-of-truth repo фабрики: existing rules were present, but execution still escaped the required closeout path.

## Статус
исправлен
