# Bug Report: check-template-drift false-positive on optional bootstrap zone

- Date: `2026-04-23`
- Type: defect
- Layer: `factory-template / factory/producer/extensions/workspace-packs/factory-ops`
- Status: `fixed-in-scope`

## Reproduce

1. Run:
   `python3 factory/producer/extensions/workspace-packs/factory-ops/check-template-drift.py /projects/factory-template /projects/factory-template/tests/onboarding-smoke/.tmp-run/brownfield-novice/novice-brownfield-smoke --format json`
2. Inspect `drift` and `summary`.

## Evidence

- `sync_zones` contains `bootstrap`.
- Generated downstream project does not include `bootstrap` as a project-root sync zone.
- Report marks `bootstrap` as:
  - `status: missing`
  - `factory_exists: true`
  - `project_exists: false`
- `summary.has_drift` becomes `true` partly because of this expected missing zone.

## Expected

Optional/expected-absent zones should not be treated as drift issue in summary verdict.

## Actual

Expected missing `bootstrap` is counted as drift-like issue/noise.

## Scope Decision

- Fix in current scope: `yes`
- Reusable issue: `yes` (affects downstream operator reporting UX)

## Fix Applied

- `factory-sync-manifest.yaml`: `bootstrap` переведен в declarative optional zone (`optional_in_project: true`).
- `check-template-drift.py`:
  - добавлен статус `optional-missing-project`;
  - optional missing больше не засчитывается как drift в `summary.has_drift`;
  - human summary теперь явно показывает `optional-missing`.
- `export-template-patch.sh` поддерживает structured `sync_zones` entries и корректно помечает optional-absent зоны.

## Verification

- `python3 factory/producer/extensions/workspace-packs/factory-ops/check-template-drift.py <factory> <downstream> --format json`:
  - `bootstrap` -> `optional-missing-project`
  - `summary.has_drift` -> `false` (при отсутствии других проблем).
- `bash template-repo/scripts/verify-all.sh ci` -> green.
