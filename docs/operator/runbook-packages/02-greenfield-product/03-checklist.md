# Чеклист: greenfield-product

| ID | Статус [ ] | Окно | Кто делает | Действие | Команда / UI path | Ожидаемый результат | Evidence | Следующий шаг |
|---|---|---|---|---|---|---|---|---|
| GF-000 | [ ] | Browser ChatGPT / VS Code / Codex app | Пользователь | Проверить стартовое состояние | Factory-template verified, contour готов | Пользователь в ChatGPT Project шаблона фабрики | Factory Project открыт | GF-005 |
| GF-005 | [ ] | ChatGPT Project шаблона фабрики | Пользователь | Открыть новый чат | Project `factory-template` -> New chat | Новый чат открыт внутри factory-template Project | Видно имя Project | GF-010 |
| GF-010 | [ ] | Новый чат factory-template Project | Пользователь | Ввести trigger command | `новый проект` | ChatGPT начинает scenario-pack опрос | Ответ с вопросами | GF-020 |
| GF-020 | [ ] | Новый чат factory-template Project | Пользователь | Пройти опрос | Ответить: название, идея, тип, readiness, contour, blockers | Опрос завершен | Ответы в чате | GF-030 |
| GF-030 | [ ] | Factory ChatGPT Project / runbook | Пользователь + ChatGPT Project | Проверить readiness checklist | Сверить Codex/VPS/SSH/GitHub readiness | Ready или возврат в setup runbook | Readiness state | GF-040 |
| GF-040 | [ ] | Factory ChatGPT Project | ChatGPT Project | Сформировать стартовый Codex handoff | One-block handoff после опроса | Handoff содержит project data, readiness, contour, boundary | Handoff block | GF-050 |
| GF-050 | [ ] | Remote Codex chat/window | Пользователь | Вставить handoff в Codex | Новый Codex chat/window -> paste one block | Codex выводит handoff receipt | Handoff receipt | GF-060 |
| GF-060 | [ ] | Remote Codex chat/window | Codex | Выполнить project automation | Codex создает repo/root/core/verify/sync | Automation green или blocker | Repo URL, verify, sync | GF-070 |
| GF-070 | [ ] | Remote Codex chat/window | Codex | Вернуть repo-first instruction | Финальный closeout Codex | Готовая instruction получена | Instruction block | GF-080 |
| GF-080 | [ ] | Browser ChatGPT | Пользователь | Создать ChatGPT Project боевого проекта | ChatGPT -> Projects -> New project | Боевой Project создан | Project exists | GF-090 |
| GF-090 | [ ] | Battle ChatGPT Project settings | Пользователь | Вставить repo-first instruction | Paste instruction from Codex | Instruction сохранена | Saved instruction | GF-100 |
| GF-100 | [ ] | Battle ChatGPT Project | Пользователь | Начать дальнейшую работу в боевом Project | Новый чат в battle Project | Project следует repo-first правилам | First repo-first response | STOP |
