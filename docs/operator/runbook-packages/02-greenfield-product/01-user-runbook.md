# Пользовательский ранбук: greenfield-product

Цель: создать или вести новый боевой проект, который сразу является `greenfield-product` / `greenfield-active`.
Этот package стартует не с пустого ПК, а после готового `factory-template` setup: пользователь уже умеет открыть remote Codex context по `docs/operator/runbook-packages/01-factory-template/01-user-runbook.md`.

## Настройка только пользователем

Маркер слоя: `USER-ONLY SETUP`.
Пользователь делает только external setup: имя проекта, GitHub repo/access, ChatGPT Project, secrets/approvals и открытие remote Codex context.
Допустимые contours: `vscode-remote-ssh-codex-extension` через `Codex extension / Codex chat` в VS Code Remote SSH или fallback `codex-app-remote-ssh`.

### GF-000. Зафиксировать параметры проекта

- Окно: Browser ChatGPT / Browser GitHub.
- Делает: Пользователь.
- Зачем: Codex нужен canonical project target.
- Что нужно до начала: Factory-template setup готов до remote Codex takeover.
- Где взять значения: `<project-slug>` придумать латиницей; `<repo-owner>/<repo-name>` взять из GitHub.
- Команды для копирования:

```text
project_preset: greenfield-product
recommended_mode: greenfield
lifecycle_state: greenfield-active
project_slug: <project-slug>
github_repo: <repo-owner>/<repo-name>
remote_root: /projects/<project-slug>
```

- Куда вставить: В ChatGPT handoff или заметки.
- Ожидаемый результат: Есть один target root `/projects/<project-slug>`.
- Если ошибка: Не создавайте helper repo как sibling в `/projects`; временные материалы кладите в `/projects/<project-slug>/_incoming/`.
- Evidence: Project slug и repo target записаны без секретов.
- Следующий шаг: `GF-010`.

### GF-010. Подготовить external access

- Окно: Browser GitHub / Browser ChatGPT.
- Делает: Пользователь.
- Зачем: Codex сможет создать/вести project repo и handoff.
- Что нужно до начала: `GF-000`.
- Где взять значения: GitHub owner/name и ChatGPT Project connector.
- Команды для копирования:

```text
Проверить:
- GitHub repo создан или owner/name однозначны для создания Codex;
- ChatGPT Project подключен к GitHub;
- secrets/approvals не вставлены в handoff;
- release/deploy approval нужен только если scope этого требует.
```

- Куда вставить: Не вставлять; выполнить в GitHub/ChatGPT UI.
- Ожидаемый результат: Repo/access/approvals готовы или blocker явно известен.
- Если ошибка: Если GitHub write path недоступен, Codex должен зафиксировать blocker, а не просить пользователя выполнять internal repo work.
- Evidence: Repo URL или planned owner/name; секреты не копировать.
- Следующий шаг: `GF-020`.

### GF-020. Точка передачи Codex

- Окно: VS Code Remote SSH `Codex extension / Codex chat` или Codex app remote thread.
- Делает: Пользователь.
- Зачем: Передать создание/ведение greenfield project Codex.
- Что нужно до начала: Remote Codex context готов по factory-template user-runbook.
- Где взять значения: Handoff из ChatGPT Project.
- Команды для копирования:

```text
Вставить один цельный handoff block.
Обязательно: Язык ответа Codex: русский.
Обязательно: project_preset greenfield-product.
После вставки Codex создает/ведет project root сам.
```

- Куда вставить: Новый remote Codex chat/window.
- Ожидаемый результат: Codex дает route receipt и начинает `02-codex-runbook.md`.
- Если ошибка: Если Codex context локальный, открыть remote chat/window заново.
- Evidence: Route receipt и remote shell check.
- Следующий шаг: `CODEX-AUTOMATION`.

Маркер границы: `Codex takeover point`.

## Автоматизация Codex

Маркер слоя: `CODEX-AUTOMATION`.
После `GF-020` Codex выполняет project creation/materialization, GitHub repo setup при доступном write path, greenfield docs, verify и sync.
