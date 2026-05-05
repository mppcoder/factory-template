# Очередь Universal Codex задач

Этот отчет является read-only control plane. Он не запускает Codex, не меняет registry и не переключает model/profile/reasoning.

## Сводка

- registry: `template-repo/template/.chatgpt/task-registry.yaml`
- schema: `factory-task-registry/v1`
- project_code: `FT`
- next_task_number: `2`
- open_tasks: `1`
- compact line: Tasks: 0 ready-for-handoff -> 0 ready-for-codex -> 0 running -> 0 human-review

## Статусы

| Status | Count |
|---|---:|
| `draft` | 1 |

## Очередь

| Task | Class | Status | Human boundary | Blocked by | Next action | Evidence |
|---|---|---|---|---|---|---|
| `FT-TASK-0001` Example universal Codex task | `feature` | `draft` | review | none | Replace example task or create real task through allocator or bridge. | none |

## Команды подготовки

### `FT-TASK-0001`

- status: `draft`
- preview:

```bash
python3 template-repo/scripts/preview-task-handoff.py --registry template-repo/template/.chatgpt/task-registry.yaml --task-id FT-TASK-0001 --output reports/handoffs/FT-TASK-0001-preview.md
```

- prepare pack:

```bash
python3 template-repo/scripts/prepare-task-pack.py --registry template-repo/template/.chatgpt/task-registry.yaml --task-id FT-TASK-0001 --write
```

- mark ready for Codex after review:

```bash
python3 template-repo/scripts/prepare-task-pack.py --registry template-repo/template/.chatgpt/task-registry.yaml --task-id FT-TASK-0001 --mark-ready-for-codex --sync-dashboard --write
```
