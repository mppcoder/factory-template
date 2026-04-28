# Task pack для Codex

## Идентификатор изменения
chg-20260428-gpt55-prompt-migration

## Заголовок
GPT-5.5 prompt migration for factory-template

## Класс изменения
migration

## Режим выполнения
codex-led

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
manual-ui (default)

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
factory-template self-improvement / prompt-migration

## Выбранный сценарий
template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md

## Этап pipeline
source-map -> prompt-inventory -> migration-plan -> remediation -> verification -> closeout

## Разрешение handoff
yes

## Маршрут defect-capture
reports/bugs/2026-04-28-gpt-5-5-prompt-migration-gap.md

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
