# Beginner intake missing default decisions

Дата: 2026-04-29
Статус: remediation in progress
Слой: `docs/operator/runbook-packages`, `template-repo/scenario-pack`, `.chatgpt` intake/dashboard artifacts, validators

## Summary

Опрос пользователя для создания боевого проекта недостаточно beginner-first. Для новичка нельзя задавать все решения как пустые expert-only поля, если фабрика может предложить безопасное рекомендуемое решение на основе repo policy, official docs, известных best practices, масштаба проекта или уже введенной концепции.

## Route

- `launch_source`: `chatgpt-handoff`
- `task_class`: `deep`
- `selected_profile`: `deep`
- `selected_model`: `gpt-5.5`
- `selected_reasoning_effort`: `high`
- `selected_scenario`: `template-repo/scenario-pack/00-master-router.md -> defect-capture -> scenario/questionnaire default-decision remediation -> verification -> closeout`
- `pipeline_stage`: `beginner-first intake UX remediation`
- `defect_capture_path`: `required`

## Evidence

- `docs/operator/runbook-packages/02-greenfield-product/01-user-runbook.md` step `GF-020` просил пользователя ответить на набор полей, но не требовал сначала выбрать режим default decisions.
- `template-repo/scenario-pack/04-discovery-new-project.md`, `05-clarify-scope.md` и `06-user-spec-generation.md` описывали, что собрать, но не требовали recommendation-first question format.
- Brownfield entry/user-runbooks фиксировали canonical root/incoming boundaries, но не объявляли их как рекомендуемые defaults с понятным override path.
- `template-repo/template/.chatgpt/intake.yaml` и lifecycle dashboard не содержали `default_decision_mode`, accepted/overridden defaults, uncertainty notes и unresolved decision counters.
- `validate-runbook-packages.py` проверял наличие guided questionnaire, но не блокировал blank expert-only questions там, где должен существовать safe default.

## Expected behavior

Intake/questionnaire flows должны иметь default-decision layer:

- в начале опроса ChatGPT Project спрашивает, использовать ли рекомендуемые решения по умолчанию;
- global modes: `global-defaults`, `confirm-each-default`, `manual`;
- per-question mode показывает вопрос, рекомендацию по умолчанию, короткое объяснение, действие при Enter/`по умолчанию` и способ указать свой вариант;
- safe defaults всегда explainable и overrideable;
- risky, paid, destructive, security, privacy, legal, secret-related decisions не автопринимаются без explicit user confirmation;
- intake/handoff artifacts фиксируют accepted defaults, overridden defaults, source basis, uncertainty notes и only-real confirmation decisions.

## Remediation plan

- Добавить default-decision contract в package contract.
- Обновить greenfield и brownfield user-facing flows.
- Обновить scenario-pack discovery/scope/spec и brownfield entry/audit wording.
- Обновить generated intake/dashboard artifacts.
- Добавить validator coverage для recommendation-first questionnaire и default-decision state.
- Синхронизировать release-facing docs.

