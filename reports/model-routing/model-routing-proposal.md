# Proposal по маршрутизации моделей

## Текущий mapping
- quick: gpt-5.4-mini / low / plan medium
- build: gpt-5.5 / medium / plan medium
- deep: gpt-5.5 / high / plan high
- review: gpt-5.5 / high / plan high

## Сводка live catalog
источник: codex debug models
статус: available

- gpt-5.5: low, medium, high, xhigh
- gpt-5.4: low, medium, high, xhigh
- gpt-5.4-mini: low, medium, high, xhigh
- gpt-5.3-codex: low, medium, high, xhigh
- gpt-5.2: low, medium, high, xhigh
- codex-auto-review: low, medium, high, xhigh
- gpt-5.3-codex-spark: low, medium, high, xhigh

## Предложенный mapping
- quick: gpt-5.5 / low / plan medium / manual_review_required=True
- build: gpt-5.5 / medium / plan medium / manual_review_required=False
- deep: gpt-5.5 / high / plan high / manual_review_required=False
- review: gpt-5.5 / high / plan high / manual_review_required=False

## Evidence поддержки reasoning
- gpt-5.5: low, medium, high, xhigh
- gpt-5.4: low, medium, high, xhigh
- gpt-5.4-mini: low, medium, high, xhigh
- gpt-5.3-codex: low, medium, high, xhigh
- gpt-5.2: low, medium, high, xhigh
- codex-auto-review: low, medium, high, xhigh
- gpt-5.3-codex-spark: low, medium, high, xhigh

## Риски совместимости
- promotion модели для profile меняет executable routing и требует ручного review

## Политика prompt migration
default action: proposal-required
prompt_review_required: true

Official OpenAI source baseline:
- https://developers.openai.com/api/docs/guides/latest-model
- https://developers.openai.com/api/docs/guides/prompt-guidance
- https://developers.openai.com/api/docs/guides/prompt-optimizer

Required prompt review:
- не считать новую model drop-in replacement
- создать fresh prompt baseline для affected prompt-like artifacts
- проверить outcome-first contract: целевой результат, success criteria, constraints, evidence requirements, output shape, stop rules
- сверить reasoning, verbosity и tool-use guidance с official OpenAI docs
- обновить validators/evals, которые ловят drift старого prompt pattern
- сохранить repo-first, defect-capture, handoff, routing и closeout invariants

Required prompt artifacts:
- reports/model-routing/model-routing-proposal.md
- reports/prompt-migration/
- template-repo/scripts/validate-gpt55-prompt-contract.py или successor validator для новой model
- tests/artifact-eval/specs/*prompt-contract*.yaml

Manual review required for:
- любой automatic profile promotion
- удаление или ослабление prompt constraints
- перенос старого prompt stack без fresh baseline
- отсутствие official OpenAI source map

Новая model не считается drop-in replacement. Перед promotion profile mapping нужно проверить prompt-like artifacts по актуальным официальным рекомендациям OpenAI, обновить prompt contract / validators / evals и сохранить repo-first invariants.

## Точные файлы для обновления
- template-repo/codex-model-routing.yaml
- template-repo/codex-routing.yaml
- template-repo/template/.codex/config.toml
- template-repo/scripts/codex_task_router.py
- template-repo/scripts/validate-codex-routing.py
- template-repo/scripts/validate-gpt55-prompt-contract.py или successor validator для новой model
- tests/artifact-eval/specs/*prompt-contract*.yaml
- reports/prompt-migration/

## Нужен ручной review
true

## Findings JSON / данные findings
```json
{
  "missing_configured_models": [],
  "unsupported_reasoning": [],
  "new_candidate_models": [
    "codex-auto-review",
    "gpt-5.2",
    "gpt-5.3-codex",
    "gpt-5.3-codex-spark",
    "gpt-5.4"
  ],
  "profiles_that_can_be_upgraded": [
    {
      "profile": "quick",
      "current_model": "gpt-5.4-mini",
      "candidate_model": "gpt-5.5",
      "manual_review_required": true
    }
  ],
  "profiles_requiring_manual_review": [],
  "task_class_profile_errors": []
}
```
