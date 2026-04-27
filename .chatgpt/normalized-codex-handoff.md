# Нормализованный handoff для Codex

## Источник запуска
chatgpt-handoff

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
factory-template

## Выбранный сценарий
post-2.5/downstream-multi-cycle-sync

## Этап pipeline
audit → evidence → remediation-if-needed

## Артефакты для обновления
- .chatgpt/codex-input.md
- .chatgpt/codex-context.md
- .chatgpt/codex-task-pack.md
- .chatgpt/verification-report.md
- .chatgpt/done-report.md
- reports/bugs/
- reports/factory-feedback/

## Разрешение handoff
yes

## Маршрут defect-capture
reports/bugs/YYYY-MM-DD-downstream-multi-cycle-sync-gap.md

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
`.chatgpt/codex-input.md`

## Опциональная команда строгого запуска
`./scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute`

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
CODEX HANDOFF — DOWNSTREAM MULTI-CYCLE SYNC PROOF

launch_source: chatgpt-handoff
task_class: downstream-sync-validation
selected_profile: deep
selected_model: gpt-5.5
selected_reasoning_effort: high
project_profile: factory-template
selected_scenario: post-2.5/downstream-multi-cycle-sync
pipeline_stage: audit → evidence → remediation-if-needed
handoff_allowed: true
defect_capture_path: reports/bugs/YYYY-MM-DD-downstream-multi-cycle-sync-gap.md

Язык ответа Codex: русский.

ЦЕЛЬ: Доказать, что downstream sync v3 выдерживает несколько циклов: initial template sync, manual project-owned edits, advisory review, safe-generated update, safe-clone update, rollback, brownfield transition → greenfield conversion.

АРТЕФАКТЫ ОБНОВИТЬ:
- docs/downstream-upgrade-policy.md
- reports/release/downstream-multi-cycle-sync-report.md
- factory/producer/extensions/workspace-packs/factory-ops/*
- MATRIX_TEST.sh
- TEST_REPORT.md
- CURRENT_FUNCTIONAL_STATE.md

ЗАДАЧИ:
1. Создать synthetic downstream fixture для multi-cycle sync.
2. В цикле 1 применить safe-generated/safe-clone.
3. В цикле 2 сделать manual project-owned edits.
4. В цикле 3 обновить template-owned files и проверить project-owned не перезаписан, advisory-review не применён автоматически, rollback metadata корректна.
5. В цикле 4 проверить rollback.
6. В отдельном сценарии проверить brownfield converted_greenfield.
7. Обновить report и TEST_REPORT.

Дополнительно учесть Stage 5: проверить production VPS field pilot docs/scripts/reports как template-owned/safe или advisory зоны без перезаписи project-owned runtime env/secrets: deploy/.env, .factory-runtime/, field-pilot reports, backup/rollback transcripts и real VPS approval boundary.

КРИТЕРИИ ПРИЕМКИ:
- Multi-cycle sync report есть и честен.
- Project-owned изменения защищены.
- Advisory-review требует ручного review.
- Rollback работает после нескольких циклов.
- Brownfield history сохраняется после conversion.
- bash template-repo/scripts/verify-all.sh ci проходит.

COMPLETION PACKAGE:
В финале указать downstream/battle repo sync commands, что safe to apply, что review-only, что manual-only, требуется ли ChatGPT Project Sources fallback, и Реестр внешних действий по контурам: factory-template ChatGPT Project, downstream repo sync, downstream ChatGPT Project, real VPS/user approval, secrets/manual boundary.
