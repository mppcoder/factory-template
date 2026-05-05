# Очередь Universal Codex задач

Этот отчет является read-only control plane. Он не запускает Codex, не меняет registry и не переключает model/profile/reasoning.

## Сводка

- registry: `template-repo/template/.chatgpt/task-registry.yaml`
- schema: `factory-task-registry/v1`
- project_code: `FT`
- next_task_number: `2`
- open_tasks: `0`
- compact line: Tasks: 0 ready-for-handoff -> 0 ready-for-codex -> 0 running -> 0 human-review

## Статусы

| Status | Count |
|---|---:|
| `not_applicable` | 1 |

## Очередь

| Task | Class | Status | Human boundary | Blocked by | Next action | Evidence |
|---|---|---|---|---|---|---|
| `FT-TASK-0001` Example universal Codex task | `feature` | `not_applicable` | review | none | Create the first real task through allocator or issue bridge. | none |

## Команды подготовки

### `FT-TASK-0001`

- status: `not_applicable`
- terminal task: команды подготовки не нужны.
