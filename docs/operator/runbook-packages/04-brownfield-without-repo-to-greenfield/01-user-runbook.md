# Пользовательский ранбук: путь без repo

Цель: собрать входящие материалы в target root, затем передать Codex inventory/reconstruction/with-repo conversion.

Brownfield without repo — intake/reconstruction path, не финальный тип проекта.

## Настройка только пользователем

Маркер слоя: `USER-ONLY SETUP`.
Пользователь собирает incoming materials в `_incoming`, дает access/approvals и открывает remote Codex context. Codex выполняет inventory/reconstruction/conversion. Intake работает в recommendation-first режиме: safe defaults объясняются и могут быть заменены.
Если incoming материалы относятся к VPS/runtime, пользователь передает только безопасные сведения о выбранном Ubuntu/VPS image, runtime versions и policy approvals. Codex не делает automatic remediation или upgrade без отдельного user approval gate.
Допустимые contours: `vscode-remote-ssh-codex-extension` или fallback `codex-app-remote-ssh`.

### BWO-000. Зафиксировать target root и incoming boundary

- Окно: Browser ChatGPT / Windows Explorer / VS Code Remote SSH.
- Делает: Пользователь.
- Зачем: Temporary/reconstructed/intermediate repos не должны быть siblings в `/projects`.
- Что нужно до начала: Есть архив, папка, ссылка или другой набор исходных материалов; factory-template remote setup готов.
- Где взять значения: `<project-slug>` придумать латиницей; `<incoming-source>` взять из локальной папки/архива/ссылки. Если пользователь не просит иначе, default-decision layer рекомендует `/projects/<target-slug>/_incoming` для материалов, все reconstructed/intermediate repos только внутри target project root, затем evidence inventory -> reconstruction -> with-repo adoption -> greenfield conversion.
- Команды для копирования:

```text
default_decision_mode: global-defaults | confirm-each-default | manual
accepted_defaults:
  - incoming materials live in /projects/<target-slug>/_incoming
  - reconstructed/intermediate repos live only inside target project root
  - evidence inventory before reconstruction
  - reconstruction before with-repo adoption
overridden_defaults: []
default_source_basis:
  - repo-policy
  - best-practice
uncertainty_notes:
  - materials may need sanitized inventory before commit
decisions_requiring_user_confirmation:
  - secret/private data handling
  - destructive cleanup approval

entry_path: brownfield-without-repo-to-greenfield
project_root: /projects/<project-slug>
incoming_dir: /projects/<project-slug>/_incoming
reconstructed_repo: /projects/<project-slug>/reconstructed-repo
target_profile: greenfield-product
target_lifecycle: greenfield-converted
done_rule: conversion или documented blocker
```

- Куда вставить: В ChatGPT handoff или заметки.
- Ожидаемый результат: Один target root определен; `_incoming` живет внутри него; defaults accepted or overridden; custom overrides captured.
- Если ошибка: Не создавайте `/projects/reconstructed-repo` или `/projects/temp-audit`.
- Evidence: Target root и incoming source записаны без секретов.
- Следующий шаг: `BWO-010`.

### BWO-005. Если проект уже лежит в нестандартных папках VPS

- Окно: Browser ChatGPT / VS Code Remote SSH.
- Делает: Пользователь.
- Зачем: Иногда боевой проект уже существует как runtime distribution или
  overlay folder без git repo. Это допустимый brownfield input, но не active
  source root.
- Что нужно до начала: Есть absolute paths к папкам проекта без repo или вне
  стандарта `/projects`.
- Где взять значения: С VPS, без чтения secret files. Примеры:
  `/root/.openclaw` как patched runtime distribution,
  `/root/openclaw-plus` как overlay customization layer.
- Команды для копирования:

```text
nonstandard_vps_folder_intake:
  patched_runtime_distribution_source: /absolute/path/to/runtime-distribution
  overlay_customization_source: /absolute/path/to/overlay-or-customizations
  target_project_root: /projects/<project-slug>
  reconstructed_repo: /projects/<project-slug>/reconstructed-repo
  active_source_root_required: true
  legacy_runtime_source_required: false
  secrets_boundary: do_not_copy_raw_values
```

- Куда вставить: В ChatGPT handoff или заметки.
- Ожидаемый результат: Codex знает, какие folders инвентаризировать как
  evidence, но не использует их как active repo roots.
- Если ошибка: Если папка содержит runtime state, logs, databases, `.env`,
  tokens или private keys, Codex делает sanitized inventory, а не copy/commit.
- Evidence: Absolute paths и роль каждой папки записаны без секретов.
- Следующий шаг: `BWO-010`.

### BWO-010. Разместить материалы в `_incoming`

- Окно: VS Code Remote SSH terminal / Explorer upload / SCP client.
- Делает: Пользователь.
- Зачем: Codex должен видеть bounded input directory.
- Что нужно до начала: `BWO-000`, remote SSH доступ работает.
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
- Если ошибка: Если материалы содержат secrets, production dumps или private transcripts, не коммитьте их; Codex должен сделать sanitized intake register.
- Evidence: `ls -la _incoming` показывает материалы или пустую папку, готовую к upload.
- Следующий шаг: `BWO-020`.

### BWO-020. Точка передачи Codex

- Окно: Remote Codex chat/window.
- Делает: Пользователь.
- Зачем: Передать inventory/reconstruction/conversion Codex.
- Что нужно до начала: Remote Codex context открыт в `/projects/<project-slug>`.
- Где взять значения: Handoff из ChatGPT Project.
- Команды для копирования:

```text
Вставить один цельный handoff block.
Обязательно: Язык ответа Codex: русский.
Обязательно: temporary/reconstructed/intermediate repos не являются siblings в /projects.
После вставки Codex делает inventory/reconstruction/conversion сам.
```

- Куда вставить: Новый remote Codex chat/window.
- Ожидаемый результат: Codex дает route receipt и начинает `02-codex-runbook.md`.
- Если ошибка: Если Codex открыт в `/projects`, а не `/projects/<project-slug>`, открыть target root заново.
- Evidence: Route receipt и remote root check.
- Следующий шаг: `CODEX-AUTOMATION`.

Маркер границы: `Codex takeover point`.

## Автоматизация Codex

Маркер слоя: `CODEX-AUTOMATION`.
Codex выполняет inventory, sanitized evidence, reconstruction inside target root, with-repo conversion, validators и verified sync при доступности.
