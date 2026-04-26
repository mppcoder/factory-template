# Production VPS preset gap

## Статус

Исправляется в текущем scope.

## Reproduce

1. Открыть `deploy/presets/`.
2. Сравнить доступные preset-файлы с production VPS acceptance set: `starter`, `app-db`, `reverse-proxy-tls`, `backup`, `healthcheck`.
3. Проверить `template-repo/scripts/deploy-dry-run.sh` и `template-repo/scripts/validate-operator-env.py`.

## Evidence

- В `deploy/presets/` были только `app-db.yaml` и `reverse-proxy.yaml`.
- Backup hook был смешан с `app-db`, поэтому нельзя было включить database без backup preset.
- TLS preset назывался `reverse-proxy`, а acceptance требует явный `reverse-proxy-tls`.
- Healthcheck preset отсутствовал как отдельный operator opt-in слой.
- `verify-all.sh` проверял env validation, но не запускал dry-run для starter и app-db overlays.

## Layer classification

- `template deploy layer`
- `operator validation layer`
- `operator docs layer`
- `verification layer`

## Scope decision

Defect входит в текущую remediation-задачу `2.5-ga/production-vps-presets`.

## Self-handoff

- `launch_source`: `chatgpt-handoff`
- `task_class`: `feature-operator-hardening`
- `selected_profile`: `deep`
- `selected_model`: `gpt-5.5`
- `selected_reasoning_effort`: `high`
- `project_profile`: `factory-template`
- `selected_scenario`: `2.5-ga/production-vps-presets`
- `pipeline_stage`: `remediation`
- `artifacts_to_update`: `deploy/*`, `template-repo/scripts/*deploy*`, `validate-operator-env.py`, `operator-dashboard.py`, `docs/deploy-on-vps.md`, `docs/operator-next-step.md`, `TEST_REPORT.md`
- `handoff_allowed`: `true`

Продолжение в текущем route допустимо: profile/scenario/reasoning совпадают с основным task.

## Verification note

Во время проверки новой dry-run smoke обвязки найден и исправлен in-scope cleanup bug: `trap RETURN` в `verify-all.sh` конфликтовал с `set -u` после выхода из функции. Cleanup заменён на явный `rm -rf` внутри smoke helper.
