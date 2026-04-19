# Release Checklist

## Scope

- Repo: `factory-template`
- Current release line: `2.4.0`
- Current working section in changelog: `Unreleased`

## Intent Signals

- [ ] release pass started
- [ ] release note drafted
- [ ] go/no-go review in progress

## Before Release Decision

- [ ] Проверить `CHANGELOG.md`
- [ ] Проверить `CURRENT_FUNCTIONAL_STATE.md`
- [ ] Проверить `TEST_REPORT.md`
- [ ] Проверить `VERIFY_SUMMARY.md`
- [ ] Проверить `RELEASE_NOTE_TEMPLATE.md`
- [ ] При необходимости свериться с `COMMIT_MESSAGE_GUIDE.md`
- [ ] Проверить `meta-template-project/RELEASE_NOTES.md`
- [ ] Убедиться, что release note отражает изменения в template/runtime/policy layer

## Required Commands

- [ ] `bash POST_UNZIP_SETUP.sh`
- [ ] `bash VALIDATE_FACTORY_TEMPLATE_OPS.sh`
- [ ] `bash SMOKE_TEST.sh`
- [ ] `bash EXAMPLES_TEST.sh`
- [ ] `bash MATRIX_TEST.sh`
- [ ] `bash CLEAN_VERIFY_ARTIFACTS.sh`
- [ ] `bash PRE_RELEASE_AUDIT.sh`

## Release Layer Checks

- [ ] `VERSION.md`, `FACTORY_MANIFEST.yaml` и `template-repo/TEMPLATE_MANIFEST.yaml` согласованы
- [ ] `factory-template-ops-policy.yaml` валиден
- [ ] curated Sources packs собираются
- [ ] boundary-actions guide генерируется
- [ ] временные verify artifacts очищены перед release build

## External Boundary Readiness

- [ ] есть готовые инструкции для `git` / GitHub
- [ ] есть готовые инструкции для ChatGPT Project Sources
- [ ] нет шагов, требующих ручного угадывания

## Go / No-Go

- [ ] release bundle можно собирать
- [ ] или явно зафиксирован `no-release` с причиной
