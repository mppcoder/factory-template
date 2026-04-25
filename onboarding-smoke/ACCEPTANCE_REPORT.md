# Onboarding Smoke Acceptance

- Run timestamp (UTC): `2026-04-25T21:05:24Z`
- Runner: `onboarding-smoke/run-novice-e2e.sh`
- Root: `/projects/factory-template`

## Результаты сценариев

1. `greenfield-novice`
- status: `green`
- expected preset: `greenfield-product`
- generated project: `/projects/factory-template/onboarding-smoke/.tmp-run/greenfield-novice/novice-greenfield-smoke`
- log: `/projects/factory-template/onboarding-smoke/.tmp-run/greenfield-novice.txt`

2. `brownfield-without-repo-novice`
- status: `green`
- expected preset: `brownfield-without-repo`
- generated project: `/projects/factory-template/onboarding-smoke/.tmp-run/brownfield-without-repo-novice/novice-brownfield-no-repo-smoke`
- log: `/projects/factory-template/onboarding-smoke/.tmp-run/brownfield-without-repo-novice.txt`

3. `brownfield-modernization-novice`
- status: `green`
- expected preset: `brownfield-with-repo-modernization`
- generated project: `/projects/factory-template/onboarding-smoke/.tmp-run/brownfield-modernization-novice/novice-brownfield-modernization-smoke`
- log: `/projects/factory-template/onboarding-smoke/.tmp-run/brownfield-modernization-novice.txt`

4. `brownfield-integration-novice`
- status: `green`
- expected preset: `brownfield-with-repo-integration`
- generated project: `/projects/factory-template/onboarding-smoke/.tmp-run/brownfield-integration-novice/novice-brownfield-integration-smoke`
- log: `/projects/factory-template/onboarding-smoke/.tmp-run/brownfield-integration-novice.txt`

5. `brownfield-audit-novice`
- status: `green`
- expected preset: `brownfield-with-repo-audit`
- generated project: `/projects/factory-template/onboarding-smoke/.tmp-run/brownfield-audit-novice/novice-brownfield-audit-smoke`
- log: `/projects/factory-template/onboarding-smoke/.tmp-run/brownfield-audit-novice.txt`

6. `guided-launcher-greenfield`
- status: `green`
- expected preset: `greenfield-product`
- generated project: `/projects/factory-template/onboarding-smoke/.tmp-run/guided-launcher-greenfield/guided-launcher-greenfield-smoke`
- log: `/projects/factory-template/onboarding-smoke/.tmp-run/guided-launcher-greenfield.txt`

7. `guided-launcher-brownfield-no-repo`
- status: `green`
- expected preset: `brownfield-without-repo`
- generated project: `/projects/factory-template/onboarding-smoke/.tmp-run/guided-launcher-brownfield-no-repo/guided-launcher-brownfield-no-repo-smoke`
- log: `/projects/factory-template/onboarding-smoke/.tmp-run/guided-launcher-brownfield-no-repo.txt`

8. `guided-launcher-brownfield-with-repo`
- status: `green`
- expected preset: `brownfield-with-repo-modernization`
- generated project: `/projects/factory-template/onboarding-smoke/.tmp-run/guided-launcher-brownfield-with-repo/guided-launcher-brownfield-with-repo-smoke`
- log: `/projects/factory-template/onboarding-smoke/.tmp-run/guided-launcher-brownfield-with-repo.txt`

9. `guided-launcher-continue-flow`
- status: `green`
- expected preset: `greenfield-product`
- generated project: `/projects/factory-template/onboarding-smoke/.tmp-run/guided-launcher-continue-flow/guided-launcher-continue-flow-smoke`
- log: `/projects/factory-template/onboarding-smoke/.tmp-run/guided-launcher-continue-flow.txt`


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
