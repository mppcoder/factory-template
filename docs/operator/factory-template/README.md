# Пакет: только для проекта шаблона фабрики проектов

Этот комплект предназначен **только для проекта `factory-template`**.

В него не входят отдельные runbook'и для:

- brownfield shell,
- reconstructed repo,
- product greenfield package.

Фокус только на одном контуре:

```text
/projects/factory-template/
```

Правило верхнего уровня:
- в `/projects` лежат только project roots;
- `_incoming` допускается только внутри project root;
- brownfield temporary/intermediate/reconstructed repos не должны появляться как соседи `factory-template` в `/projects`.

## Состав

1. `01-runbook-dlya-polzovatelya-factory-template.md`
2. `02-runbook-dlya-codex-factory-template.md`
3. `03-mode-routing-factory-template.md`
4. `04-chatgpt-project-sources-factory-template-20-cap.md`
5. `04-vps-remote-ssh-full-handoff-orchestration.md`
6. `05-backlog-dorabotok-factory-template.md`
7. `06-codex-config-factory-template.toml`
8. `07-AGENTS-factory-template.md`

## Назначение

Сделать рабочую схему, в которой:

- `factory-template` — отдельный главный repo шаблона;
- ChatGPT Project шаблона — repo-first слой для сценарной работы, архитектуры, исследований и release-решений;
- Codex в VS Code по SSH — основной исполнитель по самому шаблону;
- пользователь закрывает только внешние границы.
