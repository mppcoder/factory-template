# Контракт слоя пакетов ранбуков

## Контракт для новичка

Runbook packages являются практическим слоем "с пустого ПК до Codex takeover", а не пересказом scenario-pack.
Каждый package обязан явно разделять:

- `USER-ONLY SETUP`: действия, которые Codex не может сделать без внешнего доступа, UI, учетной записи, secret entry или remote connection.
- `CODEX-AUTOMATION`: действия, которые начинаются после takeover point и выполняются Codex в remote/repo context.

User-runbook должен вести новичка через конкретные окна, значения и команды.
Для каждого user-facing шага используется card format:

- `Окно`;
- `Делает`;
- `Зачем`;
- `Что нужно до начала`;
- `Где взять значения`;
- `Команды для копирования`;
- `Куда вставить`;
- `Ожидаемый результат`;
- `Если ошибка`;
- `Следующий шаг`.

Если шаг выполняется в UI без shell command, в `Команды для копирования` пишется короткий checklist block, который оператор может copy-paste в заметки или сверить по экрану.

User-runbook останавливается на `Codex takeover point`: remote Codex context уже может выполнять команды на VPS. После этого пользователь вставляет один большой handoff, а Codex переходит к Codex-runbook.

Обязательные Codex setup contours:

- `codex-app-remote-ssh`;
- `vscode-remote-ssh-codex-extension`.

Оба contour должны иметь явную takeover point и не обещать, что advisory text сам переключит model/profile/reasoning.

Codex-runbook обязан начинаться с проверки remote context и дальше сам выполнять:

- VPS preflight;
- установку системных пакетов;
- установку Node/Python/git/gh/Codex CLI и нужных tools;
- создание project root;
- clone/sync GitHub repo;
- bootstrap/setup;
- targeted/quick verify;
- drift remediation;
- dashboard update;
- verified sync, если доступен `origin` и verify green.

## Канонический старт нового боевого проекта

Для любого нового боевого проекта canonical start channel — ChatGPT Project шаблона фабрики `factory-template`.
Пользователь открывает новый чат в этом Project и пишет команду:

```text
новый проект
```

После этого ChatGPT Project по repo-first instruction сначала читает `template-repo/scenario-pack/00-master-router.md`, проводит scenario-pack guided questionnaire, проверяет readiness по runbook/checklist и только затем формирует один стартовый Codex handoff.

Codex не является первым каналом постановки задачи для новичка. Codex является executor после handoff: создает repo/root/core, запускает wizard/verify/sync и готовит repo-first instruction для боевого ChatGPT Project.

## Источники истины

Executable routing остается в:

- `template-repo/codex-routing.yaml`;
- `.codex/config.toml`;
- `template-repo/scripts/resolve-codex-task-route.py`;
- `template-repo/scripts/launch-codex-task.sh`;
- `template-repo/scripts/orchestrate-codex-handoff.py`.

Advisory/policy layer остается в:

- `AGENTS.md`;
- `template-repo/scenario-pack/`;
- `docs/operator/`;
- `.chatgpt/*`;
- release-facing docs.

Runbook packages не переключают модель, профиль или reasoning внутри уже открытой сессии. Надежная routing boundary — новый task launch; user-facing default для VS Code Codex extension — новый чат/окно, ручной picker, затем один handoff block.
Brownfield здесь всегда означает временный adoption/reconstruction path, а не финальный класс проекта.

## Окна и границы

Каждый пакет обязан явно разделять:

- Browser ChatGPT Project;
- VS Code Remote SSH на VPS;
- Codex extension / Codex chat;
- Terminal only fallback;
- GitHub UI / external UI;
- secrets и external approvals.

## Финальные состояния

- `factory-template`: `greenfield-product` + `factory-producer-owned` layer.
- `greenfield-product`: active project root, lifecycle `greenfield-active` или после adoption `greenfield-converted`.
- `brownfield with repo`: transitional state до conversion или documented blocker.
- `brownfield without repo`: intake/reconstruction path; temporary/reconstructed/intermediate repos живут только внутри target project root, не siblings в `/projects`.

## Обязательные гейты

- master router прочитан из repo;
- выбран entry package;
- handoff содержит `Язык ответа Codex: русский`;
- one-paste handoff не заменяется ссылкой на файл;
- commands из verify layer существуют;
- brownfield done требует conversion или explicit blocker;
- transitional materials после conversion архивированы, переименованы или перенесены так, чтобы не путаться с active greenfield root;
- dashboard показывает phase, gates, blockers и next action.
