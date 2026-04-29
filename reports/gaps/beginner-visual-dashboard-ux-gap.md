# Gap: beginner visual dashboard UX еще не обязателен

- id: `gap-2026-04-29-beginner-visual-dashboard-ux`
- captured_at: `2026-04-29`
- launch_source: `chatgpt-handoff`
- selected_profile: `build`
- selected_scenario: `template-repo/scenario-pack/00-master-router.md + project-lifecycle-dashboard / beginner UX visualization path`
- pipeline_stage: `gap-capture -> architecture refinement -> implementation -> verification -> release-followup`
- reusable_template_gap: `yes`
- affected_project: `factory-template`
- downstream_impact: `generated/battle projects need the same beginner-readable state readout without inspecting YAML, logs or repo tree`

## Проблема

Repo-native `project-lifecycle-dashboard` уже существует как canonical state + Markdown renderer + validator, но beginner visual UX contract для двух основных интерфейсов пользователя еще не закреплен как обязательный слой.

Новичок не должен читать YAML, логи, workspace tree или validator output, чтобы понять:

- где сейчас проект;
- что делает Codex;
- что уже готово;
- есть ли блокеры;
- нужно ли действие пользователя;
- где открыть полный отчет.

## Затронутые слои

| Layer | Impact |
|---|---|
| ChatGPT Project | Нужна короткая mini status card в ответах, без технического шума и без ручного выдумывания green status. |
| Codex App / VS Code Codex extension | Нужна execution progress card: route receipt, текущая wave/task, blockers, verify/sync status и external action boundary. |
| Repo Markdown Dashboard | `reports/project-lifecycle-dashboard.md` остается full board и canonical visual artifact. |
| Validator / quick verify | Нужно ловить false green, false no-user-action, false Codex execution claim, false advisory auto-switch и heavy default UI promise. |

## Текущее частичное покрытие

- `docs/operator/factory-template/06-project-lifecycle-dashboard.md` описывает canonical dashboard, renderer, validator, owner boundaries и связь с cockpit/operator dashboard.
- `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml` хранит dashboard state.
- `template-repo/scripts/render-project-lifecycle-dashboard.py` рендерит full Markdown board.
- `template-repo/scripts/validate-project-lifecycle-dashboard.py` уже ловит часть false green, invalid owner boundaries, secret-like content и false auto-switch claims.
- `docs/operator/factory-template/05-orchestration-cockpit-lite.md` объясняет parent/child handoff cockpit, но не является короткой user-facing execution card.
- `template-repo/scripts/operator-dashboard.py` покрывает runtime/deploy detail, но не заменяет lifecycle/dashboard UX.
- `docs/feature-execution-lite.md` описывает wave/checkpoint semantics, но не закрепляет ChatGPT/Codex mini-readouts.

## Желаемый UX

Default beginner-safe surface состоит из трех readouts:

1. ChatGPT mini card: коротко отвечает на вопросы “где мы?”, “что делается?”, “что готово?”, “что от меня нужно?”, “что дальше?”.
2. Codex execution card: показывает route receipt, progress, blockers, next internal action и external user action boundary.
3. Markdown dashboard: `reports/project-lifecycle-dashboard.md` показывает полный state readout в VS Code Markdown Preview или GitHub preview.

Все три поверхности должны использовать единый язык статусов и owner boundaries:

- statuses: `pending`, `in_progress`, `blocked`, `passed`, `failed`, `completed`, `not_applicable`;
- owner boundaries: `internal-repo-follow-up`, `external-user-action`, `runtime-action`, `downstream-battle-action`, `model-mapping-blocker`, `secret-boundary-blocker`.

Любое `green/done/completed` должно иметь `evidence` или `accepted_reason`.

## Граница no-heavy-web-default

Этот gap не требует и не разрешает добавлять default web UI, daemon, SQLite, websocket/live-refresh, Telegram notifications или background worker.

Допустимый default: ChatGPT card + Codex progress card + Markdown dashboard, с renderer/validator поверх того же dashboard YAML.

## Требуемая remediation

- Добавить beginner visual contract в dashboard source-of-truth.
- Добавить templates для ChatGPT mini card и Codex execution card.
- Расширить renderer так, чтобы он мог выводить `markdown-full`, `chatgpt-card` и `codex-card` из одного YAML.
- Расширить validator targeted правилами для visual card contract.
- Подключить positive/negative fixtures к quick verify.
- Обновить operator docs, README и functional state.
