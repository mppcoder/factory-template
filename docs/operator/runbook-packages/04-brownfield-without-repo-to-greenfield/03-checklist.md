# Чеклист: путь без repo

| ID | Статус [ ] | Окно | Кто делает | Действие | Команда / UI path | Ожидаемый результат | Evidence | Следующий шаг |
|---|---|---|---|---|---|---|---|---|
| BWO-000 | [ ] | Browser ChatGPT / Explorer / VS Code | Пользователь | Зафиксировать target root и incoming boundary | `project_root: /projects/<project-slug>` | `_incoming` внутри target root | Target root + incoming source | BWO-010 |
| BWO-010 | [ ] | VS Code Remote SSH / upload tool | Пользователь | Разместить материалы в `_incoming` | `mkdir -p /projects/<project-slug>/_incoming`; upload files | Материалы доступны Codex | `ls -la _incoming` | BWO-020 |
| BWO-020 | [ ] | Remote Codex chat/window | Пользователь | Вставить one-block handoff | Новый remote Codex chat/window -> paste one block | Codex начинает reconstruction/conversion | Route receipt | CODEX-AUTOMATION |
