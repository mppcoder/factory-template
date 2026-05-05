Ты Codex. launch_source=task-registry-handoff.

Обязательное первое действие: открой и прочитай `template-repo/scenario-pack/00-master-router.md`.
После чтения выведи короткий route receipt и только потом переходи к реализации.

Route receipt values:
selected_project_profile: factory-template self-improvement / automation-orchestration implementation
selected_scenario: template-repo/scenario-pack/00-master-router.md
pipeline_stage: implementation
artifacts_to_update:
- template-repo/template/.chatgpt/task-registry.yaml
- reports/handoffs/FT-TASK-0001-codex-handoff.md
handoff_allowed: true
handoff_shape: codex-task-handoff
task_class: feature
selected_profile: deep
selected_reasoning_effort: high
selected_model: repo-configured; do not assume live auto-switch

Routing and execution boundary:
- Advisory layer: AGENTS, scenario-pack, runbooks, `.chatgpt` guidance and this handoff text.
- Executable routing layer: named profiles, launcher scripts, Codex picker, Codex CLI, Codex app, Codex cloud or future adapter.
- Не утверждай, что advisory text переключает model/profile/reasoning внутри уже открытой Codex-сессии.
- Manual UI default: открыть новый Codex app или VS Code Codex extension chat, выбрать model/reasoning в picker, затем вставить handoff.
- planned_execution_mode: Codex decides after task graph analysis; do not claim orchestrated-child-sessions unless child/subagent sessions are actually used.

Task:
task_id: FT-TASK-0001
title: Example universal Codex task
goal: Показать минимальную структуру universal task, из которой можно собрать Codex handoff.
source_kind: example
source_ref: 

Execution preferences:
preferred_surface: codex_app
workspace_mode: repo_root_or_per_task_worktree
allowed_surfaces:
- codex_app
- vscode_remote_ssh_codex_extension
- codex_cli
- codex_cloud
- symphony_like_runner

outputs_required:
- codex_handoff
- verification_evidence
- dashboard_update
- closeout_summary

dependencies.blocked_by:
- none
dependencies.unlocks:
- none

Human boundary:
requires_review: true
requires_secret: false
external_user_action: false
- Если external_user_action=true, не выполняй это действие за пользователя и вынеси его в final closeout.
- Не добавляй secrets, tokens, passwords, private keys, private repo URLs или raw sensitive logs в публичные issue/PR/docs.

Verification commands:
- python3 template-repo/scripts/validate-task-registry.py template-repo/template/.chatgpt/task-registry.yaml
- python3 template-repo/scripts/validate-codex-task-handoff.py reports/handoffs/FT-TASK-0001-codex-handoff.md

Closeout requirements:
- В финальном ответе пиши по-русски.
- Укажи actual_execution_mode и child/subagent count.
- Перечисли, что изменено, какие проверки запускались и их результат.
- Перед финальным closeout обязательно выполни: git status --short --branch
- Если repo dirty, branch ahead, commit/push невозможны или verify blocked, явно назови sync/blocker.
- Не заявляй full Symphony daemon, background worker, Telegram/Slack bot, web app, database, auto-merge или auto-deploy, если они реально не реализованы.
