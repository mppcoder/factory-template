# Direct Codex Self-Handoff

Если задача пришла в Codex напрямую, без handoff из ChatGPT Project, direct task не должен сразу переходить к коду.

## Обязательный порядок
1. Открыть `00-master-router.md`.
2. Классифицировать задачу.
3. Зафиксировать `project profile`, `scenario`, `pipeline stage`, `artifacts to update`, `handoff allowed`.
4. Если задача defect-class: пройти defect-capture path.
5. Запустить executable router для выбора `task_class` и `selected_profile`.
6. Зафиксировать launch record в `.chatgpt/task-launch.yaml`.
7. Сформировать `.chatgpt/direct-task-self-handoff.md`.
8. Сформировать готовый visible self-handoff block для стартового ответа Codex.
9. Только после этого переходить к remediation / implementation / review.

## Важное ограничение
Нельзя считать старую уже открытую сессию Codex надежной единицей маршрутизации.
Self-handoff и profile selection должны быть привязаны к новому task launch boundary.

## Правило visible gate
Для direct task self-handoff должен быть видим пользователю в первом substantive ответе Codex.
Недостаточно только записать `.chatgpt/direct-task-self-handoff.md` или молча держать классификацию в памяти.
