# Отчет о дефекте

## Идентификатор
bug-006-internal-followup-misclassified-as-user-closeout

## Краткий заголовок
Factory-template мог ошибочно переводить внутренний release-followup в user-only closeout после remediation/push.

## Где найдено
Repo: `factory-template`, reusable process / closeout semantics layer:

- router
- decision policy
- handoff rules
- done/closeout rules
- runbook / AGENTS / codex task pack guidance

## Ожидаемое поведение
- Если после remediation, verify или push остаются внутренние Codex-eligible задачи внутри repo, ответ должен выдавать inline handoff в том же ответе.
- User-only closeout допустим только для реальных внешних границ.
- При mixed follow-up сначала должен идти внутренний handoff, затем отдельная инструкция пользователю только на внешний шаг.

## Фактическое поведение
- Модель могла трактовать remaining release-followup и closeout-sync как внешний следующий шаг.
- В результате ответ завершался только блоком `Инструкция пользователю`, хотя внутренняя repo-работа еще не была закрыта.

## Evidence
- [PROJECT] Router и done-closeout ранее фиксировали inline handoff и footer раздельно, но не задавали явный precedence rule для internal repo follow-up.
- [PROJECT] Boundary/handoff guidance не запрещала user footer вытеснять внутренний release-followup handoff.

## Затронутый слой
factory-template

## Нужен ли feedback в фабрику
Нет, потому что дефект найден и исправляется в source-of-truth repo самой фабрики.

## Статус
исправлен
