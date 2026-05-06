# Self-handoff для прямой задачи в Codex

Если задача пришла в Codex напрямую, без handoff из ChatGPT Project, direct task не должен сразу переходить к коду.

Этот сценарий не применяется к `launch_source: chatgpt-handoff`. Для готового ChatGPT handoff Codex исполняет входящий handoff, а в первом ответе может дать только `handoff receipt` / `route receipt` без создания нового self-handoff.

## Обязательный порядок
1. Открыть `00-master-router.md`.
2. Классифицировать задачу.
3. Зафиксировать `project profile`, `scenario`, `pipeline stage`, `artifacts to update`, `handoff allowed`.
4. Если задача defect-class: пройти defect-capture path.
5. Запустить executable router для выбора `task_class` и `selected_profile`.
6. Выделить visible Codex request identity в `.chatgpt/codex-work-index.yaml` (`FT-CX-....`) без расходования ChatGPT `FT-CH` counter.
7. Сформировать compact project card через repo renderer.
8. Зафиксировать launch record в `.chatgpt/task-launch.yaml`.
9. Сформировать `.chatgpt/direct-task-self-handoff.md`.
10. Сформировать готовый visible self-handoff block для стартового ответа Codex.
11. Только после этого переходить к remediation / implementation / review.

## Важное ограничение
Нельзя считать старую уже открытую сессию Codex надежной единицей маршрутизации.
Self-handoff и profile selection должны быть привязаны к новому task launch boundary.

## Правило visible gate
Для direct task self-handoff должен быть видим пользователю в первом substantive ответе Codex.
Недостаточно только записать `.chatgpt/direct-task-self-handoff.md` или молча держать классификацию в памяти.

Первый substantive ответ Codex для direct task должен начинаться с:

````markdown
## Номер запроса Codex
```text
<PROJECT_CODE>-CX-<NNNN> <task-slug>
```

## Карточка проекта
<compact project status card>
````

`Номер запроса Codex` берется из `.chatgpt/codex-work-index.yaml`. Если materialized write не подтвержден, вместо номера выводится exact blocker:

```text
Нужно выделить номер через repo codex-work-index / allocator.
```

`Карточка проекта` берется из `render-project-lifecycle-dashboard.py --format chatgpt-card --stdout` и должна содержать project name, lifecycle chain, `Модули:` и `В работе:`. Если renderer недоступен, это blocker; нельзя заменять карточку пересказом.

Запрещено называть прием готового ChatGPT handoff self-handoff. Это route receipt, а не дублирование или замена handoff.
