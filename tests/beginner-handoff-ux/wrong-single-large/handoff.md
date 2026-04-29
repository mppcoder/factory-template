# Wrong single-agent shape for large task / негативный пример

```text
Язык ответа Codex: русский
Отвечай пользователю по-русски.

CODEX HANDOFF

launch_source: chatgpt-handoff
handoff_shape: single-agent-handoff
task_class: deep
selected_profile: deep
selected_model: gpt-5.5
selected_reasoning_effort: high
selected_plan_mode_reasoning_effort: high
apply_mode: manual-ui
strict_launch_mode: optional
selected_scenario: template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md

Используй один цельный handoff block. уже открытая live session не является надежным auto-switch механизмом.
2+ независимые child subtasks требуют different selected_profile and selected_model, но ошибочно выбран single-agent.
parent orchestration не требуется.
continuation outcome: если внешних действий нет, следующий пользовательский шаг отсутствует.
```
