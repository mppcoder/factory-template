# Как работают feedback, drift и Codex task pack

## Feedback в фабрику
Если проблема относится не к проекту, а к фабрике:
1. используйте `meta-feedback/factory-bug-report.md` или `meta-feedback/factory-task.md`;
2. заполните шаблон;
3. перенесите результат в `meta-template-project`.

## Drift detection
Optional layer `workspace-packs/factory-ops/` позволяет:
- сравнивать фабрику и рабочий проект;
- выявлять drift;
- принимать решение о selective sync.

## Codex task pack
Скрипт `create-codex-task-pack.py` собирает из текущего проекта:
- `codex-context.md`
- `codex-task-pack.md`
- `done-checklist.md`
