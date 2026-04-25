# Отчет о проверке результата

## Что проверяли
- Feature 16: automatic checking of newly available Codex/OpenAI models and controlled model-routing updates.
- Canonical mapping task class -> selected_profile -> selected_model / selected_reasoning_effort / selected_plan_mode_reasoning_effort.
- Live catalog available, unavailable and fixture-limited paths.
- Normalized handoff fields and docs for manual UI vs optional strict launcher boundaries.

## Model catalog status
- Live `codex debug models` was available.
- Current configured models are present: `gpt-5.5`, `gpt-5.4-mini`.
- Reasoning support validated for low/medium/high/plan-mode mappings.
- New candidate models detected but not promoted automatically: `codex-auto-review`, `gpt-5.2`, `gpt-5.3-codex`, `gpt-5.3-codex-spark`, `gpt-5.4`.
- Proposal artifact generated at `reports/model-routing/model-routing-proposal.md`.

## Что подтверждено
- `resolve-codex-task-route.py` emits `selected_model`, `selected_reasoning_effort`, `selected_plan_mode_reasoning_effort`, catalog status, launch command and `codex --profile`.
- `check-codex-model-catalog.py` reports missing configured models, unsupported reasoning, new candidates and profiles that can be upgraded.
- Unavailable live catalog mode warns and does not promote mappings.
- Strict unavailable mode fails.
- Fixture-limited catalog detects unsupported reasoning.
- `validate-codex-routing.py` validates the new model-routing artifact and live reasoning support.

## Команды проверки
- `python3 template-repo/scripts/resolve-codex-task-route.py template-repo --launch-source chatgpt-handoff --task-text "feature: update model routing" --json`: passed.
- `python3 template-repo/scripts/check-codex-model-catalog.py .`: passed.
- `python3 template-repo/scripts/check-codex-model-catalog.py . --json`: passed.
- `python3 template-repo/scripts/check-codex-model-catalog.py . --write-proposal`: passed.
- `python3 template-repo/scripts/check-codex-model-catalog.py . --catalog-fixture template-repo/tests/fixtures/codex-model-catalog-limited.yaml --json`: passed and reported unsupported reasoning.
- `PATH=/no-such-dir /usr/bin/python3 template-repo/scripts/check-codex-model-catalog.py .`: passed with warning.
- `PATH=/no-such-dir /usr/bin/python3 template-repo/scripts/validate-codex-routing.py . --strict`: failed as expected.
- `python3 template-repo/scripts/validate-codex-task-pack.py .`: passed.
- `python3 template-repo/scripts/validate-codex-routing.py .`: passed.
- `bash template-repo/scripts/verify-all.sh quick`: passed.
- `bash SMOKE_TEST.sh`: initially caught missing generated README model-catalog guidance; passed after template README fix.
- `bash template-repo/scripts/verify-all.sh full`: passed.
- `bash template-repo/scripts/export-sources-pack.sh .`: passed.

## Итоговый вывод
- Feature 16 implemented.
- Mapping was not promoted automatically; proposal-only policy was applied.
- Live model catalog was available during verification.
