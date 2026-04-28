# Отчет о завершении

## Что было запрошено

Добавить к запрету плоского дерева repo в `/projects` правило, что все промежуточные repo должны находиться внутри repo целевого greenfield проекта.

## Что реально сделано

- Зафиксирован reusable defect для неоднозначной формулировки project-root boundary.
- Active docs/scenario-pack/bootstrap guidance теперь требуют размещать temporary/intermediate/reconstructed/helper repos внутри repo целевого `greenfield-product`.
- Добавлен `workspace_layout_policy` в `template-repo/tree-contract.yaml`.
- `validate-tree-contract.py` проверяет наличие этого правила в active source paths.
- Добавлен Artifact Eval `project-root-boundary` и подключен в `verify-all.sh`.

## Какие артефакты обновлены

- `.chatgpt/codex-input.md`
- `.chatgpt/codex-context.md`
- `.chatgpt/codex-task-pack.md`
- `.chatgpt/direct-task-source.md`
- `.chatgpt/direct-task-self-handoff.md`
- `.chatgpt/direct-task-response.md`
- `.chatgpt/normalized-codex-handoff.md`
- `.chatgpt/task-launch.yaml`
- `.chatgpt/task-index.yaml`
- `.chatgpt/stage-state.yaml`
- `.chatgpt/verification-report.md`
- `.chatgpt/done-report.md`
- `README.md`
- `ENTRY_MODES.md`
- `docs/tree-contract.md`
- `docs/brownfield-to-greenfield-transition.md`
- `docs/operator/factory-template/README.md`
- `docs/operator/factory-template/01-runbook-dlya-polzovatelya-factory-template.md`
- `template-repo/scenario-pack/01-global-rules.md`
- `template-repo/scenario-pack/brownfield/00-brownfield-entry.md`
- `template-repo/template/docs/codex-workflow.md`
- `factory/producer/extensions/workspace-packs/vscode-codex-bootstrap/README.md`
- `factory/producer/ops/templates/factory-template-boundary-actions.template.md`
- `template-repo/tree-contract.yaml`
- `template-repo/scripts/validate-tree-contract.py`
- `template-repo/scripts/verify-all.sh`
- `tests/artifact-eval/specs/project-root-boundary.yaml`
- `tests/artifact-eval/reports/project-root-boundary.md`
- `reports/bugs/2026-04-28-flat-project-tree-intermediate-repo-gap.md`
- `reports/factory-feedback/feedback-2026-04-28-flat-project-tree-intermediate-repo-gap.md`

## Что осталось вне объема

- Реальные `/projects` директории не менялись; это policy/validator update.

## Итог закрытия

- `bash template-repo/scripts/verify-all.sh quick`: PASS.
- Verified sync выполняется после финального prereq check.
