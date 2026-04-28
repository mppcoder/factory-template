# Пользовательский ранбук: путь с существующим repo

Цель: принять существующий repo как canonical project root, провести audit/adoption/conversion и завершить рабочее состояние как `greenfield-product` / `greenfield-converted`.

Brownfield with repo не является финальным типом проекта.

## Настройка только пользователем

Маркер слоя: `USER-ONLY SETUP`.
Пользователь делает только внешний setup:

- ChatGPT plan с Codex access;
- GitHub account и доступ к existing repo;
- GitHub connector в ChatGPT Project;
- remote SSH / VPS / SSH alias;
- VS Code Remote SSH + Codex IDE extension или Codex app remote connection;
- external approvals на risky migration, если нужны.

Если remote/Codex setup еще не готов, сначала пройдите `../01-factory-template/01-user-runbook.md` до `FT-500`, заменив repo и alias на проектные значения.

### BWR-000. Зафиксировать existing repo

- Окно: Browser GitHub / Browser ChatGPT.
- Делает: Пользователь.
- Зачем: Codex должен знать canonical repo, а не создавать sibling clone.
- Что нужно до начала: GitHub repo существует.
- Где взять значения: `<repo-owner>/<repo-name>` из GitHub URL; `<project-slug>` обычно repo name.
- Команды для копирования:

```text
entry_path: brownfield-with-repo-to-greenfield
existing_repo: <repo-owner>/<repo-name>
project_root: /projects/<project-slug>
target_profile: greenfield-product
target_lifecycle: greenfield-converted
done_rule: conversion или documented blocker
```

- Куда вставить: В ChatGPT handoff или заметки перед Codex takeover.
- Ожидаемый результат: Есть один canonical target root `/projects/<project-slug>`.
- Если ошибка: Не создавайте рядом `/projects/<project-slug>-converted` или `/projects/audit-repo`.
- Следующий шаг: `BWR-010`.

### BWR-010. Открыть existing repo в remote context

- Окно: VS Code Remote SSH / VPS terminal.
- Делает: Пользователь.
- Зачем: Codex должен работать в existing repo root.
- Что нужно до начала: SSH alias работает; repo доступен по GitHub.
- Где взять значения: Clone URL из GitHub.
- Команды для копирования:

```bash
mkdir -p /projects
cd /projects
test -d <project-slug>/.git || git clone https://github.com/<repo-owner>/<repo-name>.git <project-slug>
cd /projects/<project-slug>
git status --short --branch
```

- Куда вставить: Remote terminal, только если repo еще не открыт. Если Codex уже может выполнять команды, этот clone step можно оставить Codex.
- Ожидаемый результат: `/projects/<project-slug>` является existing repo root.
- Если ошибка: Если repo private, GitHub auth должен быть выполнен через `gh auth login` или SSH key; секреты не вставлять в handoff.
- Следующий шаг: `BWR-020`.

### BWR-020. Точка передачи Codex

- Окно: Codex extension / Codex chat.
- Делает: Пользователь.
- Зачем: Передать audit/adoption/conversion Codex.
- Что нужно до начала: Remote Codex context открыт в `/projects/<project-slug>`.
- Где взять значения: Handoff из ChatGPT Project.
- Команды для копирования:

```text
Вставить один цельный handoff block.
Обязательно: Язык ответа Codex: русский.
Обязательно: brownfield done требует conversion или documented blocker.
```

- Куда вставить: Новый Codex chat/window в remote context.
- Ожидаемый результат: Codex дает route receipt и начинает CODEX-AUTOMATION.
- Если ошибка: Если Codex работает не в existing repo root, остановить и открыть правильный folder.
- Следующий шаг: `CODEX-AUTOMATION`.

Маркер границы: `Codex takeover point`.

## Автоматизация Codex

Маркер слоя: `CODEX-AUTOMATION`.
После takeover Codex сам materialize-ит repo-first core без перезаписи product code, заполняет audit evidence, защищает project-owned zones, выполняет conversion gates, запускает validators и делает verified sync при доступности.
