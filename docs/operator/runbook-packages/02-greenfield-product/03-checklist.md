# Чеклист: greenfield-product

| ID | Статус [ ] | Окно | Кто делает | Действие | Команда / UI path | Ожидаемый результат | Evidence | Следующий шаг |
|---|---|---|---|---|---|---|---|---|
| GF-000 | [ ] | Browser ChatGPT / GitHub | Пользователь | Зафиксировать project slug, repo и root | `project_preset: greenfield-product` | Target root `/projects/<project-slug>` определен | Project slug и repo URL | GF-010 |
| GF-010 | [ ] | Browser GitHub / ChatGPT | Пользователь | Подготовить external access | GitHub repo/access + ChatGPT connector | Repo/access/approvals готовы или blocker известен | Repo URL или blocker | GF-020 |
| GF-020 | [ ] | Remote Codex chat/window | Пользователь | Вставить один handoff | Новый remote Codex chat/window -> paste one block | Codex начинает automation | Remote shell check | CODEX-AUTOMATION |
