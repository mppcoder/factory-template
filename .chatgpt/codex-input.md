# Codex handoff input

## Контекст
- Repo: `factory-template`
- Изменение уровня factory-template, а не project-only.
- Нужно усилить completion/handoff layer так, чтобы после relevant change Codex не останавливался на общем footer, а выдавал канонический source-update completion package.

## Что должен сделать исполнитель
- Обновить scenario/done rules и runbook/AGENTS.
- Добавить impact model в boundary policy.
- Усилить codex-task-pack generation/validation и boundary-actions template.
- Обновить closeout/release-facing artifacts и bug report.

## Ограничения
- Не размывать release semantics.
- Не добавлять автоматическое управление внешними UI.
- Не делать новый тяжёлый subsystem, если достаточно policy/checklist/template extension.
