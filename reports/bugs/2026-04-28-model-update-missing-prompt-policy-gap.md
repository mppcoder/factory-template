# Bug report: model update без обязательной prompt policy миграции

Дата: 2026-04-28
Слой: `factory-template`
Статус: remediated in current scope

## Summary

В repo уже был контур auto-check/proposal для live Codex model catalog, но promotion proposal не был жестко связан с обновлением prompt policy под новую model. Это могло привести к изменению `selected_model` без проверки актуальных рекомендаций OpenAI по prompt behavior, reasoning, verbosity, tool-use и evals.

## Evidence

- `template-repo/codex-model-routing.yaml` содержал `model_policy.promotion_policy`, но не содержал `prompt_migration_policy`.
- `template-repo/scripts/check-codex-model-catalog.py --write-proposal` создавал model-routing proposal без prompt migration section.
- GPT-5.5 migration уже добавила prompt contract validator, но model promotion flow не требовал companion prompt-policy review для следующей новой model.

## Expected

Любой new model candidate / profile promotion должен создавать или требовать:
- official OpenAI source map;
- fresh prompt baseline, а не drop-in replacement;
- affected prompt-like artifacts;
- validators/evals для prompt drift;
- manual review boundary до profile promotion.

## Actual

Model proposal мог ограничиться mapping/reasoning compatibility и точными файлами routing update.

## Classification

Reusable factory defect: `model-routing` layer и `prompt-policy` layer были связаны только концептуально, но не проверяемым repo contract.

## Remediation

- Добавлен `prompt_migration_policy` в `template-repo/codex-model-routing.yaml`.
- `check-codex-model-catalog.py --write-proposal` теперь пишет prompt migration section.
- Добавлен validator `template-repo/scripts/validate-model-prompt-policy.py`.
- Добавлен Artifact Eval spec/report `model-prompt-policy`.
- `verify-all.sh` запускает validator и eval spec.
- Обновлены docs model routing / Codex workflow / integrations.
