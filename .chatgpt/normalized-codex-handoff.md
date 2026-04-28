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
factory-template as greenfield-product + factory-producer-owned layer

## Выбранный сценарий
template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md -> minimal required self-improvement/change/release-followup path

## Этап pipeline
Plan №5 kickoff -> internal hardening -> runner + quality evidence polish -> VPS Remote SSH-first full handoff orchestration -> verification -> release-facing closeout

## Артефакты для обновления
- docs/releases/plan-5-internal-hardening-roadmap.md
- docs/operator/factory-template/04-vps-remote-ssh-full-handoff-orchestration.md
- template-repo/template/docs/codex-workflow.md
- docs/operator/factory-template/03-mode-routing-factory-template.md
- template-repo/codex-routing.yaml
- template-repo/scenario-pack/15-handoff-to-codex.md
- .chatgpt/normalized-codex-handoff.md
- template-repo/template/.chatgpt/normalized-codex-handoff.md
- template-repo/scripts/orchestrate-codex-handoff.py
- template-repo/scripts/validate-codex-orchestration.py
- template-repo/scripts/validate-curated-pack-quality.py
- template-repo/scripts/validate-verified-sync-fallback-evidence.py
- tests/codex-orchestration/
- tests/curated-pack-quality/
- docs/releases/post-2.5-gap-register.md
- CURRENT_FUNCTIONAL_STATE.md
- TEST_REPORT.md
- CHANGELOG.md

## Разрешение handoff
yes

## Маршрут defect-capture
not defect-class initially; if any mismatch, stale routing, validator gap, false default path, Cloud/App overclaim, or repo-rule inconsistency is found, run defect-capture first, then remediate.

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
Plan №5: internal hardening / runner + quality evidence polish + VPS Remote SSH-first Full Handoff Orchestration Layer.

Цель: добавить repo-native orchestration layer, где default path идет через VS Code Remote SSH to VPS, Codex extension в этом repo context, repo-native parent orchestrator, отдельные Codex CLI child sessions и parent operational report. Codex App / Cloud Director optional, not default.

Граница scope: не переоткрывать Plan №4 P4-S5 real downstream app pilot и не требовать real downstream app для Plan №5.
