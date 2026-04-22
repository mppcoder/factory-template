# Release Checklist

## Scope

- Repo: `factory-template`
- Current release line: `2.4.4`
- Current working section in changelog: `2.4.4`

## Intent Signals

- [x] release pass started
- [x] release note drafted
- [x] go/no-go review in progress

## Before Release Decision

- [x] Проверить `CHANGELOG.md`
- [x] Проверить `CURRENT_FUNCTIONAL_STATE.md`
- [x] Проверить `TEST_REPORT.md`
- [x] Проверить `VERIFY_SUMMARY.md`
- [x] Проверить `RELEASE_NOTES.md`
- [x] Проверить `RELEASE_NOTE_TEMPLATE.md`
- [x] Проверить `.chatgpt/release-decision.yaml`
- [x] При необходимости свериться с `COMMIT_MESSAGE_GUIDE.md`
- [x] Проверить `meta-template-project/RELEASE_NOTES.md`
- [x] Убедиться, что release note отражает изменения в template/runtime/policy layer
- [x] Убедиться, что `RELEASE_NOTES.md` является notes source в `.chatgpt/release-decision.yaml`

## Required Commands

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
