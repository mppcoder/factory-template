# Downstream smoke report Universal Task Control / отчет проверки

## Маршрут

- selected_project_profile: `factory-template self-improvement / downstream materialization`
- selected_scenario: `template-repo/scenario-pack/00-master-router.md`
- pipeline_stage: `verification`
- handoff_allowed: `true`
- handoff_shape: `codex-task-handoff`

## Среда

- smoke type: temporary generated project
- generated project name: `UTC Full Smoke`
- generated slug: `utc-full-smoke`
- mutation boundary: temporary directory under `/tmp`, removed after run
- GitHub API: not used
- Codex launch: not used
- canonical generated registry: `.chatgpt/task-registry.yaml`

## Команды smoke

```bash
printf 'UTC Full Smoke\nutc-full-smoke\ngreenfield-product\ngreenfield\nfeature\ncodex-led\n' | \
  FACTORY_REGISTRY_MODE=skip /projects/factory-template/template-repo/launcher.sh
cd utc-full-smoke
python3 scripts/validate-task-registry.py
python3 scripts/allocate-task-id.py
python3 scripts/allocate-task-id.py --append-draft --title "Downstream smoke task" --goal "Проверить generated Universal Task Control flow." --task-class docs --source-kind smoke --source-ref reports/downstream-materialization/smoke-report.md
python3 scripts/validate-task-registry.py
python3 scripts/update-task-status.py --task-id FT-TASK-0002 --status ready_for_handoff --reason "Task route is clear for downstream smoke." --sync-dashboard --write
python3 scripts/preview-task-handoff.py --task-id FT-TASK-0002 --output reports/handoffs/FT-TASK-0002-preview.md
python3 scripts/prepare-task-pack.py --task-id FT-TASK-0002 --mark-ready-for-codex --sync-dashboard --write
python3 scripts/validate-codex-task-handoff.py reports/handoffs/FT-TASK-0002-codex-handoff.md
python3 scripts/validate-task-registry.py
python3 scripts/render-task-queue.py --output reports/task-queue.md
python3 scripts/validate-project-lifecycle-dashboard.py .chatgpt/project-lifecycle-dashboard.yaml
python3 scripts/render-project-lifecycle-dashboard.py --format chatgpt-card --stdout
```

## Результаты

| Step | Evidence | Status |
|---|---|---|
| Materialize generated project | `Проект создан: ./utc-full-smoke` | passed |
| Validate initial registry | `TASK REGISTRY OK: schema=factory-task-registry/v1, tasks=1` | passed |
| Allocate task id | `next_task_id=FT-TASK-0002`, `dry_run=true` | passed |
| Append draft | `allocated_task_id=FT-TASK-0002`, `registry_updated=.chatgpt/task-registry.yaml` | passed |
| Validate after append | `TASK REGISTRY OK: schema=factory-task-registry/v1, tasks=2` | passed |
| Mark ready for handoff | `status_transition=draft->ready_for_handoff` | passed |
| Preview | `task_handoff_preview=reports/handoffs/FT-TASK-0002-preview.md` | passed |
| Prepare pack and mark ready for Codex | `status_transition=ready_for_handoff->ready_for_codex` | passed |
| Validate generated handoff | `CODEX TASK HANDOFF OK: reports/handoffs/FT-TASK-0002-codex-handoff.md` | passed |
| Validate final registry | `TASK REGISTRY OK: schema=factory-task-registry/v1, tasks=2` | passed |
| Render queue | `task_queue=reports/task-queue.md` | passed |
| Queue path normalization | `registry: .chatgpt/task-registry.yaml`, `python3 scripts/prepare-task-pack.py ...` | passed |
| Dashboard validation | `PROJECT LIFECYCLE DASHBOARD ВАЛИДЕН` | passed |
| Dashboard Universal Task Control | `registry_path: .chatgpt/task-registry.yaml`, `ready_for_codex: 1` | passed |

## Вывод

Downstream Universal Task Control materialization подтвержден: generated project содержит registry, scripts, Issue Forms, operator docs and report target dirs; task lifecycle проходит от allocation до `ready_for_codex` и dashboard/queue evidence без мутации canonical factory state.
