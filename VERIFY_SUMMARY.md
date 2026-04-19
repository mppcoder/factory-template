# Verify Summary

## Repo

- `factory-template`

## Current Verify Baseline

- `VERSION_SYNC_CHECK.sh`: PASS
- `VALIDATE_FACTORY_TEMPLATE_OPS.sh`: PASS
- `SMOKE_TEST.sh`: PASS
- `EXAMPLES_TEST.sh`: PASS
- `MATRIX_TEST.sh`: PASS
- `CLEAN_VERIFY_ARTIFACTS.sh && PRE_RELEASE_AUDIT.sh`: PASS

## Verified Layers

- release metadata and version sync
- launcher and generated project scaffolding
- structural validators
- defect-capture / alignment / handoff checks
- curated Sources packs policy
- boundary-actions generation
- phase-aware Sources recommendation
- automatic phase detection

## Known Residual Limits

- `MATRIX_TEST.sh` остаётся representative runner, а не exhaustive coverage всех возможных комбинаций
- phase detection валидируется rule-based по changed paths, а не через более глубокий semantic анализ repo intent
- `release` phase now requires both changed-path signals and checked intent markers in `RELEASE_CHECKLIST.md`
- `bugfix-drift` phase now requires both bug/validator path signals and bug-report intent markers in `reports/bugs/*.md`
- release/no-release решение остаётся отдельным операторским решением
- git-операции в этом окружении нужно выполнять последовательно; параллельный `commit/push/fetch/remote change` может давать ложные результаты

## Operator Use

Этот файл служит короткой опорой перед:

- `git init`
- подключением `origin`
- публикацией в GitHub
- ручной загрузкой Sources в ChatGPT Project

## Git Sync Note

- `git commit`, `git push`, `git fetch`, `git remote set-url` выполнять только последовательно
- если `git push origin main` ведет себя нестабильно, используйте прямой SSH push:
  `git push git@github.com:mppcoder/factory-template.git main`
