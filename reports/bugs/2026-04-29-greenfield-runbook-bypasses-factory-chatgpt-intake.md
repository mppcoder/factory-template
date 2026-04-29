# Greenfield runbook bypasses factory ChatGPT intake

Дата: 2026-04-29

## Summary

Greenfield runbook incorrectly starts the project from Codex input instead of the factory-template ChatGPT Project intake. It bypasses the core factory workflow: user says `новый проект` in a new factory-template ChatGPT chat, scenario-pack conducts guided questionnaire, verifies user readiness via runbook/checklist, and only then emits the starter Codex handoff.

## Route

- `launch_source`: `direct-task`
- `task_class`: `deep`
- `selected_profile`: `deep`
- `selected_model`: `gpt-5.5`
- `selected_reasoning_effort`: `high`
- `selected_scenario`: `template-repo/scenario-pack/00-master-router.md -> defect-capture -> runbook package remediation -> verification -> closeout`
- `pipeline_stage`: `greenfield package factory ChatGPT intake correction`
- `defect_capture_path`: `required`

## Evidence

- `docs/operator/runbook-packages/02-greenfield-product/01-user-runbook.md` начинал flow с прямого сообщения в Codex: "Сообщить Codex название и идею".
- `02-codex-runbook.md` ожидал raw project name input вместо стартового handoff, сформированного ChatGPT Project шаблона фабрики.
- `03-checklist.md` начинал path с выбора названия и Codex handoff, но не фиксировал factory-template ChatGPT Project, новый чат, команду `новый проект`, guided questionnaire и readiness check.
- Dashboard не фиксировал `intake_channel`, `trigger_command`, `handoff_ready`, `codex_takeover_ready`, `battle_chatgpt_project_created`, `battle_repo_created_by`.

## Correct workflow

1. Пользователь открывает ChatGPT Project шаблона фабрики `factory-template`.
2. Пользователь создает новый чат.
3. Пользователь пишет `новый проект`.
4. ChatGPT Project по repo-first instruction читает `template-repo/scenario-pack/00-master-router.md`.
5. ChatGPT Project проводит guided questionnaire: название, идея, тип проекта, readiness, Codex contour, blockers.
6. ChatGPT Project формирует один стартовый Codex handoff.
7. Пользователь вставляет handoff в Codex.
8. Codex выполняет repo/root/core/verify/sync и готовит repo-first instruction для боевого ChatGPT Project.
9. Пользователь создает ChatGPT Project боевого проекта и вставляет готовую instruction.

## Remediation

- Перестроить `02-greenfield-product` user-runbook/checklist/verify/closeout вокруг factory-template ChatGPT Project intake.
- Codex-runbook должен принимать ChatGPT-generated handoff, не raw project name.
- Validator должен блокировать Codex-first greenfield wording.
- Dashboard и release-facing docs должны отражать canonical starting point.
