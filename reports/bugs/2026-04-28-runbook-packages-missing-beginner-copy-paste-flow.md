# Пакеты ранбуков не дают beginner copy-paste flow

Дата: 2026-04-28

## Summary

Текущий runbook package layer не является beginner zero-to-working runbook. Он содержит meta-policy, routing и abstract checklist items, но не дает пользователю конкретных команд, окон, проверок и takeover-точки. Runbook должен вести оператора от состояния "есть только ПК" до состояния "Codex получил remote-доступ и дальше сам разворачивает `factory-template`".

## Route

- `launch_source`: `chatgpt-handoff`
- `task_class`: `deep`
- `selected_profile`: `deep`
- `selected_model`: `gpt-5.5`
- `selected_reasoning_effort`: `high`
- `selected_scenario`: `template-repo/scenario-pack/00-master-router.md -> defect-capture -> runbook package remediation -> verification -> closeout`
- `pipeline_stage`: `remediation of beginner zero-to-codex-ready runbooks`
- `defect_capture_path`: `required`

## Evidence

- `docs/operator/runbook-packages/01-factory-template/01-user-runbook.md` описывал контуры Browser/VS Code/Codex/terminal, но не давал novice steps вида "Окно / команды / куда вставить / expected result".
- `docs/operator/runbook-packages/01-factory-template/02-codex-runbook.md` начинался уже после handoff, но не отделял user-only setup от Codex automation после remote takeover.
- Остальные packages повторяли high-level routing и checklist style, поэтому downstream operator не получал переносимый beginner flow.
- `template-repo/scripts/validate-runbook-packages.py` проверял наличие маркеров и command paths, но не требовал `USER-ONLY SETUP`, `CODEX-AUTOMATION`, takeover-point, обязательные factory steps или формат user step cards.
- Первый remediation pass оставил mismatch: factory user-runbook использовал `FT-200/FT-300/FT-400/FT-500` вместо требуемых `FT-150A/FT-150B/FT-160/FT-170/FT-180`.
- `03-checklist.md` смешивал user steps с process/meta checks (`route receipt`, `defect-capture`, release-facing docs), поэтому не был зеркалом beginner user-runbook.
- Dashboard `runbook_packages` не показывал `current_step`, `active_contour`, `takeover_ready` и `checklist_path`.

## Layer classification

- Advisory/policy layer: affected.
- Operator runbook package layer: affected.
- Executable routing layer: not the source of the bug; validator coverage should be extended.
- Downstream-consumed template content: affected, because packages are exported in `sources-pack-runbook-packages`.

## Required remediation

- Разделить packages на `USER-ONLY SETUP` и `CODEX-AUTOMATION`.
- Полностью переписать `01-factory-template/01-user-runbook.md` как beginner runbook с шагами `FT-000` и далее.
- Зафиксировать два user-facing Codex setup contours:
  - `codex-app-remote-ssh`;
  - `vscode-remote-ssh-codex-extension`.
- Остановить user-runbook на takeover point: когда remote Codex thread/extension может выполнять команды на VPS.
- Перенести bootstrap, install, clone, verify, drift fix, dashboard update и verified sync в `02-codex-runbook.md`.
- Расширить validator, чтобы abstract-only packages больше не проходили verification.
- Проверять, что каждый user-runbook step присутствует в checklist и каждый checklist ID существует в user-runbook.
- Проверять required SSH commands, оба Codex contours, takeover boundary, explained placeholders и Codex automation clone/setup/verify tokens.
- Разделить verify на user readiness до takeover и Codex automation после takeover.

## Expected done state

- Beginner может пройти user-runbook copy-paste шагами без знания repo internals.
- Codex-runbook начинает работу только после remote Codex context и сам выполняет repo/runtime automation.
- Targeted verify green или blocker explicitly documented.

## Remediation notes

- Starting point для пользователя после fix: `docs/operator/runbook-packages/01-factory-template/01-user-runbook.md`, шаг `FT-000`.
- Default contour для новичка: `vscode-remote-ssh-codex-extension`.
- Fallback contour: `codex-app-remote-ssh`.
- После `FT-170` пользовательский ранбук должен остановиться: clone/setup/verify/dashboard/sync выполняет Codex.
