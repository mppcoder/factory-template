# Onboarding Smoke Acceptance

- Run timestamp (UTC): `2026-04-29T11:10:17Z`
- Runner: `tests/onboarding-smoke/run-novice-e2e.sh`
- Root: `/projects/factory-template`

## Результаты сценариев

1. `greenfield-novice`
- status: `green`
- expected preset: `greenfield-product`
- generated project: `/projects/factory-template/tests/onboarding-smoke/.tmp-run/greenfield-novice/novice-greenfield-smoke`
- log: `/projects/factory-template/tests/onboarding-smoke/.tmp-run/greenfield-novice.txt`
- duration_seconds: `2`
- manual_interventions: `0`

2. `brownfield-without-repo-novice`
- status: `green`
- expected preset: `brownfield-without-repo`
- generated project: `/projects/factory-template/tests/onboarding-smoke/.tmp-run/brownfield-without-repo-novice/novice-brownfield-no-repo-smoke`
- log: `/projects/factory-template/tests/onboarding-smoke/.tmp-run/brownfield-without-repo-novice.txt`
- duration_seconds: `3`
- manual_interventions: `0`

3. `brownfield-modernization-novice`
- status: `green`
- expected preset: `brownfield-with-repo-modernization`
- generated project: `/projects/factory-template/tests/onboarding-smoke/.tmp-run/brownfield-modernization-novice/novice-brownfield-modernization-smoke`
- log: `/projects/factory-template/tests/onboarding-smoke/.tmp-run/brownfield-modernization-novice.txt`
- duration_seconds: `3`
- manual_interventions: `0`

4. `brownfield-integration-novice`
- status: `green`
- expected preset: `brownfield-with-repo-integration`
- generated project: `/projects/factory-template/tests/onboarding-smoke/.tmp-run/brownfield-integration-novice/novice-brownfield-integration-smoke`
- log: `/projects/factory-template/tests/onboarding-smoke/.tmp-run/brownfield-integration-novice.txt`
- duration_seconds: `2`
- manual_interventions: `0`

5. `brownfield-audit-novice`
- status: `green`
- expected preset: `brownfield-with-repo-audit`
- generated project: `/projects/factory-template/tests/onboarding-smoke/.tmp-run/brownfield-audit-novice/novice-brownfield-audit-smoke`
- log: `/projects/factory-template/tests/onboarding-smoke/.tmp-run/brownfield-audit-novice.txt`
- duration_seconds: `3`
- manual_interventions: `0`

6. `guided-launcher-greenfield`
- status: `green`
- expected preset: `greenfield-product`
- generated project: `/projects/factory-template/tests/onboarding-smoke/.tmp-run/guided-launcher-greenfield/guided-launcher-greenfield-smoke`
- log: `/projects/factory-template/tests/onboarding-smoke/.tmp-run/guided-launcher-greenfield.txt`
- duration_seconds: `3`
- manual_interventions: `0`

7. `guided-launcher-brownfield-no-repo`
- status: `green`
- expected preset: `brownfield-without-repo`
- generated project: `/projects/factory-template/tests/onboarding-smoke/.tmp-run/guided-launcher-brownfield-no-repo/guided-launcher-brownfield-no-repo-smoke`
- log: `/projects/factory-template/tests/onboarding-smoke/.tmp-run/guided-launcher-brownfield-no-repo.txt`
- duration_seconds: `3`
- manual_interventions: `0`

8. `guided-launcher-brownfield-with-repo`
- status: `green`
- expected preset: `brownfield-with-repo-modernization`
- generated project: `/projects/factory-template/tests/onboarding-smoke/.tmp-run/guided-launcher-brownfield-with-repo/guided-launcher-brownfield-with-repo-smoke`
- log: `/projects/factory-template/tests/onboarding-smoke/.tmp-run/guided-launcher-brownfield-with-repo.txt`
- duration_seconds: `3`
- manual_interventions: `0`

9. `guided-launcher-continue-flow`
- status: `green`
- expected preset: `greenfield-product`
- generated project: `/projects/factory-template/tests/onboarding-smoke/.tmp-run/guided-launcher-continue-flow/guided-launcher-continue-flow-smoke`
- log: `/projects/factory-template/tests/onboarding-smoke/.tmp-run/guided-launcher-continue-flow.txt`
- duration_seconds: `3`
- manual_interventions: `0`


## KPI-сводка novice path

- total scenarios: `9`
- passed scenarios: `9`
- completion_rate_percent: `100`
- max_time_to_first_success_seconds: `3`
- max_time_to_first_success_minutes_ceiling: `1`
- total_manual_interventions: `0`
- planned wizard answers are controlled scenario inputs, not support interventions.

## Что проверено

- Wizard fallback выбирает маршруты без ручного знания внутренних preset-имен.
- Guided launcher проходит полный путь через единый entrypoint: greenfield, brownfield без repo, brownfield с repo и continue-flow.
- В generated project проверен preset в `.chatgpt/active-scenarios.yaml`.
- Проверен mode parity через `validate-mode-parity.py`.
- Покрыты canonical modes:
  - `greenfield-product`
  - `brownfield-without-repo`
  - `brownfield-with-repo-modernization`
  - `brownfield-with-repo-integration`
  - `brownfield-with-repo-audit`
- Базовые validators (bootstrap path):
  - `validate-project-preset.py`
  - `validate-policy-preset.py`
  - `validate-change-profile.py`
  - `validate-task-graph.py`
  - `validate-stage.py`
  - `validate-versioning-layer.py`
  - `validate-defect-capture.py`
  - `validate-alignment.py`
  - `validate-mode-parity.py`
  - `create-codex-task-pack.py`
  - `validate-codex-task-pack.py`
  - `validate-codex-routing.py`
- Длинный novice-flow после bootstrap:
  - `tools/fill_smoke_artifacts.py`
  - `validate-stage.py`
  - `validate-evidence.py`
  - `validate-quality.py`
  - `validate-handoff.py`
  - `check-dod.py`
- Шаги guided path:
  - `--guided` создает проект и workspace первой задачи.
  - `--continue` создает следующий feature workspace и печатает operator next step.
