# Superseded handoff not written off

Дата: 2026-04-29
Статус: fixed in current scope
Слой: `.chatgpt/handoff-implementation-register.yaml`, handoff closeout guidance, lifecycle dashboard validator

## Summary

Handoff implementation register фиксировал handoff/self-handoff задачи, но не требовал списывать старый handoff, если в том же чате по той же задаче был создан новый handoff. Из-за этого broken/clarified/reworked handoff мог остаться активным в очереди вместе с replacement handoff.

## Route

- `launch_source`: `direct-task`
- `task_class`: `build`
- `selected_profile`: `build`
- `selected_model`: `gpt-5.5`
- `selected_reasoning_effort`: `medium`
- `selected_scenario`: `template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md -> defect-capture -> remediation -> verification`
- `pipeline_stage`: `defect capture -> implementation -> verification -> release-followup`
- `defect_capture_path`: `required`

## Evidence

- Register поддерживал `not_applicable` и `archived`, но не имел явного `superseded` status.
- Validator не проверял, что в одной replacement group остается только один active handoff.
- Scenario guidance говорила обновлять matching item при closeout, но не требовала при создании нового handoff проверить старые handoff этого же chat/task.

## Expected behavior

Если в текущем чате создается новый handoff по той же задаче, Codex/ChatGPT должен:

- найти старые handoff items той же `handoff_group`;
- списать старые активные items как `superseded` или `not_applicable`;
- заполнить `superseded_by`, `replacement_reason`, `evidence`;
- у нового handoff заполнить `replaces`;
- оставить только один active handoff в группе.

## Remediation

- Добавлен статус `superseded`.
- Добавлены поля `handoff_group`, `handoff_revision`, `replaces`, `superseded_by`, `replacement_reason`.
- Validator ловит несколько active items в одной handoff group и broken replacement links.
- Dashboard показывает group/revision и закрытые `superseded` items.

