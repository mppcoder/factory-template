# Отчет о дефекте

## Идентификатор
bug-035-closeout-stopped-before-internal-followup-and-user-instruction

## Краткий заголовок
Closeout остановился перед внутренним brownfield follow-up и не выдал обязательный пользовательский completion package.

## Где найдено

Repo: `factory-template`

Слои:
- brownfield closeout;
- direct-task self-handoff;
- completion / boundary actions;
- generated `.chatgpt/direct-task-response.md`;
- Codex routing validator.

## Шаги воспроизведения

1. Запустить полевой тест `brownfield-without-repo` для `/root/.openclaw` и `/root/openclaw-plus`.
2. Завершить intake-артефакты и явно назвать следующий безопасный внутренний этап: `source-candidate-map`.
3. Отправить финальный summary без выполнения `source-candidate-map`.
4. Не добавить `## Инструкция пользователю`, хотя ответ фактически оставил следующий шаг пользователю.
5. Дождаться follow-up пользователя: "продолжай, почему остановился?"

## Ожидаемое поведение

- Если следующий шаг является internal Codex-eligible follow-up и текущий route совместим, Codex продолжает выполнение в том же task.
- Если нужен новый task launch, Codex выдает один цельный inline handoff.
- Если остается внешний или пользовательский шаг, финальный ответ завершается `## Инструкция пользователю`.
- Если внешних действий нет, финальный ответ явно говорит: `Внешних действий не требуется.`

## Фактическое поведение

- Ответ остановился на summary после intake.
- Следующий внутренний этап `source-candidate-map` был оставлен как будущий шаг.
- Обязательный пользовательский completion package отсутствовал.
- Пользователь был вынужден вручную написать "продолжай".

## Evidence

- [REAL] Follow-up пользователя: "продолжай, почему остановился? Исправь баг остановки, требующей ручного продолжения. Исправь баг отсутсвия инструкции пользователю по дальнейшим действиям."
- [PROJECT] `brownfield/reverse-engineering-summary.md` и `.chatgpt/reality-check.md` после intake называли следующий безопасный этап `source-candidate-map`.
- [PROJECT] `template-repo/scripts/codex_task_router.py` генерировал direct-task response в legacy self-handoff формате с финальной формулировкой "Только после этого блока допустимы remediation / implementation / verification", что не защищало от остановки.
- [PROJECT] `template-repo/scripts/validate-codex-routing.py` проверял legacy-маркеры direct-task response, но не требовал publishable handoff block, continuation rule и closeout instruction rule.

## Классификация слоя

`factory-template`

## Нужен ли feedback в фабрику

Да. Это reusable process defect: правила уже существовали, но generator/validator не предотвращали остановку и отсутствие финального пользовательского блока.

## Исправление

- `render_direct_task_response` теперь генерирует publishable sections `## Применение в Codex UI`, `## Строгий launch mode (опционально)`, `## Handoff в Codex`.
- Direct-task handoff явно запрещает завершать ответ только self-handoff block при совместимом route.
- Direct-task handoff явно требует `## Инструкция пользователю` при внешнем шаге и фразу `Внешних действий не требуется.` при полностью внутреннем closeout.
- `validate-codex-routing.py` закрепляет эти требования.
- Scenario-pack и generated boundary/done checklist расширены для brownfield source-candidate internal follow-up.

## Статус

исправлено в текущем scope
