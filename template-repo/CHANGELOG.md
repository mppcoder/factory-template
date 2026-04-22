# Журнал изменений шаблона

## [Unreleased]
### Добавлено
- reusable scripts `verified-sync` и `execute-release-decision` для generated project automation
- templates для `release-decision`, `sync-report` и `release-report`
- lightweight follow-up mode для low-risk post-verify docs/ignore cleanup
- internal-followup precedence rule для handoff/boundary layers generated project
- completion package и impact model для repo-first instruction layers generated project
- immediate completion-package rule для generated closeout/handoff behavior
- generated boundary guidance больше не должна перекладывать internal prepare/export commands на пользователя
- executable routing layer для каждой новой Codex-задачи: `codex-routing.yaml`, named profiles и launcher/router scripts
- direct-task self-handoff standard с `.chatgpt/task-launch.yaml`, `.chatgpt/normalized-codex-handoff.md`, `.chatgpt/direct-task-self-handoff.md` и `.chatgpt/direct-task-response.md`
- root-level visual/workflow reference doc для архитектуры шаблона и основных deployment/update событий

### Изменено
- template/runtime/policy layer теперь закрепляет обязательный inline Codex handoff, если handoff уже допустим и задача достаточно определена
- template guidance теперь требует финальный блок `Инструкция пользователю` при любом pending user/external step
- generated projects теперь могут отделять verified sync от release publication
- generated docs, `.chatgpt` artifacts и validators теперь различают advisory layer и executable routing layer
- generated direct-task contour теперь требует отдельный visible response artifact до remediation и проверяется routing validator-ом

### Исправлено
- устранен reusable process gap между router, handoff rules, runbook, AGENTS и closeout layer
- устранен template defect: routing по типу задачи больше не сводится к одному static profile без launch-time фиксации
- устранен template process gap, при котором direct task мог не показывать self-handoff явно в первом substantive ответе

## [2.4.2] - 2026-04-20
### Изменено
- template layer синхронизирован с repo-first режимом для ChatGPT Projects
- generated guidance теперь требует сначала читать GitHub repo и `00-master-router.md`

## [2.4.1] - 2026-04-20
### Добавлено
- профиль `brownfield-dogfood-codex-assisted` для dogfood-сценария brownfield without repo
- класс изменения `brownfield-stabilization` с поддержкой `hybrid` и `codex-led`
- шаблонные `.codex` конфиги и подагенты для session-specific specialization внутри Codex; task-based routing для новых задач позже вынесен в launcher/router layer
- workspace pack `vscode-codex-dogfood-bootstrap` для старта из одного окна VS Code с дальнейшим переходом на отдельные окна по проектам

### Изменено
- launcher теперь предлагает новый профиль и новый класс изменения
- policy preset и scenario-pack расширены под evidence-first → stabilization → reconstructed repo → clean package flow


## [2.4.0] - 2026-04-16
### Изменено
- launcher и generated versioning layer переведены на финальную версию фабрики `2.4.0`
- generated project origin и changelog больше не несут `rc2` как текущую фабричную версию

## [2.4.0-rc2] - 2026-04-15
### Добавлено
- единый release-alignment/versioning layer для generated projects
- автоматическая генерация `VERSION.md`, `CHANGELOG.md`, `CURRENT_FUNCTIONAL_STATE.md`
- валидатор versioning layer

### Изменено
- `project-origin.md` и launcher синхронизированы с актуальной версией фабрики
