# FP-04: Downstream sync cycle 1 / первый downstream sync

## Статус

- Current status: `passed`
- Evidence class: field pilot
- Result: `passed-on-openclaw-brownfield-lineage`
- Execution date: `2026-04-26`
- Downstream repo: `https://github.com/mppcoder/openclaw-brownfield`
- Local checkout: `/projects/openclaw-brownfield`
- Evidence commit: `1826f07`

## Входные условия

- Есть real downstream project из FP-01, FP-02 или FP-03.
- Downstream project имеет committed baseline state перед sync.
- Operator может сохранить sanitized changed-path inventory и rollback evidence.

Observed input:

- Downstream lineage: OpenClaw brownfield repo from FP-02/FP-03.
- Baseline status before sync: clean on `main...origin/main`.
- Baseline commit before cycle evidence commit: `3c026fd`.

## Ожидаемый результат

- Template patch export для downstream project.
- Human-readable upgrade summary.
- Safe-zone apply result.
- Rollback proof.
- Defect reports для каждого failed или surprising step.

## Фактический результат

- Template patch export completed.
- Upgrade summary generated.
- Safe-zone apply completed for `2` template-owned scenario files.
- Rollback check passed.
- Rollback with project snapshot restore completed.
- Project-owned OpenClaw zones were preview-only and not overwritten.

## Измеряемые KPI

| KPI | Pass threshold | Result |
|---|---:|---:|
| Safe-zone apply success | `100%` или documented blocker | pass |
| Rollback success | `100%` | pass |
| Project-owned overwrite incidents | `0` | `0` |
| Undocumented manual interventions | `0` | `0` |

## Команды / шаги

1. Зафиксировать downstream baseline:
   `git status --short --branch`
2. Export template patch:
   `bash factory/producer/extensions/workspace-packs/factory-ops/export-template-patch.sh <factory-root> <downstream-root>`
3. Сгенерировать upgrade summary:
   `python3 factory/producer/extensions/workspace-packs/factory-ops/upgrade-report.py <factory-root> <downstream-root> --format markdown --output UPGRADE_SUMMARY.md`
4. Проверить и применить safe zones:
   `bash factory/producer/extensions/workspace-packs/factory-ops/apply-template-patch.sh <downstream-root>/_factory-sync-export --check`
   `bash factory/producer/extensions/workspace-packs/factory-ops/apply-template-patch.sh <downstream-root>/_factory-sync-export --apply-safe-zones --with-project-snapshot`
5. Проверить rollback:
   `bash factory/producer/extensions/workspace-packs/factory-ops/rollback-template-patch.sh <downstream-root>/_factory-sync-export --check`
   `bash factory/producer/extensions/workspace-packs/factory-ops/rollback-template-patch.sh <downstream-root>/_factory-sync-export --rollback --restore-project-snapshot`

Executed commands:

```bash
git status --short --branch
bash /projects/factory-template/factory/producer/extensions/workspace-packs/factory-ops/export-template-patch.sh /projects/factory-template /projects/openclaw-brownfield --dry-run
python /projects/factory-template/factory/producer/extensions/workspace-packs/factory-ops/upgrade-report.py /projects/factory-template /projects/openclaw-brownfield --format markdown --output /projects/openclaw-brownfield/_factory-sync-export/UPGRADE_SUMMARY-cycle1.md
bash /projects/factory-template/factory/producer/extensions/workspace-packs/factory-ops/apply-template-patch.sh /projects/openclaw-brownfield/_factory-sync-export --check
bash /projects/factory-template/factory/producer/extensions/workspace-packs/factory-ops/apply-template-patch.sh /projects/openclaw-brownfield/_factory-sync-export --apply-safe-zones --with-project-snapshot
bash /projects/factory-template/factory/producer/extensions/workspace-packs/factory-ops/rollback-template-patch.sh /projects/openclaw-brownfield/_factory-sync-export --check
bash /projects/factory-template/factory/producer/extensions/workspace-packs/factory-ops/rollback-template-patch.sh /projects/openclaw-brownfield/_factory-sync-export --rollback --restore-project-snapshot
bash scripts/verify-all.sh
```

Command results:

- safe-generated preview: `3`, generated for apply: `2`.
- applied safe files: `template-repo/scenario-pack/00-master-router.md`, `template-repo/scenario-pack/16-done-closeout.md`.
- rollback: `restored_files=2`, `removed_files=0`, `missing_backup_entries=0`, `project_snapshot_restored=true`.
- downstream verify: `VERIFY-ALL ПРОЙДЕН (full)`.

## Pass criteria / критерии прохождения

- Safe-zone apply successful или blocked с clear linked defect.
- Rollback restores expected baseline.
- Project-owned files не overwritten.
- Downstream project remains usable after the cycle.

Status: passed.

## Fail criteria / критерии провала

- Apply или rollback fails без linked defect report.
- Project-owned files changed by safe-zone apply.
- Operator не может identify what changed.

## Repo artifacts to retain / сохраняемые артефакты

- Upgrade summary.
- Changed-path inventory.
- Apply and rollback result summary.
- Links to defects или blockers.

Retained in:

- `https://github.com/mppcoder/openclaw-brownfield` commit `1826f07`.
- `/projects/openclaw-brownfield/downstream-sync/cycle-1.md`.
