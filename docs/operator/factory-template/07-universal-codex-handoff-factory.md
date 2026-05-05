# Universal Codex Handoff Factory

## Назначение

Universal Codex Handoff Factory делает `factory-template` repo-native фабрикой задач для Codex. Идея простая: любая задача, которая может попасть в Codex, сначала получает нормальную запись в repo, понятный маршрут, handoff и проверяемые evidence.

MVP не является daemon, web app, Telegram/Slack bot, database, background worker или полноценным Symphony runtime. Это легкий слой файлов, скриптов, issue templates, dashboard и runbook.

## Почему нужен universal task layer

Bug-only feedback покрывает только ошибки. Реальная разработка вайбкод-проекта состоит из разных классов задач:

- `bug`: ошибка, regression, missing step;
- `feature`: новая возможность;
- `docs`: объяснение, runbook, пример;
- `research`: вопрос перед решением;
- `audit`: проверка качества, privacy, release readiness;
- `refactor`: внутреннее улучшение без смены поведения;
- `release`: подготовка выпуска;
- `maintenance`: регулярная repo/VPS поддержка;
- `downstream_sync`: перенос feedback из боевого repo;
- `curator`: предложение reusable skill/runbook/validator.

Universal task layer не подменяет GitHub Issues и не заменяет ChatGPT. Он задает общий repo-owned формат, из которого можно получить Codex-ready handoff и dashboard status.

## Что уже было

До этого MVP в проекте уже были важные контуры:

- `template-repo/scenario-pack/00-master-router.md` как обязательная точка маршрутизации;
- `project-lifecycle-dashboard.yaml` и Markdown/card renderer;
- `.chatgpt/handoff-implementation-register.yaml` для контроля реализации handoff;
- `.chatgpt/chat-handoff-index.yaml` и `.chatgpt/codex-work-index.yaml` для stable ChatGPT/Codex identifiers;
- validators для route, dashboard, handoff UX, runbook packages и release-facing evidence.

## Что добавляет MVP

MVP добавляет repo-native основу для всех Codex-задач:

- `template-repo/template/.chatgpt/task-registry.yaml` - canonical registry для `FT-TASK-NNNN`;
- `template-repo/scripts/validate-task-registry.py` - проверка схемы, классов, статусов, route и evidence;
- `template-repo/scripts/task-to-codex-handoff.py` - генератор одного copy-paste Codex handoff;
- `template-repo/scripts/validate-codex-task-handoff.py` - проверка generated handoff;
- `.github/ISSUE_TEMPLATE/*.yml` - GitHub Issue Forms для основных task classes;
- `docs/operator/factory-template/08-chatgpt-codex-github-vps-one-paste-flow.md` - русскоязычный one-paste flow;
- `universal_task_control` в lifecycle dashboard.

В generated downstream project canonical generated path для registry: `.chatgpt/task-registry.yaml`. В самом шаблонном repo source-of-truth лежит в `template-repo/template/.chatgpt/task-registry.yaml`.

## Relation to Symphony

Symphony-подобные идеи полезны как future path:

- issue/task tracker как control plane;
- per-task workspace или worktree для изоляции;
- bounded runner, который берет одну задачу, запускает Codex и пишет evidence;
- dashboard/cockpit для видимого статуса.

MVP пока не daemon. Он не слушает очередь, не запускает background worker, не делает auto-merge и не деплоит production.

## Relation to OpenClaw+ as ideas

OpenClaw-style routing полезен как архитектурная метафора:

- role routing: разные классы задач могут идти через разные профили;
- gateway/intake pattern: GitHub Issue, ChatGPT handoff и scheduled task приводятся к одному task registry;
- bounded child sessions: будущий runner может запускать ограниченные child sessions;
- visible route/status: пользователь видит route receipt, dashboard и closeout.

В MVP нет зависимости от messaging runtime. Handoff остается одним `codex-task-handoff`; факт `single-session execution` или `orchestrated-child-sessions` решает Codex после анализа task graph.

## Relation to Hermes as ideas

Hermes-подобный learning loop допустим только как repo-reviewed процесс:

- reusable learning попадает в repo artifacts;
- future Factory Curator предлагает skill/runbook/validator;
- человек или Codex review проверяет evidence;
- скрытого самообучения вне repo нет.

Curator proposal в GitHub Issue не должен автоматически менять template. Он создает проверяемую задачу.

## Execution surfaces

Поддерживаемые поверхности:

- Codex app;
- VS Code Remote SSH Codex extension;
- Codex CLI;
- Codex cloud;
- future App Server adapter;
- future Symphony-like runner.

Advisory layer: `AGENTS`, `scenario-pack`, runbooks, `.chatgpt` guidance и handoff text.

Executable routing layer: named profiles, launcher scripts, Codex picker, Codex CLI, Codex app, Codex cloud или future adapter.

Нельзя считать, что advisory text сам переключает model/profile/reasoning внутри уже открытой Codex session. Manual UI default: открыть новый Codex chat, выбрать model/reasoning в picker и вставить handoff.

## Beginner default flow

1. Пользователь формулирует идею в ChatGPT.
2. ChatGPT помогает сделать запись или handoff.
3. Codex читает `template-repo/scenario-pack/00-master-router.md`.
4. Codex выводит route receipt.
5. Codex меняет repo, запускает проверки и обновляет dashboard.
6. GitHub хранит issue/PR/history.
7. VPS дает среду выполнения, когда задача касается runtime.

## Advanced automation flow

Future automation может добавить:

- bridge GitHub Issue -> task registry;
- allocator для `FT-TASK-NNNN`;
- task-to-handoff в CI или local launcher;
- per-task worktree;
- bounded runner with explicit consent;
- curator proposal queue.

Даже в advanced flow секреты, paid actions, production deploy, public external reports и required human review остаются boundary и требуют подтверждения.

## Privacy/security boundaries

- Не публиковать secrets, tokens, passwords, private keys.
- Не публиковать raw private logs или данные клиентов.
- External user reports по умолчанию идут как sanitized draft.
- Public submission требует review и consent.
- Merge, deploy, paid/security-sensitive actions не автоматизируются без явного разрешения.
- Green status требует evidence или accepted_reason.

## Definition of Done

MVP считается готовым, когда:

- `task-registry.yaml` существует и валидируется;
- generator создает один copy-paste Codex handoff;
- generated handoff проходит validator;
- GitHub Issue templates покрывают основные task classes;
- one-paste runbook понятен новичку;
- dashboard показывает Universal Task Control без false green;
- docs объясняют future path к Symphony/OpenClaw/Hermes как идеи, а не hard dependency;
- `verify-all quick` или targeted validators зеленые, либо blocker явно зафиксирован.
