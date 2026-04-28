# Отчет о проверке результата

## Что проверяли

- GPT-5.5 prompt migration для prompt-like artifacts `factory-template`.
- Актуальность `.chatgpt/codex-input.md` для входящего `chatgpt-handoff`.
- Outcome-first baseline в template `.chatgpt` и generated task-pack / normalized handoff.
- Сохранение repo-first, defect-capture, handoff, routing и closeout invariants.
- Reasoning profile policy без silent promotion `quick`.
- Durable drift checks через validator и Artifact Eval.

## Статус defect-capture

- Bug report создан: `reports/bugs/2026-04-28-gpt-5-5-prompt-migration-gap.md`.
- Factory feedback создан: `reports/factory-feedback/feedback-2026-04-28-gpt-5-5-prompt-migration-gap.md`.
- Слой: `factory-template`.
- Статус remediation: fixed-in-current-scope.

## Что подтверждено

- `.chatgpt/codex-input.md` заменен со stale downstream sync task на текущий GPT-5.5 migration handoff.
- `template-repo/scripts/create-codex-task-pack.py` и `template-repo/scripts/codex_task_router.py` добавляют базовый prompt contract для GPT-5.5.
- `template-repo/template/.chatgpt/codex-input.md` использует русскоязычные outcome-first sections.
- `tests/artifact-eval/specs/gpt-5-5-prompt-contract.yaml` и `validate-gpt55-prompt-contract.py` ловят stale handoff и отсутствие prompt contract.
- `quick` остается на `gpt-5.4-mini` как осознанная routing policy; live catalog предложил upgrade candidate, но manual review required.

## Команды проверки

- `git diff --check`: PASS.
- `python3 template-repo/scripts/validate-codex-routing.py`: PASS.
- `python3 template-repo/scripts/check-codex-model-catalog.py`: PASS, `catalog_status=available`, `gpt-5.5` live model present, `missing_configured_models=[]`.
- `python3 template-repo/scripts/validate-beginner-handoff-ux.py`: PASS.
- `python3 template-repo/scripts/validate-gpt55-prompt-contract.py .`: PASS.
- `python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/gpt-5-5-prompt-contract.yaml --output tests/artifact-eval/reports/gpt-5-5-prompt-contract.md`: PASS.
- `python3 template-repo/scripts/validate-artifact-eval-report.py tests/artifact-eval/reports/gpt-5-5-prompt-contract.md`: PASS.
- `python3 template-repo/scripts/validate-human-language-layer.py .`: PASS, active findings `0`.
- `bash template-repo/scripts/verify-all.sh ci`: PASS, `VERIFY-ALL ПРОЙДЕН (ci)`.

## Аудит остаточных prompt patterns

- `rg` по old model IDs: остатки классифицированы как intentional quick profile, model catalog compatibility, historical reports, orchestration fixtures или generated evidence.
- `rg` по `think step by step|current date|as an AI`: остатки только в validator/spec negative markers и report classification; static `current date:` prompt instruction в critical surfaces не найден.
- `rg` по `self-handoff`: допустимые остатки относятся к direct task / incidental defect boundary; `chatgpt-handoff` route фиксирует `handoff receipt`.

## Итоговый вывод

GPT-5.5 prompt migration выполнена и проверена. Repo green по обязательному verification contour; closeout/sync state фиксируется отдельно.
