# Parent orchestration handoff UX fixture / позитивный пример

```text
Язык ответа Codex: русский
Отвечай пользователю по-русски.

CODEX HANDOFF

launch_source: chatgpt-handoff
handoff_shape: codex-task-handoff
task_class: deep
selected_profile: deep
selected_model: gpt-5.5
selected_reasoning_effort: high
selected_plan_mode_reasoning_effort: high
apply_mode: manual-ui
strict_launch_mode: optional
selected_scenario: template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md

Используй один цельный handoff block. уже открытая live session не является надежным auto-switch механизмом.
Codex решает фактический режим исполнения после анализа task graph и в closeout указывает execution_mode и child/subagent count.
Orchestration candidate signals: independent child subtasks, different route requirements, deferred_user_actions.
parent plan expectations: если Codex выбирает orchestrated-child-sessions, parent Codex validates plan before child session files.
child subtask boundaries: each child has explicit task_class/profile/model/reasoning/scenario.
Parent plan uses user_actions_policy: defer-to-final-closeout.
deferred_user_actions and placeholder_replacements must be listed in final parent closeout.
Every blocker must include owner_boundary.
route explanation: deterministic keyword/rule-based routing; not a semantic classifier.
continuation outcome: если внешних действий нет, следующий пользовательский шаг отсутствует.
```

Внешних действий не требуется. Следующий пользовательский шаг отсутствует; задачи текущего scope выполнены полностью.
