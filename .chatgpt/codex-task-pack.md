# Task pack для Codex

## Change ID
chg-20260423-020

## Заголовок
Default downstream ChatGPT Projects to no in clean repo-first mode

## Класс изменения
small-fix

## Режим выполнения
codex-led

## Launch source
chatgpt-handoff

## Task class
build

## Selected profile
build

## Selected model
gpt-5.4

## Selected reasoning effort
medium

## Selected plan mode reasoning
medium

## Apply mode
manual-ui

## Strict launch mode
optional

## Manual UI default
Для интерактивной работы в VS Code Codex extension откройте новый чат/окно Codex, вручную выберите `selected_model=gpt-5.4` и `selected_reasoning_effort=medium` в picker, затем вставьте handoff.
Новый чат + вставка handoff и executable launcher path — не одно и то же.
Уже открытая live session не является надежным auto-switch механизмом.

## Optional strict launch command
./scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute

## Direct Codex command behind launcher
codex --profile build

## Project profile
factory-template

## Selected scenario
00-master-router.md

## Pipeline stage
defect-capture -> classification -> remediation -> verify

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
task_class: build
selected_profile: build
selected_model: gpt-5.4
selected_reasoning_effort: medium
apply_mode: manual-ui
strict_launch_mode: optional
project_profile: factory-template
selected_scenario: 00-master-router.md
pipeline_stage: defect-capture -> classification -> remediation -> verify
artifacts_to_update:
  - template-repo/scenario-pack/00-master-router.md
  - template-repo/scenario-pack/15-handoff-to-codex.md
  - template-repo/scenario-pack/16-done-closeout.md
  - template-repo/scripts/create-codex-task-pack.py
  - template-repo/scripts/validate-codex-task-pack.py
  - docs/template-architecture-and-event-workflows.md
  - .chatgpt/codex-input.md
  - .chatgpt/codex-context.md
  - .chatgpt/codex-task-pack.md
  - .chatgpt/verification-report.md
  - .chatgpt/done-report.md
  - reports/bugs/bug-020-repo-first-completion-package-overstates-downstream-chatgpt-updates.md
  - reports/factory-feedback/feedback-020-repo-first-completion-package-overstates-downstream-chatgpt-updates.md
handoff_allowed: yes
defect_capture_path: reproduce -> evidence -> bug report -> layer classification -> remediation

## Контекст
- Шаблонный completion package слишком широко трактует contour `downstream/battle ChatGPT Projects`.
- Для чистого repo-first режима это должен быть `нет` по умолчанию, а не generic contour, который легко превращается в `да`.

## Что именно нужно сделать
- Зафиксировать reusable process defect completion-layer.
- Переписать source-of-truth rules и generator так, чтобы `Нужно ли обновлять repo-first инструкции battle ChatGPT Projects` по умолчанию означало `нет` для чистого repo-first режима.
- Сохранить `да` только как legacy/hybrid fallback.
- Пересобрать `.chatgpt` artifacts, проверить validators и довести change до verified sync.

## Какие артефакты являются источником правды
- `AGENTS.md`
- `template-repo/AGENTS.md`
- `template-repo/scenario-pack/00-master-router.md`
- `template-repo/scenario-pack/15-handoff-to-codex.md`
- `template-repo/scenario-pack/16-done-closeout.md`
- `template-repo/scripts/create-codex-task-pack.py`
- `template-repo/scripts/validate-codex-task-pack.py`
- `README.md`

## Что запрещено делать
- Нельзя трактовать downstream ChatGPT Project instructions как default contour в чистом repo-first режиме.
- Нельзя советовать refresh `Sources` или переписывание Project instructions там, где source-of-truth уже давно читается из репо.

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
