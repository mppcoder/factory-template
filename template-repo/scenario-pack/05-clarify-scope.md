# Уточнение границ проекта

Используй выбранный `default_decision_mode` из discovery. Если режим еще не выбран, сначала задай вопрос default-decision layer из `04-discovery-new-project.md`.

Вопросы о границах должны быть recommendation-first, если safe default существует:

- покажи вопрос;
- покажи recommended default;
- объясни, почему он подходит, в 1-2 короткие строки;
- явно напиши, что Enter/`по умолчанию` принимает рекомендацию;
- явно напиши, как указать свой вариант.

Не считай recommended default истиной. Фиксируй source basis: `repo-policy`, `official-docs`, `best-practice`, `project-scale` или `user-override`. Если решение требует свежей проверки, добавь `requires fresh check` в `uncertainty_notes`.

Сформулируй:
- что входит в объем;
- что не входит в объем;
- что требует отдельного согласования.

В `decisions_requiring_user_confirmation` оставляй только реальные внешние/рискованные решения: paid, destructive, security, privacy, legal, secret-related, production deploy или irreversible migration.
