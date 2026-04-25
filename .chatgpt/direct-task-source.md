classification: direct-task
project_profile: factory-template
selected_scenario: 16-done-closeout.md + 17-direct-task-self-handoff.md
pipeline_stage: closeout sync
artifacts_to_update:
  - .chatgpt/task-launch.yaml
  - .chatgpt/direct-task-self-handoff.md
  - .chatgpt/direct-task-response.md
  - git commit
  - origin/main
handoff_allowed: yes
defect_capture_path: not-required-by-text-signal
task: закрывай, комить и пуш
