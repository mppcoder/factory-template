# Отчет о проверке результата

## Что проверяли

- Связку model availability auto-check / model-routing proposal с prompt policy migration.
- Наличие `prompt_migration_policy` в `codex-model-routing.yaml`.
- Генерацию prompt migration section в `reports/model-routing/model-routing-proposal.md`.
- Validator/eval, которые ловят отсутствие companion prompt-policy review.
- Сохранение rule: новая model не является drop-in replacement и требует official OpenAI source map.

## Статус defect-capture

- Bug report создан: `reports/bugs/2026-04-28-model-update-missing-prompt-policy-gap.md`.
- Factory feedback создан: `reports/factory-feedback/feedback-2026-04-28-model-update-missing-prompt-policy-gap.md`.
- Слой: `factory-template`.
- Статус remediation: fixed-in-current-scope.

## Что подтверждено

- `template-repo/codex-model-routing.yaml` содержит `prompt_migration_policy`.
- `template-repo/scripts/check-codex-model-catalog.py --write-proposal` добавляет section `## Политика prompt migration`.
- `reports/model-routing/model-routing-proposal.md` содержит official OpenAI source baseline и required prompt artifacts.
- `template-repo/scripts/validate-model-prompt-policy.py` проходит.
- Artifact Eval report `tests/artifact-eval/reports/model-prompt-policy.md` валиден.

## Команды проверки

- `python3 template-repo/scripts/check-codex-model-catalog.py . --write-proposal`: PASS.
- `python3 template-repo/scripts/validate-model-prompt-policy.py .`: PASS.
- `python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/model-prompt-policy.yaml --output tests/artifact-eval/reports/model-prompt-policy.md`: PASS.
- `python3 template-repo/scripts/validate-artifact-eval-report.py tests/artifact-eval/reports/model-prompt-policy.md`: PASS.
- `git diff --check`: PASS.
- `python3 template-repo/scripts/validate-codex-task-pack.py .`: PASS.
- `python3 template-repo/scripts/validate-codex-routing.py .`: PASS.
- `python3 template-repo/scripts/validate-human-language-layer.py .`: PASS, active findings `0`.
- `bash template-repo/scripts/verify-all.sh quick`: PASS, `VERIFY-ALL ПРОЙДЕН (quick)`.

## Итоговый вывод

Model update contour теперь требует companion prompt-policy migration по official OpenAI guidance до promotion profile mapping. Quick verify прошел.
