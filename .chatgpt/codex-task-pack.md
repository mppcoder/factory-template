# Task pack для Codex

## Change ID
chg-20260423-018

## Заголовок
Make VS Code Codex handoff UI-first by default

## Класс изменения
bugfix

## Режим выполнения
codex-led

## Launch source
chatgpt-handoff

## Task class
deep

## Selected profile
deep

## Selected model
gpt-5.4

## Selected reasoning effort
high

## Selected plan mode reasoning
high

## Apply mode
manual-ui

## Strict launch mode
optional

## Manual UI default
Для интерактивной работы в VS Code Codex extension откройте новый чат/окно Codex, вручную выберите `selected_model=gpt-5.4` и `selected_reasoning_effort=high` в picker, затем вставьте handoff.
Новый чат + вставка handoff и executable launcher path — не одно и то же.
Уже открытая live session не является надежным auto-switch механизмом.

## Optional strict launch command
./scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute

## Direct Codex command behind launcher
codex --profile deep

## Project profile
factory-template

## Selected scenario
00-master-router.md

## Pipeline stage
defect-capture -> classification -> remediation

## Handoff allowed
yes

## Defect capture path
reproduce -> evidence -> bug report -> layer classification -> remediation

## Repo Rules Priority
При исполнении handoff приоритет у правил repo: `AGENTS`, runbook, scenario-pack, policy files и других канонических файлов этого репозитория.
Общие рабочие инструкции применять только там, где они не конфликтуют с repo rules и старшими системными ограничениями среды.

## Handoff input
# Входной пакет для Codex

launch_source: chatgpt-handoff
task_class: deep
selected_profile: deep
selected_model: gpt-5.4
selected_reasoning_effort: high
apply_mode: manual-ui
strict_launch_mode: optional
project_profile: factory-template
selected_scenario: 00-master-router.md
pipeline_stage: defect-capture -> classification -> remediation
artifacts_to_update:
  - template-repo/scenario-pack/00-master-router.md
  - template-repo/codex-routing.yaml
  - template-repo/scripts/bootstrap-codex-task.py
  - template-repo/scripts/launch-codex-task.sh
  - .chatgpt/codex-input.md
  - .chatgpt/codex-context.md
  - .chatgpt/codex-task-pack.md
  - .chatgpt/verification-report.md
  - .chatgpt/done-report.md
  - source-facing runbooks/guides/templates for Codex / VS Code Codex extension handoff
  - completion package / downstream update instructions if source files change
handoff_allowed: yes
defect_capture_path: reproduce -> evidence -> bug report -> layer classification -> remediation

## Контекст
- Шаблон корректно различает advisory/policy layer и executable routing layer, но user-facing default UX для VS Code Codex extension перегружен launcher-first flow.
- Пользователь для interactive extension workflow не должен быть вынужден идти в terminal, если достаточно manual picker selection в новом окне/чате Codex.
- При этом нельзя обещать auto-switch profile/model/reasoning внутри уже открытой live session.

## Что именно нужно сделать
- Зафиксировать defect-capture по UX mismatch: проблема в default template behavior, а не в пользователе.
- Явно различить `manual-ui (default)`, `launcher-first strict mode (optional)` и `already-open session = non-canonical fallback`.
- Пересобрать handoff/completion слой так, чтобы для VS Code Codex extension по умолчанию выдавался UI-first handoff с `selected_profile`, `selected_model`, `selected_reasoning_effort`, `selected_scenario`, `pipeline_stage` и короткой manual UI apply-инструкцией.
- Сохранить launcher path только как optional strict mode для automation / reproducibility / shell-first / scripted launch.
- Обновить source-facing docs, templates, validators и generated `.chatgpt` artifacts под dual-path contract.
- Подготовить completion package для factory/downstream/ChatGPT Project source sync, если затронут downstream-consumed sources.

## Какие артефакты являются источником правды
- `AGENTS.md`
- `template-repo/scenario-pack/00-master-router.md`
- `template-repo/scenario-pack/12-bug-analysis.md`
- `template-repo/scenario-pack/15-handoff-to-codex.md`
- `template-repo/codex-routing.yaml`
- `template-repo/scripts/*codex*`
- `template-repo/template/docs/*`

## Что запрещено делать
- Нельзя подавать launcher-first path как обязательный default для интерактивной работы в VS Code Codex extension.
- Нельзя утверждать, что handoff text, static profile или уже открытая live session сами автоматически переключают model/profile/reasoning.
- Нельзя смешивать `новый чат + вставка handoff` с `new task launch через executable launcher`.

## Обязательное правило фиксации дефектов
Если в ходе анализа, реализации, тестирования, reverse engineering или verification обнаружен дефект, регрессия, расхождение, пропущенный шаг, шаблонный сбой или reusable process failure, его нельзя silently patch.

Нужно:
1. создать или обновить bug report в `reports/bugs/`;
2. собрать evidence и шаги воспроизведения;
3. указать слой дефекта: `project-only`, `factory-template` или `shared/unknown`;
4. определить, исправляется ли дефект в текущем scope или требует отдельного task boundary;
5. выполнить self-handoff для нового defect;
6. при необходимости подготовить ChatGPT handoff bug note или deep-research prompt;
7. если проблема reusable — создать или обновить factory feedback в `reports/factory-feedback/` или `meta-feedback/`;
8. только после этого или одновременно с этим делать fix.
