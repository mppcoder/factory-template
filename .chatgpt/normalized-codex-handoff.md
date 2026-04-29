# Нормализованный handoff для Codex

## Источник запуска
chatgpt-handoff

## Вид handoff
single-agent-handoff

## Evidence для вида handoff
- явный override handoff_shape: single-agent-handoff

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
factory-template self-improvement

## Выбранный сценарий
template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md -> docs/operator/factory-template/04-vps-remote-ssh-full-handoff-orchestration.md

## Этап pipeline
handoff policy modernization -> routing UX -> validation -> closeout

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
reports/bugs/2026-04-29-handoff-shape-validator-drift.md

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

## Базовый prompt contract для GPT-5.5
- GPT-5.5 не считать drop-in replacement для старого prompt stack.
- Начинать с fresh baseline: роль/область ответственности, ожидаемый outcome, success criteria, constraints, output shape и stop rules.
- Сохранять обязательные repo invariants: чтение router, defect-capture, handoff/routing/closeout rules.
- Убирать лишнюю пошаговую процессность, если путь не является обязательным repo invariant.
- Для tool-heavy задач явно задавать evidence requirements, validation commands и fallback/blocker behavior.
- Держать stable rules выше task-specific dynamic content, чтобы prompt caching и повторное использование оставались устойчивыми.
- Не вставлять current date как постоянную model instruction; даты reports/filenames фиксировать как metadata.

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