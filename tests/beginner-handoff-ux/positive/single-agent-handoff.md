# Single-agent handoff UX fixture / позитивный пример

```text
Язык ответа Codex: русский
Отвечай пользователю по-русски.

CODEX HANDOFF

launch_source: chatgpt-handoff
handoff_shape: codex-task-handoff
goal_contract:
  normalized_goal: "Выполнить цельную build задачу."
  definition_of_done: ["Evidence satisfies DoD."]
  evidence_required: ["validator/report evidence"]
  proxy_signal_denylist: ["tests passed alone", "file exists alone", "commit exists alone", "green dashboard alone", "validator passed alone"]
goal_runtime_recommendation: goal_first_contract_only
codex_goal_live_validation_required: true
task_class: build
selected_profile: build
selected_model: gpt-5.5
selected_reasoning_effort: medium
selected_plan_mode_reasoning_effort: medium
apply_mode: manual-ui
strict_launch_mode: optional
selected_scenario: template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md

Используй один цельный handoff block. уже открытая live session не является надежным auto-switch механизмом.
Codex /goal runtime optional and live-gated; success must not be claimed from proxy signals alone.
Codex решает фактический режим исполнения после анализа task graph и в closeout указывает execution_mode и child/subagent count.
Задача цельная и выполняется одним route/profile; ожидаемый runtime mode: single-session execution.
continuation outcome: если внешних действий нет, следующий пользовательский шаг отсутствует.
```

Внешних действий не требуется. Следующий пользовательский шаг отсутствует; задачи текущего scope выполнены полностью.
