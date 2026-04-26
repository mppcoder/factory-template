# FP-04: Downstream sync cycle 1 / первый downstream sync

## Статус

- Current status: `pending`
- Evidence class: field pilot
- Result: `no-field-evidence`

## Входные условия

- Есть real downstream project из FP-01, FP-02 или FP-03.
- Downstream project имеет committed baseline state перед sync.
- Operator может сохранить sanitized changed-path inventory и rollback evidence.

## Ожидаемый результат

- Template patch export для downstream project.
- Human-readable upgrade summary.
- Safe-zone apply result.
- Rollback proof.
- Defect reports для каждого failed или surprising step.

## Измеряемые KPI

| KPI | Pass threshold |
|---|---:|
| Safe-zone apply success | `100%` или documented blocker |
| Rollback success | `100%` |
| Project-owned overwrite incidents | `0` |
| Undocumented manual interventions | `0` |

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

## Pass criteria / критерии прохождения

- Safe-zone apply successful или blocked с clear linked defect.
- Rollback restores expected baseline.
- Project-owned files не overwritten.
- Downstream project remains usable after the cycle.

## Fail criteria / критерии провала

- Apply или rollback fails без linked defect report.
- Project-owned files changed by safe-zone apply.
- Operator не может identify what changed.

## Repo artifacts to retain / сохраняемые артефакты

- Upgrade summary.
- Changed-path inventory.
- Apply and rollback result summary.
- Links to defects или blockers.
