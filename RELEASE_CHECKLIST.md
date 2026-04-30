# Release checklist / чеклист релиза

## Scope / область

- Repo: `factory-template`
- Current release line: `2.5.2`
- Current working section in changelog: `2.5.2`
- Next planned release program line: `none`
- Release truth source: `docs/releases/release-scorecard.yaml`
- Current 2.5 stage: `release publication / release artifact assembly`
- Status: `2.5.2 Package Ready`
- GA-ready: `true`

## Intent signals / сигналы намерения

- [x] release pass started
- [x] release note drafted
- [x] go/no-go review in progress

## Перед release decision

- [x] Проверить `CHANGELOG.md`
- [x] Проверить `CURRENT_FUNCTIONAL_STATE.md`
- [x] Проверить `TEST_REPORT.md`
- [x] Проверить `UPGRADE_SUMMARY.md`
- [x] Проверить `tests/onboarding-smoke/ACCEPTANCE_REPORT.md`
- [x] Проверить `VERIFY_SUMMARY.md`
- [x] Проверить `RELEASE_NOTES.md`
- [x] Проверить `RELEASE_NOTE_TEMPLATE.md`
- [x] Проверить `.chatgpt/release-decision.yaml`
- [x] При необходимости свериться с `COMMIT_MESSAGE_GUIDE.md`
- [x] Проверить `docs/releases/factory-template-release-notes.md`
- [x] Убедиться, что release note отражает изменения в template/runtime/policy layer
- [x] Убедиться, что `RELEASE_NOTES.md` является notes source в `.chatgpt/release-decision.yaml`

## Обязательные команды

- [x] `bash template-repo/scripts/verify-all.sh ci`
- [x] `bash tests/onboarding-smoke/run-novice-e2e.sh`
- [x] `bash POST_UNZIP_SETUP.sh`
- [x] `bash VALIDATE_FACTORY_TEMPLATE_OPS.sh`
- [x] `bash VALIDATE_VERIFIED_SYNC_PREREQS.sh`
- [x] `bash VALIDATE_RELEASE_DECISION.sh`
- [x] `bash VALIDATE_RELEASE_NOTES_SOURCE.sh`
- [x] `python3 template-repo/scripts/validate-release-scorecard.py .`
- [x] `bash SMOKE_TEST.sh`
- [x] `bash EXAMPLES_TEST.sh`
- [x] `bash MATRIX_TEST.sh`
- [x] `bash CLEAN_VERIFY_ARTIFACTS.sh`
- [x] `bash PRE_RELEASE_AUDIT.sh`
- [x] `bash RELEASE_BUILD.sh`
- [x] `sha256sum -c factory-v2.5.2.zip.sha256`
- [x] `python3 template-repo/scripts/validate-release-package.py <archive> --checksum <sha256> --manifest <manifest>`
- [x] `python3 factory/producer/extensions/workspace-packs/factory-ops/upgrade-report.py <factory-root> <downstream-root> --format markdown --output UPGRADE_SUMMARY.md`
- [x] `bash factory/producer/extensions/workspace-packs/factory-ops/apply-template-patch.sh <downstream-root>/_factory-sync-export --apply-safe-zones`
- [x] `bash factory/producer/extensions/workspace-packs/factory-ops/apply-template-patch.sh <downstream-root>/_factory-sync-export --apply-safe-zones --with-project-snapshot`
- [x] `bash factory/producer/extensions/workspace-packs/factory-ops/rollback-template-patch.sh <downstream-root>/_factory-sync-export --rollback`
- [x] `bash factory/producer/extensions/workspace-packs/factory-ops/rollback-template-patch.sh <downstream-root>/_factory-sync-export --rollback --restore-project-snapshot`

## Обязательные CI checks (branch protection contract)

- [x] `CI / verify-baseline`
- [x] `CI / release-bundle-dry-run`
- [x] Верификация fix-пакета на GitHub Actions: run `24840192862` (2026-04-23), оба job в статусе `success`

## Verify entrypoint / точка входа проверки

- [x] Операторский единый запуск: `bash template-repo/scripts/verify-all.sh`
- [x] Быстрый режим: `bash template-repo/scripts/verify-all.sh quick`
- [x] CI-режим: `bash template-repo/scripts/verify-all.sh ci`

## Проверки release layer

- [x] `VERSION.md`, `FACTORY_MANIFEST.yaml` и `template-repo/TEMPLATE_MANIFEST.yaml` согласованы
- [x] `bash RELEASE_BUILD.sh` создает `factory-v2.5.2.zip`, `factory-v2.5.2.manifest.yaml` и `factory-v2.5.2.zip.sha256`
- [x] archive распакован в temp и содержит один root `factory-v2.5.2/`
- [x] release archive содержит только ASCII paths (`NON_ASCII_COUNT=0`) для portable GUI/Windows unzip compatibility
- [x] release archive исключает transient `.tmp-run/` и проходит portable path-length gate (`MAX_PATH_LEN <= 180`)
- [x] в распакованном root проходят `bash POST_UNZIP_SETUP.sh` и targeted package verification
- [x] `factory-template-ops-policy.yaml` валиден
- [x] curated export/reference packs собираются
- [x] boundary-actions guide генерируется
- [x] verified sync выполнен или детерминированно завершился как no-op
- [x] временные verify artifacts очищены перед release build

## Готовность external boundary

- [x] есть готовые инструкции для `git` / GitHub
- [x] есть готовые инструкции для repo-first ChatGPT Project
- [x] нет шагов, требующих ручного угадывания

## Go / no-go решение

- [x] release bundle можно собирать с manifest/checksum evidence
- [x] явно зафиксирован patch release package для `2.5.2`

## 2.5 program framing gate (closed)

- [x] Зафиксирован dual-track контур: `2.5-A` (engineering hardening) и `2.5-B` (beginner-first productization)
- [x] Канонический roadmap создан: `docs/releases/2.5-roadmap.md`
- [x] Канонические метрики и пороги MVP/full зафиксированы: `docs/releases/2.5-success-metrics.md`
- [x] `README.md`, `CURRENT_FUNCTIONAL_STATE.md` и `RELEASE_NOTES.md` синхронизированы с новой целью `2.5`
- [x] Repo-first и scenario-pack принципы сохранены в release-facing описании

## 2.5 RC closeout gate (verify-closeout)

- [x] Downstream dry-run/apply/rollback path человекочитаемо описан и проверен (`UPGRADE_SUMMARY.md`)
- [x] `greenfield novice` E2E зеленый (`tests/onboarding-smoke/ACCEPTANCE_REPORT.md`)
- [x] `brownfield novice` E2E зеленый (`tests/onboarding-smoke/ACCEPTANCE_REPORT.md`)
- [x] `TEST_REPORT.md` и release-facing docs обновлены как beginner-first + hardening, а не docs-only polish
- [x] инцидентные дефекты из verify-прохода зафиксированы через defect-capture path
- [x] GA-ready declared
- [x] GA KPI evidence зафиксирован: `docs/releases/2.5-ga-kpi-evidence.md`

## 2.5 scorecard gates

- [x] `G25-0` — program framing и scope normalization закрыты.
- [x] `G25-RC` — RC closeout evidence прошел для downstream trial.
- [x] `G25-GA` — passed: full KPI evidence подтвержден.

## 2.5.1 field pilot follow-up

- [x] Зафиксировано, что `2.5.0 GA Ready` опирается на repo-controlled evidence, а не на completed field proof.
- [x] Создан roadmap полевого пилота: `docs/releases/2.5.1-field-pilot-roadmap.md`.
- [x] Создан field evidence register: `reports/release/2.5-field-pilot-evidence.md`.
- [x] Созданы scenario checklists с pass/fail criteria: `reports/release/field-pilot-scenarios/*.md`.
- [x] FP-01 battle greenfield project executed and evidence retained.
- [x] FP-02 battle brownfield without repo executed, GitHub repo `mppcoder/openclaw-brownfield` pushed at commit `7b3d1a4`, and evidence retained.
- [x] FP-03 battle brownfield with repo executed on `mppcoder/openclaw-brownfield` commit `3c026fd` and evidence retained.
- [x] FP-04 downstream sync cycle 1 executed on `mppcoder/openclaw-brownfield` commit `1826f07` and evidence retained.
- [x] FP-05 downstream sync cycle 2 executed on same lineage commit `2dc6515` and evidence retained.
