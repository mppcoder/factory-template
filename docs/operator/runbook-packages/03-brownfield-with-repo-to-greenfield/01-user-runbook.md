# Пользовательский ранбук: путь с существующим repo

Цель: дать Codex доступ к existing repo, чтобы Codex выполнил audit/adoption/conversion и завершил состояние как `greenfield-product` / `greenfield-converted`.

Brownfield with repo не является финальным типом проекта.

## Настройка только пользователем

Маркер слоя: `USER-ONLY SETUP`.
Пользователь предоставляет existing repo access/path и approvals. Codex выполняет audit/adoption/conversion.
Допустимые contours: `vscode-remote-ssh-codex-extension` или fallback `codex-app-remote-ssh`.

### BWR-000. Зафиксировать existing repo

- Окно: Browser GitHub / Browser ChatGPT.
- Делает: Пользователь.
- Зачем: Codex должен работать с canonical repo, а не создавать sibling clone.
- Что нужно до начала: Existing repo существует; factory-template remote setup готов.
- Где взять значения: `<repo-owner>/<repo-name>` взять из GitHub URL; `<project-slug>` обычно repo name.
- Команды для копирования:

```text
entry_path: brownfield-with-repo-to-greenfield
existing_repo: <repo-owner>/<repo-name>
project_root: /projects/<project-slug>
target_profile: greenfield-product
target_lifecycle: greenfield-converted
done_rule: conversion или documented blocker
```

- Куда вставить: В ChatGPT handoff или заметки.
- Ожидаемый результат: Один canonical project root определен.
- Если ошибка: Не создавайте `/projects/<project-slug>-converted`, `/projects/audit-repo` или sibling helper repo.
- Evidence: Existing repo URL и target root.
- Следующий шаг: `BWR-010`.

### BWR-010. Дать repo access и approvals

- Окно: Browser GitHub / Browser ChatGPT.
- Делает: Пользователь.
- Зачем: Codex нужен read/write path или явный blocker.
- Что нужно до начала: `BWR-000`.
- Где взять значения: GitHub permissions, protected branch policy, required approval rules.
- Команды для копирования:

```text
Проверить:
- GitHub connector/gh has repo access;
- protected branch approvals известны;
- risky migration approval дан или отмечен как blocker;
- secrets не вставлены в handoff.
```

- Куда вставить: Не вставлять; проверить в GitHub/ChatGPT UI.
- Ожидаемый результат: Access/approval boundary ясен.
- Если ошибка: Если write path недоступен, Codex создает documented blocker после audit.
- Evidence: Repo access state или blocker без секретов.
- Следующий шаг: `BWR-020`.

### BWR-020. Точка передачи Codex

- Окно: Remote Codex chat/window.
- Делает: Пользователь.
- Зачем: Передать audit/adoption/conversion Codex.
- Что нужно до начала: Remote Codex context готов, repo/access boundary известен.
- Где взять значения: Handoff из ChatGPT Project.
- Команды для копирования:

```text
Вставить один цельный handoff block.
Обязательно: Язык ответа Codex: русский.
Обязательно: brownfield done требует conversion или documented blocker.
После вставки Codex делает audit/adoption/conversion сам.
```

- Куда вставить: Новый remote Codex chat/window.
- Ожидаемый результат: Codex дает route receipt и начинает `02-codex-runbook.md`.
- Если ошибка: Если Codex не в target repo/root context, открыть remote context заново.
- Evidence: Route receipt и remote shell/repo check.
- Следующий шаг: `CODEX-AUTOMATION`.

Маркер границы: `Codex takeover point`.

## Автоматизация Codex

Маркер слоя: `CODEX-AUTOMATION`.
Codex выполняет audit/adoption/conversion, validators и verified sync при доступности.
