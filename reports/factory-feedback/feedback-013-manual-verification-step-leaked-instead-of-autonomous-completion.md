# Factory Feedback: internal verification can still leak into user instructions

## Исходный bug report
`reports/bugs/bug-013-manual-verification-step-leaked-instead-of-autonomous-completion.md`

## Почему это проблема фабрики
Фабрика уже различает internal repo work и реальные внешние boundary actions. Но assistant всё ещё может в финальном ответе предложить пользователю ручной verification "на всякий случай", даже когда этот verification должен быть completed autonomously inside the repo. Это размывает границу ответственности и увеличивает операторскую нагрузку без причины.

## Где проявилось
`factory-template`, post-remediation closeout after root-level routing/config fix.

## Повторяемый паттерн
- internal fix уже выполнен;
- verification commands доступны assistant directly;
- external blocker отсутствует;
- вместо финального automation summary пользователю предлагается manual verification step;
- пользователь вынужден напоминать, что internal checks должны выполняться самим assistant.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- closeout behavior
- boundary discipline
- operator guidance
- automation-first completion semantics

## Как проверить исправление
1. Если internal verification может быть выполнен assistant inside repo, он выполняется до финального ответа без перекладывания на пользователя.
2. `## Инструкция пользователю` не содержит optional manual verification commands для внутренней repo-работы.
3. Финальный ответ сообщает already-completed verification result instead of asking the user to rerun it manually.

## Статус
зафиксировано
