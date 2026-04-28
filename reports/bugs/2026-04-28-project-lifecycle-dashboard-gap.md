# Отчет о gap: отсутствует единая панель жизненного цикла проекта

- id: `gap-2026-04-28-project-lifecycle-dashboard`
- captured_at: `2026-04-28`
- launch_source: `chatgpt-handoff`
- selected_profile: `deep`
- selected_scenario: `template-repo/scenario-pack/00-master-router.md -> advanced feature-execution-lite path`
- pipeline_stage: `intake -> gap-capture -> architecture -> implementation -> verification -> release-followup`
- reusable_template_gap: `yes`
- affected_project: `factory-template`
- downstream_impact: `generated/battle projects need a template-owned repo-native status surface`

## Проблема

В repo уже есть частичные state/control артефакты:

- `.chatgpt/task-state.yaml`
- `.chatgpt/stage-state.yaml`
- `.chatgpt/task-index.yaml`
- `feature-execution-lite` checkpoint artifacts
- `orchestration-cockpit-lite`
- `operator-dashboard.py`
- release scorecard and runtime reports

Эти артефакты полезны, но они разрознены. Начинающий оператор не может открыть одну repo-native страницу и увидеть состояние проекта от идеи до release, deploy/runtime и post-release improvement.

## Evidence

- `template-repo/template/.chatgpt/task-state.yaml` хранит только boundary текущей задачи и следующий шаг.
- `template-repo/template/.chatgpt/stage-state.yaml` хранит только pipeline gates.
- `template-repo/template/.chatgpt/task-index.yaml` хранит только active change и task list.
- `docs/feature-execution-lite.md` описывает multi-wave feature execution, но не показывает прогресс в единой lifecycle surface.
- `docs/operator/factory-template/05-orchestration-cockpit-lite.md` покрывает parent/child handoff orchestration, но не lifecycle от idea/spec до release/deploy/operate/improve.
- `template-repo/scripts/operator-dashboard.py` покрывает deploy/runtime readiness, но не product lifecycle, active change, feature waves, release readiness или improvement queue.
- `CURRENT_FUNCTIONAL_STATE.md` фиксирует Plan №6 cockpit-lite/productization, но Plan №7 unified lifecycle dashboard до этой задачи отсутствовал.

## Затронутые слои

| Layer | Impact |
|---|---|
| advisory/policy | Docs должны объяснять, как читать lifecycle state, и сохранять boundary между advisory routing и executable routing. |
| executable routing | Dashboard может показывать selected profile/model/reasoning из route receipt, но не должен утверждать, что advisory text auto-switches уже открытую Codex session. |
| template-owned generated project artifacts | Canonical `.chatgpt/project-lifecycle-dashboard.yaml` должен materialize downstream без утечки `factory/producer/*` paths в root боевого проекта. |
| operator/runtime docs | Runtime/deploy evidence из operator dashboard нужно использовать как input signal, а не дублировать вторую deploy system. |

## Required remediation

- Добавить template-owned canonical lifecycle dashboard YAML.
- Добавить Markdown/CLI renderer, который агрегирует существующие state files при наличии.
- Добавить validator для schema, statuses, evidence on completed gates, boundary taxonomy, next actions и запрета false auto-switch claims.
- Обновить docs и quick verify, чтобы contract оставался живым.

## Не входит в scope

- Не добавлять default web app.
- Не добавлять daemon или background worker.
- Не добавлять SQLite/database stack.
- Не обещать Telegram/notification layer.
- Не заменять `orchestration-cockpit-lite` или `operator-dashboard.py`.

## Boundary decision

`factory-template` рассматривается как `greenfield-product` с дополнительным `factory-producer-owned` layer. Generated/battle projects получают dashboard artifact как template-owned state, но не получают factory-producer-owned root paths.
