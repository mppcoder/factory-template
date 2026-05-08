# Goal-first intake цели

Этот сценарий нормализует новую задачу в `goal_contract` до обычного scenario route.

## Назначение

Зафиксировать:
- понятную цель;
- измеримый результат;
- evidence и validation path;
- scope и non-goals;
- safety, permissions и budget guardrails;
- stop conditions;
- proxy-signal denylist.

Goal-first intake не заменяет discovery, spec, decomposition, handoff или execution scenarios. Он только подготавливает контракт цели, после чего router продолжает обычный маршрут.

## Когда запускать

Запускай после чтения `00-master-router.md`, title/card contract и repo status card:
- пользователь начал с `goal`, `goal:`, `/goal`, `цель`, `цель:`;
- пришел `chatgpt-handoff`;
- пришла direct Codex task;
- новая задача уже содержит ожидаемый результат, который можно нормализовать.

## Минимальная нормализация

Если цель достаточно ясна, не задавай лишних вопросов. Зафиксируй safe defaults и продолжай route.

Минимальный `goal_contract`:

```yaml
goal_contract:
  version: goal-contract/v1
  goal_id: ""
  goal_command_source:
    raw_user_goal: ""
    normalized_goal: ""
    goal_first_trigger: inferred_from_task
  outcome:
    desired_result: ""
    definition_of_done:
      - ""
    success_metrics:
      - ""
    evidence_required:
      - ""
    evidence_sources:
      - ""
  boundaries:
    scope:
      - ""
    non_goals:
      - ""
    destructive_actions_allowed: false
    production_actions_allowed: false
    secrets_allowed: false
  validation:
    primary_verification_commands:
      - ""
    secondary_verification:
      - ""
    proxy_signal_denylist:
      - "tests passed alone"
      - "file exists alone"
      - "commit exists alone"
      - "green dashboard alone"
      - "validator passed alone"
    goal_achievement_rule: "mark achieved only when evidence satisfies DoD, not when proxy signals pass"
  runtime:
    goal_runtime_recommendation: manual_review
    codex_goal_live_validation_required: true
    codex_goal_live_validation_evidence: ""
    tool_feedback_ready: false
    mcp_or_metrics_needed:
      - ""
    observation_cadence: "operator check every 15-20 minutes for long goal loops"
    budget_guardrails:
      token_budget: ""
      time_budget: ""
      max_iterations: ""
      stop_when:
        - budget_limited
        - tool_limited
        - quota_wall
        - goal_drift
        - unsafe_action
    pause_resume_policy:
      user_controls_lifecycle: true
      model_must_not_clear_or_pause_goal_without_user_instruction: true
  continuation:
    if_budget_limited:
      required_summary:
        - done
        - remaining
        - blockers
        - next recommended goal
    if_unmet:
      create_followup_handoff: true
  side_channel:
    allowed_for_clarifications: true
    must_not_mutate_goal_without_confirmation: true
```

## Правило уточнения

Задай один короткий уточняющий вопрос только если нельзя безопасно определить DoD или validation contour.

Если можно безопасно infer:
- явно назови defaults;
- продолжай route;
- отметь uncertainty в `goal_contract`.

## Правило runtime

`goal first` обязателен как template contract.
`Codex /goal runtime` optional:
- использовать только после live CLI validation;
- если feature flag `goals` есть, но experimental/off by default, считать его рабочим только по явному выбору пользователя или operator policy;
- не считать `/goal` включенным в уже открытой session без нового launch/runtime confirmation;
- не рекомендовать long autonomous loop без observation cadence и stop criteria.

## Guard для feedback tools

Goal runtime не рекомендуется, если нет feedback tools:
- tests;
- validators;
- metrics;
- logs;
- reports;
- manual evidence checklist.

Если feedback tools отсутствуют, ставь `goal_runtime_recommendation: requires_feedback_setup` или `not_recommended`.

## Антипаттерны

Запрещено:
- vague goal без DoD, например "сделай лучше";
- proxy-only closure;
- production/destructive/default full-auto runtime;
- unbounded long loop;
- goal, зависящий от real metrics, но без access к этим metrics;
- изменение active goal через side-channel clarification без явного confirmation.

## Pattern для broad tasks

Для migration/architecture/broad refactor не запускай один гигантский goal.
Используй `scrappy -> PRD -> clean`:
- exploratory goal: найти рабочий путь и собрать evidence;
- PRD/spec goal: превратить findings в проверяемую spec;
- clean implementation goal: реализовать spec с DoD и validation path.
