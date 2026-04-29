# Отчет о завершении

## Что было запрошено

Передернуть и классифицировать исторические красные GitHub Actions CI #1-#5 без ошибочного превращения superseded PR checks в новые repo regressions.

## Что реально сделано

- Прочитан `template-repo/scenario-pack/00-master-router.md`; входящий `chatgpt-handoff` принят как route receipt.
- Проверены current workflow baseline, open Issues, open PRs и PR #4.
- Найдены точные run IDs для CI #1-#5.
- Для каждого CI #1-#5 собраны metadata, annotations и failed-log/job-log evidence.
- Выполнен rerun `--failed` для всех пяти исторических CI.
- PR #1/#2/#3 runs классифицированы как historical superseded.
- CI #1 и CI #5 классифицированы как old fixed bug snapshots.
- При current-main verification closeout найден отдельный verification portability defect и исправлен минимальным patch.
- Post-fix CI #96 выявил, что defect-capture bug report quotes тоже должны быть allowed history для legacy scan; добавлен follow-up allowlist для `reports/bugs/*`.

## Какие артефакты обновлены

- `.chatgpt/verification-report.md`
- `.chatgpt/done-report.md`
- `VERIFY_SUMMARY.md`
- `reports/bugs/2026-04-29-historical-actions-rerun-regression.md`
- `reports/factory-feedback/feedback-2026-04-29-historical-actions-rerun-regression.md`

## Что изменено в repo

- `PRE_RELEASE_AUDIT.sh`: single-file legacy check no longer depends on `rg`.
- `VERSION_SYNC_CHECK.sh`: repo-wide legacy scan now uses `find` + `grep` from repo root with repo-relative allowlist matching.
- `template-repo/template/.chatgpt/project-origin.md`: active template factory identity updated to `factory-v2.5.0` / `2.5.0`.
- `VERSION_SYNC_CHECK.sh`: `reports/bugs/*` allowed as defect-capture history for quoted legacy evidence.

## Итог закрытия

- Clean-worktree `bash template-repo/scripts/verify-all.sh ci`: PASS with this fix-set.
- Historical CI #1-#5 remain classified as historical/stale; no current workflow action regression found.
- Final sync status фиксируется после commit/push.
