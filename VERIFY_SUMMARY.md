# Сводка verify

## Repo / репозиторий

- `factory-template`

## Текущий verify baseline

- `bash template-repo/scripts/verify-all.sh ci`: PASS (`2026-04-26`)
- `bash CLEAN_VERIFY_ARTIFACTS.sh`: PASS (`2026-04-26`)
- `bash PRE_RELEASE_AUDIT.sh`: PASS (`2026-04-26`)
- `bash RELEASE_BUILD.sh /tmp/factory-template-2.5.zip`: PASS (`2026-04-26`)
- `VERSION_SYNC_CHECK.sh`: PASS
- `VALIDATE_FACTORY_TEMPLATE_OPS.sh`: PASS
- `SMOKE_TEST.sh`: PASS
- `EXAMPLES_TEST.sh`: PASS
- `MATRIX_TEST.sh`: PASS
- `CLEAN_VERIFY_ARTIFACTS.sh && PRE_RELEASE_AUDIT.sh`: PASS

## Решение G25-GA

- Статус: pass.
- Причина: full-KPI evidence зафиксирован для всех `M25-*`.
- Evidence: `docs/releases/2.5-ga-kpi-evidence.md`.
- `ga_ready` установлен в `true`; release-facing docs синхронизированы с scorecard.

## Baseline планирования после 2.5

- `docs/releases/2.5.1-roadmap.md`: добавлен, status `planned, not release-ready`.
- `docs/releases/2.6-roadmap.md`: добавлен, status `planned, not release-ready`.
- `docs/releases/post-2.5-gap-register.md`: добавлен.
- `reports/bugs/2026-04-27-post-25-release-planning-gap.md`: defect capture закрыт как `remediated-in-current-scope`.
- Completed proof отделен от pending external runtime proof; `2.5.0` scorecard не изменялся.

## Baseline внешних действий

- `reports/bugs/2026-04-27-external-actions-oververbose-closeout.md`: defect capture закрыт как `remediated-in-current-scope`.
- Compact closeout contract: если внешних действий нет, финальный ответ говорит `Внешних действий не требуется.`
- Если внешние действия есть, `## Инструкция пользователю` содержит только реальные external/manual actions.
- `validate-codex-task-pack.py` закрепляет compact outcome и ловит oververbose no-op ledger.

## Проверенные слои

- release metadata и version sync
- root release notes source и release-facing reference package
- canonical preset naming и разделение optional/reference contour
- launcher и generated project scaffolding
- structural validators
- defect-capture / alignment / handoff checks
- verified sync prereqs, denylist/no-op path и fallback push strategy
- release decision validation и publish fallback reporting
- curated reference/export packs policy
- boundary-actions generation
- phase-aware pack recommendation
- repo-first ChatGPT Project instruction layer
- automatic phase detection
- automatic phase detection self-test
- согласованность README, release docs, scenario-pack guidance и фактической структуры repo

## Известные остаточные ограничения

- `MATRIX_TEST.sh` остаётся representative runner, а не exhaustive coverage всех возможных комбинаций
- phase detection валидируется rule-based по changed paths, а не через более глубокий semantic анализ repo intent
- `release` phase теперь требует и changed-path signals, и отмеченные intent markers в `RELEASE_CHECKLIST.md`
- `bugfix-drift` phase теперь требует и bug/validator path signals, и bug-report intent markers в `reports/bugs/*.md`
- release decision для `G25-GA` зафиксирован как GA pass; дальнейшие KPI расширения не блокируют текущий release
- git-операции в этом окружении нужно выполнять последовательно; параллельный `commit/push/fetch/remote change` может давать ложные результаты
- auto GitHub Release publication зависит от доступности `gh` и не должна считаться гарантированной без отдельной проверки auth/runtime

## Использование оператором

Этот файл служит короткой опорой перед:

- `git init`
- подключением `origin`
- публикацией в GitHub
- обновлением repo-first инструкции в ChatGPT Project
- repo-side подготовкой boundary-actions и reference/export artifacts

## Git sync note / заметка по синхронизации

- `VERIFIED_SYNC.sh` использовать как основной verified path для auto commit/push
- `git commit`, `git push`, `git fetch`, `git remote set-url` выполнять только последовательно
- если `git push origin main` ведет себя нестабильно, используйте прямой SSH push:
  `git push git@github.com:mppcoder/factory-template.git main`
