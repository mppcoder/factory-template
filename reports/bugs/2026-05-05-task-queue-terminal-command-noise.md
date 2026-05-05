# Очередь задач показывает команды подготовки для terminal tasks

Дата: 2026-05-05

## Класс

- task_class: `bug`
- layer: Universal Task Control / queue renderer
- severity: medium
- status: fixed-in-current-scope

## Воспроизведение

1. Mark template example task `FT-TASK-0001` as `not_applicable`.
2. Run:

```bash
python3 template-repo/scripts/render-task-queue.py \
  --registry template-repo/template/.chatgpt/task-registry.yaml \
  --output reports/task-queue.md
```

## Фактический результат

`reports/task-queue.md` shows preview/prepare/ready commands for `FT-TASK-0001` even though the task is terminal `not_applicable`.

## Ожидаемый результат

Terminal tasks should remain visible in the queue for audit, but the commands section should say that no preparation commands are needed.

## Исправление

Update `render-task-queue.py` so `verified`, `superseded`, `not_applicable` and `archived` tasks do not show actionable preparation commands.

## Проверка

- `python3 template-repo/scripts/render-task-queue.py --registry template-repo/template/.chatgpt/task-registry.yaml --output reports/task-queue.md`
- `bash template-repo/scripts/verify-all.sh quick`
