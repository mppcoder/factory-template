# Greenfield runbook wrongly assigns GitHub setup to user

Дата: 2026-04-29

## Summary

Пакет `02-greenfield-product` неверно проводил границу внешних действий пользователя при создании боевого проекта. User-runbook допускал, что пользователь готовит GitHub repo/access/repo URL, хотя правильная граница: пользователь выбирает название проекта, сообщает его Codex, создает ChatGPT Project в UI и вставляет готовую repo-first инструкцию, которую подготовил Codex.

## Route

- `launch_source`: `direct-task`
- `task_class`: `deep`
- `selected_profile`: `deep`
- `selected_model`: `gpt-5.5`
- `selected_reasoning_effort`: `high`
- `selected_scenario`: `template-repo/scenario-pack/00-master-router.md -> defect-capture -> runbook package remediation -> verification -> closeout`
- `pipeline_stage`: `greenfield-product package external-boundary correction`
- `defect_capture_path`: `required`

## Evidence

- `docs/operator/runbook-packages/02-greenfield-product/01-user-runbook.md` просил пользователя определить `<repo-owner>/<repo-name>`, GitHub repo/access и repo URL.
- `03-checklist.md` также фиксировал repo URL как evidence пользовательского шага.
- `04-verify.md` требовал, чтобы GitHub repo/access были определены до takeover.

## Correct boundary

User-only для нового боевого проекта:

- выбрать название проекта;
- сообщить Codex название и краткую идею;
- создать ChatGPT Project в UI;
- вставить готовую repo-first инструкцию, подготовленную Codex.

Codex делает сам при отсутствии blocker:

- нормализует slug/repo name;
- создает GitHub repo;
- добавляет `origin`;
- делает initial commit/push;
- создает project root на VPS;
- запускает wizard/launcher;
- materializes repo-first core;
- создает/обновляет `.chatgpt`, `AGENTS`, scenario-pack, dashboard, project-knowledge;
- выполняет bootstrap/verify;
- делает verified sync;
- готовит текст инструкции для ChatGPT Project.

## Remediation

- Переписать `02-greenfield-product` user-runbook/checklist/verify под correct boundary.
- Усилить validator, чтобы greenfield package не мог просить пользователя создать GitHub repo, clone, origin, first push, launcher или verify при готовом Codex contour.
- Обновить dashboard/release-facing docs.
