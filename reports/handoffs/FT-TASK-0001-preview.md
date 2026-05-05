# Предпросмотр Codex handoff task

Этот файл является preview. Он не запускает Codex, не переключает model/profile/reasoning и не является execution evidence.

## Задача

- registry: `template-repo/template/.chatgpt/task-registry.yaml`
- task_id: `FT-TASK-0001`
- title: Example universal Codex task
- class/priority/status: `feature` / `medium` / `draft`
- source: `example` ``
- bucket для dashboard: `triage`
- next_action: Replace example task or create real task through allocator or bridge.

## Маршрут

- selected_project_profile: factory-template self-improvement / automation-orchestration implementation
- selected_scenario: `template-repo/scenario-pack/00-master-router.md`
- pipeline_stage: `implementation`
- handoff_allowed: `True`
- handoff_shape: `codex-task-handoff`
- selected_profile: `deep`
- selected_reasoning_effort: `high`
- selected_model: `repo-configured; do not assume live auto-switch`

## Граница запуска

- Advisory layer: AGENTS, scenario-pack, runbooks, `.chatgpt` guidance и generated handoff text.
- Executable routing layer: Codex picker, launcher scripts, Codex CLI/app/cloud или future adapter.
- Manual UI default: открыть новый Codex chat, выбрать model/reasoning в picker и вставить generated handoff.
- Already-open live session: non-canonical fallback без обещаний auto-switch.

## Файл handoff

- planned handoff file: `reports/handoffs/FT-TASK-0001-codex-handoff.md`
- команда генерации:

```bash
python3 template-repo/scripts/task-to-codex-handoff.py --registry template-repo/template/.chatgpt/task-registry.yaml --task-id FT-TASK-0001 --output reports/handoffs/FT-TASK-0001-codex-handoff.md
```

## Предпросмотр dashboard

- open_tasks: `1`
- compact line: Tasks: 0 ready-for-handoff -> 0 ready-for-codex -> 0 running -> 0 human-review
- текущая задача учитывается как: `triage`

## Зависимости

blocked_by:
- нет

unlocks:
- нет

## Человеческая граница

- requires_review: `True`
- requires_secret: `False`
- external_user_action: `False`

## Артефакты

- template-repo/template/.chatgpt/task-registry.yaml
- reports/handoffs/FT-TASK-0001-codex-handoff.md

## Команды проверки

- python3 template-repo/scripts/validate-task-registry.py template-repo/template/.chatgpt/task-registry.yaml
- python3 template-repo/scripts/validate-codex-task-handoff.py reports/handoffs/FT-TASK-0001-codex-handoff.md

## Следующий безопасный шаг

1. Проверить preview и task status `draft`.
2. Если task готов, сгенерировать handoff в `reports/handoffs/FT-TASK-0001-codex-handoff.md`.
3. Передать generated handoff в новый Codex chat или launcher-first path.
