# Чеклист: путь без repo

| ID | Статус [ ] | Окно | Кто делает | Действие | Команда / UI path | Ожидаемый результат | Evidence | Следующий шаг |
|---|---|---|---|---|---|---|---|---|
| BWO-000 | [ ] | Browser ChatGPT / Explorer / VS Code | Пользователь | Зафиксировать target root, incoming boundary и default decisions | `project_root: /projects/<project-slug>` plus accepted/overridden defaults | `_incoming` внутри target root; defaults accepted or overridden | Target root + incoming source + default decision state | BWO-010 |
| BWO-005 | [ ] | Browser ChatGPT / VS Code Remote SSH | Пользователь | Указать non-standard VPS folders без repo, если проект уже лежит вне стандарта | `nonstandard_vps_folder_intake` with absolute paths and roles | Folders treated as intake/evidence candidates, not active source roots | Paths + role map without secrets | BWO-010 |
| BWO-010 | [ ] | VS Code Remote SSH / upload tool | Пользователь | Разместить материалы в `_incoming` | `mkdir -p /projects/<project-slug>/_incoming`; upload files | Материалы доступны Codex | `ls -la _incoming` | BWO-020 |
| BWO-020 | [ ] | Remote Codex chat/window | Пользователь | Вставить one-block handoff | Новый remote Codex chat/window -> paste one block | Codex начинает reconstruction/conversion | Route receipt | CODEX-AUTOMATION |
