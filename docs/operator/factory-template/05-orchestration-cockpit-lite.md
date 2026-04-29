# Orchestration cockpit lite / лёгкая панель оркестрации

## Назначение

`orchestration-cockpit-lite` показывает beginner-readable состояние full handoff orchestration без web app, daemon, SQLite, Telegram notifications или background-worker promises.

Это repo-native слой поверх Plan №5 runner:

- parent handoff id и title;
- route receipt и route explanation;
- child tasks with profile/model/reasoning/status;
- blockers with owner boundary;
- deferred user actions;
- placeholder replacements;
- next action;
- финальный continuation outcome.

Это не полный lifecycle dashboard проекта. Cockpit отвечает на вопрос “как идет этот parent handoff и его child tasks”. Верхний `project-lifecycle-dashboard` агрегирует cockpit вместе с task/stage state, feature waves, release readiness, runtime/deploy state и post-release improvement queue.

Для новичка короткий readout этого же исполнения показывает `Codex execution card` из `project-lifecycle-dashboard`: route receipt, активная wave/task, completed/remaining steps, blockers, next internal action и external action boundary.

Cockpit остается detailed orchestration artifact для parent handoff: он хранит child task table, deferred user actions, placeholder replacements и continuation outcome. Execution card не заменяет cockpit, а показывает пользователю короткую версию хода исполнения прямо в Codex App / VS Code Codex chat.

Важно разделять parent orchestration и межчатовую очередь handoff/self-handoff задач:

- `orchestration-cockpit-lite` показывает один parent handoff и его child tasks;
- `.chatgpt/handoff-implementation-register.yaml` фиксирует задачи, которые могли появиться в другом ChatGPT-чате или как Codex self-handoff и должны быть реализованы, заблокированы, сняты или verified;
- `project-lifecycle-dashboard` показывает оба слоя рядом, чтобы handoff-задача не исчезла после закрытия чата.

## Где лежат артефакты

- Source template: `template-repo/template/.chatgpt/orchestration-cockpit.yaml`.
- Markdown template: `reports/orchestration/orchestration-cockpit.md.template`.
- Renderer: `template-repo/scripts/render-orchestration-cockpit.py`.
- Validator: `template-repo/scripts/validate-orchestration-cockpit.py`.

Связанный верхний слой:

- `docs/operator/factory-template/06-project-lifecycle-dashboard.md`;
- `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml`;
- `template-repo/scripts/render-project-lifecycle-dashboard.py`;
- `template-repo/scripts/validate-project-lifecycle-dashboard.py`.

## Beginner default / режим для новичка

Default path остается lightweight:

1. Пользователь вставляет один цельный parent handoff в новый Codex chat/window в VS Code Remote SSH repo context.
2. Parent Codex выводит `handoff receipt` / `route receipt`.
3. Parent Codex materializes or reads `codex-orchestration/v1` plan.
4. Parent Codex validates plan and cockpit before writing child session files.
5. Parent Codex runs repo-native orchestrator with `--execute` only when the parent handoff explicitly asks full orchestration.
6. Cockpit shows what happened and what the next action is.

No hidden second internal shell step for the operator: shell commands are parent Codex work or strict troubleshooting fallback.

## Route explanation / объяснение маршрута

Route receipt должен объяснять:

- detected `task_class`;
- selected `selected_profile`;
- repo-configured `selected_model`;
- `selected_reasoning_effort`;
- `selected_plan_mode_reasoning_effort`;
- keywords/rules/evidence that matched;
- whether live model catalog validation is current, stale or unavailable.

Этот слой deterministic/keyword/rule-based. Он не обещает semantic classifier.

Advisory handoff text does not switch model/profile/reasoning inside an already-open live session. Reliable executable routing requires a new task launch or manual picker selection in a new Codex chat/window.

Lifecycle dashboard может показывать эти поля как status readout, но он наследует ту же boundary: advisory text не является auto-switch механизмом.

## Cockpit status model / модель статуса

Allowed parent status:

- `planned`;
- `validated`;
- `dry-run`;
- `executing`;
- `completed`;
- `blocked`.

Allowed child status:

- `planned`;
- `session-file-written`;
- `executed`;
- `blocked`;
- `skipped`.

Allowed owner boundaries:

- `internal-repo-follow-up`;
- `external-user-action`;
- `runtime-action`;
- `downstream-battle-action`;
- `model-mapping-blocker`;
- `secret-boundary-blocker`.

## Пример команды parent Codex

```bash
python3 template-repo/scripts/render-orchestration-cockpit.py \
  --input template-repo/template/.chatgpt/orchestration-cockpit.yaml \
  --output reports/orchestration/orchestration-cockpit.md

python3 template-repo/scripts/validate-orchestration-cockpit.py \
  template-repo/template/.chatgpt/orchestration-cockpit.yaml
```

Эти команды выполняет Codex внутри repo. Пользователь не должен запускать их вручную для обычного one-paste flow.

## Safe rehearsal boundary / граница репетиции

Synthetic rehearsal может использовать placeholders вроде `__REAL_DOWNSTREAM_REPO__` и `__REAL_APP_IMAGE__`, но обязана явно писать:

- no secrets;
- no real VPS mutation;
- no real downstream app proof;
- dry-run or execute-safe only;
- manual intervention count;
- blockers with owner boundary.
