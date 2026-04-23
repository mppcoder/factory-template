# Bug Report: novice onboarding E2E covers only bootstrap validators

- Date: `2026-04-23`
- Type: defect
- Layer: `factory-template / onboarding-smoke`
- Status: `fixed-in-scope`

## Reproduce

1. Run:
   `bash onboarding-smoke/run-novice-e2e.sh`
2. Open `onboarding-smoke/ACCEPTANCE_REPORT.md`.

## Evidence

- Report verifies route selection, preset alignment and baseline validators only.
- No long-flow checks are executed (`validate-evidence.py`, `validate-quality.py`, `check-dod.py` after artifact filling).
- Result can be green while post-bootstrap novice lifecycle is not exercised.

## Expected

Novice acceptance should include at least one longer user flow beyond bootstrap validators.

## Actual

Current acceptance remains shallow and mostly structural.

## Scope Decision

- Fix in current scope: `yes`
- Reusable issue: `yes` (release readiness quality gate)

## Fix Applied

- `onboarding-smoke/run-novice-e2e.sh` расширен:
  - после bootstrap validators запускается `tools/fill_smoke_artifacts.py`;
  - добавлен post-bootstrap long-flow validation:
    - `validate-stage.py`
    - `validate-evidence.py`
    - `validate-quality.py`
    - `validate-handoff.py`
    - `check-dod.py`
- `onboarding-smoke/ACCEPTANCE_REPORT.md` теперь явно фиксирует long-flow acceptance section.

## Verification

- `bash onboarding-smoke/run-novice-e2e.sh` -> green.
- `onboarding-smoke/ACCEPTANCE_REPORT.md` содержит блок `Long-flow novice acceptance (post-bootstrap)`.
- `bash template-repo/scripts/verify-all.sh ci` -> green (включает novice onboarding smoke).
