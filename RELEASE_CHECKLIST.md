# Release Checklist

## Scope

- Repo: `factory-template`
- Current release line: `2.4.4`
- Current working section in changelog: `2.4.4`
- Next planned release program line: `2.5`

## Intent Signals

- [x] release pass started
- [x] release note drafted
- [x] go/no-go review in progress

## Before Release Decision

- [x] Проверить `CHANGELOG.md`
- [x] Проверить `CURRENT_FUNCTIONAL_STATE.md`
- [x] Проверить `TEST_REPORT.md`
- [x] Проверить `UPGRADE_SUMMARY.md`
- [x] Проверить `onboarding-smoke/ACCEPTANCE_REPORT.md`
- [x] Проверить `VERIFY_SUMMARY.md`
- [x] Проверить `RELEASE_NOTES.md`
- [x] Проверить `RELEASE_NOTE_TEMPLATE.md`
- [x] Проверить `.chatgpt/release-decision.yaml`
- [x] При необходимости свериться с `COMMIT_MESSAGE_GUIDE.md`
- [x] Проверить `meta-template-project/RELEASE_NOTES.md`
- [x] Убедиться, что release note отражает изменения в template/runtime/policy layer
- [x] Убедиться, что `RELEASE_NOTES.md` является notes source в `.chatgpt/release-decision.yaml`

## Required Commands

- [x] `bash template-repo/scripts/verify-all.sh ci`
- [x] `bash onboarding-smoke/run-novice-e2e.sh`
- [x] `bash POST_UNZIP_SETUP.sh`
- [x] `bash VALIDATE_FACTORY_TEMPLATE_OPS.sh`
- [x] `bash VALIDATE_VERIFIED_SYNC_PREREQS.sh`
- [x] `bash VALIDATE_RELEASE_DECISION.sh`
- [x] `bash VALIDATE_RELEASE_NOTES_SOURCE.sh`
- [x] `bash SMOKE_TEST.sh`
- [x] `bash EXAMPLES_TEST.sh`
- [x] `bash MATRIX_TEST.sh`
- [x] `bash CLEAN_VERIFY_ARTIFACTS.sh`
- [x] `bash PRE_RELEASE_AUDIT.sh`
- [x] `python3 workspace-packs/factory-ops/upgrade-report.py <factory-root> <downstream-root> --format markdown --output UPGRADE_SUMMARY.md`
- [x] `bash workspace-packs/factory-ops/apply-template-patch.sh <downstream-root>/_factory-sync-export --apply-safe-zones`
- [x] `bash workspace-packs/factory-ops/apply-template-patch.sh <downstream-root>/_factory-sync-export --apply-safe-zones --with-project-snapshot`
- [x] `bash workspace-packs/factory-ops/rollback-template-patch.sh <downstream-root>/_factory-sync-export --rollback`
- [x] `bash workspace-packs/factory-ops/rollback-template-patch.sh <downstream-root>/_factory-sync-export --rollback --restore-project-snapshot`

## Required CI Checks (Branch Protection Contract)

- [x] `CI / verify-baseline`
- [x] `CI / release-bundle-dry-run`
- [x] Верификация fix-пакета на GitHub Actions: run `24840192862` (2026-04-23), оба job в статусе `success`

## Verify Entrypoint

- [x] Операторский единый запуск: `bash template-repo/scripts/verify-all.sh`
- [x] Быстрый режим: `bash template-repo/scripts/verify-all.sh quick`
- [x] CI-режим: `bash template-repo/scripts/verify-all.sh ci`

## Release Layer Checks

- [x] `VERSION.md`, `FACTORY_MANIFEST.yaml` и `template-repo/TEMPLATE_MANIFEST.yaml` согласованы
- [x] `factory-template-ops-policy.yaml` валиден
- [x] curated export/reference packs собираются
- [x] boundary-actions guide генерируется
- [x] verified sync выполнен или детерминированно завершился как no-op
- [x] временные verify artifacts очищены перед release build

## External Boundary Readiness

- [x] есть готовые инструкции для `git` / GitHub
- [x] есть готовые инструкции для repo-first ChatGPT Project
- [x] нет шагов, требующих ручного угадывания

## Go / No-Go

- [x] release bundle можно собирать
- [ ] или явно зафиксирован `no-release` с причиной

## 2.5 Program Framing Gate (Remediation-Prep)

- [x] Зафиксирован dual-track контур: `2.5-A` (engineering hardening) и `2.5-B` (beginner-first productization)
- [x] Канонический roadmap создан: `docs/releases/2.5-roadmap.md`
- [x] Канонические метрики и пороги MVP/full зафиксированы: `docs/releases/2.5-success-metrics.md`
- [x] `README.md`, `CURRENT_FUNCTIONAL_STATE.md` и `RELEASE_NOTES.md` синхронизированы с новой целью `2.5`
- [x] Repo-first и scenario-pack принципы сохранены в release-facing описании

## 2.5 RC Closeout Gate (Verify-Closeout)

- [x] Downstream dry-run/apply/rollback path человекочитаемо описан и проверен (`UPGRADE_SUMMARY.md`)
- [x] `greenfield novice` E2E зеленый (`onboarding-smoke/ACCEPTANCE_REPORT.md`)
- [x] `brownfield novice` E2E зеленый (`onboarding-smoke/ACCEPTANCE_REPORT.md`)
- [x] `TEST_REPORT.md` и release-facing docs обновлены как beginner-first + hardening, а не docs-only polish
- [x] инцидентные дефекты из verify-прохода зафиксированы через defect-capture path
- [ ] GA-ready объявлен

## 2.5 Next 5 Handoff Gates

1. `H25-01 / Gate G25-1a` — hardening backlog normalization и risk register готовы; артефакты: `docs/releases/2.5-roadmap.md`, `RELEASE_NOTES.md`.
2. `H25-02 / Gate G25-2a` — beginner-first onboarding flow и UI-contract baseline зафиксированы; артефакты: `README.md`, `docs/releases/2.5-roadmap.md`.
3. `H25-03 / Gate G25-1` — safe-defaults и compatibility contracts формализованы для downstream evolution; артефакты: `CURRENT_FUNCTIONAL_STATE.md`, `docs/releases/2.5-success-metrics.md`.
4. `H25-04 / Gate G25-3` — MVP-срез `2.5-A + 2.5-B` подтвержден по MVP-порогам; артефакты: `RELEASE_CHECKLIST.md`, `docs/releases/2.5-success-metrics.md`.
5. `H25-05 / Gate G25-4` — full `2.5` release readiness подтверждён по full-порогам и release closeout; артефакты: `RELEASE_NOTES.md`, `RELEASE_CHECKLIST.md`, `docs/releases/2.5-roadmap.md`.
