# Итоговый отчёт по закрытию изменения

## Что было запрошено
- Разобраться с bug, при котором в handoff был помечен высокий уровень рассуждений, а generated artifacts показывали `medium`.

## Что реально сделано
- Создан bug report `reports/bugs/bug-015-explicit-handoff-reasoning-overridden-by-keyword-routing.md`.
- Создан factory feedback `reports/factory-feedback/feedback-015-explicit-handoff-reasoning-overridden-by-keyword-routing.md`.
- В `template-repo/scripts/codex_task_router.py` добавлен разбор structured handoff payload:
  - router теперь читает explicit `selected_model`, `selected_reasoning_effort`, `selected_profile`, `selected_scenario`, `pipeline_stage` и другие handoff fields;
  - если requested profile не существует в executable routing spec, router подбирает совместимый executable profile по model/reasoning;
  - keyword fallback остаётся запасным механизмом, а не перетирает explicit handoff route.
- Нормализация boolean/scalar override values сделана более предсказуемой для generated artifacts.

## Какие артефакты обновлены
- `template-repo/scripts/codex_task_router.py`
- `reports/bugs/bug-015-explicit-handoff-reasoning-overridden-by-keyword-routing.md`
- `reports/factory-feedback/feedback-015-explicit-handoff-reasoning-overridden-by-keyword-routing.md`
- `.chatgpt/task-index.yaml`
- `.chatgpt/codex-input.md`
- `.chatgpt/verification-report.md`
- `.chatgpt/done-report.md`

## Что осталось вне объёма
- Дополнительная стандартизация vocabulary между внешним handoff profile names и локальными executable profile IDs за пределами текущего fallback matching.

## Итог закрытия
- Explicit high-reasoning handoff больше не должен silently превращаться в `medium` внутри generated launch artifacts.
- Новый task launch теперь честнее отражает structured handoff intent и при необходимости маппит его в совместимый executable profile.
