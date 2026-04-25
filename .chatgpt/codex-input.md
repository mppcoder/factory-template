task_class: build
selected_profile: build
project_profile: factory-template self-improvement
selected_scenario: defect-capture -> remediation -> verify -> closeout
pipeline_stage: remediation -> verify -> closeout
handoff_allowed: yes
defect_capture_path: reproduce -> evidence -> bug report -> layer classification -> factory feedback if reusable -> remediation
artifacts_to_update:
  - template-repo/scenario-pack/00-master-router.md
  - template-repo/scenario-pack/01-global-rules.md
  - template-repo/scenario-pack/12-bug-analysis.md
  - template-repo/scenario-pack/15-handoff-to-codex.md
  - template-repo/scenario-pack/16-done-closeout.md
  - template-repo/scenario-pack/17-direct-task-self-handoff.md
  - template-repo/codex-routing.yaml
  - template-repo/scripts/bootstrap-codex-task.py
  - template-repo/scripts/codex_task_router.py
  - template-repo/scripts/create-codex-task-pack.py
  - template-repo/scripts/validate-codex-routing.py
  - template-repo/scripts/validate-codex-task-pack.py
  - template-repo/scripts/validate-handoff-response-format.py
  - template-repo/scripts/validate-operator-env.py
  - .chatgpt/verification-report.md
  - .chatgpt/done-report.md
  - reports/bugs/
  - reports/factory-feedback/

Задача:
Исправить два process defects в factory-template:
1. Codex не должен перекладывать доступный GitHub PR merge на пользователя, если GitHub write path доступен, checks green, PR доступен для merge и нет обязательного человеческого approval или другого blocker.
2. Человекочитаемые ответы, инструкции, отчеты, closeout и generated guidance должны быть на русском языке; английский допустим только для технических идентификаторов, команд, файлов, ключей конфигурации и literal values.

Нужно пройти defect-capture, внести remediation в repo rules/generators/validators, проверить и закрыть задачу внутри repo.
