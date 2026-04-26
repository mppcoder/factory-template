# Factory feedback 035: closeout stopped before internal follow-up and missed user instruction

Дата: 2026-04-26
Источник: `reports/bugs/bug-035-closeout-stopped-before-internal-followup-and-user-instruction.md`
Слой: `factory-template`
Статус: исправлено

## Суть

Полевой brownfield тест показал, что closeout может остановиться после intake, хотя следующий шаг `source-candidate-map` является внутренней Codex-eligible работой. Одновременно финальный ответ может не дать `## Инструкция пользователю`, хотя фактически оставляет продолжение пользователю.

## Почему это reusable defect

Правила про internal follow-up и mandatory user instruction уже были в scenario-pack, но generator/validator не закрепляли их на уровне direct-task response:
- старый self-handoff формат не был publishable handoff package;
- continuation rule был неявным;
- финальный closeout rule не был видим в generated direct-task response;
- brownfield source-candidate follow-up не был явно назван в списке internal follow-up examples.

## Требование к фабрике

- Direct-task self-handoff должен быть стартовым gate, а не точкой остановки.
- Если route совместим, Codex должен продолжать внутреннюю работу без ручного "продолжай".
- Если внешний шаг остается, финальный ответ обязан завершаться `## Инструкция пользователю`.
- Если внешнего шага нет, финальный ответ обязан явно сказать, что внешних действий не требуется.
- Brownfield source-candidate map / reconstruction allowlist / denylist / change-map должны считаться internal follow-up.

## Проверка исправления

- `bootstrap-codex-task.py` генерирует `.chatgpt/direct-task-response.md` с publishable handoff sections.
- `validate-codex-routing.py` падает, если direct-task response не содержит continuation guardrail и closeout instruction guardrail.
- `validate-codex-task-pack.py` проверяет boundary/done checklist на запрет ручного "продолжай" для internal follow-up.
