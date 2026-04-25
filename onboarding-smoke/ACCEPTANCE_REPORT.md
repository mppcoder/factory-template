# Onboarding Smoke Acceptance

- Run timestamp (UTC): `2026-04-25T07:47:56Z`
- Runner: `onboarding-smoke/run-novice-e2e.sh`
- Root: `/projects/factory-template`

## Scenario Results

1. `greenfield-novice`
- status: `green`
- expected preset: `greenfield-product`
- generated project: `/projects/factory-template/onboarding-smoke/.tmp-run/greenfield-novice/novice-greenfield-smoke`
- log: `/projects/factory-template/onboarding-smoke/.tmp-run/greenfield-novice.txt`

2. `brownfield-novice`
- status: `green`
- expected preset: `brownfield-with-repo-modernization`
- generated project: `/projects/factory-template/onboarding-smoke/.tmp-run/brownfield-novice/novice-brownfield-smoke`
- log: `/projects/factory-template/onboarding-smoke/.tmp-run/brownfield-novice.txt`

3. `guided-launcher-greenfield`
- status: `green`
- expected preset: `greenfield-product`
- generated project: `/projects/factory-template/onboarding-smoke/.tmp-run/guided-launcher-greenfield/guided-launcher-smoke`
- log: `/projects/factory-template/onboarding-smoke/.tmp-run/guided-launcher-greenfield.txt`

## What Was Verified

- Beginner wizard route selection without manual preset terminology.
- Guided launcher route selection and project creation through the unified entrypoint.
- Generated project preset alignment in `.chatgpt/active-scenarios.yaml`.
- Baseline validators (bootstrap path):
  - `validate-project-preset.py`
  - `validate-policy-preset.py`
  - `validate-change-profile.py`
  - `validate-task-graph.py`
  - `validate-stage.py`
  - `validate-versioning-layer.py`
  - `validate-defect-capture.py`
  - `validate-alignment.py`
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
