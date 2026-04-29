# Чеклист: путь с существующим repo

| ID | Статус [ ] | Окно | Кто делает | Действие | Команда / UI path | Ожидаемый результат | Evidence | Следующий шаг |
|---|---|---|---|---|---|---|---|---|
| BWR-000 | [ ] | Browser GitHub / ChatGPT | Пользователь | Зафиксировать existing repo, target root и default decisions | `existing_repo: <repo-owner>/<repo-name>` plus accepted/overridden defaults | Canonical root определен; defaults accepted or overridden | Repo URL + root + default decision state | BWR-010 |
| BWR-010 | [ ] | Browser GitHub / ChatGPT | Пользователь | Дать repo access и approvals | GitHub connector/permissions/protected branch review | Access boundary ясен | Access state или blocker | BWR-020 |
| BWR-020 | [ ] | Remote Codex chat/window | Пользователь | Вставить one-block handoff | Новый remote Codex chat/window -> paste one block | Codex начинает audit/adoption/conversion | Route receipt | CODEX-AUTOMATION |
