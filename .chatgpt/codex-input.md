# Codex handoff input

## Контекст
- Repo: `factory-template`
- Изменение уровня factory-template, а не project-only.
- Нужно исправить reusable process bug в closeout semantics: internal repo follow-up после remediation/push не должен классифицироваться как user-only closeout.

## Что должен сделать исполнитель
- Обновить router, global rules, decision policy, handoff rules и done-closeout.
- Синхронизировать runbook, AGENTS, mode-routing, policy manifests и change classes.
- Усилить codex-task-pack generation/validation и зафиксировать defect отдельным bug report.

## Ограничения
- Не размывать release semantics.
- Не убирать footer для реальных внешних границ.
- Не перепридумывать всю фазовую модель.
