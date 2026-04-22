# Отчёт о проверке результата

## Что проверяли
- `python3 -m py_compile template-repo/scripts/codex_task_router.py template-repo/scripts/bootstrap-codex-task.py template-repo/scripts/resolve-codex-task-route.py template-repo/scripts/create-codex-task-pack.py`
- reproduce path через `python3 template-repo/scripts/resolve-codex-task-route.py . --launch-source chatgpt-handoff --task-text '<structured handoff>'`
- bootstrap path через `python3 template-repo/scripts/bootstrap-codex-task.py . --launch-source chatgpt-handoff --task-text '<structured handoff>'`

## Что подтверждено
- Router компилируется без синтаксических ошибок.
- До исправления тот же structured handoff приводил к `selected_reasoning_effort=medium`.
- После исправления structured handoff с `selected_reasoning_effort: high` резолвится в:
  - `selected_profile=deep`
  - `selected_reasoning_effort=high`
  - `launch_command=codex --profile deep`
- Generated `.chatgpt/task-launch.yaml` и `.chatgpt/normalized-codex-handoff.md` больше не теряют explicit high-reasoning intent.
- Если requested profile из handoff не исполним (`repo-maintenance`), router фиксирует это в reasons и выбирает совместимый executable profile вместо silent downgrade.

## Что не подтверждено или требует повторной проверки
- Отдельная интеграционная проверка downstream battle repos с их собственными routing presets не запускалась.

## Итоговый вывод
- Defect воспроизведён и устранён в executable router.
- Structured handoff routing fields теперь влияют на launch record сильнее, чем keyword-only fallback.
