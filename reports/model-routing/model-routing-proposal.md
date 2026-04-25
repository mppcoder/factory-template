# Model Routing Proposal

## Current Mapping
- quick: gpt-5.4-mini / low / plan medium
- build: gpt-5.5 / medium / plan medium
- deep: gpt-5.5 / high / plan high
- review: gpt-5.5 / high / plan high

## Live Catalog Summary
source: codex debug models
status: available

- gpt-5.5: low, medium, high, xhigh
- gpt-5.4: low, medium, high, xhigh
- gpt-5.4-mini: low, medium, high, xhigh
- gpt-5.3-codex: low, medium, high, xhigh
- gpt-5.2: low, medium, high, xhigh
- codex-auto-review: low, medium, high, xhigh
- gpt-5.3-codex-spark: low, medium, high, xhigh

## Proposed Mapping
- quick: gpt-5.5 / low / plan medium / manual_review_required=True
- build: gpt-5.5 / medium / plan medium / manual_review_required=False
- deep: gpt-5.5 / high / plan high / manual_review_required=False
- review: gpt-5.5 / high / plan high / manual_review_required=False

## Reasoning Support Evidence
- gpt-5.5: low, medium, high, xhigh
- gpt-5.4: low, medium, high, xhigh
- gpt-5.4-mini: low, medium, high, xhigh
- gpt-5.3-codex: low, medium, high, xhigh
- gpt-5.2: low, medium, high, xhigh
- codex-auto-review: low, medium, high, xhigh
- gpt-5.3-codex-spark: low, medium, high, xhigh

## Compatibility Risks
- profile model promotion changes executable routing and needs manual review

## Exact Files To Update
- template-repo/codex-model-routing.yaml
- template-repo/codex-routing.yaml
- template-repo/template/.codex/config.toml
- template-repo/scripts/codex_task_router.py
- template-repo/scripts/validate-codex-routing.py

## Manual Review Required
true

## Findings JSON
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
