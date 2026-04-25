# Safe Upgrade UX Summary

- Generated (UTC): `2026-04-25T11:01:19+00:00`
- Factory root: `/projects/factory-template`
- Downstream project root: `/projects/factory-template/onboarding-smoke/.tmp-run/brownfield-novice/novice-brownfield-smoke`
- Template version: `2.4.4`
- Sync contract version: `2`
- Verdict: `patch-ready`

## Drift Snapshot

- Sync zones: `ok=12` / `drift=0` / `missing=0` / `total=12`
- Materialized files: `ok=1` / `issues=0` / `total=1`

## Tiered Impact Preview

| Tier | Manifest Items | Preview Items | Generated For Apply | Apply Eligible |
| --- | ---: | ---: | ---: | --- |
| `safe` | `7` | `3` | `2` | `True` |
| `advisory` | `2` | `0` | `0` | `False` |
| `manual-only` | `4` | `0` | `0` | `False` |

### Preview Items

- `[safe]` `bootstrap` status=`optional-missing-project` generated=`False`
- `[safe]` `.chatgpt/examples/done-report.example.md` status=`drift` generated=`True`
- `[safe]` `tasks/codex/codex-task-mandatory-bug-capture.block.md` status=`drift` generated=`True`

## Upgrade Bundle Snapshot

- Bundle path: `/projects/factory-template/onboarding-smoke/.tmp-run/brownfield-novice/novice-brownfield-smoke/_factory-sync-export`
- Changed files in bundle: `2`
- Safe generated targets: `2`
- Generated files to materialize: `2`
- Rollback state present: `True`
- Rollback tracked files: `2`

### Changed Files

- `template-repo/template/.chatgpt/examples/done-report.example.md`
- `template-repo/template/tasks/codex/codex-task-mandatory-bug-capture.block.md`

### Generated Files (safe materialization)

- `.chatgpt/examples/done-report.example.md`
- `tasks/codex/codex-task-mandatory-bug-capture.block.md`

## Canonical Operator Commands

1. Prepare/refresh bundle (dry-run):
```bash
/projects/factory-template/workspace-packs/factory-ops/export-template-patch.sh /projects/factory-template /projects/factory-template/onboarding-smoke/.tmp-run/brownfield-novice/novice-brownfield-smoke --dry-run
```
2. Review bundle before apply:
```bash
/projects/factory-template/workspace-packs/factory-ops/apply-template-patch.sh /projects/factory-template/onboarding-smoke/.tmp-run/brownfield-novice/novice-brownfield-smoke/_factory-sync-export --check
```
3. Apply safe zones:
```bash
/projects/factory-template/workspace-packs/factory-ops/apply-template-patch.sh /projects/factory-template/onboarding-smoke/.tmp-run/brownfield-novice/novice-brownfield-smoke/_factory-sync-export --apply-safe-zones
```
4. Apply safe zones with full-project snapshot (optional but safer for mixed manual sessions):
```bash
/projects/factory-template/workspace-packs/factory-ops/apply-template-patch.sh /projects/factory-template/onboarding-smoke/.tmp-run/brownfield-novice/novice-brownfield-smoke/_factory-sync-export --apply-safe-zones --with-project-snapshot
```
5. Inspect rollback state:
```bash
/projects/factory-template/workspace-packs/factory-ops/rollback-template-patch.sh /projects/factory-template/onboarding-smoke/.tmp-run/brownfield-novice/novice-brownfield-smoke/_factory-sync-export --check
```
6. Roll back safe-zone materialization if needed:
```bash
/projects/factory-template/workspace-packs/factory-ops/rollback-template-patch.sh /projects/factory-template/onboarding-smoke/.tmp-run/brownfield-novice/novice-brownfield-smoke/_factory-sync-export --rollback
```
7. Roll back and restore full project snapshot (if snapshot mode was used):
```bash
/projects/factory-template/workspace-packs/factory-ops/rollback-template-patch.sh /projects/factory-template/onboarding-smoke/.tmp-run/brownfield-novice/novice-brownfield-smoke/_factory-sync-export --rollback --restore-project-snapshot
```

## UX Safety Notes

- `--dry-run` and `--check` are read-only.
- `--apply-safe-zones` now creates rollback metadata before overwriting generated targets.
- `rollback-template-patch.sh --rollback` restores previous content (or removes file if it did not exist).
- Optional snapshot mode adds full-project restore path for manual changes outside generated safe-zones.
