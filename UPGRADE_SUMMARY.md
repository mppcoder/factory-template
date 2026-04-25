# Сводка safe upgrade UX

- Generated (UTC): `2026-04-25T11:01:19+00:00`
- Factory root: `/projects/factory-template`
- Downstream project root: `/projects/factory-template/onboarding-smoke/.tmp-run/brownfield-novice/novice-brownfield-smoke`
- Template version: `2.4.4`
- Sync contract version: `2`
- Verdict: `patch-ready`

## Snapshot drift / снимок расхождений

- Sync zones: `ok=12` / `drift=0` / `missing=0` / `total=12`
- Materialized files: `ok=1` / `issues=0` / `total=1`

## Tiered impact preview / preview влияния

| Tier | Manifest Items | Preview Items | Generated For Apply | Apply Eligible |
| --- | ---: | ---: | ---: | --- |
| `safe` | `7` | `3` | `2` | `True` |
| `advisory` | `2` | `0` | `0` | `False` |
| `manual-only` | `4` | `0` | `0` | `False` |

### Preview items / элементы preview

- `[safe]` `bootstrap` status=`optional-missing-project` generated=`False`
- `[safe]` `.chatgpt/examples/done-report.example.md` status=`drift` generated=`True`
- `[safe]` `tasks/codex/codex-task-mandatory-bug-capture.block.md` status=`drift` generated=`True`

## Snapshot upgrade bundle / снимок upgrade bundle

- Bundle path: `/projects/factory-template/onboarding-smoke/.tmp-run/brownfield-novice/novice-brownfield-smoke/_factory-sync-export`
- Changed files in bundle: `2`
- Safe generated targets: `2`
- Generated files to materialize: `2`
- Rollback state present: `True`
- Rollback tracked files: `2`

### Changed files / измененные файлы

- `template-repo/template/.chatgpt/examples/done-report.example.md`
- `template-repo/template/tasks/codex/codex-task-mandatory-bug-capture.block.md`

### Generated files / generated files для safe materialization

- `.chatgpt/examples/done-report.example.md`
- `tasks/codex/codex-task-mandatory-bug-capture.block.md`

## Канонические команды оператора

1. Подготовить/обновить bundle (dry-run):
```bash
/projects/factory-template/workspace-packs/factory-ops/export-template-patch.sh /projects/factory-template /projects/factory-template/onboarding-smoke/.tmp-run/brownfield-novice/novice-brownfield-smoke --dry-run
```
2. Проверить bundle перед apply:
```bash
/projects/factory-template/workspace-packs/factory-ops/apply-template-patch.sh /projects/factory-template/onboarding-smoke/.tmp-run/brownfield-novice/novice-brownfield-smoke/_factory-sync-export --check
```
3. Применить safe zones:
```bash
/projects/factory-template/workspace-packs/factory-ops/apply-template-patch.sh /projects/factory-template/onboarding-smoke/.tmp-run/brownfield-novice/novice-brownfield-smoke/_factory-sync-export --apply-safe-zones
```
4. Применить safe zones с full-project snapshot (optional, но безопаснее для mixed manual sessions):
```bash
/projects/factory-template/workspace-packs/factory-ops/apply-template-patch.sh /projects/factory-template/onboarding-smoke/.tmp-run/brownfield-novice/novice-brownfield-smoke/_factory-sync-export --apply-safe-zones --with-project-snapshot
```
5. Проверить rollback state:
```bash
/projects/factory-template/workspace-packs/factory-ops/rollback-template-patch.sh /projects/factory-template/onboarding-smoke/.tmp-run/brownfield-novice/novice-brownfield-smoke/_factory-sync-export --check
```
6. Откатить safe-zone materialization при необходимости:
```bash
/projects/factory-template/workspace-packs/factory-ops/rollback-template-patch.sh /projects/factory-template/onboarding-smoke/.tmp-run/brownfield-novice/novice-brownfield-smoke/_factory-sync-export --rollback
```
7. Откатить и восстановить full project snapshot, если использовался snapshot mode:
```bash
/projects/factory-template/workspace-packs/factory-ops/rollback-template-patch.sh /projects/factory-template/onboarding-smoke/.tmp-run/brownfield-novice/novice-brownfield-smoke/_factory-sync-export --rollback --restore-project-snapshot
```

## UX safety notes / заметки безопасности UX

- `--dry-run` and `--check` are read-only.
- `--apply-safe-zones` now creates rollback metadata before overwriting generated targets.
- `rollback-template-patch.sh --rollback` restores previous content (or removes file if it did not exist).
- Optional snapshot mode adds full-project restore path for manual changes outside generated safe-zones.
