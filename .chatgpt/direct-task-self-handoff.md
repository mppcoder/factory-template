# Self-handoff для прямой задачи

## Источник запуска
direct-task

## Класс задачи
deep

## Evidence для класса задачи
- явный override task_class: deep
- явный override selected_profile: deep

## Выбранный профиль
deep

## Выбранная модель
gpt-5.5

## Выбранное reasoning effort
high

## Выбранное reasoning effort для plan mode
high

## Режим применения
manual-ui

## Ручное применение через UI
- Откройте новый чат/окно Codex в VS Code extension.
- Вручную выберите model `gpt-5.5` и reasoning `high` в picker.
- Только после этого вставьте handoff.
- Codex должен отвечать пользователю на русском языке; английский допустим только для technical literal values.
- Уже открытая live session не считается надежным auto-switch boundary.

## Язык ответа Codex
Русский. Английский допустим только для technical literal values: команды, пути, YAML/JSON keys, model IDs и route fields.

## Строгий режим запуска
optional

## Профиль проекта
brownfield-without-repo

## Выбранный сценарий
brownfield/11-codex-assisted-stabilization.md

## Этап pipeline
fp-02-github-remote-and-roadmap-continuation

## Артефакты для обновления
- .chatgpt/task-launch.yaml
- .chatgpt/direct-task-source.md
- .chatgpt/direct-task-self-handoff.md
- .chatgpt/normalized-codex-handoff.md
- .chatgpt/direct-task-response.md
- .chatgpt/boundary-actions.md
- .chatgpt/done-checklist.md
- reports/bugs/bug-037-github-repo-creation-misclassified-as-user-step.md
- reports/factory-feedback/feedback-037-github-repo-creation-misclassified-as-user-step.md
- reports/bugs/bug-038-generated-project-root-script-verify-all-wrong-root.md
- reports/factory-feedback/feedback-038-generated-project-root-script-verify-all-wrong-root.md
- reports/release/field-pilot-scenarios/02-brownfield-without-repo.md
- reports/release/2.5-field-pilot-evidence.md
- brownfield/reconstruction-repo-report.md
- brownfield/gap-register.md
- .chatgpt/evidence-register.md
- .chatgpt/reality-check.md
- .chatgpt/verification-report.md
- .chatgpt/done-report.md

## Разрешение handoff
no

## Маршрут defect-capture
reproduce -> evidence -> bug report -> layer classification -> factory feedback if reusable -> remediation

## Правило launch boundary
Выбор модели и reasoning mode считается надежным только на новом запуске Codex для новой задачи.

## Правило интерактивного режима по умолчанию
Для интерактивной работы в VS Code Codex extension основной пользовательский путь: открыть новое окно/чат Codex, вручную выбрать model/reasoning в picker и затем вставить handoff.

## Правило executable switch
Строго воспроизводимое executable-переключение в live Codex для этого repo: явный новый task launch через launcher и selected_profile.

## Правило строгого запуска
Launcher-first path остается опциональным строгим режимом для автоматизации, воспроизводимости, запуска из shell и scripted launch.

## Правило fallback для live session
Уже открытая live session не является надежным механизмом автопереключения profile/model/reasoning и допустима только как неканонический fallback.

## Правило ожиданий по модели
selected_model и selected_reasoning_effort фиксируют repo-configured mapping выбранного executable profile; live availability подтверждается отдельной проверкой `codex debug models`, а advisory handoff text сам по себе ничего не переключает.

## Статус catalog check
available

## Последняя catalog check UTC
2026-04-25T18:26:17Z

## Примечание по live availability
selected_model совпадает с последним сохраненным snapshot repo catalog; перед внешними обещаниями повторите live catalog check

## Путь launch artifact
`.chatgpt/direct-task-source.md`

## Опциональная команда строгого запуска
`./scripts/launch-codex-task.sh --launch-source direct-task --task-file .chatgpt/direct-task-source.md --execute`

## Сценарии для строгого запуска
- автоматизация
- воспроизводимость
- запуск из shell
- scripted launch

## Прямая команда Codex за launcher
`codex --profile deep`

## Диагностика проблем
- Если вы работаете через VS Code Codex extension интерактивно, используйте новый чат/окно, вручную выставьте selected_model и selected_reasoning_effort в picker, а затем вставьте handoff.
- Новый чат + вставка handoff и новый task launch через executable launcher — не одно и то же; не выдавайте manual UI apply за auto-switch.
- Если handoff вставлен в уже открытую или случайную Codex chat-сессию без ручной проверки picker, это неканонический путь: route может остаться устаревшим.
- Если нужна строгая воспроизводимость, автоматизация или запуск из shell, используйте optional strict launch_command.
- Если после launch или manual UI apply виден sticky last-used profile/model/reasoning, закройте текущую сессию, откройте новую и при необходимости выполните launch_command, затем проверьте именованный profile в local Codex config.
- Если selected_model отсутствует в live catalog, обновите codex-routing.yaml или local profile mapping, прежде чем обещать этот model ID пользователю.
- Если новый model ID появился в live catalog, сначала создайте proposal через `scripts/check-codex-model-catalog.py --write-proposal`; promotion profile mapping требует ручного review.

## Текст задачи
task_class: deep
selected_profile: deep
project_profile: brownfield-without-repo
selected_scenario: brownfield/11-codex-assisted-stabilization.md
pipeline_stage: fp-02-github-remote-and-roadmap-continuation
handoff_allowed: no
artifacts_to_update:
  - .chatgpt/task-launch.yaml
  - .chatgpt/direct-task-source.md
  - .chatgpt/direct-task-self-handoff.md
  - .chatgpt/normalized-codex-handoff.md
  - .chatgpt/direct-task-response.md
  - .chatgpt/boundary-actions.md
  - .chatgpt/done-checklist.md
  - reports/bugs/bug-037-github-repo-creation-misclassified-as-user-step.md
  - reports/factory-feedback/feedback-037-github-repo-creation-misclassified-as-user-step.md
  - reports/bugs/bug-038-generated-project-root-script-verify-all-wrong-root.md
  - reports/factory-feedback/feedback-038-generated-project-root-script-verify-all-wrong-root.md
  - reports/release/field-pilot-scenarios/02-brownfield-without-repo.md
  - reports/release/2.5-field-pilot-evidence.md
  - brownfield/reconstruction-repo-report.md
  - brownfield/gap-register.md
  - .chatgpt/evidence-register.md
  - .chatgpt/reality-check.md
  - .chatgpt/verification-report.md
  - .chatgpt/done-report.md
defect_capture_path: reproduce -> evidence -> bug report -> layer classification -> factory feedback if reusable -> remediation

Исправить пойманные баги: не останавливаться просьбой пользователю создать GitHub repo и прислать URL, если gh/GitHub write path доступен; дать четкую инструкцию по внешним действиям только при реальном blocker; исправить generated root scripts/verify-all.sh, который в downstream repo вычислял ROOT как /projects. Создать/подключить GitHub remote для /projects/openclaw-brownfield и продолжить field pilot roadmap честно.
