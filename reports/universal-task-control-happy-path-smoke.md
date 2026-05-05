# Отчет проверки Universal Task Control

Дата проверки: 2026-05-05

## Назначение

Этот отчет фиксирует операторский happy path для repo-native Universal Task Control. Проверка выполнялась на временной копии `task-registry.yaml` и `project-lifecycle-dashboard.yaml`, поэтому canonical template state не менялся.

Проверяемая цепочка:

1. Валидировать registry.
2. Посмотреть следующий `FT-TASK` без записи.
3. Зарезервировать draft task.
4. Перевести task в `ready_for_handoff`.
5. Сгенерировать preview и Codex handoff.
6. Явно перевести task в `ready_for_codex`.
7. Срендерить очередь task.
8. Повторно валидировать registry, handoff и dashboard.

## Команды

```bash
python3 template-repo/scripts/validate-task-registry.py "$TMP/task-registry.yaml"
python3 template-repo/scripts/allocate-task-id.py --registry "$TMP/task-registry.yaml"
python3 template-repo/scripts/allocate-task-id.py --registry "$TMP/task-registry.yaml" --append-draft --title "Operator happy path smoke" --goal "Проверить repo-native Universal Task Control happy path." --task-class docs --source-kind smoke --source-ref reports/universal-task-control-happy-path-smoke.md
python3 template-repo/scripts/update-task-status.py --registry "$TMP/task-registry.yaml" --dashboard "$TMP/project-lifecycle-dashboard.yaml" --task-id FT-TASK-0002 --status ready_for_handoff --reason "Task route is clear for smoke." --sync-dashboard --write
python3 template-repo/scripts/preview-task-handoff.py --registry "$TMP/task-registry.yaml" --task-id FT-TASK-0002 --handoff-output "$TMP/FT-TASK-0002-codex-handoff.md" --output "$TMP/FT-TASK-0002-preview.md"
python3 template-repo/scripts/prepare-task-pack.py --registry "$TMP/task-registry.yaml" --dashboard "$TMP/project-lifecycle-dashboard.yaml" --task-id FT-TASK-0002 --preview-output "$TMP/FT-TASK-0002-preview.md" --handoff-output "$TMP/FT-TASK-0002-codex-handoff.md" --mark-ready-for-codex --sync-dashboard --write
python3 template-repo/scripts/render-task-queue.py --registry "$TMP/task-registry.yaml" --output "$TMP/task-queue.md"
python3 template-repo/scripts/validate-task-registry.py "$TMP/task-registry.yaml"
python3 template-repo/scripts/validate-codex-task-handoff.py "$TMP/FT-TASK-0002-codex-handoff.md"
python3 template-repo/scripts/validate-project-lifecycle-dashboard.py "$TMP/project-lifecycle-dashboard.yaml"
```

## Результат

```text
TASK REGISTRY OK: schema=factory-task-registry/v1, tasks=1
next_task_id=FT-TASK-0002
dry_run=true
allocated_task_id=FT-TASK-0002
status_transition=draft->ready_for_handoff
task_handoff_preview=.../FT-TASK-0002-preview.md
CODEX TASK HANDOFF OK: .../FT-TASK-0002-codex-handoff.md
status_transition=ready_for_handoff->ready_for_codex
task_pack_prepare=write
launch_boundary=does_not_start_codex
route_boundary=advisory_preview_only_no_model_or_reasoning_autoswitch
task_queue=.../task-queue.md
TASK REGISTRY OK: schema=factory-task-registry/v1, tasks=2
PROJECT LIFECYCLE DASHBOARD ВАЛИДЕН
```

## Очередь после smoke

Ожидаемая compact line:

```text
Tasks: 0 ready-for-handoff -> 1 ready-for-codex -> 0 running -> 0 human-review
```

Ожидаемые статусы:

| Status | Count |
|---|---:|
| `ready_for_codex` | 1 |
| `draft` | 1 |

## Границы

- Smoke не запускает Codex.
- Smoke не переключает model/profile/reasoning.
- Smoke не меняет canonical `template-repo/template/.chatgpt/task-registry.yaml`.
- Public external reports, secrets, merge и production deploy не входят в этот контур.

## Вывод

Universal Task Control happy path подтвержден: оператор может безопасно пройти от registry до Codex-ready handoff и queue evidence без daemon/background runner и без скрытой мутации template state.
