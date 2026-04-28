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
manual-ui (default)

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
factory-template self-improvement / prompt-migration

## Выбранный сценарий
template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md

## Этап pipeline
source-map -> prompt-inventory -> migration-plan -> remediation -> verification -> closeout

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
reports/bugs/2026-04-28-gpt-5-5-prompt-migration-gap.md

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
task_class: deep
selected_profile: deep
selected_model: gpt-5.5
selected_reasoning_effort: high
selected_plan_mode_reasoning_effort: high
apply_mode: manual-ui (default)
strict_launch_mode: optional
project_profile: factory-template self-improvement / prompt-migration
selected_scenario: template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md
pipeline_stage: source-map -> prompt-inventory -> migration-plan -> remediation -> verification -> closeout
handoff_allowed: true
defect_capture_path: reports/bugs/2026-04-28-gpt-5-5-prompt-migration-gap.md

Язык ответа Codex: русский.
Отвечай пользователю по-русски. Английский допустим только для technical literal values: команды, пути, YAML/JSON keys, model IDs и route fields.

## Целевой результат

Переработать prompt-like артефакты `factory-template` под GPT-5.5 как fresh prompt baseline, не как drop-in replacement старого prompt stack.

## Критерии успеха

- Prompt-like handoff/task-pack/template artifacts начинаются с outcome-first contract: роль/область ответственности при необходимости, expected outcome, success criteria, constraints, evidence requirements, output shape, stop rules.
- Обязательные repo invariants сохранены: сначала `00-master-router.md`, advisory vs executable routing, defect-capture, inline handoff, verification/closeout/sync-state.
- Reasoning profile policy сохранен: `build` -> `gpt-5.5`/`medium`, `deep` -> `gpt-5.5`/`high`, `review` -> `gpt-5.5`/`high`, `quick` остается `gpt-5.4-mini` без silent promotion.
- Validators/evals ловят drift старых prompt patterns: stale `.chatgpt/codex-input.md`, отсутствие GPT-5.5 prompt contract, `self-handoff` вместо `handoff receipt` для `chatgpt-handoff`, forbidden prompt phrases.
- Closeout reports честно фиксируют source map, gap map, remediation, verification, model catalog status, defects/factory feedback и sync status.

## Ограничения

- Использовать только официальные OpenAI/OpenAI Docs/Help Center sources для внешних рекомендаций.
- Не утверждать live availability `selected_model` без live catalog check.
- Не переписывать repo-first contract в мягкую рекомендацию.
- Не удалять defect-capture gates.
- Не добавлять secrets, tokens, private transcripts или credentials.
- Не смешивать эту миграцию со старыми task artifacts.

## Требования к доказательствам

- Repo evidence: `AGENTS.md`, `template-repo/scenario-pack/00-master-router.md`, `template-repo/scenario-pack/15-handoff-to-codex.md`, `template-repo/codex-routing.yaml`, `template-repo/template/.codex/config.toml`.
- Official docs evidence: OpenAI `Using GPT-5.5`, OpenAI `Prompt guidance`, OpenAI `Prompt optimizer`, OpenAI Help Center `GPT-5.3 and GPT-5.5 in ChatGPT`.
- Prompt inventory: `.chatgpt/*`, template `.chatgpt/*`, scenario-pack, tasks/codex, skills, operator docs, bootstrap, template docs, artifact eval specs, routing/config and scripts that render handoff/task packs.

## Артефакты для обновления

- `.chatgpt/codex-input.md`
- `.chatgpt/codex-context.md`
- `.chatgpt/codex-task-pack.md`
- `.chatgpt/verification-report.md`
- `.chatgpt/done-report.md`
- `reports/prompt-migration/2026-04-28-gpt-5-5-prompt-inventory.md`
- `reports/prompt-migration/2026-04-28-gpt-5-5-prompt-migration-report.md`
- `reports/bugs/2026-04-28-gpt-5-5-prompt-migration-gap.md`
- `reports/factory-feedback/feedback-2026-04-28-gpt-5-5-prompt-migration-gap.md`
- prompt-generating scripts, template `.chatgpt` files and artifact-eval specs when needed
- `CURRENT_FUNCTIONAL_STATE.md`
- `VERIFY_SUMMARY.md`
- `CHANGELOG.md`

## Проверка

- `git status --short --branch`
- `git diff --check`
- `python3 template-repo/scripts/validate-codex-routing.py`
- `python3 template-repo/scripts/check-codex-model-catalog.py` или зафиксировать blocker/live catalog unavailable
- `python3 template-repo/scripts/validate-beginner-handoff-ux.py` или зафиксировать если script отсутствует/неприменим
- `bash template-repo/scripts/verify-all.sh ci`
- `rg` audit old model/prompt patterns with manual classification

## Правила остановки

- Если command отсутствует или падает из-за внешнего blocker, зафиксировать command, error summary, blocker/non-blocker и next-best check.
- Если нужен model-routing promotion для `quick`, не менять автоматически; создать proposal в `reports/model-routing/` и пометить manual review required.
- Если найден reusable defect, сначала зафиксировать bug report и factory feedback, затем remediation.