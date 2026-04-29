# Пользовательский ранбук: greenfield-product

Цель: создать новый боевой проект как `greenfield-product` / `greenfield-active`.
Этот package стартует после готового `factory-template`: шаблон установлен, verified, и Codex уже умеет работать через `codex-app-remote-ssh` или `vscode-remote-ssh-codex-extension`.

## Настройка только пользователем

Маркер слоя: `USER-ONLY SETUP`.
Пользователь делает только внешние UI-действия, которые Codex не может выполнить сам: выбирает название проекта, сообщает его Codex, создает ChatGPT Project в UI и вставляет готовую repo-first инструкцию, которую подготовил Codex.

Пользователь не создает GitHub repo, не clone-ит repo, не добавляет `origin`, не делает initial commit/push, не запускает launcher/wizard/verify и не materialize-ит repo-first core. Это делает Codex, если нет явного blocker.

Допустимые contours: `vscode-remote-ssh-codex-extension` через `Codex extension / Codex chat` в VS Code Remote SSH или fallback `codex-app-remote-ssh`.

### GF-000. Выбрать название проекта

- Окно: Browser ChatGPT / заметки.
- Делает: Пользователь.
- Зачем: Codex использует название как исходное product name и сам нормализует slug/repo name по правилам factory-template.
- Что нужно до начала: Factory-template установлен и verified; remote Codex contour работает.
- Где взять значения: Название придумывает пользователь; краткая идея проекта optional.
- Команды для копирования:

```text
Название проекта: <PROJECT_NAME>
Краткая идея проекта: <PROJECT_IDEA>
```

- Куда вставить: В заметки или сразу в сообщение Codex на шаге `GF-010`.
- Ожидаемый результат: Есть human-readable название проекта и, если нужно, короткое описание идеи.
- Если ошибка: Если название слишком общее, добавьте 2-5 слов контекста; Codex сам предложит slug.
- Evidence: `<PROJECT_NAME>` выбран; GitHub repo еще не создается пользователем.
- Следующий шаг: `GF-010`.

### GF-010. Сообщить Codex название и идею

- Окно: Remote Codex chat/window в готовом factory-template context.
- Делает: Пользователь.
- Зачем: Codex получает минимальный input и дальше сам создает repo/root/core/verify/sync.
- Что нужно до начала: `GF-000`; открыт remote Codex context через `codex-app-remote-ssh` или `vscode-remote-ssh-codex-extension`.
- Где взять значения: `<PROJECT_NAME>` и optional `<PROJECT_IDEA>` из `GF-000`.
- Команды для копирования:

```text
Создай новый greenfield-product.
Название проекта: <PROJECT_NAME>
Краткая идея проекта: <PROJECT_IDEA>

Пользовательские внешние действия ограничены:
- я создам ChatGPT Project в UI;
- я вставлю туда готовую repo-first инструкцию, которую подготовит Codex.

Все остальное делает Codex: GitHub repo, slug/repo name, origin, initial commit/push, /projects root, wizard/launcher, repo-first core, .chatgpt, AGENTS, scenario-pack, dashboard, project-knowledge, bootstrap/verify, verified sync.
```

- Куда вставить: В новый remote Codex chat/window.
- Ожидаемый результат: Codex дает route receipt и начинает `02-codex-runbook.md`: нормализует slug, создает GitHub repo/root, запускает wizard/verify/sync и готовит repo-first instruction text.
- Если ошибка: Если Codex сообщает blocker по GitHub write permission, security approval, secret, paid/dangerous external action или ChatGPT Project UI, выполните только этот внешний шаг.
- Evidence: Codex принял название и начал automation; GitHub repo/root создаются Codex.
- Следующий шаг: `GF-020`.

### GF-020. Создать ChatGPT Project в UI

- Окно: Browser ChatGPT.
- Делает: Пользователь.
- Зачем: ChatGPT Project создается во внешнем UI, это не делает Codex.
- Что нужно до начала: `GF-010`; можно создать project пока Codex готовит repo-first instruction.
- Где взять значения: Project display name: `<PROJECT_NAME>`.
- Команды для копирования:

```text
ChatGPT UI path:
1. Открыть ChatGPT.
2. Projects -> New project.
3. Название: <PROJECT_NAME>.
4. Создать project.
5. Не вставлять временные/самодельные инструкции; дождаться готового текста от Codex.
```

- Куда вставить: Не в терминал; выполнить в Browser ChatGPT UI.
- Ожидаемый результат: Пустой ChatGPT Project создан с названием `<PROJECT_NAME>`.
- Если ошибка: Если UI не дает создать project, зафиксируйте screenshot/error text без секретов и передайте Codex как external blocker.
- Evidence: ChatGPT Project создан; instruction field пока пустой или ожидает готовый текст.
- Следующий шаг: `GF-030`.

### GF-030. Вставить готовую repo-first инструкцию

- Окно: Browser ChatGPT Project settings/instructions.
- Делает: Пользователь.
- Зачем: Codex подготовил точный instruction text после создания repo/root/core, и пользователь вставляет его во внешний UI.
- Что нужно до начала: `GF-020`; Codex вернул готовый repo-first instruction text.
- Где взять значения: Готовый текст взять из финального сообщения Codex после `02-codex-runbook.md`.
- Команды для копирования:

```text
Вставить в ChatGPT Project instructions ровно готовый блок, который подготовил Codex.
Не редактировать repo path, GitHub URL, scenario entrypoint и language contract вручную.
```

- Куда вставить: Browser ChatGPT -> созданный Project -> Settings/Instructions.
- Ожидаемый результат: ChatGPT Project содержит repo-first instruction, указывающую на созданный Codex repo/root и `template-repo/scenario-pack/00-master-router.md`.
- Если ошибка: Если instruction слишком длинная или UI не сохраняет, отправьте Codex error text/screenshot; Codex подготовит короткую совместимую версию.
- Evidence: ChatGPT Project instruction сохранена.
- Следующий шаг: `STOP`.

Маркер границы: `Codex takeover point` уже достигнут на `GF-010`; `GF-020` и `GF-030` остаются внешними UI-действиями пользователя.

## Автоматизация Codex

Маркер слоя: `CODEX-AUTOMATION`.
После `GF-010` Codex сам выполняет GitHub repo creation, slug/repo naming, `origin`, initial commit/push, VPS project root, wizard/launcher, repo-first core, `.chatgpt`, `AGENTS`, scenario-pack, dashboard, project-knowledge, bootstrap/verify, verified sync и готовит repo-first instruction для `GF-030`.
