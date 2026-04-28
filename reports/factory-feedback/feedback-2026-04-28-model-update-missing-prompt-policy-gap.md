# Factory feedback: связать model promotion и prompt policy update

Дата: 2026-04-28
Source bug: `reports/bugs/2026-04-28-model-update-missing-prompt-policy-gap.md`
Статус: applied

## Feedback

Auto-check новых моделей не должен завершаться только proposal по `selected_model`. Для каждой новой candidate model нужен companion prompt-policy contour, основанный на official OpenAI docs.

## Factory-level change

- `codex-model-routing.yaml` хранит `prompt_migration_policy`.
- Model routing proposal включает prompt migration section.
- Validator проверяет official source baseline, fresh prompt baseline, prompt artifacts и manual review boundary.
- Quick verify ловит отсутствие этой связки.

## Acceptance

- `python3 template-repo/scripts/validate-model-prompt-policy.py .` проходит.
- `reports/model-routing/model-routing-proposal.md` содержит `## Политика prompt migration`.
- `bash template-repo/scripts/verify-all.sh quick` запускает новый validator.
