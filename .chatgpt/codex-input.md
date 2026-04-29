CODEX HANDOFF — GPT-5.5 PROMPT MIGRATION FOR FACTORY-TEMPLATE

launch_source: chatgpt-handoff
handoff_shape: single-agent-handoff
task_class: deep
selected_profile: deep
selected_model: gpt-5.5
selected_reasoning_effort: high
selected_plan_mode_reasoning_effort: high
apply_mode: manual-ui
strict_launch_mode: optional
project_profile: factory-template self-improvement
selected_scenario: template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md -> docs/operator/factory-template/04-vps-remote-ssh-full-handoff-orchestration.md
pipeline_stage: handoff policy modernization -> routing UX -> validation -> closeout
handoff_allowed: yes
defect_capture_path: reports/bugs/2026-04-29-handoff-shape-validator-drift.md

Язык ответа Codex: русский
Отвечай пользователю по-русски.

Цель: добавить обязательный выбор вида handoff для новой задачи и сделать validators/tests shape-aware.

Почему parent orchestration не требуется: задача цельная, выполняется одним deep route в одном repo и не требует child Codex sessions.
