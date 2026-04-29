# Wrong parent shape for small task / негативный пример

```text
Язык ответа Codex: русский
Отвечай пользователю по-русски.

CODEX HANDOFF

launch_source: chatgpt-handoff
handoff_shape: parent-orchestration-handoff
task_class: quick
selected_profile: quick
selected_model: gpt-5.4-mini
selected_reasoning_effort: low
selected_plan_mode_reasoning_effort: medium
apply_mode: manual-ui
strict_launch_mode: optional
selected_scenario: template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md

Используй один цельный parent handoff block. уже открытая live session не является надежным auto-switch механизмом.
Маленькая цельная task выполняется one profile, но ошибочно выбрана parent orchestration.
parent plan expectations: parent Codex validates plan before child session files.
child subtask boundaries: each child has explicit task_class/profile/model/reasoning/scenario.
Parent plan uses user_actions_policy: defer-to-final-closeout.
deferred_user_actions and placeholder_replacements must be listed in final parent closeout.
Every blocker must include owner_boundary.
route explanation: deterministic keyword/rule-based routing; not a semantic classifier.
continuation outcome: если внешних действий нет, следующий пользовательский шаг отсутствует.
```
