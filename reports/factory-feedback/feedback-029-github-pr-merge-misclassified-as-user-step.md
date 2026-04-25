# Factory Feedback: доступный GitHub PR merge не должен становиться пользовательским шагом

## Исходный bug report
`reports/bugs/bug-029-github-pr-merge-misclassified-as-user-step.md`

## Почему это проблема фабрики
Фабрика уже различает внутреннюю repo-работу и внешние пользовательские границы, но правило было слишком грубым: `GitHub UI` мог автоматически восприниматься как внешний шаг даже тогда, когда `gh` или GitHub connector позволяли безопасно завершить PR closeout.

## Где проявилось
`factory-template`, closeout после сводного исправления GitHub Actions workflow.

## Повторяемый паттерн
- PR создан текущей задачей;
- checks green;
- PR доступен для merge;
- GitHub write path доступен;
- required human approval отсутствует;
- Codex вместо merge просит пользователя выполнить GitHub UI step.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- closeout behavior
- GitHub boundary classification
- operator guidance
- automation-first completion semantics

## Как проверить исправление
1. Перед пользовательским GitHub closeout Codex проверяет доступность `gh`/GitHub connector, состояние checks, mergeability и blockers.
2. Если blockers нет, Codex сам выполняет ready/merge/delete-branch/local sync.
3. Если blocker есть, финальный ответ называет конкретную причину, почему действие осталось внешним.

## Статус
fixed
