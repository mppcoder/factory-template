# Пользовательский ранбук: greenfield-product

Цель: создать или вести новый боевой проект, который с первого рабочего состояния является `greenfield-product` и `greenfield-active`.

## Настройка только пользователем

Маркер слоя: `USER-ONLY SETUP`.
Пользователь делает только внешний setup:

- ChatGPT plan с Codex access;
- GitHub account и, если нужен private repo, доступ к нужной организации;
- GitHub connector в ChatGPT Project;
- VS Code, Remote - SSH, GitHub Pull Requests and Issues, Codex IDE extension, YAML, Markdown All in One;
- Codex app optional;
- Timeweb/VPS или другой remote host;
- SSH key, `~/.ssh/config`, проверка `ssh <project-vps-alias>`;
- выбор contour `codex-app-remote-ssh` или `vscode-remote-ssh-codex-extension`.

Если setup делается с нуля, пройдите `../01-factory-template/01-user-runbook.md` шаги `FT-000`..`FT-500`, заменив:

- repo: `<OWNER>/<NEW_REPO>`;
- target root: `/projects/<project-slug>`;
- SSH alias: `<project-slug>-vps`.

### GF-000. Зафиксировать параметры нового проекта

- Окно: Browser ChatGPT / заметки.
- Делает: Пользователь.
- Зачем: Codex нужен project slug и GitHub target.
- Что нужно до начала: ChatGPT, GitHub и remote SSH setup готовы.
- Где взять значения: `<project-slug>` придумайте латиницей; `<repo-owner>` и `<repo-name>` берутся из GitHub.
- Команды для копирования:

```text
project_preset: greenfield-product
recommended_mode: greenfield
lifecycle_state: greenfield-active
project_slug: <project-slug>
github_repo: <repo-owner>/<repo-name>
remote_root: /projects/<project-slug>
```

- Куда вставить: В будущий ChatGPT handoff или заметки.
- Ожидаемый результат: Есть один canonical project root `/projects/<project-slug>`.
- Если ошибка: Не создавайте sibling helper repos в `/projects`; входящие материалы кладите в `/projects/<project-slug>/_incoming/`.
- Следующий шаг: `GF-010`.

### GF-010. Открыть remote Codex context

- Окно: VS Code Remote SSH / Codex app remote thread.
- Делает: Пользователь.
- Зачем: После этого Codex сам materialize-ит project root.
- Что нужно до начала: SSH alias работает.
- Где взять значения: SSH alias из `~/.ssh/config`.
- Команды для копирования:

```bash
hostname && whoami && pwd
```

- Куда вставить: Remote terminal в VS Code или Codex app remote shell check.
- Ожидаемый результат: Команда выполняется на VPS, не на локальном Windows.
- Если ошибка: Вернитесь к SSH setup из factory-template user-runbook.
- Следующий шаг: `GF-020`.

### GF-020. Точка передачи Codex

- Окно: Codex extension / Codex chat.
- Делает: Пользователь.
- Зачем: Передать создание greenfield project Codex.
- Что нужно до начала: Remote Codex context открыт.
- Где взять значения: Handoff готовит ChatGPT Project; он должен содержать `Язык ответа Codex: русский`.
- Команды для копирования:

```text
Вставить один цельный handoff block.
Не использовать ссылку на файл.
Не делить handoff на несколько сообщений.
```

- Куда вставить: Новый Codex chat/window в remote context.
- Ожидаемый результат: Codex дает route receipt и переходит к `02-codex-runbook.md`.
- Если ошибка: Если Codex не в remote context, открыть новый remote chat/window.
- Следующий шаг: `CODEX-AUTOMATION`.

Маркер границы: `Codex takeover point`.

## Автоматизация Codex

Маркер слоя: `CODEX-AUTOMATION`.
После `GF-020` Codex сам создает `/projects/<project-slug>`, запускает `first-project-wizard.py` или equivalent scaffold path, materialize-ит repo-first core, создает/подключает GitHub repo при доступном write path, заполняет greenfield docs, запускает verify и closeout.

## Границы

Brownfield artifacts не должны появляться, если проект не проходит adoption/conversion path.
Already-open live session является только non-canonical fallback и не переключает model/profile/reasoning сама по себе.
