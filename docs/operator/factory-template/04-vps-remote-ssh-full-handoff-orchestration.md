# VPS Remote SSH-first full handoff orchestration

## Назначение

Этот runbook описывает default путь для большой задачи:

1. Browser ChatGPT Project готовит один большой Codex handoff.
2. Operator открывает VS Code Remote SSH window, connected to VPS.
3. В этом окне открыт repo root `mppcoder/factory-template`.
4. Codex extension в этом же VS Code Remote SSH контексте получает один цельный handoff.
5. Repo-native orchestrator раскладывает handoff в subtask specs.
6. Отдельные Codex CLI sessions запускаются на VPS/repo context.
7. Parent orchestration report собирает результаты, blockers и финальный closeout.

## Default path по умолчанию

Default user-facing path: `VPS Remote SSH-first`.
Beginner zero-to-Codex-ready setup is maintained in `docs/operator/runbook-packages/01-factory-template/01-user-runbook.md`.
This orchestration runbook starts after the same takeover point: the operator has a remote Codex context on the VPS through `codex-app-remote-ssh` or `vscode-remote-ssh-codex-extension`.

Минимальный операторский поток — one-paste autopilot:

1. Откройте Browser ChatGPT Project и получите один большой handoff block.
2. Откройте VS Code, подключенный к VPS через Remote SSH.
3. Откройте repo root на VPS.
4. Откройте новый Codex chat/window в VS Code Remote SSH.
5. Вручную выберите `selected_model` и `selected_reasoning_effort` в picker, если picker доступен.
6. Вставьте один цельный handoff block.

На этом пользовательское действие для запуска full handoff заканчивается. Дальше parent Codex в этом VPS/repo context сам:
- verifies the VPS context;
- installs missing system/Codex tooling when needed;
- clones or opens `/projects/factory-template`;
- выводит `handoff receipt` / `route receipt`;
- materializes or reads the parent orchestration plan from the pasted handoff;
- validates the plan before any session files are written;
- runs the repo-native orchestrator with explicit execution when the handoff is marked as full orchestration;
- collects the parent orchestration report and child results;
- performs repo-local verification, commit and push when allowed by repo closeout rules.

Canonical parent Codex command for full orchestration:

`orchestrate-codex-handoff.py --execute` is the parent Codex execution path for one-paste autopilot.

```bash
python3 template-repo/scripts/orchestrate-codex-handoff.py \
  --plan <parent-orchestration-plan.yaml> \
  --report reports/orchestration/parent-orchestration-report.md \
  --execute
```

Manual shell execution by the operator is not the default path. It is only a troubleshooting / strict reproduction fallback.

Dry-run fallback for debugging:

```bash
python3 template-repo/scripts/orchestrate-codex-handoff.py \
  --plan tests/codex-orchestration/fixtures/valid/parent-plan.yaml \
  --report reports/orchestration/parent-orchestration-report.md
```

Dry-run writes the parent report and per-subtask handoff files without starting child Codex CLI sessions. Real child sessions start only when parent Codex uses explicit `--execute` from the parent handoff instructions.

## Опциональные альтернативы

Codex app local/remote repo context допустим только если thread работает с тем же VPS/repo filesystem and shell context.

Codex App / Cloud Director является optional, not default. Используйте cloud delegation только если пользователь явно выбрал cloud, repo/security boundary это разрешает, и задача не требует local-only secrets/runtime.

## Граница routing

Already-open live session не является надежным auto-switch mechanism.

`Новый чат + вставка handoff` и executable launch через repo runner — разные вещи:
- manual UI path требует ручного выбора model/reasoning в picker;
- strict path требует нового task launch/profile selection;
- child session не наследует parent route by default.

Каждый child subtask должен иметь:
- `selected_profile`;
- `selected_model`;
- `selected_reasoning_effort`;
- `selected_plan_mode_reasoning_effort`;
- `selected_scenario`;
- `task_class`.

Если live model availability не проверена, report должен писать `requires live validation`, а не обещать availability.

## Ответственность parent orchestrator

Parent orchestrator:
- validates one parent handoff / one orchestration plan;
- normalizes a large ChatGPT handoff into a checked `codex-orchestration/v1` parent plan when the parent handoff contains structured orchestration data;
- renders or validates `orchestration-cockpit-lite` so the operator can see parent status, child tasks, blockers, deferred user actions, placeholder replacements and next action;
- records route explanation for `task_class`, `selected_profile`, `selected_model`, reasoning effort and live catalog boundary;
- resolves each subtask through repo routing config;
- applies `user_actions_policy: defer-to-final-closeout`;
- moves all user-required actions into `deferred_user_actions`;
- uses safe temporary placeholders where possible and records `placeholder_replacements`;
- writes per-subtask handoff/session files;
- prints dry-run commands;
- writes parent report;
- records blockers and owner boundary;
- does not execute specialist work inline when subtask routing says separate session/profile.
- in one-paste autopilot, is launched by parent Codex after paste, not by a second operator action.

Parent orchestrator does not:
- store secrets;
- hardcode VPS IP, username, token or private transcript;
- silently change configured model mapping;
- promote Codex App/Cloud Director into the default path;
- claim that a pasted handoff changes model/profile/reasoning inside an already-open session.

Security boundary: no secrets in handoff, reports, fixtures, transcripts or repo.

## Правило user actions last

Для большого handoff оркестр агентов работает по правилу `defer-to-final-closeout`.

Это значит:
- все действия, где нужен пользователь, внешний UI, secret entry, real VPS approval, real downstream repo или real application artifact, переносятся в конец parent plan;
- child subtasks получают только repo-local работу, которую можно выполнить без ожидания пользователя;
- если работа может продолжаться с synthetic/safe data, используются temporary placeholders;
- каждый placeholder записывается в `placeholder_replacements` с owner `operator` и timing `final-user-action`;
- финальный parent closeout обязан напомнить, какие placeholders заменить на реальные данные и какие checks повторить после замены.

Safe placeholder examples:
- `__REAL_APP_IMAGE__` вместо настоящего application image;
- `__REAL_DOMAIN__` вместо production hostname;
- `__REAL_VPS_TARGET__` вместо конкретного target host;
- `__REAL_DOWNSTREAM_REPO__` вместо private downstream repo path.

Forbidden placeholder use:
- нельзя подставлять fake secrets;
- нельзя коммитить `.env` content;
- нельзя утверждать, что placeholder evidence является real runtime/downstream proof;
- нельзя блокировать internal repo subtasks только потому, что финальное external значение будет известно позже.

## Таксономия failure/blocker

| Code | Meaning | Owner boundary |
|---|---|---|
| `internal-repo-follow-up` | Repo docs/scripts/tests need update. | Codex/repo |
| `external-user-action` | User must choose/approve/provide an external artifact. | operator |
| `runtime-action` | VPS/runtime/deploy action needs approved runtime context. | operator + runtime |
| `downstream-battle-action` | Real downstream repo/app proof is needed. | downstream owner |
| `model-mapping-blocker` | Configured model/profile is missing or requires live validation. | repo + live Codex catalog |
| `secret-boundary-blocker` | Secret-like content appeared in handoff/fixtures/report. | operator |

## Пример parent handoff

```yaml
schema: codex-orchestration/v1
parent:
  id: p5-example-parent
  title: VPS Remote SSH-first orchestration example
  launch_source: chatgpt-handoff
  selected_scenario: template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md
  apply_mode: manual-ui
  strict_launch_mode: optional
  default_context: VPS Remote SSH repo context
  user_actions_policy: defer-to-final-closeout
subtasks:
  - id: docs-quick
    title: Update operator wording
    task_class: quick
    selected_profile: quick
    selected_model: gpt-5.4-mini
    selected_reasoning_effort: low
    selected_plan_mode_reasoning_effort: medium
    selected_scenario: template-repo/scenario-pack/14-docs-normalization.md
    owner_boundary: internal-repo-follow-up
    prompt: "Проверить wording docs and update Russian operator text."
  - id: runner-build
    title: Patch runner script
    task_class: build
    selected_profile: build
    selected_model: gpt-5.5
    selected_reasoning_effort: medium
    selected_plan_mode_reasoning_effort: medium
    selected_scenario: template-repo/scenario-pack/15-handoff-to-codex.md
    owner_boundary: internal-repo-follow-up
    prompt: "Implement dry-run report generation."
  - id: audit-deep
    title: Audit routing mismatch
    task_class: deep
    selected_profile: deep
    selected_model: gpt-5.5
    selected_reasoning_effort: high
    selected_plan_mode_reasoning_effort: high
    selected_scenario: template-repo/scenario-pack/00-master-router.md
    owner_boundary: internal-repo-follow-up
    prompt: "Audit routing docs versus executable config."
  - id: verify-review
    title: Review verification evidence
    task_class: review
    selected_profile: review
    selected_model: gpt-5.5
    selected_reasoning_effort: high
    selected_plan_mode_reasoning_effort: high
    selected_scenario: template-repo/scenario-pack/16-done-closeout.md
    owner_boundary: internal-repo-follow-up
    prompt: "Run targeted validators and summarize residual risk."
deferred_user_actions:
  - id: replace-real-app-image
    action: "Заменить `__REAL_APP_IMAGE__` на настоящий application image перед real downstream proof."
    timing: final-closeout
    owner_boundary: external-user-action
placeholder_replacements:
  - placeholder: __REAL_APP_IMAGE__
    description: "Настоящий application image для downstream/battle runtime proof."
    final_value_owner: operator
    replacement_timing: final-user-action
```

## Пример dry-run output

```text
ORCHESTRATION DRY-RUN
- docs-quick: codex --profile quick < reports/orchestration/sessions/docs-quick.md
- runner-build: codex --profile build < reports/orchestration/sessions/runner-build.md
- audit-deep: codex --profile deep < reports/orchestration/sessions/audit-deep.md
- verify-review: codex --profile review < reports/orchestration/sessions/verify-review.md
```

## Пример report output

```text
# Отчет parent Codex orchestration

Status: dry-run
Default path: VPS Remote SSH-first
Cloud default: false

| Subtask | Profile | Model | Reasoning | Status | Boundary |
|---|---|---|---|---|---|
| docs-quick | quick | gpt-5.4-mini | low | session-file-written | internal-repo-follow-up |
| runner-build | build | gpt-5.5 | medium | session-file-written | internal-repo-follow-up |
| audit-deep | deep | gpt-5.5 | high | session-file-written | internal-repo-follow-up |
| verify-review | review | gpt-5.5 | high | session-file-written | internal-repo-follow-up |
```

Final user-action reminder example:

```text
## Финальные действия пользователя
- replace-real-app-image: заменить `__REAL_APP_IMAGE__` на настоящий image и повторить runtime proof.

## Напоминания о замене placeholder values
- `__REAL_APP_IMAGE__` -> настоящий application image для downstream/battle runtime proof.
```

## Правила validation

The repo validator rejects:
- docs that promote Codex App/Cloud Director into the default path;
- child subtasks without explicit profile/model/reasoning/scenario;
- multi-block handoff for user copy-paste;
- wording that treats an already-open session as route switching;
- unredacted secrets, `.env`-like content or private transcripts in examples.

Plan №6 productization validators add beginner UX checks:
- `validate-parent-orchestration-plan.py` checks the parent plan template and a concrete `codex-orchestration/v1` plan;
- `validate-orchestration-cockpit.py` checks cockpit status, route receipt, blockers, deferred actions, placeholders and next action;
- `validate-route-explain.py` checks deterministic keyword/rule-based route explanations and prevents semantic-classifier overclaim;
- `validate-beginner-handoff-ux.py` checks one copy-paste block, no file-based handoff, no hidden second operator shell step, no fake auto-switch claims and final continuation outcome.

## Official boundary note / официальная граница

OpenAI docs describe Codex CLI as a local terminal agent that can read, edit and run code in the selected directory. Codex IDE extension works side by side in the IDE and can also delegate to cloud. Codex app local mode asks the user to select a project folder and make sure Local is selected. Help Center distinguishes `Codex Local` controls from `Codex Cloud` controls.

References:
- `https://developers.openai.com/codex/cli`
- `https://developers.openai.com/codex/ide`
- `https://developers.openai.com/codex/app`
- `https://help.openai.com/en/articles/11369540-icodex-in-chatgpt`
