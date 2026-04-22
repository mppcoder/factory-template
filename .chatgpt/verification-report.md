# Отчёт о проверке результата

## Что проверяли
- `rg -n --hidden --glob '!.git' '/projects/_incoming|/projects/_release|/projects/_artifacts|reconstructed-brownfield-repo|brownfield-evidence|dogfood-brownfield-shell|/projects/\\*'`
- адресная проверка обновлённых runbook/scenario/workspace файлов
- `python3 tools/generate_factory_template_boundary_actions.py`
- `python3 tools/validate_factory_template_ops_policy.py`
- `git diff --check`
- `python3 template-repo/scripts/check-dod.py .`
- `python3 template-repo/scripts/create-codex-task-pack.py .`
- `python3 template-repo/scripts/validate-codex-task-pack.py .`
- `python3 template-repo/scripts/validate-codex-routing.py .`

## Что подтверждено
- В сценарном и operator слоях зафиксировано одно правило: в `/projects` лежат только project roots.
- `_incoming` в актуальных ключевых инструкциях описан как project-local подпапка.
- Brownfield without repo теперь явно запрещает создавать temporary/intermediate/reconstructed repos прямо в `/projects`.
- Workspace/bootstrap материалы больше не продвигают плоскую россыпь служебных каталогов в корне `/projects`.
- Boundary actions guide regenerated successfully and now points to `/projects/factory-template/_incoming`.
- Process miss after initial closeout separately captured as reusable defect in `reports/bugs/bug-012-missed-verified-sync-and-user-instruction-after-closeout.md`.
- Remediation for bug-012 works as intended: `check-dod.py` now blocks dishonest closeout without successful verified sync report and passes after required closeout artifacts are present.
- Root-level routing/config drift is fixed: `create-codex-task-pack.py .` now successfully resolves profile selection through fallback routing spec and produced a valid task pack on `factory-template` root.

## Что не подтверждено или требует повторной проверки
- Полный downstream sync в уже созданных боевых repo не выполнялся в рамках этого change.
- Полная интеграционная проверка downstream боевых repo не запускалась в рамках этого change.
- Отдельных неподтверждённых блокеров по root-level `create-codex-task-pack.py` больше не осталось.

## Итоговый вывод
- Repo приведён к каноническому VPS layout rule без явных конфликтов в основных docs/templates/workspace слоях.
- Closeout/automation layer дополнительно усилен против повторения bug-012.
- Root repo теперь поддерживает тот же executable routing fallback, что и generated projects, без ручного копирования `codex-routing.yaml` в корень.
