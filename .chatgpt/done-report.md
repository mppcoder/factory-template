# Отчет о завершении

## Что было запрошено
- Implement feature 16: automatic checking of newly available Codex/OpenAI models.
- Add controlled update/proposal path for files that map task classes to selected_profile, selected_model, selected_reasoning_effort and selected_plan_mode_reasoning_effort.
- Keep repo-configured mapping separate from live Codex catalog, manual VS Code picker and optional strict launcher profile selection.

## Что реально сделано
- Added canonical `template-repo/codex-model-routing.yaml`.
- Added reusable catalog helper and `template-repo/scripts/check-codex-model-catalog.py`.
- Resolver now merges canonical model routing into executable route selection.
- Bootstrap/launcher/generated task-pack surfaces preserve selected model, reasoning and plan-mode reasoning.
- Validator checks model-routing consistency, live catalog support and strict unavailable mode.
- Proposal generated at `reports/model-routing/model-routing-proposal.md`.
- Source-facing docs/runbooks explain model availability auto-check and troubleshooting.
- Scenario-pack handoff rules now require plan-mode reasoning and honest live-availability wording.
- Scenario-pack source export refreshed into `_sources-export/scenario-pack.tar.gz`.

## Какие артефакты обновлены
- `.chatgpt/boundary-actions.md`
- `.chatgpt/codex-input.md`
- `.chatgpt/codex-task-pack.md`
- `.chatgpt/handoff-response.md`
- `.chatgpt/normalized-codex-handoff.md`
- `.chatgpt/task-launch.yaml`
- `.chatgpt/verification-report.md`
- `.chatgpt/done-report.md`
- `README.md`
- `template-repo/README.md`
- `template-repo/codex-routing.yaml`
- `template-repo/codex-model-routing.yaml`
- `template-repo/scenario-pack/15-handoff-to-codex.md`
- `template-repo/scripts/codex_task_router.py`
- `template-repo/scripts/codex_model_catalog.py`
- `template-repo/scripts/check-codex-model-catalog.py`
- `template-repo/scripts/create-codex-task-pack.py`
- `template-repo/scripts/launch-codex-task.sh`
- `template-repo/scripts/validate-codex-routing.py`
- `template-repo/template/.chatgpt/codex-task-pack.md`
- `template-repo/template/.chatgpt/task-launch.yaml`
- `template-repo/template/.codex/config.toml`
- `template-repo/template/docs/codex-workflow.md`
- `template-repo/template/docs/integrations.md`
- `template-repo/tests/fixtures/codex-model-catalog-limited.yaml`
- `reports/model-routing/model-routing-proposal.md`
- `CHANGELOG.md`
- `template-repo/CHANGELOG.md`

## Что не потребовалось
- Automatic profile promotion не выполнялась; policy оставлен proposal-only.
- Новое defect-capture не потребовалось: routing drift/remediation blocker не был найден.

## Итог закрытия
- Feature 16 завершена и проверена.
- Live catalog был доступен.
- Known limitation: `codex debug models` availability зависит от local Codex CLI; unavailable mode intentionally warns unless strict mode is requested.
