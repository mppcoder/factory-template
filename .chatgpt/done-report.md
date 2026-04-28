# Отчет о завершении

## Что было запрошено

- Дополнительно предусмотреть обновление политики промптов под новую модель при автообновлении выбора моделей и режимов.
- Делать это по рекомендациям OpenAI, а не только через замену model slug.

## Что реально сделано

- Зафиксирован reusable defect model update без prompt-policy gate.
- Добавлен `prompt_migration_policy` в `template-repo/codex-model-routing.yaml`.
- Model-routing proposal теперь включает prompt migration section.
- Добавлен validator `template-repo/scripts/validate-model-prompt-policy.py`.
- Добавлен Artifact Eval spec/report `model-prompt-policy`.
- `verify-all.sh` запускает новый validator и eval spec.
- Обновлены docs `template-repo/README.md`, `codex-workflow.md`, `integrations.md`.

## Какие артефакты обновлены

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
- `CHANGELOG.md`
- `CURRENT_FUNCTIONAL_STATE.md`
- `VERIFY_SUMMARY.md`
- `reports/bugs/2026-04-28-model-update-missing-prompt-policy-gap.md`
- `reports/factory-feedback/feedback-2026-04-28-model-update-missing-prompt-policy-gap.md`
- `reports/model-routing/model-routing-proposal.md`
- `template-repo/codex-model-routing.yaml`
- `template-repo/scripts/check-codex-model-catalog.py`
- `template-repo/scripts/validate-model-prompt-policy.py`
- `template-repo/scripts/verify-all.sh`
- `template-repo/README.md`
- `template-repo/template/docs/codex-workflow.md`
- `template-repo/template/docs/integrations.md`
- `tests/artifact-eval/specs/model-prompt-policy.yaml`
- `tests/artifact-eval/reports/model-prompt-policy.md`

## Что осталось вне объема

- Фактический promotion `quick` на `gpt-5.5` не выполнялся; proposal помечает это как manual review required.

## Итог закрытия

- Prompt-policy companion gate добавлен.
- Новая model больше не может считаться только routing update без prompt migration review.
- Verification прошел; sync status фиксируется через verified sync.
