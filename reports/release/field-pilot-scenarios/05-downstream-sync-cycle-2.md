# FP-05: Downstream sync cycle 2 / второй downstream sync

## Статус

- Current status: `pending`
- Evidence class: field pilot
- Result: `no-field-evidence`

## Входные условия

- FP-04 completed или имеет accepted blocker, который всё ещё позволяет second controlled sync attempt.
- Используется та же downstream lineage, а не fresh one-off fixture.
- Cycle 1 artifacts сохранены для comparison.

## Ожидаемый результат

- Second template patch export against post-cycle-1 downstream state.
- Second upgrade summary.
- Evidence, что project-owned state из cycle 1 preserved.
- Second rollback proof.

## Измеряемые KPI

| KPI | Pass threshold |
|---|---:|
| Same-lineage sync cycles completed | `2` |
| Project-owned preservation after cycle 2 | `100%` |
| Rollback success | `100%` |
| Critical defects open at closeout | `0` |

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

## Pass criteria / критерии прохождения

- Cycle 2 applies on same downstream lineage.
- Cycle 1 project-owned state preserved.
- Rollback remains reliable after repeated sync.
- Any new gap captured before remediation.

## Fail criteria / критерии провала

- Cycle 2 works only on fresh project и не доказывает repeated downstream use.
- Second cycle loses или overwrites project-owned state.
- Rollback cannot restore expected state.

## Repo artifacts to retain / сохраняемые артефакты

- Cycle 2 upgrade summary.
- Cycle 1 vs cycle 2 changed-path comparison.
- Preservation check notes.
- Rollback result summary.
