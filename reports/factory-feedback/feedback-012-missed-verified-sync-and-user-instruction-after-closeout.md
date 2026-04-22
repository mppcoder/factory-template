# Factory Feedback: closeout can still miss verified sync and same-response user instruction

## Исходный bug report
`reports/bugs/bug-012-missed-verified-sync-and-user-instruction-after-closeout.md`

## Почему это проблема фабрики
Фабрика уже содержит правила про mandatory verified sync, immediate `## Инструкция пользователю` и defect capture for reusable process failures. Но реальный execution pass всё равно завершился раньше canonical closeout boundary. Значит, rule presence сама по себе ещё не гарантирует process compliance в actual response behavior.

## Где проявилось
`factory-template`, remediation -> verification -> done closeout flow, repo-first instruction update contour.

## Повторяемый паттерн
- remediation и local verification завершены;
- downstream-affected change уже требует completion package;
- verified sync technically available;
- но модель всё равно может остановиться на summary without sync and without same-response user instruction;
- defect capture happens only after the user points out the miss.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- scenario-pack closeout rules
- runbook / AGENTS enforcement layer
- `.chatgpt` closeout artifacts
- verified sync discipline
- reusable defect-capture discipline

## Как проверить исправление
1. Для change с green verify и configured remote final closeout automatically runs canonical verified sync or explicitly explains the real blocker.
2. Если change затрагивает downstream-consumed content, `## Инструкция пользователю` появляется в том же финальном ответе без follow-up reminder.
3. Если такое правило всё же нарушено, defect capture создаётся immediately in the same remediation/closeout turn, а не только после отдельного напоминания пользователя.

## Статус
исправлено в source-of-truth repo через DoD/checklist/closeout guardrails.
