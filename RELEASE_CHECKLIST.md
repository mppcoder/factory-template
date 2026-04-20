# Release Checklist

## Scope

- Repo: `factory-template`
- Current release line: `2.4.1`
- Current working section in changelog: `2.4.1`

## Intent Signals

- [x] release pass started
- [x] release note drafted
- [x] go/no-go review in progress

## Before Release Decision

- [x] Проверить `CHANGELOG.md`
- [x] Проверить `CURRENT_FUNCTIONAL_STATE.md`
- [x] Проверить `TEST_REPORT.md`
- [x] Проверить `VERIFY_SUMMARY.md`
- [x] Проверить `RELEASE_NOTE_TEMPLATE.md`
- [x] При необходимости свериться с `COMMIT_MESSAGE_GUIDE.md`
- [x] Проверить `meta-template-project/RELEASE_NOTES.md`
- [x] Убедиться, что release note отражает изменения в template/runtime/policy layer

## Required Commands

- [x] `bash POST_UNZIP_SETUP.sh`
- [x] `bash VALIDATE_FACTORY_TEMPLATE_OPS.sh`
- [x] `bash SMOKE_TEST.sh`
- [x] `bash EXAMPLES_TEST.sh`
- [x] `bash MATRIX_TEST.sh`
- [x] `bash CLEAN_VERIFY_ARTIFACTS.sh`
- [x] `bash PRE_RELEASE_AUDIT.sh`

## Release Layer Checks

- [x] `VERSION.md`, `FACTORY_MANIFEST.yaml` и `template-repo/TEMPLATE_MANIFEST.yaml` согласованы
- [x] `factory-template-ops-policy.yaml` валиден
- [x] curated Sources packs собираются
- [x] boundary-actions guide генерируется
- [x] временные verify artifacts очищены перед release build

## External Boundary Readiness

- [x] есть готовые инструкции для `git` / GitHub
- [x] есть готовые инструкции для ChatGPT Project Sources
- [x] нет шагов, требующих ручного угадывания

## Go / No-Go

- [x] release bundle можно собирать
- [ ] или явно зафиксирован `no-release` с причиной
