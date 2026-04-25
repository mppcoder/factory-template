# Task pack для Codex

## Идентификатор изменения
chg-20260423-021

## Заголовок
Default factory-template ChatGPT Project to no unless instruction contract changed

## Класс изменения
small-fix

## Режим выполнения
codex-led

## Источник запуска
chatgpt-handoff

## Класс задачи
build

## Выбранный профиль
build

## Выбранная модель
gpt-5.5

## Выбранное reasoning effort
medium

## Выбранное reasoning effort для plan mode
medium

## Режим применения
manual-ui

## Строгий режим запуска
optional

## Ручной UI по умолчанию
Для интерактивной работы в VS Code Codex extension откройте новый чат/окно Codex, вручную выберите `selected_model=gpt-5.5` и `selected_reasoning_effort=medium` в picker, затем вставьте handoff.
Новый чат + вставка handoff и executable launcher path — не одно и то же.
Уже открытая live session не является надежным auto-switch механизмом.

## Опциональная команда строгого запуска
./scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute

## Прямая команда Codex за launcher
codex --profile build

## Профиль проекта
factory-template self-improvement

## Выбранный сценарий
defect-capture -> remediation -> verify -> closeout

## Этап pipeline
remediation -> verify -> closeout

## Разрешение handoff
yes

## Маршрут defect-capture
reproduce -> evidence -> bug report -> layer classification -> factory feedback if reusable -> remediation

## Приоритет правил repo
При исполнении handoff приоритет у правил repo: `AGENTS`, runbook, scenario-pack, policy files и других канонических файлов этого репозитория.
Общие рабочие инструкции применять только там, где они не конфликтуют с repo rules и старшими системными ограничениями среды.

## Входные данные handoff
task_class: build
selected_profile: build
project_profile: factory-template self-improvement
selected_scenario: defect-capture -> remediation -> verify -> closeout
pipeline_stage: remediation -> verify -> closeout
handoff_allowed: yes
defect_capture_path: reproduce -> evidence -> bug report -> layer classification -> factory feedback if reusable -> remediation
artifacts_to_update:
  - template-repo/scenario-pack/00-master-router.md
  - template-repo/scenario-pack/01-global-rules.md
  - template-repo/scenario-pack/12-bug-analysis.md
  - template-repo/scenario-pack/15-handoff-to-codex.md
  - template-repo/scenario-pack/16-done-closeout.md
  - template-repo/scenario-pack/17-direct-task-self-handoff.md
  - template-repo/codex-routing.yaml
  - template-repo/scripts/bootstrap-codex-task.py
  - template-repo/scripts/codex_task_router.py
  - template-repo/scripts/create-codex-task-pack.py
  - template-repo/scripts/validate-codex-routing.py
  - template-repo/scripts/validate-codex-task-pack.py
  - template-repo/scripts/validate-handoff-response-format.py
  - template-repo/scripts/validate-operator-env.py
  - .chatgpt/verification-report.md
  - .chatgpt/done-report.md
  - reports/bugs/
  - reports/factory-feedback/

Задача:
Исправить два process defects в factory-template:
1. Codex не должен перекладывать доступный GitHub PR merge на пользователя, если GitHub write path доступен, checks green, PR доступен для merge и нет обязательного человеческого approval или другого blocker.
2. Человекочитаемые ответы, инструкции, отчеты, closeout и generated guidance должны быть на русском языке; английский допустим только для технических идентификаторов, команд, файлов, ключей конфигурации и literal values.

Нужно пройти defect-capture, внести remediation в repo rules/generators/validators, проверить и закрыть задачу внутри repo.

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
