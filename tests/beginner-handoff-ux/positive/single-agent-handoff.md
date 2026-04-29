# Single-agent handoff UX fixture / позитивный пример

```text
Язык ответа Codex: русский
Отвечай пользователю по-русски.

CODEX HANDOFF

launch_source: chatgpt-handoff
handoff_shape: codex-task-handoff
task_class: build
selected_profile: build
selected_model: gpt-5.5
selected_reasoning_effort: medium
selected_plan_mode_reasoning_effort: medium
apply_mode: manual-ui
strict_launch_mode: optional
selected_scenario: template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md

Используй один цельный handoff block. уже открытая live session не является надежным auto-switch механизмом.
Codex решает фактический режим исполнения после анализа task graph и в closeout указывает execution_mode и child/subagent count.
Задача цельная и выполняется одним route/profile; ожидаемый runtime mode: single-session execution.
continuation outcome: если внешних действий нет, следующий пользовательский шаг отсутствует.
```

Внешних действий не требуется. Следующий пользовательский шаг отсутствует; задачи текущего scope выполнены полностью.
