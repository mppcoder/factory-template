# Журнал изменений шаблона

## [Unreleased]
### Добавлено
- reusable scripts `verified-sync` и `execute-release-decision` для generated project automation
- templates для `release-decision`, `sync-report` и `release-report`
- lightweight follow-up mode для low-risk post-verify docs/ignore cleanup
- internal-followup precedence rule для handoff/boundary layers generated project
- source-update completion package и impact model для boundary/handoff layers generated project
- immediate completion-package rule для generated closeout/handoff behavior
- generated boundary guidance больше не должна перекладывать internal prepare/export commands на пользователя

### Изменено
- template/runtime/policy layer теперь закрепляет обязательный inline Codex handoff, если handoff уже допустим и задача достаточно определена
- template guidance теперь требует финальный блок `Инструкция пользователю` при любом pending user/external step
- generated projects теперь могут отделять verified sync от release publication

### Исправлено
- устранен reusable process gap между router, handoff rules, runbook, AGENTS и closeout layer

## [2.4.2] - 2026-04-20
### Изменено
- template layer синхронизирован с hybrid-моделью Sources: direct hot-set для daily use и canonical archive pack для steady snapshot
- generated guidance теперь исходит из единого declarative Sources manifest

## [2.4.1] - 2026-04-20
### Добавлено
- профиль `brownfield-dogfood-codex-assisted` для dogfood-сценария brownfield without repo
- класс изменения `brownfield-stabilization` с поддержкой `hybrid` и `codex-led`
- шаблонные `.codex` конфиги и подагенты для автоматического переключения режимов внутри одной живой сессии
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
