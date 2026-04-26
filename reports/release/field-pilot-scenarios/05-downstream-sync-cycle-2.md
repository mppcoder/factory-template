# FP-05: Downstream sync cycle 2 / второй downstream sync

## Статус

- Current status: `passed`
- Evidence class: field pilot
- Result: `passed-on-same-openclaw-brownfield-lineage`
- Execution date: `2026-04-26`
- Downstream repo: `https://github.com/mppcoder/openclaw-brownfield`
- Local checkout: `/projects/openclaw-brownfield`
- Evidence commit: `2dc6515`

## Входные условия

- FP-04 completed или имеет accepted blocker, который всё ещё позволяет second controlled sync attempt.
- Используется та же downstream lineage, а не fresh one-off fixture.
- Cycle 1 artifacts сохранены для comparison.

Observed input:

- FP-04 completed on the same lineage at commit `1826f07`.
- Cycle 1 artifact `downstream-sync/cycle-1.md` existed before cycle 2, after safe apply and after rollback.
- Baseline status before cycle 2: clean on `main...origin/main`.

## Ожидаемый результат

- Second template patch export against post-cycle-1 downstream state.
- Second upgrade summary.
- Evidence, что project-owned state из cycle 1 preserved.
- Second rollback proof.

## Фактический результат

- Second template patch export completed against the post-cycle-1 downstream state.
- Second safe-zone apply completed for the same `2` template-owned scenario files.
- Cycle 1 evidence remained present before and after rollback.
- Second rollback with project snapshot restore completed.
- Project-owned OpenClaw zones were not overwritten.

## Измеряемые KPI

| KPI | Pass threshold | Result |
|---|---:|---:|
| Same-lineage sync cycles completed | `2` | `2` |
| Project-owned preservation after cycle 2 | `100%` | pass |
| Rollback success | `100%` | pass |
| Critical defects open at closeout | `0` | `0` |

## Команды / шаги

1. Зафиксировать post-cycle-1 baseline:
   `git status --short --branch`
2. Export second template patch:
   `bash factory/producer/extensions/workspace-packs/factory-ops/export-template-patch.sh <factory-root> <downstream-root>`
3. Сгенерировать second upgrade summary:
   `python3 factory/producer/extensions/workspace-packs/factory-ops/upgrade-report.py <factory-root> <downstream-root> --format markdown --output UPGRADE_SUMMARY.md`
4. Выполнить safe-zone apply with project snapshot.
5. Проверить project-owned preservation через сравнение changed-path inventory с cycle 1.
6. Выполнить rollback check и rollback restore.
7. Записать results в `reports/release/2.5-field-pilot-evidence.md`.

Executed commands:

```bash
git status --short --branch
bash /projects/factory-template/factory/producer/extensions/workspace-packs/factory-ops/export-template-patch.sh /projects/factory-template /projects/openclaw-brownfield --dry-run
python /projects/factory-template/factory/producer/extensions/workspace-packs/factory-ops/upgrade-report.py /projects/factory-template /projects/openclaw-brownfield --format markdown --output /projects/openclaw-brownfield/_factory-sync-export/UPGRADE_SUMMARY-cycle2.md
bash /projects/factory-template/factory/producer/extensions/workspace-packs/factory-ops/apply-template-patch.sh /projects/openclaw-brownfield/_factory-sync-export --check
bash /projects/factory-template/factory/producer/extensions/workspace-packs/factory-ops/apply-template-patch.sh /projects/openclaw-brownfield/_factory-sync-export --apply-safe-zones --with-project-snapshot
test -f /projects/openclaw-brownfield/downstream-sync/cycle-1.md
bash /projects/factory-template/factory/producer/extensions/workspace-packs/factory-ops/rollback-template-patch.sh /projects/openclaw-brownfield/_factory-sync-export --check
bash /projects/factory-template/factory/producer/extensions/workspace-packs/factory-ops/rollback-template-patch.sh /projects/openclaw-brownfield/_factory-sync-export --rollback --restore-project-snapshot
test -f /projects/openclaw-brownfield/downstream-sync/cycle-1.md
bash scripts/verify-all.sh
```

Command results:

- safe-generated preview: `3`, generated for apply: `2`.
- rollback: `restored_files=2`, `removed_files=0`, `missing_backup_entries=0`, `project_snapshot_restored=true`.
- preservation check: `downstream-sync/cycle-1.md` remained present.
- downstream verify: `VERIFY-ALL ПРОЙДЕН (full)`.

## Pass criteria / критерии прохождения

- Cycle 2 applies on same downstream lineage.
- Cycle 1 project-owned state preserved.
- Rollback remains reliable after repeated sync.
- Any new gap captured before remediation.

Status: passed.

## Fail criteria / критерии провала

- Cycle 2 works only on fresh project и не доказывает repeated downstream use.
- Second cycle loses или overwrites project-owned state.
- Rollback cannot restore expected state.

## Repo artifacts to retain / сохраняемые артефакты

- Cycle 2 upgrade summary.
- Cycle 1 vs cycle 2 changed-path comparison.
- Preservation check notes.
- Rollback result summary.

Retained in:

- `https://github.com/mppcoder/openclaw-brownfield` commit `2dc6515`.
- `/projects/openclaw-brownfield/downstream-sync/cycle-1.md`.
- `/projects/openclaw-brownfield/downstream-sync/cycle-2.md`.
