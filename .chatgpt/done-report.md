# Отчет о завершении

## Что было запрошено

- Переработать prompt-like artifacts `factory-template` под GPT-5.5 как fresh prompt baseline.
- Использовать только официальные OpenAI sources для внешней baseline-части.
- Сохранить repo-first, defect-capture, handoff, routing и closeout invariants.
- Обновить tests/evals/validators, чтобы drift старых prompt patterns ловился автоматически.

## Что реально сделано

- Собран prompt inventory и source map.
- Зафиксирован reusable defect stale/prompt-contract gap.
- Обновлен active `.chatgpt/codex-input.md`.
- Обновлены generated `.chatgpt` task artifacts.
- Добавлен базовый prompt contract для GPT-5.5 в генераторы task-pack и normalized handoff.
- Template `.chatgpt/codex-input.md` переведен на outcome-first sections.
- Добавлен validator `validate-gpt55-prompt-contract.py`.
- Добавлен Artifact Eval spec/report `gpt-5-5-prompt-contract`.
- `verify-all.sh` подключает новый validator и eval spec.

## Какие артефакты обновлены

- `.chatgpt/codex-input.md`
- `.chatgpt/codex-context.md`
- `.chatgpt/codex-task-pack.md`
- `.chatgpt/normalized-codex-handoff.md`
- `.chatgpt/handoff-response.md`
- `.chatgpt/task-index.yaml`
- `.chatgpt/stage-state.yaml`
- `.chatgpt/task-launch.yaml`
- `.chatgpt/verification-report.md`
- `.chatgpt/done-report.md`
- `reports/bugs/2026-04-28-gpt-5-5-prompt-migration-gap.md`
- `reports/factory-feedback/feedback-2026-04-28-gpt-5-5-prompt-migration-gap.md`
- `reports/prompt-migration/2026-04-28-gpt-5-5-prompt-inventory.md`
- `reports/prompt-migration/2026-04-28-gpt-5-5-prompt-migration-report.md`
- `template-repo/scripts/create-codex-task-pack.py`
- `template-repo/scripts/codex_task_router.py`
- `template-repo/scripts/validate-gpt55-prompt-contract.py`
- `template-repo/scripts/verify-all.sh`
- `template-repo/template/.chatgpt/codex-input.md`
- `template-repo/template/.chatgpt/codex-task-pack.md`
- `tests/artifact-eval/specs/gpt-5-5-prompt-contract.yaml`
- `tests/artifact-eval/reports/gpt-5-5-prompt-contract.md`
- `tests/onboarding-smoke/ACCEPTANCE_REPORT.md`

## Что осталось вне объема

- Automatic promotion `quick` с `gpt-5.4-mini` на `gpt-5.5` не выполнялся; это требует отдельного proposal/manual review.
- API migration не выполнялась, потому что задача касалась prompt-like artifacts и Codex routing.

## Итог закрытия

- Verification contour прошел.
- Model catalog live check доступен и подтверждает `gpt-5.5`.
- Defect/factory feedback созданы.
- Внешних действий по текущему scope не требуется.
