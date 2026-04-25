task_class: build
selected_profile: build
project_profile: factory-template
selected_scenario: 17-direct-task-self-handoff.md -> 15-handoff-to-codex.md -> implementation/remediation
pipeline_stage: implementation
handoff_allowed: yes
defect_capture_path: not-required-by-text-signal
artifacts_to_update:
  - template-repo/codex-routing.yaml
  - template-repo/scripts/codex_task_router.py
  - template-repo/template/.codex/config.toml
  - workspace-packs/vscode-codex-bootstrap/codex/global-codex-config.example.toml
  - factory_template_only_pack/03-mode-routing-factory-template.md
  - factory_template_only_pack/06-codex-config-factory-template.toml
  - .chatgpt/direct-task-self-handoff.md
  - .chatgpt/direct-task-response.md
  - .chatgpt/task-launch.yaml

task: обновить список рекомендуемых моделей для выполнения handoff с учетом выхода GPT-5.5
