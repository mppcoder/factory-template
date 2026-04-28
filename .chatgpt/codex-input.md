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

Поддерживать GPT-5.5 prompt migration baseline для `factory-template`: fresh prompt baseline, outcome-first contract, success criteria, constraints, evidence requirements, output shape и stop rules.

## Критерии успеха

- Prompt-like artifacts сохраняют GPT-5.5 contract и не считают GPT-5.5 drop-in replacement.
- Repo invariants сохранены: router-first, advisory vs executable routing, defect-capture, handoff/closeout/sync-state.
- Reasoning profile policy сохранен: `build` -> `gpt-5.5`/`medium`, `deep` -> `gpt-5.5`/`high`, `review` -> `gpt-5.5`/`high`, `quick` остается `gpt-5.4-mini` без silent promotion.
- Validators/evals ловят stale handoff, forbidden prompt phrases и missing prompt contract markers.

## Ограничения

- Использовать только official OpenAI/OpenAI Docs/Help Center sources для внешних prompt recommendations.
- Не утверждать live model availability без live catalog check.
- Не переписывать repo-first contract в advisory-only рекомендацию.
- Не удалять defect-capture gates.
- Не добавлять secrets, private transcripts или credentials.

## Требования к доказательствам

- Repo evidence: `AGENTS.md`, `template-repo/scenario-pack/00-master-router.md`, `template-repo/scenario-pack/15-handoff-to-codex.md`, `template-repo/codex-routing.yaml`, `template-repo/template/.codex/config.toml`.
- Official docs evidence: OpenAI latest model guide, prompt guidance, prompt optimizer and Help Center GPT-5.3/GPT-5.5 model picker facts.
- Prompt inventory evidence: `.chatgpt/*`, template `.chatgpt/*`, scenario-pack, tasks/codex, skills, operator docs, bootstrap, template docs, artifact eval specs, routing/config and prompt-rendering scripts.

## Форма результата

- Source map -> gap map -> remediation -> verification.
- User-facing closeout на русском языке: changed files, tests, sync status and external actions.
- Handoff output as one copy-paste block when handoff is needed.

## Правила остановки

- Если command отсутствует или падает из-за внешнего blocker, зафиксировать command, error summary, blocker/non-blocker и next-best check.
- Если нужен model-routing promotion для `quick`, не менять автоматически; создать proposal в `reports/model-routing/` и пометить manual review required.
- Если найден reusable defect, сначала зафиксировать bug report и factory feedback, затем remediation.

## Динамические поля задачи

- task goal: maintain GPT-5.5 prompt migration contract.
- selected profile/model/reasoning: `deep` / `gpt-5.5` / `high`.
- artifacts_to_update: prompt-like artifacts, validators/evals and closeout reports when drift is found.
