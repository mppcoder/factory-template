# Пользовательский ранбук: путь без repo

Цель: принять входящие материалы без нормализованного repo, реконструировать canonical repo внутри target project root, затем пройти with-repo adoption/conversion и завершить как `greenfield-product` / `greenfield-converted`.

Brownfield without repo — это intake/reconstruction path, не финальный тип проекта.

## Настройка только пользователем

Маркер слоя: `USER-ONLY SETUP`.
Пользователь делает только внешний setup:

- ChatGPT plan с Codex access;
- GitHub account и connector;
- remote SSH / VPS / SSH alias;
- VS Code Remote SSH + Codex IDE extension или Codex app remote connection;
- передача исходных материалов в sanitized form;
- approvals на ownership, reconstruction и secrets boundary.

Если remote/Codex setup еще не готов, сначала пройдите `../01-factory-template/01-user-runbook.md` до `FT-500`, заменив alias/root на проектные значения.

### BWO-000. Зафиксировать target root и входящие материалы

- Окно: Browser ChatGPT / Windows Explorer / VS Code Remote SSH.
- Делает: Пользователь.
- Зачем: Temporary/reconstructed/intermediate repos не должны быть siblings в `/projects`.
- Что нужно до начала: Есть архив, папка, ссылка или другой набор исходных материалов.
- Где взять значения: `<project-slug>` придумайте латиницей; `<incoming-source>` это путь/ссылка на материалы.
- Команды для копирования:

```text
entry_path: brownfield-without-repo-to-greenfield
project_root: /projects/<project-slug>
incoming_dir: /projects/<project-slug>/_incoming
reconstructed_repo: /projects/<project-slug>/reconstructed-repo
target_profile: greenfield-product
target_lifecycle: greenfield-converted
done_rule: conversion или documented blocker
```

- Куда вставить: В ChatGPT handoff или заметки.
- Ожидаемый результат: Есть один target root; все входящие материалы идут внутрь него.
- Если ошибка: Не создавайте `/projects/reconstructed-repo` или `/projects/temp-audit` как sibling project root.
- Следующий шаг: `BWO-010`.

### BWO-010. Поместить материалы в `_incoming/`

- Окно: VS Code Remote SSH terminal / Explorer upload / SCP client.
- Делает: Пользователь.
- Зачем: Codex должен реконструировать repo из bounded input directory.
- Что нужно до начала: Remote SSH доступ работает.
- Где взять значения: `<project-slug>` из `BWO-000`.
- Команды для копирования:

```bash
mkdir -p /projects/<project-slug>/_incoming
cd /projects/<project-slug>
pwd
ls -la _incoming
```

- Куда вставить: Remote terminal. Затем загрузить архивы/файлы в `_incoming/` через VS Code Explorer, SCP или другой безопасный канал.
- Ожидаемый результат: Материалы находятся в `/projects/<project-slug>/_incoming/`.
- Если ошибка: Если материалы содержат secrets, production dumps или private transcripts, не коммитьте их; попросите Codex сделать sanitized intake register.
- Следующий шаг: `BWO-020`.

### BWO-020. Точка передачи Codex

- Окно: Codex extension / Codex chat.
- Делает: Пользователь.
- Зачем: Передать intake/reconstruction/adoption Codex.
- Что нужно до начала: Remote Codex context открыт в `/projects/<project-slug>`.
- Где взять значения: Handoff из ChatGPT Project.
- Команды для копирования:

```text
Вставить один цельный handoff block.
Обязательно: Язык ответа Codex: русский.
Обязательно: temporary/reconstructed/intermediate repos не являются siblings в /projects.
Обязательно: brownfield done требует conversion или documented blocker.
```

- Куда вставить: Новый Codex chat/window в remote context.
- Ожидаемый результат: Codex дает route receipt и начинает CODEX-AUTOMATION.
- Если ошибка: Если Codex видит только `/projects` без target root, откройте `/projects/<project-slug>`.
- Следующий шаг: `CODEX-AUTOMATION`.

Маркер границы: `Codex takeover point`.

## Автоматизация Codex

Маркер слоя: `CODEX-AUTOMATION`.
После takeover Codex сам проводит intake, secret scan/sanitization register, reconstruction внутри target root, with-repo adoption cycle, conversion gates, validators и verified sync при доступности.
