# Чеклист: greenfield-product

| ID | Статус [ ] | Окно | Кто делает | Действие | Команда / UI path | Ожидаемый результат | Evidence | Следующий шаг |
|---|---|---|---|---|---|---|---|---|
| GF-000 | [ ] | Browser ChatGPT / заметки | Пользователь | Выбрать название проекта | `Название проекта: <PROJECT_NAME>` | Название проекта выбрано | `<PROJECT_NAME>` | GF-010 |
| GF-010 | [ ] | Remote Codex chat/window | Пользователь | Сообщить Codex название и идею | Paste block из `GF-010` | Codex начинает создавать repo/root/core/verify/sync | Route receipt или remote automation start | GF-020 |
| GF-020 | [ ] | Browser ChatGPT | Пользователь | Создать ChatGPT Project в UI | ChatGPT -> Projects -> New project -> `<PROJECT_NAME>` | Пустой Project создан | Project exists | GF-030 |
| GF-030 | [ ] | Browser ChatGPT Project settings | Пользователь | Вставить готовую repo-first инструкцию | Paste instruction text, подготовленный Codex | Project instructions сохранены | Saved instruction | STOP |
