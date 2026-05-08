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
- temporary/intermediate/reconstructed/helper repos должны жить внутри repo целевого `greenfield-product`;
- такие промежуточные repo не должны появляться как соседи `factory-template` или других project roots в `/projects`.

## Состав

1. `01-runbook-dlya-polzovatelya-factory-template.md`
2. `02-runbook-dlya-codex-factory-template.md`
3. `03-mode-routing-factory-template.md`
4. `04-chatgpt-project-sources-factory-template-20-cap.md`
5. `04-vps-remote-ssh-full-handoff-orchestration.md`
6. `05-backlog-dorabotok-factory-template.md`
7. `05-orchestration-cockpit-lite.md`
8. `06-project-lifecycle-dashboard.md`
9. `07-beginner-visual-dashboard-ux.md`
10. `07-AGENTS-factory-template.md`
11. `07-universal-codex-handoff-factory.md`
12. `08-chatgpt-codex-github-vps-one-paste-flow.md`
13. `telegram-feedback-channel.md`

## Назначение

Сделать рабочую схему, в которой:

- `factory-template` — отдельный главный repo шаблона;
- ChatGPT Project шаблона — repo-first слой для сценарной работы, архитектуры, исследований и release-решений;
- Codex в VS Code по SSH — основной исполнитель по самому шаблону;
- пользователь закрывает только внешние границы.
