# Отчет о дефекте

## Идентификатор
bug-003-inline-handoff-and-user-instruction-gap

## Краткий заголовок
Scenario-pack и process docs допускают ответ с аналитикой вместо готового handoff и не делают финальный блок `Инструкция пользователю` обязательным при pending external/user step.

## Где найдено
Repo: `factory-template`, reusable process layer:

- `template-repo/scenario-pack/`
- `docs/operator/factory-template/`
- policy manifests и boundary-actions generation

## Шаги воспроизведения
1. Дойти до состояния, где `codex_handoff_allowed` уже закрыт и задача достаточно определена.
2. Сформировать ответ через router/policy/handoff path.
3. Проверить, требует ли процесс в том же ответе выдать готовый handoff.
4. Сформировать ответ, где нужен следующий шаг пользователя или внешнее действие.
5. Проверить, делает ли process layer обязательным финальный блок `Инструкция пользователю`.

## Ожидаемое поведение
- Если handoff уже допустим и задача достаточно определена, ChatGPT обязан выдать готовый inline handoff в том же ответе.
- Если в ответе остается pending external/user step, обязателен финальный блок `## Инструкция пользователю` с канонической структурой.

## Фактическое поведение
- Router требует указать, разрешен ли handoff, но не требует жестко выдать сам handoff в том же ответе.
- Runbook и boundary guidance говорят о пошаговых инструкциях, но не фиксируют единый обязательный финальный блок `Инструкция пользователю` на уровне scenario-pack и manifests.

## Evidence
- [PROJECT] `template-repo/scenario-pack/00-master-router.md` требовал статус handoff, но не требовал inline handoff в том же ответе.
- [PROJECT] `template-repo/scenario-pack/15-handoff-to-codex.md` содержал только precheck перед handoff.
- [PROJECT] `template-repo/scenario-pack/16-done-closeout.md` не запрещал closeout без финального user-instruction блока при pending external/user step.
- [PROJECT] runbook/AGENTS и boundary-actions partial guidance уже подразумевали инструкции пользователю, но без единой обязательной финальной нормы.

## Затронутый слой
factory-template

## Нужен ли feedback в фабрику
Нет, потому что defect найден и исправляется прямо в source-of-truth repo фабрики.

## Исправление
- добавить обязательное правило inline handoff в router / decision policy / handoff rules;
- добавить обязательное правило финального блока `Инструкция пользователю` в scenario-pack, runbook, AGENTS, manifests и boundary-actions generation;
- зафиксировать defect как reusable process remediation в repo.

## Статус
исправляется
