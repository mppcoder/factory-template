task_class: deep
selected_profile: deep
project_profile: brownfield-without-repo
selected_scenario: brownfield/00-brownfield-entry.md
pipeline_stage: brownfield-without-repo-intake
handoff_allowed: no
artifacts_to_update:
  - .chatgpt/task-launch.yaml
  - .chatgpt/direct-task-source.md
  - .chatgpt/direct-task-self-handoff.md
  - .chatgpt/normalized-codex-handoff.md
  - brownfield/system-inventory.md
  - brownfield/repo-audit.md
  - brownfield/as-is-architecture.md
  - brownfield/gap-register.md
  - brownfield/reverse-engineering-plan.md
  - brownfield/reverse-engineering-summary.md
  - brownfield/decision-log.md
  - .chatgpt/evidence-register.md
  - .chatgpt/reality-check.md
defect_capture_path: brownfield gap -> structured defect/gap report before remediation planning

Полевой тест шаблона фабрики проектов на brownfield without repo. Реальные входные корни: /root/.openclaw как настроенный дистрибутив, /root/openclaw-plus как тонкий слой кастомных доработок дистрибутива. Начать evidence-first intake/reconstruction, проверить фактическое наличие корней, repo-state и безопасную canonical project layout; не переходить к remediation до фиксации inventory/repo-audit/gap register.
