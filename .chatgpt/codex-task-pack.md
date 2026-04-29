# Task pack для Codex

## Идентификатор изменения
chg-20260428-project-root-boundary

## Заголовок
Закрепить project-root boundary для intermediate repos

## Класс изменения
не заполнен

## Режим выполнения
не заполнен

## Источник запуска
chatgpt-handoff

## Класс задачи
deep

## Выбранный профиль
deep

## Выбранная модель
gpt-5.5

## Выбранное reasoning effort
high

## Выбранное reasoning effort для plan mode
high

## Статус model catalog
available

## Примечание по live availability
selected_model совпадает с последним сохраненным snapshot repo catalog; перед внешними обещаниями повторите live catalog check

## Режим применения
manual-ui

## Строгий режим запуска
optional

## Ручной UI по умолчанию
Для интерактивной работы в VS Code Codex extension откройте новый чат/окно Codex, вручную выберите `selected_model=gpt-5.5` и `selected_reasoning_effort=high` в picker, затем вставьте handoff.
Новый чат + вставка handoff и executable launcher path — не одно и то же.
Уже открытая live session не является надежным auto-switch механизмом.

## Язык ответа Codex
Русский. Codex должен отвечать пользователю по-русски; английский допустим только для technical literal values: команды, пути, YAML/JSON keys, model IDs и route fields.

## Опциональная команда строгого запуска
./scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute

## Прямая команда Codex за launcher
codex --profile deep

## Профиль проекта
factory-template self-improvement

## Выбранный сценарий
template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md -> docs/operator/factory-template/04-vps-remote-ssh-full-handoff-orchestration.md

## Этап pipeline
handoff policy modernization -> routing UX -> validation -> closeout

## Разрешение handoff
yes

## Маршрут defect-capture
reports/bugs/2026-04-29-handoff-shape-validator-drift.md

## Приоритет правил repo
При исполнении handoff приоритет у правил repo: `AGENTS`, runbook, scenario-pack, policy files и других канонических файлов этого репозитория.
Общие рабочие инструкции применять только там, где они не конфликтуют с repo rules и старшими системными ограничениями среды.

## Базовый prompt contract для GPT-5.5
GPT-5.5 не считать drop-in replacement для старого prompt stack. Для prompt-like артефактов используйте fresh baseline:
- роль / область ответственности, если она нужна;
- ожидаемый outcome;
- success criteria;
- constraints и allowed side effects;
- evidence requirements и tool-use rules;
- output shape и verbosity;
- stop rules / closeout conditions.

Подробную пошаговую процессность оставляйте только там, где она является repo invariant: repo-first router, advisory vs executable routing, defect-capture, handoff, verification, closeout и sync-state. Stable rules держите выше dynamic task-specific fields.

## Входные данные handoff
CODEX HANDOFF — GPT-5.5 PROMPT MIGRATION FOR FACTORY-TEMPLATE

launch_source: chatgpt-handoff
handoff_shape: single-agent-handoff
task_class: deep
selected_profile: deep
selected_model: gpt-5.5
selected_reasoning_effort: high
selected_plan_mode_reasoning_effort: high
apply_mode: manual-ui
strict_launch_mode: optional
project_profile: factory-template self-improvement
selected_scenario: template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md -> docs/operator/factory-template/04-vps-remote-ssh-full-handoff-orchestration.md
pipeline_stage: handoff policy modernization -> routing UX -> validation -> closeout
handoff_allowed: yes
defect_capture_path: reports/bugs/2026-04-29-handoff-shape-validator-drift.md

Язык ответа Codex: русский
Отвечай пользователю по-русски.

Цель: добавить обязательный выбор вида handoff для новой задачи и сделать validators/tests shape-aware.

Почему parent orchestration не требуется: задача цельная, выполняется одним deep route в одном repo и не требует child Codex sessions.

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
