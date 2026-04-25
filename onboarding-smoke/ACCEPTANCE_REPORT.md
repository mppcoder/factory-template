# Onboarding Smoke Acceptance

- Run timestamp (UTC): `2026-04-25T19:57:52Z`
- Runner: `onboarding-smoke/run-novice-e2e.sh`
- Root: `/projects/factory-template`

## Scenario Results

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

7. `guided-launcher-brownfield-audit`
- status: `green`
- expected preset: `brownfield-with-repo-audit`
- generated project: `/projects/factory-template/onboarding-smoke/.tmp-run/guided-launcher-brownfield-audit/guided-launcher-brownfield-audit-smoke`
- log: `/projects/factory-template/onboarding-smoke/.tmp-run/guided-launcher-brownfield-audit.txt`


## What Was Verified

- Beginner wizard route selection without manual preset terminology for all canonical presets.
- Guided launcher route selection and project creation through the unified entrypoint for greenfield and brownfield.
- Generated project preset alignment in `.chatgpt/active-scenarios.yaml`.
- Mode parity validation through `validate-mode-parity.py`.
- Canonical modes covered:
  - `greenfield-product`
  - `brownfield-without-repo`
  - `brownfield-with-repo-modernization`
  - `brownfield-with-repo-integration`
  - `brownfield-with-repo-audit`
- Baseline validators (bootstrap path):
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
- Long-flow novice acceptance (post-bootstrap):
  - `tools/fill_smoke_artifacts.py`
  - `validate-stage.py`
  - `validate-evidence.py`
  - `validate-quality.py`
  - `validate-handoff.py`
  - `check-dod.py`
