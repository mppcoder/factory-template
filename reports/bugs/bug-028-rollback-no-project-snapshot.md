# Bug Report: rollback does not restore manual changes outside safe-zone files

- Date: `2026-04-23`
- Type: defect
- Layer: `factory-template / workspace-packs/factory-ops`
- Status: `fixed-in-scope`

## Reproduce

1. Prepare downstream project and patch bundle.
2. Make manual edit in non-safe-zone file (for example `README.md` in downstream project).
3. Run:
   - `bash workspace-packs/factory-ops/apply-template-patch.sh <bundle> --apply-safe-zones`
   - `bash workspace-packs/factory-ops/rollback-template-patch.sh <bundle> --rollback`
4. Re-check manual edit.

## Evidence

- `rollback-template-patch.sh` restores only files listed in `rollback-state.json`.
- Files outside generated safe-zone targets are not part of state and remain changed.
- This limits rollback guarantee for downstream operators in mixed manual+template update sessions.

## Expected

Operator should have optional full-project rollback path to restore entire project state captured before apply.

## Actual

Rollback scope is limited to generated safe-zone files.

## Scope Decision

- Fix in current scope: `yes` (add optional project snapshot + restore mode)
- Reusable issue: `yes` (downstream safety UX)

## Fix Applied

- `apply-template-patch.sh`:
  - добавлен optional flag `--with-project-snapshot` для режима `--apply-safe-zones`;
  - создается full-project snapshot archive (`project-snapshot.tar.gz`, исключая `.git` и `_factory-sync-export`);
  - snapshot metadata добавляется в `rollback-state.json`.
- `rollback-template-patch.sh`:
  - добавлен optional flag `--restore-project-snapshot` для режима `--rollback`;
  - реализовано восстановление полного snapshot состояния проекта (с удалением лишних non-excluded файлов).
- `upgrade-report.py` и operator docs обновлены под snapshot commands.

## Verification

- Reproduce с manual marker вне safe-zone:
  - apply: `--apply-safe-zones --with-project-snapshot`
  - rollback: `--rollback --restore-project-snapshot`
  - marker удаляется после rollback.
- `MATRIX_TEST.sh` теперь включает `manual-marker-after-rollback` check.
- `bash MATRIX_TEST.sh` и `bash template-repo/scripts/verify-all.sh ci` -> green.
