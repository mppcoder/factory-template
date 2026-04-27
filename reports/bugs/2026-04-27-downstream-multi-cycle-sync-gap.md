# Downstream multi-cycle sync proof gap

Дата: 2026-04-27.

## Summary

Downstream sync v3 уже имел synthetic safe/advisory/manual pass в `MATRIX_TEST.sh`, но этот pass не доказывал устойчивость нескольких последовательных циклов: safe apply -> project-owned manual edits -> advisory review -> новый safe update -> rollback -> brownfield conversion.

Дополнительно Stage 5 production VPS field-pilot artifacts не были явно разведены в sync manifest по safe/advisory/manual boundary: deploy templates/scripts, docs/reports, `deploy/.env`, `.factory-runtime/`, runtime transcripts и real VPS approval boundary.

## Reproduce

1. Запустить прежний `bash MATRIX_TEST.sh`.
2. Найти downstream sync block вокруг `tiered-preview-v3-multizone`.
3. Проверить, что он выполняет один synthetic export/apply/rollback pass на одном downstream fixture.
4. Проверить `factory-sync-manifest.yaml`: production VPS field-pilot docs/scripts/reports/runtime boundaries не описаны как отдельный downstream sync contour.

## Evidence

- Старый matrix path проверял `safe-generated`, `safe-clone`, `advisory-review`, `manual-project-owned`, но не сохранял отдельную multi-cycle fixture/report.
- Rollback проверялся после одного apply, а не после manual edits между циклами.
- Brownfield `converted_greenfield` был покрыт lifecycle validators, но не отдельной downstream sync проверкой сохранения brownfield history.
- Field-pilot deploy/runbook/runtime boundaries существовали в docs/scripts, но не были явно закреплены в sync manifest.

## Expected

- Multi-cycle sync report существует и честно описывает synthetic boundary.
- Project-owned изменения защищены между циклами.
- Advisory-review не применяется автоматически.
- Rollback metadata корректна после нескольких циклов.
- Brownfield history сохраняется после `converted_greenfield`.
- Production VPS field-pilot docs/scripts/reports синхронизируются как safe/advisory zones, а `deploy/.env`, `.factory-runtime/`, runtime transcripts, real VPS approval и secrets остаются manual-only.

## Actual

До remediation это было частично доказано только одним matrix pass и field evidence на downstream repo, без отдельного repo-controlled multi-cycle validator.

## Layer classification

- Слой: factory ops / downstream sync v3 validation.
- Reusable issue: да, потому что downstream/battle repos полагаются на один и тот же sync manifest и rollback tooling.
- Severity: medium. Safe apply path уже был ограничен, но acceptance evidence было недостаточно для multi-cycle guarantee.

## Remediation status

Исправлено in-scope:

- добавлен `factory/producer/extensions/workspace-packs/factory-ops/validate-downstream-multi-cycle-sync.py`;
- расширен `factory-sync-manifest.yaml` для production VPS field-pilot safe/advisory/manual boundaries;
- `MATRIX_TEST.sh` запускает multi-cycle proof;
- создан `reports/release/downstream-multi-cycle-sync-report.md`;
- обновлены `docs/downstream-upgrade-policy.md`, `TEST_REPORT.md`, `CURRENT_FUNCTIONAL_STATE.md`.

## Verification

- `python3 factory/producer/extensions/workspace-packs/factory-ops/validate-downstream-multi-cycle-sync.py . --report-output reports/release/downstream-multi-cycle-sync-report.md` проходит.
- Финальная acceptance-команда: `bash template-repo/scripts/verify-all.sh ci`.
