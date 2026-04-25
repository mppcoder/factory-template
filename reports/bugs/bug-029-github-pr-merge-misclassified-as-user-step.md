# Отчет о дефекте

## Идентификатор
bug-029-github-pr-merge-misclassified-as-user-step

## Краткий заголовок
Доступное слияние GitHub PR было ошибочно переложено на пользователя как внешний шаг.

## Тип дефекта
reusable-process-defect

## Где найдено
- Финальный closeout после сводного исправления GitHub Actions workflow.
- Сценарный слой `template-repo/scenario-pack/00-master-router.md`.
- Сценарный слой `template-repo/scenario-pack/16-done-closeout.md`.
- Generated boundary guidance `.chatgpt/boundary-actions.md`.

## Шаги воспроизведения
1. Завершить remediation внутри repo.
2. Открыть GitHub PR, созданный текущей задачей.
3. Убедиться, что `gh` авторизован, PR доступен для merge, checks green и нет обязательного человеческого approval.
4. Завершить ответ просьбой к пользователю вручную review/merge PR.
5. После замечания пользователя выполнить тот же PR merge через доступный `gh`.

## Ожидаемое поведение
- Если GitHub write path доступен, checks green, PR доступен для merge и нет review/policy blocker, Codex сам выполняет перевод из draft, merge, удаление branch и local sync.
- Пользовательский внешний шаг допустим только при конкретном blocker: нет авторизации, нет прав, required human review, red/pending checks, конфликт, неясная merge strategy, release/security approval или другой UI-only шаг.
- Финальный closeout должен сообщать уже выполненное действие, а не просить пользователя выполнить внутренне доступный merge.

## Фактическое поведение
- PR #4 был доступен для merge, checks green, `gh` был доступен и авторизован.
- Codex сначала попросил пользователя review/merge PR #4 вручную.
- После прямого запроса пользователя Codex выполнил `gh pr ready`, `gh pr merge --squash --delete-branch`, `git pull --ff-only` и cleanup local branch без блокеров.

## Evidence
- [REAL] PR #4 был успешно merged через `gh` после дополнительного запроса пользователя.
- [REAL] Merge commit: `48d8ee52ba42d56ba8cd1178f6ade91d5d6ee23c`.
- [PROJECT] Open PR list после merge пуст.
- [PROJECT] Local `main` синхронизирован с `origin/main`.

## Слой дефекта
factory-template

## Классификация failing layer
closeout / GitHub boundary classification / user-action leakage

## Связь с текущим scope
fixed-in-current-scope

## Self-handoff решение
current-route-valid

## Решение / статус
fixed
