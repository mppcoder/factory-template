# Отчет миграции prompt-артефактов на GPT-5.5

Дата: 2026-04-28
Route: `template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md`

## Карта источников (source map)

Official OpenAI baseline:
- `https://developers.openai.com/api/docs/guides/latest-model`
- `https://developers.openai.com/api/docs/guides/prompt-guidance`
- `https://developers.openai.com/api/docs/guides/prompt-optimizer`
- `https://help.openai.com/en/articles/11909943-gpt-53-and-gpt-55-in-chatgpt`

Repo baseline:
- `AGENTS.md`
- `template-repo/scenario-pack/00-master-router.md`
- `template-repo/scenario-pack/15-handoff-to-codex.md`
- `template-repo/codex-routing.yaml`
- `template-repo/template/.codex/config.toml`
- inventory report: `reports/prompt-migration/2026-04-28-gpt-5-5-prompt-inventory.md`

## Карта gap (gap map)

| Gap | Evidence | Decision |
| --- | --- | --- |
| GPT-5.5 could be treated as drop-in | Generated task packs lacked a dedicated GPT-5.5 prompt baseline | Add explicit baseline to generators/templates. |
| Active Codex input was stale | `.chatgpt/codex-input.md` referenced old downstream sync proof | Replace with current migration handoff. |
| Outcome-first prompt contract was not durable | Template `codex-input.md` used generic process headings | Convert template to outcome/success/constraints/evidence/output/stop/dynamic sections. |
| Drift not caught automatically | No artifact eval spec or validator for GPT-5.5 prompt contract | Add validator and artifact eval spec; wire into `verify-all.sh`. |
| Old model mentions need classification | `gpt-5.4-mini` remains in quick profile and model catalog | Keep as intentional policy; no silent quick promotion. |

## Исправления (remediation)

- Updated current `.chatgpt/codex-input.md` to the GPT-5.5 migration handoff.
- Added GPT-5.5 prompt baseline to generated `codex-task-pack` output.
- Added GPT-5.5 prompt contract to normalized handoff rendering.
- Converted template `codex-input.md` to outcome-first prompt sections.
- Added `validate-gpt55-prompt-contract.py`.
- Added `tests/artifact-eval/specs/gpt-5-5-prompt-contract.yaml`.
- Added the new artifact eval spec and validator to `verify-all.sh`.
- Created defect report and factory feedback for reusable drift gap.

## Проверка (verification)

Required checks are recorded in `.chatgpt/verification-report.md`.

Expected validation surface:
- `python3 template-repo/scripts/validate-gpt55-prompt-contract.py .`
- `python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/gpt-5-5-prompt-contract.yaml --output tests/artifact-eval/reports/gpt-5-5-prompt-contract.md`
- `python3 template-repo/scripts/validate-artifact-eval-report.py tests/artifact-eval/reports/gpt-5-5-prompt-contract.md`
- repo routing and full verify commands from the handoff.

## Статус model catalog

Repo-configured mapping remains:
- `build`: `gpt-5.5`, reasoning `medium`
- `deep`: `gpt-5.5`, reasoning `high`
- `review`: `gpt-5.5`, reasoning `high`
- `quick`: `gpt-5.4-mini`, reasoning `low`

Live availability is not asserted from static config; it must be checked by `python3 template-repo/scripts/check-codex-model-catalog.py` / `codex debug models`.

## Заметки closeout

No automatic promotion of `quick` was made. If factory policy later requires all prompt work on GPT-5.5, create a separate proposal in `reports/model-routing/` with manual review required.
