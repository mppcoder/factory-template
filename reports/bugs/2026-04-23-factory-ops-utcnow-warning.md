# Bug Report: factory-ops `utcnow()` deprecation warning

- Date: `2026-04-23`
- Type: incidental regression found during `release-2.5/verify-closeout`
- Layer: `factory-template / workspace-packs/factory-ops`
- Scope decision: `fixed-in-scope`

## Reproduce

1. Run:
   - `bash workspace-packs/factory-ops/apply-template-patch.sh <bundle> --apply-safe-zones`
   - `bash workspace-packs/factory-ops/rollback-template-patch.sh <bundle> --rollback`
2. Observe stderr warning from embedded Python snippets.

## Evidence

- Warning text: `DeprecationWarning: datetime.datetime.utcnow() is deprecated ...`
- Affected files:
  - `workspace-packs/factory-ops/apply-template-patch.sh`
  - `workspace-packs/factory-ops/rollback-template-patch.sh`

## Expected

No deprecation warnings in normal upgrade/rollback operator path.

## Actual

Warnings were emitted due to `datetime.utcnow()` usage in embedded snippets.

## Fix

- Replaced `datetime.utcnow()` with timezone-aware:
  - `datetime.now(datetime.timezone.utc)` formatting to `...Z`
- Re-ran upgrade/rollback cycle after patch: warnings no longer reproduced.

## Verification

- `bash template-repo/scripts/verify-all.sh ci` — green.
- `bash MATRIX_TEST.sh` — green (includes upgrade-report + rollback checks).
